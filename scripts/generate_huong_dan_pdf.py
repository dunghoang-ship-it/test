#!/usr/bin/env python3
"""Generate a clear Vietnamese PDF guide for Windows setup."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_MONO_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

pdfmetrics.registerFont(TTFont("DejaVu", FONT_REG))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", FONT_BOLD))
pdfmetrics.registerFont(TTFont("DejaVuMono", FONT_MONO))
pdfmetrics.registerFont(TTFont("DejaVuMono-Bold", FONT_MONO_BOLD))

NAVY = colors.HexColor("#0B3D5C")
TEAL = colors.HexColor("#0E7490")
LIGHT = colors.HexColor("#F0F7FA")
CODE_BG = colors.HexColor("#F4F6F8")
BORDER = colors.HexColor("#CBD5E1")
WARN_BG = colors.HexColor("#FFF7ED")
WARN_BORDER = colors.HexColor("#F59E0B")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="DejaVu-Bold",
            fontSize=22,
            leading=28,
            textColor=colors.white,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            fontName="DejaVu",
            fontSize=12,
            leading=16,
            textColor=colors.white,
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1VN",
            fontName="DejaVu-Bold",
            fontSize=14,
            leading=20,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2VN",
            fontName="DejaVu-Bold",
            fontSize=11.5,
            leading=16,
            textColor=TEAL,
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyVN",
            fontName="DejaVu",
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=4,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletVN",
            fontName="DejaVu",
            fontSize=10,
            leading=15,
            leftIndent=12,
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeVN",
            fontName="DejaVuMono",
            fontSize=8.5,
            leading=12.5,
            textColor=colors.HexColor("#111827"),
            backColor=CODE_BG,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableCell",
            fontName="DejaVu",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#111827"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableHead",
            fontName="DejaVu-Bold",
            fontSize=8.5,
            leading=12,
            textColor=colors.white,
        )
    )
    styles.add(
        ParagraphStyle(
            name="FooterVN",
            fontName="DejaVu",
            fontSize=8,
            textColor=colors.HexColor("#64748B"),
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TipVN",
            fontName="DejaVu",
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#7C2D12"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="LinkVN",
            fontName="DejaVu",
            fontSize=9,
            leading=13,
            textColor=TEAL,
        )
    )
    return styles


def code_block(text: str, styles) -> Table:
    pre = Preformatted(text.strip("\n"), styles["CodeVN"])
    t = Table([[pre]], colWidths=[16.5 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                ("BOX", (0, 0), (-1, -1), 0.8, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def tip_box(text: str, styles) -> Table:
    p = Paragraph(text, styles["TipVN"])
    t = Table([[Paragraph("<b>Lưu ý</b>", styles["TipVN"])], [p]], colWidths=[16.5 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WARN_BG),
                ("BOX", (0, 0), (-1, -1), 1, WARN_BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def simple_table(headers, rows, styles, col_widths):
    data = [[Paragraph(h, styles["TableHead"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), styles["TableCell"]) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 12 * mm, A4[0], 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("DejaVu", 8)
    canvas.drawString(2 * cm, A4[1] - 8 * mm, "BIDV Đông Đồng Nai — Hướng dẫn cài đặt tool Thông báo nợ quá hạn")
    canvas.setFillColor(colors.HexColor("#E2E8F0"))
    canvas.rect(0, 0, A4[0], 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#475569"))
    canvas.setFont("DejaVu", 8)
    canvas.drawCentredString(A4[0] / 2, 5 * mm, f"Trang {doc.page}")
    canvas.restoreState()


def build_pdf(output: Path) -> Path:
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2 * cm,
        title="Hướng dẫn cài đặt Windows - Thông báo nợ quá hạn",
        author="BIDV Đông Đồng Nai",
    )

    story = []

    # Cover banner
    cover = Table(
        [
            [Paragraph("HƯỚNG DẪN CÀI ĐẶT TRÊN WINDOWS", styles["CoverTitle"])],
            [Paragraph("Tool tạo Thông báo nợ quá hạn (BIDV Đông Đồng Nai)", styles["CoverSub"])],
            [Paragraph("Dành cho máy tính mới — làm theo từng bước", styles["CoverSub"])],
        ],
        colWidths=[16.5 * cm],
    )
    cover.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )
    story.append(cover)
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            "Tài liệu này hướng dẫn cài <b>Git</b>, <b>Python</b>, tải project về máy và chạy lệnh tạo file Word thông báo nợ quá hạn.",
            styles["BodyVN"],
        )
    )
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER, spaceAfter=6))

    # Mục lục ngắn
    story.append(Paragraph("Nội dung chính", styles["H1VN"]))
    for item in [
        "1. Cài Git",
        "2. Cài Python",
        "3. Clone project về máy",
        "4. Cài thư viện Python",
        "5. Chạy thử với dữ liệu mẫu",
        "6. Dùng file Excel thật",
        "7. Điền linh hoạt đơn vị liên hệ (bỏ P.KHCN)",
        "8. Lệnh trên Mac",
        "9. Các cột Excel cần có",
        "10. Tham số thường dùng",
        "11. Lỗi hay gặp",
        "12. Cập nhật code mới nhất",
    ]:
        story.append(Paragraph(f"• {item}", styles["BulletVN"]))

    # 1
    story.append(Paragraph("1. Cài Git", styles["H1VN"]))
    story.append(Paragraph("1) Tải Git tại: <link href='https://git-scm.com/download/win'>https://git-scm.com/download/win</link>", styles["BodyVN"]))
    story.append(Paragraph("2) Cài với lựa chọn mặc định (bấm <b>Next</b> đến hết).", styles["BodyVN"]))
    story.append(Paragraph("3) Mở <b>Command Prompt (CMD)</b> hoặc <b>PowerShell</b>, gõ:", styles["BodyVN"]))
    story.append(code_block("git --version", styles))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Nếu hiện số phiên bản (ví dụ <b>git version 2.45.x</b>) là đã cài thành công.", styles["BodyVN"]))

    # 2
    story.append(Paragraph("2. Cài Python", styles["H1VN"]))
    story.append(Paragraph("1) Tải Python 3.11 hoặc 3.12 tại: <link href='https://www.python.org/downloads/windows/'>https://www.python.org/downloads/windows/</link>", styles["BodyVN"]))
    story.append(Paragraph("2) Chạy file cài đặt.", styles["BodyVN"]))
    story.append(tip_box("Bắt buộc tick ô <b>Add python.exe to PATH</b> trước khi bấm Install Now.", styles))
    story.append(Spacer(1, 4))
    story.append(Paragraph("3) Kiểm tra trong CMD:", styles["BodyVN"]))
    story.append(code_block("python --version\npip --version", styles))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Nếu lệnh <b>python</b> không nhận: đóng CMD rồi mở lại. Nếu vẫn lỗi, cài lại Python và nhớ tick Add to PATH.", styles["BodyVN"]))

    # 3
    story.append(Paragraph("3. Clone project về máy", styles["H1VN"]))
    story.append(Paragraph("Mở CMD và chạy lần lượt:", styles["BodyVN"]))
    story.append(
        code_block(
            "cd %USERPROFILE%\\Desktop\n"
            "git clone https://github.com/dunghoang-ship-it/test.git\n"
            "cd test\n"
            "git checkout cursor/thong-bao-no-qua-han-893f",
            styles,
        )
    )
    story.append(Spacer(1, 4))
    story.append(Paragraph("Sau bước này, trên Desktop sẽ có thư mục <b>test</b>.", styles["BodyVN"]))

    # 4
    story.append(Paragraph("4. Cài thư viện Python", styles["H1VN"]))
    story.append(Paragraph("Đang đứng trong thư mục <b>test</b>, chạy:", styles["BodyVN"]))
    story.append(code_block("python -m pip install -r requirements.txt", styles))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Các thư viện sẽ được cài: <b>python-docx</b>, <b>pandas</b>, <b>openpyxl</b>.", styles["BodyVN"]))

    # 5
    story.append(Paragraph("5. Chạy thử với dữ liệu mẫu", styles["H1VN"]))

    story.append(Paragraph("5.1. Xem các dòng đang quá hạn", styles["H2VN"]))
    story.append(
        code_block(
            "python scripts\\generate_thong_bao_no_qua_han.py -i data\\bao_cao_no_qua_han_mau.xlsx --list-overdue",
            styles,
        )
    )

    story.append(Paragraph("5.2. Tạo 1 thông báo theo số tài khoản", styles["H2VN"]))
    story.append(
        code_block(
            "python scripts\\generate_thong_bao_no_qua_han.py -i data\\bao_cao_no_qua_han_mau.xlsx --account 406004006532",
            styles,
        )
    )
    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>--account</b> = số tài khoản / số khoản vay trong Excel.", styles["BodyVN"]))

    story.append(Paragraph("5.3. Tạo thông báo theo số dòng", styles["H2VN"]))
    story.append(Paragraph("(<b>1</b> = dòng dữ liệu đầu tiên sau dòng tiêu đề)", styles["BodyVN"]))
    story.append(
        code_block(
            "python scripts\\generate_thong_bao_no_qua_han.py -i data\\bao_cao_no_qua_han_mau.xlsx --row 3",
            styles,
        )
    )

    story.append(Paragraph("5.4. Tạo TẤT CẢ thông báo cho các dòng quá hạn", styles["H2VN"]))
    story.append(
        code_block(
            "python scripts\\generate_thong_bao_no_qua_han.py -i data\\bao_cao_no_qua_han_mau.xlsx --all-overdue",
            styles,
        )
    )
    story.append(Spacer(1, 4))
    story.append(Paragraph("File Word sẽ nằm trong thư mục:", styles["BodyVN"]))
    story.append(code_block("test\\output\\", styles))
    story.append(Spacer(1, 3))
    story.append(
        Paragraph(
            "Ví dụ tên file: <b>Thong_bao_no_qua_han_Nguyen_Thi_Thanh_Thuy_406004006532.docx</b>",
            styles["BodyVN"],
        )
    )

    # 6
    story.append(Paragraph("6. Dùng file Excel thật của bạn", styles["H1VN"]))
    for step in [
        "Mở Google Sheet báo cáo nợ đến hạn / quá hạn.",
        "Chọn <b>File → Download → Microsoft Excel (.xlsx)</b>.",
        "Copy file vừa tải vào thư mục <b>test\\data\\</b> (ví dụ đổi tên thành <b>bao_cao.xlsx</b>).",
        "Chạy các lệnh bên dưới.",
    ]:
        story.append(Paragraph(f"• {step}", styles["BulletVN"]))
    story.append(Spacer(1, 4))
    story.append(
        code_block(
            "REM Xem trước các dòng quá hạn\n"
            "python scripts\\generate_thong_bao_no_qua_han.py -i data\\bao_cao.xlsx --list-overdue\n\n"
            "REM Tạo tất cả thông báo quá hạn\n"
            "python scripts\\generate_thong_bao_no_qua_han.py -i data\\bao_cao.xlsx --all-overdue",
            styles,
        )
    )
    story.append(Paragraph("Tuỳ chọn đánh số văn bản tăng dần + lưu thư mục riêng:", styles["H2VN"]))
    story.append(
        code_block(
            "python scripts\\generate_thong_bao_no_qua_han.py -i data\\bao_cao.xlsx --all-overdue "
            "--so-van-ban-start 1000 --output-dir output\\batch",
            styles,
        )
    )

    # 7 - flexible contact
    story.append(Paragraph("7. Điền linh hoạt đơn vị liên hệ (bỏ P.KHCN)", styles["H1VN"]))
    story.append(
        Paragraph(
            "Đoạn liên hệ trong thông báo có thể đổi theo phòng/PGD. Chữ ký chỉ còn <b>tên người ký</b>, "
            "đã <b>bỏ dòng P.KHCN</b>.",
            styles["BodyVN"],
        )
    )
    story.append(Paragraph("Ví dụ đổi đơn vị liên hệ + số điện thoại:", styles["BodyVN"]))
    story.append(
        code_block(
            "python scripts\\generate_thong_bao_no_qua_han.py -i data\\bao_cao.xlsx --all-overdue ^\n"
            "  --don-vi-lien-he \"PGD Nhơn Trạch – Ngân hàng TMCP Đầu tư và Phát triển Việt Nam – Chi nhánh Đông Đồng Nai\" ^\n"
            "  --so-dien-thoai \"02513 123 456\" ^\n"
            "  --nguoi-ky \"Nguyễn Quốc Tuấn\"",
            styles,
        )
    )
    story.append(Spacer(1, 4))
    story.append(tip_box(
        "Nếu không truyền <b>--don-vi-lien-he</b>, mặc định vẫn là: "
        "Phòng Khách hàng cá nhân – Ngân hàng TMCP Đầu tư và Phát triển Việt Nam – Chi nhánh Đông Đồng Nai.",
        styles,
    ))

    # 8 - Mac
    story.append(Paragraph("8. Lệnh trên Mac", styles["H1VN"]))
    story.append(
        Paragraph(
            "Trên Mac dùng dấu <b>/</b> (không dùng <b>\\</b>) và lệnh <b>python3</b>:",
            styles["BodyVN"],
        )
    )
    story.append(
        code_block(
            "cd ~/Desktop/test\n"
            "git pull origin cursor/thong-bao-no-qua-han-893f\n\n"
            "python3 scripts/generate_thong_bao_no_qua_han.py -i data/bao_cao_no_qua_han_mau.xlsx --list-overdue\n\n"
            "python3 scripts/generate_thong_bao_no_qua_han.py -i data/bao_cao_no_qua_han_mau.xlsx --all-overdue\n\n"
            "python3 scripts/generate_thong_bao_no_qua_han.py -i data/bao_cao.xlsx --all-overdue \\\n"
            "  --don-vi-lien-he \"PGD Nhơn Trạch – Ngân hàng TMCP Đầu tư và Phát triển Việt Nam – Chi nhánh Đông Đồng Nai\" \\\n"
            "  --so-dien-thoai \"02513 123 456\"",
            styles,
        )
    )
    story.append(Spacer(1, 4))
    story.append(
        tip_box(
            "Nếu báo <b>unrecognized arguments: --all-overdue</b> thì đang chạy bản code cũ. "
            "Chạy <b>git pull origin cursor/thong-bao-no-qua-han-893f</b> rồi thử lại.",
            styles,
        )
    )

    # 9
    story.append(Paragraph("9. Các cột Excel cần có", styles["H1VN"]))
    story.append(
        simple_table(
            ["Cột trong Excel", "Dùng để"],
            [
                ["Khách hàng", "Tên người nhận thông báo"],
                ["Số tài khoản", "Số khoản vay"],
                ["Số dư cuối kỳ (nguyên tệ)", "Dư nợ gốc hiện tại"],
                ["Số tiền lãi hiện tại (NT)", "Lãi hiện tại"],
                ["Số tiền gốc quá hạn", "Gốc quá hạn"],
                ["Số tiền lãi quá hạn", "Lãi quá hạn"],
                ["Số ngày quá hạn gốc / lãi", "Số ngày quá hạn"],
                ["Dư lãi phạt cho gốc / lãi", "Lãi phạt"],
                ["Lịch trả gốc / lãi", "Suy ra ngày báo cáo (nếu không truyền tay)"],
            ],
            styles,
            [7.5 * cm, 9 * cm],
        )
    )

    # 10
    story.append(Paragraph("10. Tham số thường dùng", styles["H1VN"]))
    story.append(
        simple_table(
            ["Tham số", "Ý nghĩa"],
            [
                ["-i / --input", "Đường dẫn file Excel/CSV"],
                ["--account", "Số tài khoản cần tạo thông báo"],
                ["--row", "Số dòng dữ liệu (1 = dòng đầu sau header)"],
                ["--all-overdue", "Tạo cho tất cả dòng đang quá hạn"],
                ["--list-overdue", "Chỉ liệt kê, không tạo file"],
                ["--don-vi-lien-he \"...\"", "Đơn vị liên hệ (điền linh hoạt)"],
                ["--so-dien-thoai \"...\"", "Số điện thoại liên hệ"],
                ["--nguoi-ky \"...\"", "Tên người ký (không in P.KHCN)"],
                ["--ngay-bao-cao 07/07/2026", "Ghi đè ngày báo cáo"],
                ["--them-ngay 15", "Cộng thêm N ngày cho hạn thanh toán"],
                ["--output-dir output", "Thư mục lưu file Word"],
                ["--allow-not-overdue", "Vẫn tạo dù dòng chưa quá hạn"],
            ],
            styles,
            [6.5 * cm, 10 * cm],
        )
    )

    # 11
    story.append(Paragraph("11. Lỗi hay gặp và cách xử lý", styles["H1VN"]))
    story.append(
        simple_table(
            ["Lỗi", "Cách xử lý"],
            [
                ["'python' is not recognized", "Cài lại Python, tick Add python.exe to PATH, mở lại CMD"],
                ["'git' is not recognized", "Cài Git rồi mở lại CMD"],
                ["pip không chạy", "Dùng: python -m pip install -r requirements.txt"],
                ["Không tìm thấy file", "Kiểm tra đang đứng đúng thư mục test"],
                ["Thiếu cột bắt buộc", "File Excel thiếu cột Khách hàng / Số tài khoản / Số dư cuối kỳ"],
                ["chưa quá hạn — không tạo", "Dòng đó không có nợ quá hạn; chọn dòng khác hoặc dùng --all-overdue"],
                ["unrecognized arguments: --all-overdue", "Code cũ — chạy git pull rồi thử lại"],
            ],
            styles,
            [6.5 * cm, 10 * cm],
        )
    )

    # 12
    story.append(Paragraph("12. Cập nhật code mới nhất (sau này)", styles["H1VN"]))
    story.append(Paragraph("Khi đã clone rồi, chỉ cần:", styles["BodyVN"]))
    story.append(
        code_block(
            "cd %USERPROFILE%\\Desktop\\test\n"
            "git pull origin cursor/thong-bao-no-qua-han-893f\n"
            "python -m pip install -r requirements.txt",
            styles,
        )
    )
    story.append(Paragraph("Trên Mac:", styles["BodyVN"]))
    story.append(
        code_block(
            "cd ~/Desktop/test\n"
            "git pull origin cursor/thong-bao-no-qua-han-893f\n"
            "python3 -m pip install -r requirements.txt",
            styles,
        )
    )

    # Links
    story.append(Paragraph("13. Link hữu ích", styles["H1VN"]))
    links = [
        ("Repository", "https://github.com/dunghoang-ship-it/test"),
        ("Branch đang dùng", "cursor/thong-bao-no-qua-han-893f"),
        ("Pull request", "https://github.com/dunghoang-ship-it/test/pull/1"),
        (
            "Tải file TXT hướng dẫn",
            "https://github.com/dunghoang-ship-it/test/raw/cursor/thong-bao-no-qua-han-893f/HUONG_DAN_CAI_DAT_WINDOWS.txt",
        ),
        (
            "Tải file PDF này",
            "https://github.com/dunghoang-ship-it/test/raw/cursor/thong-bao-no-qua-han-893f/HUONG_DAN_CAI_DAT_WINDOWS.pdf",
        ),
    ]
    for label, url in links:
        if url.startswith("http"):
            story.append(Paragraph(f"• <b>{label}:</b> <link href='{url}'>{url}</link>", styles["BodyVN"]))
        else:
            story.append(Paragraph(f"• <b>{label}:</b> {url}", styles["BodyVN"]))

    story.append(Spacer(1, 12))
    story.append(tip_box("Khi chạy <b>--all-overdue</b>, tool chỉ tạo thông báo cho các dòng <b>đang quá hạn</b>. Các dòng chưa quá hạn sẽ được bỏ qua.", styles))

    output.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    return output


def main():
    out = Path("/workspace/HUONG_DAN_CAI_DAT_WINDOWS.pdf")
    path = build_pdf(out)
    print(f"Created: {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
