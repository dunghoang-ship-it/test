# Thông báo nợ quá hạn (mẫu BIDV)

Tạo văn bản **Thông báo nợ quá hạn** theo mẫu Google Docs, lấy dữ liệu từ 1 dòng trong báo cáo Google Sheets.

## Kết quả ví dụ

- `output/Thong_bao_no_qua_han_Nguyen_Thi_Thanh_Thuy.docx` — file Word theo đúng bố cục mẫu
- `output/Thong_bao_no_qua_han_Nguyen_Thi_Thanh_Thuy.txt` — bản xem nhanh + ghi chú map cột

### Dòng dữ liệu đã dùng

| Trường | Giá trị |
| --- | --- |
| Khách hàng | Nguyễn Thị Thanh Thúy |
| Số khoản vay | 406004006532 |
| Số dư cuối kỳ | 898.494.837 |
| Lãi hiện tại + lãi phạt | 2.041.199 |
| Gốc quá hạn | 898.494.837 |
| Lãi quá hạn + lãi phạt | 1.863.961 |
| Số ngày quá hạn | 1 |
| Trạng thái nợ | B |

## Chạy lại

```bash
pip install python-docx
python3 scripts/generate_thong_bao_no_qua_han.py
```

Sửa dữ liệu trong `scripts/generate_thong_bao_no_qua_han.py` (class `LoanNoticeData` trong `main()`) để tạo thông báo cho dòng khác.
