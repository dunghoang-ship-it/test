#!/usr/bin/env python3
"""Generate BIDV 'Thông báo nợ quá hạn' DOCX from Excel/CSV (1 row)."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

# ---------------------------------------------------------------------------
# Column aliases (header Excel/Sheet → field nội bộ)
# ---------------------------------------------------------------------------
COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "ten_khach_hang": ("khách hàng", "khach hang", "ten khach hang", "họ tên", "ho ten"),
    "so_khoan_vay": ("số tài khoản", "so tai khoan", "số khoản vay", "so khoan vay", "stk"),
    "so_du_cuoi_ky": ("số dư cuối kỳ (nguyên tệ)", "so du cuoi ky (nguyen te)", "số dư cuối kỳ", "so du cuoi ky"),
    "lai_hien_tai": ("số tiền lãi hiện tại (nt)", "so tien lai hien tai (nt)", "số tiền lãi hiện tại", "so tien lai hien tai"),
    "lai_phat_goc": ("dư lãi phạt cho gốc", "du lai phat cho goc", "phí phạt chậm thanh toán (nt)", "phi phat cham thanh toan (nt)"),
    "lai_phat_lai": ("dư lãi phạt cho lãi", "du lai phat cho lai"),
    "goc_qua_han": ("số tiền gốc quá hạn", "so tien goc qua han"),
    "lai_qua_han": ("số tiền lãi quá hạn", "so tien lai qua han"),
    "goc_tren_bill": ("số tiền gốc trên bill (cqđ)", "so tien goc tren bill (cqd)", "số tiền gốc trên bill", "so tien goc tren bill"),
    "lai_tren_bill": ("số tiền lãi trên bill (cqđ)", "so tien lai tren bill (cqd)", "số tiền lãi trên bill", "so tien lai tren bill"),
    "ngay_qua_han_goc": ("số ngày quá hạn gốc", "so ngay qua han goc"),
    "ngay_qua_han_lai": ("số ngày quá hạn lãi", "so ngay qua han lai"),
    "lich_tra_goc": ("lịch trả gốc", "lich tra goc"),
    "lich_tra_lai": ("lịch trả lãi", "lich tra lai"),
    "ngay_dao_han": ("ngày đáo hạn", "ngay dao han"),
    "ngay_cho_vay": ("ngày cho vay", "ngay cho vay"),
}


@dataclass
class LoanNoticeData:
    so_van_ban: str
    ten_khach_hang: str
    ngay_bao_cao: date
    so_khoan_vay: str
    du_no_goc: int
    du_no_lai_va_phat: int
    qua_han_goc: int
    qua_han_lai_va_phat: int
    so_ngay_qua_han: int
    so_dien_thoai: str = "02513 526 325"
    nguoi_ky: str = "Nguyễn Quốc Tuấn"
    chuc_danh_ky: str = "P.KHCN"
    ngay_them_han_thanh_toan: int = 15


def format_vnd(n: int) -> str:
    return f"{n:,}".replace(",", ".")


ONES = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]


def _read_two_digits(n: int, *, use_le: bool) -> str:
    if n < 10:
        if not n:
            return ""
        return f"lẻ {ONES[n]}" if use_le else ONES[n]
    if n < 20:
        return "mười" if n == 10 else f"mười {ONES[n % 10] if n % 10 != 5 else 'lăm'}"
    tens, ones = divmod(n, 10)
    parts = [ONES[tens], "mươi"]
    if ones == 1:
        parts.append("mốt")
    elif ones == 4:
        parts.append("tư")
    elif ones == 5:
        parts.append("lăm")
    elif ones:
        parts.append(ONES[ones])
    return " ".join(parts)


def _read_three_digits(n: int) -> str:
    hundreds, rem = divmod(n, 100)
    parts: list[str] = []
    if hundreds:
        parts.append(f"{ONES[hundreds]} trăm")
    if rem:
        parts.append(_read_two_digits(rem, use_le=bool(hundreds)))
    return " ".join(parts)


def number_to_vietnamese_words(n: int) -> str:
    if n == 0:
        return "Không đồng"
    scales = [
        (1_000_000_000_000, "nghìn tỷ"),
        (1_000_000_000, "tỷ"),
        (1_000_000, "triệu"),
        (1_000, "nghìn"),
    ]
    parts: list[str] = []
    remaining = n
    for value, label in scales:
        if remaining >= value:
            chunk = remaining // value
            remaining %= value
            parts.append(f"{_read_three_digits(chunk)} {label}")
    if remaining:
        parts.append(_read_three_digits(remaining))
    text = " ".join(" ".join(parts).split())
    return text[:1].upper() + text[1:] + " đồng"


# ---------------------------------------------------------------------------
# Excel / CSV helpers
# ---------------------------------------------------------------------------
def normalize_header(value: object) -> str:
    text = "" if value is None or (isinstance(value, float) and pd.isna(value)) else str(value)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def parse_number(value: object) -> int:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return 0
    if isinstance(value, (int,)):
        return int(value)
    if isinstance(value, float):
        return int(round(value))
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "-"}:
        return 0
    text = text.replace(" ", "")
    # Vietnamese: 1.952.579,50323  or 1952579.50323
    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")
    else:
        # thousands with dots: 898.494.837
        if re.fullmatch(r"\d{1,3}(\.\d{3})+", text):
            text = text.replace(".", "")
    try:
        return int(round(float(text)))
    except ValueError:
        return 0


def parse_date(value: object) -> date | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, pd.Timestamp):
        return value.date()
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "-", "1", "2"}:
        # sheet sometimes puts status code "1"/"2" into date-like columns
        return None
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def title_case_vn(name: str) -> str:
    name = re.sub(r"\s+", " ", name.strip())
    return " ".join(part.capitalize() for part in name.split(" "))


def slugify(name: str) -> str:
    text = unicodedata.normalize("NFKD", name)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    return text or "Khach_hang"


def load_dataframe(path: Path, sheet: str | int | None = None) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xlsm", ".xls"}:
        df = pd.read_excel(path, sheet_name=0 if sheet is None else sheet, dtype=object)
    elif suffix in {".csv", ".txt"}:
        # try utf-8-sig then utf-8 then cp1258
        last_err: Exception | None = None
        for enc in ("utf-8-sig", "utf-8", "cp1258", "latin-1"):
            try:
                df = pd.read_csv(path, dtype=object, encoding=enc)
                break
            except Exception as exc:  # noqa: BLE001
                last_err = exc
        else:
            raise RuntimeError(f"Không đọc được CSV: {last_err}")
    else:
        raise ValueError(f"Định dạng không hỗ trợ: {suffix}. Dùng .xlsx/.xls/.csv")
    df = df.dropna(how="all")
    df.columns = [str(c).strip() for c in df.columns]
    return df.reset_index(drop=True)


def resolve_columns(df: pd.DataFrame) -> dict[str, str]:
    normalized = {normalize_header(c): c for c in df.columns}
    mapping: dict[str, str] = {}
    for field, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            key = normalize_header(alias)
            if key in normalized:
                mapping[field] = normalized[key]
                break
    required = ["ten_khach_hang", "so_khoan_vay", "so_du_cuoi_ky"]
    missing = [f for f in required if f not in mapping]
    if missing:
        raise KeyError(
            "Thiếu cột bắt buộc trong file: "
            + ", ".join(missing)
            + f". Các cột hiện có: {list(df.columns)}"
        )
    return mapping


def get_cell(row: pd.Series, mapping: dict[str, str], field: str, default=None):
    col = mapping.get(field)
    if not col:
        return default
    return row.get(col, default)


def row_to_notice(
    row: pd.Series,
    mapping: dict[str, str],
    *,
    so_van_ban: str,
    ngay_bao_cao: date | None,
    them_ngay: int,
) -> LoanNoticeData:
    ten = title_case_vn(str(get_cell(row, mapping, "ten_khach_hang", "") or ""))
    so_tk = str(get_cell(row, mapping, "so_khoan_vay", "") or "").strip()
    if so_tk.endswith(".0"):
        so_tk = so_tk[:-2]

    du_no_goc = parse_number(get_cell(row, mapping, "so_du_cuoi_ky"))
    lai_hien_tai = parse_number(get_cell(row, mapping, "lai_hien_tai"))
    lai_phat_goc = parse_number(get_cell(row, mapping, "lai_phat_goc"))
    lai_phat_lai = parse_number(get_cell(row, mapping, "lai_phat_lai"))
    goc_qh = parse_number(get_cell(row, mapping, "goc_qua_han"))
    lai_qh = parse_number(get_cell(row, mapping, "lai_qua_han"))
    goc_bill = parse_number(get_cell(row, mapping, "goc_tren_bill"))
    lai_bill = parse_number(get_cell(row, mapping, "lai_tren_bill"))
    ngay_qh_goc = parse_number(get_cell(row, mapping, "ngay_qua_han_goc"))
    ngay_qh_lai = parse_number(get_cell(row, mapping, "ngay_qua_han_lai"))
    so_ngay = max(ngay_qh_goc, ngay_qh_lai)

    if goc_qh == 0 and so_ngay > 0 and goc_bill > 0:
        goc_qh = goc_bill
    if lai_qh == 0 and so_ngay > 0 and lai_bill > 0:
        lai_qh = lai_bill

    du_no_lai = lai_hien_tai + lai_phat_goc + lai_phat_lai
    qua_han_lai = lai_qh + lai_phat_goc + lai_phat_lai

    if ngay_bao_cao is None:
        base = (
            parse_date(get_cell(row, mapping, "lich_tra_goc"))
            or parse_date(get_cell(row, mapping, "lich_tra_lai"))
            or parse_date(get_cell(row, mapping, "ngay_dao_han"))
        )
        if base is not None:
            ngay_bao_cao = base + timedelta(days=so_ngay)
        else:
            ngay_bao_cao = date.today()

    return LoanNoticeData(
        so_van_ban=so_van_ban,
        ten_khach_hang=ten,
        ngay_bao_cao=ngay_bao_cao,
        so_khoan_vay=so_tk,
        du_no_goc=du_no_goc,
        du_no_lai_va_phat=du_no_lai,
        qua_han_goc=goc_qh,
        qua_han_lai_va_phat=qua_han_lai,
        so_ngay_qua_han=so_ngay,
        ngay_them_han_thanh_toan=them_ngay,
    )


def select_row(df: pd.DataFrame, mapping: dict[str, str], *, row: int | None, account: str | None) -> tuple[int, pd.Series]:
    if account:
        col = mapping["so_khoan_vay"]
        series = df[col].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
        hits = df.index[series == str(account).strip()].tolist()
        if not hits:
            raise ValueError(f"Không tìm thấy số tài khoản/khoản vay: {account}")
        idx = hits[0]
        return idx, df.loc[idx]
    if row is None:
        raise ValueError("Cần --row hoặc --account")
    # --row: 1 = dòng dữ liệu đầu tiên (sau header)
    if row < 1 or row > len(df):
        raise IndexError(f"--row phải từ 1 đến {len(df)} (file có {len(df)} dòng dữ liệu)")
    idx = row - 1
    return idx, df.iloc[idx]


# ---------------------------------------------------------------------------
# DOCX builders
# ---------------------------------------------------------------------------
def set_run_font(run, *, name="Times New Roman", size=12, bold=False, italic=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)


def set_paragraph_format(p, *, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=0, line=1.15, first_line=0):
    pf = p.paragraph_format
    pf.alignment = align
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = line
    if first_line:
        pf.first_line_indent = Cm(first_line)


def add_text(p, text, **kwargs):
    run = p.add_run(text)
    set_run_font(run, **kwargs)
    return run


def set_cell_border(cell, **borders):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge, attrs in borders.items():
        element = OxmlElement(f"w:{edge}")
        for key, value in attrs.items():
            element.set(qn(f"w:{key}"), str(value))
        tcBorders.append(element)
    tcPr.append(tcBorders)


def shade_cell(cell, fill="D9E2F3"):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def set_cell_text(cell, text, *, bold=False, size=10, align=WD_ALIGN_PARAGRAPH.CENTER):
    cell.text = ""
    p = cell.paragraphs[0]
    set_paragraph_format(p, align=align, space_before=2, space_after=2, line=1.0)
    add_text(p, text, size=size, bold=bold)


def merge_and_fill(table, r1, c1, r2, c2, text, **kwargs):
    cell = table.cell(r1, c1)
    cell.merge(table.cell(r2, c2))
    set_cell_text(cell, text, **kwargs)
    return cell


def build_document(data: LoanNoticeData, output_path: Path) -> Path:
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)

    header = doc.add_table(rows=1, cols=2)
    left, right = header.rows[0].cells

    left.text = ""
    p = left.paragraphs[0]
    set_paragraph_format(p, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.15)
    add_text(p, "NGÂN HÀNG TMCP ĐẦU TƯ\n", bold=True, size=11)
    add_text(p, "VÀ PHÁT TRIỂN VIỆT NAM\n", bold=True, size=11)
    add_text(p, "CHI NHÁNH ĐÔNG ĐỒNG NAI", bold=True, size=11)

    p2 = left.add_paragraph()
    set_paragraph_format(p2, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, line=1.15)
    add_text(p2, f"Số: {data.so_van_ban}", size=11)
    p3 = left.add_paragraph()
    set_paragraph_format(p3, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.1)
    add_text(
        p3,
        f"(V/v Thông báo nợ quá hạn đối với khách hàng ông/bà {data.ten_khach_hang})",
        size=10,
        italic=True,
    )

    right.text = ""
    p = right.paragraphs[0]
    set_paragraph_format(p, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.15)
    add_text(p, "CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM\n", bold=True, size=11)
    add_text(p, "Độc lập - Tự do - Hạnh phúc", bold=True, size=11)
    p_line = right.add_paragraph()
    set_paragraph_format(p_line, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=6)
    add_text(p_line, "________________________", size=10)
    p_date = right.add_paragraph()
    set_paragraph_format(p_date, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, line=1.15)
    add_text(
        p_date,
        f"Đồng Nai, ngày {data.ngay_bao_cao.day:02d} tháng {data.ngay_bao_cao.month:02d} năm {data.ngay_bao_cao.year}",
        size=11,
        italic=True,
    )

    title = doc.add_paragraph()
    set_paragraph_format(title, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=18, space_after=6, line=1.15)
    add_text(title, "THÔNG BÁO NỢ QUÁ HẠN", bold=True, size=14)

    greeting = doc.add_paragraph()
    set_paragraph_format(greeting, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=10, line=1.15)
    add_text(greeting, f"Kính gửi: ông/bà {data.ten_khach_hang}", bold=True, size=12)

    body1 = doc.add_paragraph()
    set_paragraph_format(body1, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line=1.0, line=1.15)
    add_text(
        body1,
        "Căn cứ Hợp đồng tín dụng ký giữa Khách hàng và Ngân hàng TMCP Đầu tư và Phát triển Việt Nam;",
        size=12,
    )

    ngay_str = data.ngay_bao_cao.strftime("%d/%m/%Y")
    body2 = doc.add_paragraph()
    set_paragraph_format(body2, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line=1.0, space_after=8, line=1.15)
    add_text(
        body2,
        "Ngân hàng TMCP Đầu tư và Phát triển Việt Nam – Chi nhánh Đông Đồng Nai "
        "(sau đây gọi là “Ngân hàng”) trân trọng thông báo đến quý khách được biết về khoản nợ "
        f"tính đến ngày {ngay_str} và đề nghị như sau:",
        size=12,
    )

    unit = doc.add_paragraph()
    set_paragraph_format(unit, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=4)
    add_text(unit, "ĐVT: Đồng", italic=True, size=10)

    table = doc.add_table(rows=4, cols=8)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    thin = {"sz": "4", "val": "single", "color": "000000"}

    merge_and_fill(table, 0, 0, 1, 0, "Số khoản vay", bold=True, size=9)
    merge_and_fill(table, 0, 1, 0, 3, "Dư nợ hiện tại", bold=True, size=9)
    merge_and_fill(table, 0, 4, 0, 6, "Dư nợ quá hạn", bold=True, size=9)
    merge_and_fill(table, 0, 7, 1, 7, "Số ngày\nquá hạn", bold=True, size=9)
    for idx, label in enumerate(["Gốc", "Lãi và\nlãi phạt", "Tổng"], start=1):
        set_cell_text(table.cell(1, idx), label, bold=True, size=9)
    for idx, label in enumerate(["Gốc", "Lãi và\nlãi phạt", "Tổng"], start=4):
        set_cell_text(table.cell(1, idx), label, bold=True, size=9)
    for r in range(2):
        for c in range(8):
            shade_cell(table.cell(r, c), "D9E2F3")

    tong_hien_tai = data.du_no_goc + data.du_no_lai_va_phat
    tong_qua_han = data.qua_han_goc + data.qua_han_lai_va_phat

    values_row = [
        data.so_khoan_vay,
        format_vnd(data.du_no_goc),
        format_vnd(data.du_no_lai_va_phat),
        format_vnd(tong_hien_tai),
        format_vnd(data.qua_han_goc),
        format_vnd(data.qua_han_lai_va_phat),
        format_vnd(tong_qua_han),
        str(data.so_ngay_qua_han),
    ]
    for c, val in enumerate(values_row):
        align = WD_ALIGN_PARAGRAPH.CENTER if c in (0, 7) else WD_ALIGN_PARAGRAPH.RIGHT
        set_cell_text(table.cell(2, c), val, size=9, align=align)

    totals = [
        "Tổng cộng",
        format_vnd(data.du_no_goc),
        format_vnd(data.du_no_lai_va_phat),
        format_vnd(tong_hien_tai),
        format_vnd(data.qua_han_goc),
        format_vnd(data.qua_han_lai_va_phat),
        format_vnd(tong_qua_han),
        "",
    ]
    for c, val in enumerate(totals):
        align = WD_ALIGN_PARAGRAPH.CENTER if c in (0, 7) else WD_ALIGN_PARAGRAPH.RIGHT
        set_cell_text(table.cell(3, c), val, bold=True, size=9, align=align)

    for row in table.rows:
        for cell in row.cells:
            set_cell_border(cell, top=thin, bottom=thin, left=thin, right=thin)

    han_thanh_toan = data.ngay_bao_cao + timedelta(days=data.ngay_them_han_thanh_toan)
    han_str = han_thanh_toan.strftime("%d/%m/%Y")

    summary = doc.add_paragraph()
    set_paragraph_format(summary, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line=1.0, space_before=12, line=1.15)
    add_text(summary, f"Tổng nợ gốc, lãi của quý khách đến ngày {ngay_str} là ", size=12)
    add_text(summary, f"{format_vnd(tong_hien_tai)} đồng", bold=True, size=12)
    add_text(
        summary,
        f" (Bằng chữ: {number_to_vietnamese_words(tong_hien_tai)}). Trong đó, tổng số tiền quá hạn là ",
        size=12,
    )
    add_text(summary, f"{format_vnd(tong_qua_han)} đồng", bold=True, size=12)
    add_text(
        summary,
        f" (Bằng chữ: {number_to_vietnamese_words(tong_qua_han)}), đề nghị quý khách thu xếp để thanh toán "
        f"toàn bộ số tiền nợ quá hạn tại Ngân hàng trước ngày {han_str}. Trường hợp quý khách không thanh toán "
        "đầy đủ nợ quá hạn trong thời gian thông báo này, Ngân hàng sẽ thực hiện các biện pháp khởi kiện, "
        "phát mại tài sản bảo đảm để thu hồi nợ.",
        size=12,
    )

    contact = doc.add_paragraph()
    set_paragraph_format(contact, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line=1.0, space_before=8, line=1.15)
    add_text(
        contact,
        "Mọi thông tin xin vui lòng liên hệ đến Phòng Khách hàng cá nhân – Ngân hàng TMCP Đầu tư và Phát triển "
        f"Việt Nam – Chi nhánh Đông Đồng Nai, số điện thoại: {data.so_dien_thoai}.",
        size=12,
    )

    closing = doc.add_paragraph()
    set_paragraph_format(closing, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=10)
    add_text(closing, "Trân trọng thông báo./.", size=12)

    footer = doc.add_table(rows=1, cols=2)
    left_f, right_f = footer.rows[0].cells
    left_f.text = ""
    p = left_f.paragraphs[0]
    set_paragraph_format(p, align=WD_ALIGN_PARAGRAPH.LEFT, line=1.15)
    add_text(p, "Nơi nhận: (…bản)", bold=True, italic=True, size=11)
    for line in ["- Như trên;", "- Ban Giám đốc B.One", "- P. KHCN B.One;", "- Lưu VT; P. QTTD."]:
        lp = left_f.add_paragraph()
        set_paragraph_format(lp, align=WD_ALIGN_PARAGRAPH.LEFT, line=1.1)
        add_text(lp, line, size=11)

    right_f.text = ""
    p = right_f.paragraphs[0]
    set_paragraph_format(p, align=WD_ALIGN_PARAGRAPH.CENTER, line=1.15)
    add_text(p, "ĐẠI DIỆN NGÂN HÀNG", bold=True, size=12)
    for _ in range(5):
        sp = right_f.add_paragraph()
        set_paragraph_format(sp, align=WD_ALIGN_PARAGRAPH.CENTER)
        add_text(sp, "", size=12)
    name_p = right_f.add_paragraph()
    set_paragraph_format(name_p, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6)
    add_text(name_p, data.nguoi_ky, bold=True, size=12)
    role_p = right_f.add_paragraph()
    set_paragraph_format(role_p, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(role_p, data.chuc_danh_ky, size=11)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tạo Thông báo nợ quá hạn từ 1 dòng Excel/CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Ví dụ:
  # Theo số tài khoản
  python3 scripts/generate_thong_bao_no_qua_han.py --input data/bao_cao.csv --account 406004006532

  # Theo số dòng (1 = dòng dữ liệu đầu tiên sau header)
  python3 scripts/generate_thong_bao_no_qua_han.py --input data/bao_cao.xlsx --row 75

  # Chỉ liệt kê các dòng đang quá hạn
  python3 scripts/generate_thong_bao_no_qua_han.py --input data/bao_cao.csv --list-overdue
""",
    )
    parser.add_argument("--input", "-i", required=True, help="Đường dẫn file .xlsx / .xls / .csv")
    parser.add_argument("--sheet", default=None, help="Tên hoặc chỉ số sheet (Excel). Mặc định sheet đầu")
    parser.add_argument("--row", type=int, default=None, help="Số dòng dữ liệu (1-based, sau header)")
    parser.add_argument("--account", "-a", default=None, help="Số tài khoản / số khoản vay")
    parser.add_argument("--so-van-ban", default="999/TB-BIDV.ĐĐN", help="Số văn bản, VD: 999/TB-BIDV.ĐĐN")
    parser.add_argument("--ngay-bao-cao", default=None, help="Ngày báo cáo dd/mm/yyyy (tuỳ chọn)")
    parser.add_argument("--them-ngay", type=int, default=15, help="Cộng thêm N ngày cho hạn thanh toán (mặc định 15)")
    parser.add_argument("--output", "-o", default=None, help="Đường dẫn file .docx đầu ra")
    parser.add_argument("--list-overdue", action="store_true", help="Liệt kê các dòng có nợ quá hạn rồi thoát")
    parser.add_argument("--allow-not-overdue", action="store_true", help="Vẫn tạo thông báo dù chưa quá hạn")
    return parser.parse_args(argv)


