# Thông báo nợ quá hạn (mẫu BIDV)

Tạo văn bản **Thông báo nợ quá hạn** theo mẫu Google Docs, đọc thẳng từ file Excel/CSV.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy với Excel / CSV

### 1) Xem các dòng đang quá hạn

```bash
python3 scripts/generate_thong_bao_no_qua_han.py \
  --input data/bao_cao_no_qua_han_mau.csv \
  --list-overdue
```

### 2) Tạo thông báo theo số tài khoản

```bash
python3 scripts/generate_thong_bao_no_qua_han.py \
  --input data/bao_cao_no_qua_han_mau.xlsx \
  --account 406004006532
```

### 3) Tạo thông báo theo số dòng (1 = dòng đầu sau header)

```bash
python3 scripts/generate_thong_bao_no_qua_han.py \
  --input data/bao_cao_no_qua_han_mau.csv \
  --row 3
```

### 4) Tạo TẤT CẢ thông báo cho các dòng quá hạn trong file

```bash
python3 scripts/generate_thong_bao_no_qua_han.py \
  --input data/bao_cao_no_qua_han_mau.xlsx \
  --all-overdue
```

Tuỳ chọn đánh số văn bản tăng dần:

```bash
python3 scripts/generate_thong_bao_no_qua_han.py \
  --input data/bao_cao_no_qua_han_mau.xlsx \
  --all-overdue \
  --so-van-ban-start 1000 \
  --output-dir output/batch
```

### Tuỳ chọn thêm

| Tham số | Ý nghĩa |
| --- | --- |
| `--all-overdue` | Tạo thông báo cho mọi dòng đang quá hạn |
| `--output-dir output` | Thư mục lưu file khi chạy hàng loạt |
| `--so-van-ban-start 1000` | Số văn bản tăng dần khi `--all-overdue` |
| `--sheet 0` | Chọn sheet Excel (tên hoặc chỉ số) |
| `--ngay-bao-cao 07/07/2026` | Ghi đè ngày báo cáo |
| `--so-van-ban 999/TB-BIDV.ĐĐN` | Số văn bản |
| `--them-ngay 15` | Cộng thêm N ngày cho hạn thanh toán |
| `--output duong/dan.docx` | Đường dẫn file Word đầu ra (1 dòng) |
| `--allow-not-overdue` | Vẫn tạo dù dòng chưa quá hạn |

File Word mặc định lưu vào `output/Thong_bao_no_qua_han_<Ten>_<SoTK>.docx`.

## File dữ liệu mẫu

- `data/bao_cao_no_qua_han_mau.csv`
- `data/bao_cao_no_qua_han_mau.xlsx`

Bạn có thể thay bằng file xuất từ Google Sheet (File → Download → `.xlsx` hoặc `.csv`), miễn còn các cột:

- Khách hàng
- Số tài khoản
- Số dư cuối kỳ (nguyên tệ)
- Số tiền lãi hiện tại (NT)
- Số tiền gốc quá hạn / Số tiền lãi quá hạn
- Số ngày quá hạn gốc / lãi
- Dư lãi phạt cho gốc / lãi
- Lịch trả gốc / lãi (để suy ngày báo cáo nếu không truyền `--ngay-bao-cao`)

## Không cần chạy code (dùng prompt)

Mở `prompts/prompt_tao_thong_bao_no_qua_han.md`, copy phần **PROMPT**, dán vào ChatGPT/Claude/Gemini, rồi thay `[DỮ LIỆU DÒNG]` bằng 1 dòng từ Google Sheet.