def list_overdue(df: pd.DataFrame, mapping: dict[str, str]) -> None:
    print(f"{'STT':>4}  {'Số TK':<16}  {'Khách hàng':<28}  {'Ngày QH':>8}  {'Gốc QH':>15}")
    print("-" * 80)
    count = 0
    for i, row in df.iterrows():
        goc = parse_number(get_cell(row, mapping, "goc_qua_han"))
        lai = parse_number(get_cell(row, mapping, "lai_qua_han"))
        d1 = parse_number(get_cell(row, mapping, "ngay_qua_han_goc"))
        d2 = parse_number(get_cell(row, mapping, "ngay_qua_han_lai"))
        days = max(d1, d2)
        if days <= 0 and goc <= 0 and lai <= 0:
            continue
        count += 1
        ten = str(get_cell(row, mapping, "ten_khach_hang", "") or "")
        stk = str(get_cell(row, mapping, "so_khoan_vay", "") or "").replace(".0", "")
        print(f"{i + 1:>4}  {stk:<16}  {ten:<28}  {days:>8}  {format_vnd(goc):>15}")
    print("-" * 80)
    print(f"Tổng dòng quá hạn: {count}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    path = Path(args.input)
    if not path.exists():
        print(f"Không tìm thấy file: {path}", file=sys.stderr)
        return 1

    sheet: str | int | None = args.sheet
    if sheet is not None and str(sheet).isdigit():
        sheet = int(sheet)

    df = load_dataframe(path, sheet=sheet)
    mapping = resolve_columns(df)

    if args.list_overdue:
        list_overdue(df, mapping)
        return 0

    if args.row is None and not args.account:
        print("Cần chỉ định --row hoặc --account. Dùng --list-overdue để xem các dòng quá hạn.", file=sys.stderr)
        return 1

    idx, row = select_row(df, mapping, row=args.row, account=args.account)
    ngay_bc = parse_date(args.ngay_bao_cao) if args.ngay_bao_cao else None
    data = row_to_notice(
        row,
        mapping,
        so_van_ban=args.so_van_ban,
        ngay_bao_cao=ngay_bc,
        them_ngay=args.them_ngay,
    )

    tong_qh = data.qua_han_goc + data.qua_han_lai_va_phat
    if data.so_ngay_qua_han <= 0 and tong_qh <= 0 and not args.allow_not_overdue:
        print(
            f"Dòng {idx + 1} (TK {data.so_khoan_vay}) chưa quá hạn — không tạo thông báo. "
            "Thêm --allow-not-overdue nếu vẫn muốn tạo.",
            file=sys.stderr,
        )
        return 2

    if args.output:
        out = Path(args.output)
    else:
        out = Path("output") / f"Thong_bao_no_qua_han_{slugify(data.ten_khach_hang)}_{data.so_khoan_vay}.docx"

    path_out = build_document(data, out)
    tong_ht = data.du_no_goc + data.du_no_lai_va_phat
    print(f"Đã tạo: {path_out}")
    print(f"Dòng Excel/CSV : {idx + 1}")
    print(f"Khách hàng     : {data.ten_khach_hang}")
    print(f"Số khoản vay   : {data.so_khoan_vay}")
    print(f"Ngày báo cáo   : {data.ngay_bao_cao.strftime('%d/%m/%Y')}")
    print(f"Tổng dư nợ HT  : {format_vnd(tong_ht)}")
    print(f"Tổng quá hạn   : {format_vnd(tong_qh)}")
    print(f"Số ngày QH     : {data.so_ngay_qua_han}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
