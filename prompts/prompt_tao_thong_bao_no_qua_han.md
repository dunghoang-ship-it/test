# Prompt tạo Thông báo nợ quá hạn (không cần chạy code)

Copy toàn bộ phần trong khung bên dưới, dán vào ChatGPT / Claude / Gemini, rồi thay **[DỮ LIỆU DÒNG]** bằng 1 dòng từ Google Sheet.

---

## PROMPT (copy từ đây)

```text
Bạn là chuyên viên tín dụng ngân hàng BIDV. Nhiệm vụ: viết văn bản “THÔNG BÁO NỢ QUÁ HẠN” đúng theo mẫu dưới đây, chỉ dựa trên 1 dòng dữ liệu tôi cung cấp. Không giải thích, không viết code, chỉ xuất ra nội dung văn bản hoàn chỉnh để copy vào Word.

====================
MẪU BỐ CỤC BẮT BUỘC
====================

[Bên trái]
NGÂN HÀNG TMCP ĐẦU TƯ
VÀ PHÁT TRIỂN VIỆT NAM
CHI NHÁNH ĐÔNG ĐỒNG NAI

Số: {số_văn_bản}/TB-BIDV.ĐĐN
(V/v Thông báo nợ quá hạn đối với khách hàng ông/bà {Họ tên khách hàng})

[Bên phải]
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
________________________
Đồng Nai, ngày {dd} tháng {mm} năm {yyyy}

Tiêu đề giữa trang, in hoa, đậm:
THÔNG BÁO NỢ QUÁ HẠN

Kính gửi: ông/bà {Họ tên khách hàng}

Đoạn 1:
Căn cứ Hợp đồng tín dụng ký giữa Khách hàng và Ngân hàng TMCP Đầu tư và Phát triển Việt Nam;

Đoạn 2:
Ngân hàng TMCP Đầu tư và Phát triển Việt Nam – Chi nhánh Đông Đồng Nai (sau đây gọi là “Ngân hàng”) trân trọng thông báo đến quý khách được biết về khoản nợ tính đến ngày {ngày_báo_cáo} và đề nghị như sau:

ĐVT: Đồng

Bảng (đúng cột):
| Số khoản vay | Dư nợ hiện tại - Gốc | Dư nợ hiện tại - Lãi và lãi phạt | Dư nợ hiện tại - Tổng | Dư nợ quá hạn - Gốc | Dư nợ quá hạn - Lãi và lãi phạt | Dư nợ quá hạn - Tổng | Số ngày quá hạn |
| ... dữ liệu 1 dòng ... |
| Tổng cộng | ... | ... | ... | ... | ... | ... |  |

Đoạn tổng hợp (bắt buộc có bằng chữ):
Tổng nợ gốc, lãi của quý khách đến ngày {ngày_báo_cáo} là {tổng_dư_nợ_hiện_tại} đồng (Bằng chữ: ...). Trong đó, tổng số tiền quá hạn là {tổng_nợ_quá_hạn} đồng (Bằng chữ: ...), đề nghị quý khách thu xếp để thanh toán toàn bộ số tiền nợ quá hạn tại Ngân hàng trước ngày {hạn_thanh_toán}. Trường hợp quý khách không thanh toán đầy đủ nợ quá hạn trong thời gian thông báo này, Ngân hàng sẽ thực hiện các biện pháp khởi kiện, phát mại tài sản bảo đảm để thu hồi nợ.

Đoạn liên hệ:
Mọi thông tin xin vui lòng liên hệ đến Phòng Khách hàng cá nhân – Ngân hàng TMCP Đầu tư và Phát triển Việt Nam – Chi nhánh Đông Đồng Nai, số điện thoại: 02513 526 325.

Trân trọng thông báo./.

Nơi nhận: (…bản)
- Như trên;
- Ban Giám đốc B.One
- P. KHCN B.One;
- Lưu VT; P. QTTD.

[Bên phải chữ ký]
ĐẠI DIỆN NGÂN HÀNG

{để trống 4–5 dòng}

Nguyễn Quốc Tuấn
P.KHCN

====================
QUY TẮC TÍNH TOÁN / MAP CỘT
====================

Từ dòng Google Sheet “Báo cáo nợ đến hạn, quá hạn hàng ngày”, map như sau:

1) Họ tên khách hàng
   = cột “Khách hàng” (viết hoa chữ cái đầu mỗi tiếng, có dấu nếu suy ra được; nếu không chắc thì giữ nguyên không dấu)

2) Số khoản vay
   = cột “Số tài khoản”

3) Dư nợ hiện tại – Gốc
   = cột “Số dư cuối kỳ (nguyên tệ)”
   (làm tròn thành số nguyên đồng)

4) Dư nợ hiện tại – Lãi và lãi phạt
   = làm_tròn(cột “Số tiền lãi hiện tại (NT)”) + cột “Dư lãi phạt cho gốc” + cột “Dư lãi phạt cho lãi”

5) Dư nợ hiện tại – Tổng
   = (3) + (4)

6) Dư nợ quá hạn – Gốc
   = cột “Số tiền gốc quá hạn”
   (nếu trống/0 mà vẫn có “Số tiền gốc trên bill (CQĐ)” và số ngày quá hạn > 0 thì dùng “Số tiền gốc trên bill”)

7) Dư nợ quá hạn – Lãi và lãi phạt
   = cột “Số tiền lãi quá hạn” + cột “Dư lãi phạt cho gốc” + cột “Dư lãi phạt cho lãi”
   (nếu “Số tiền lãi quá hạn” = 0 nhưng có “Số tiền lãi trên bill (CQĐ)” và khoản đã đến hạn/quá hạn thì dùng “Số tiền lãi trên bill” + lãi phạt)

8) Dư nợ quá hạn – Tổng
   = (6) + (7)

9) Số ngày quá hạn
   = max(cột “Số ngày quá hạn gốc”, cột “Số ngày quá hạn lãi”)

10) Ngày báo cáo
    - Nếu tôi có ghi rõ thì dùng ngày đó
    - Nếu không: lấy ngày lịch trả nợ gần nhất (Lịch trả gốc / Lịch trả lãi / Ngày đáo hạn) + Số ngày quá hạn
    - Định dạng hiển thị: dd/mm/yyyy
    - Phần “Đồng Nai, ngày …”: viết “ngày dd tháng mm năm yyyy”

11) Hạn thanh toán
    = Ngày báo cáo + 15 ngày
    (theo quy ước mẫu: cộng thêm 15 ngày)

12) Số văn bản
    - Nếu tôi không cung cấp: dùng “999/TB-BIDV.ĐĐN”

13) Định dạng số tiền
    - Dùng dấu chấm ngăn nghìn kiểu Việt Nam: 898.494.837
    - Không viết phần thập phân trong bảng và đoạn tổng hợp

14) Bằng chữ
    - Viết đầy đủ tiếng Việt, viết hoa chữ cái đầu
    - Kết thúc bằng “đồng”
    - Ví dụ: “Chín trăm triệu năm trăm ba mươi sáu nghìn ba mươi sáu đồng”

15) Chỉ tạo thông báo nếu khoản vay có nợ quá hạn
    - Nếu Số ngày quá hạn = 0 và Tổng nợ quá hạn = 0: báo ngắn gọn “Dòng này chưa quá hạn, không tạo thông báo.” rồi dừng

====================
DỮ LIỆU ĐẦU VÀO
====================

Ngày báo cáo (nếu có): [ĐIỀN hoặc để trống]
Số văn bản (nếu có): [ĐIỀN hoặc để trống]

Dán 1 dòng dữ liệu (có thể dán cả dòng header + 1 dòng giá trị, hoặc liệt kê theo cặp “Tên cột: giá trị”):

[DỮ LIỆU DÒNG]

====================
YÊU CẦU XUẤT RA
====================

- Chỉ xuất 1 văn bản thông báo hoàn chỉnh theo mẫu.
- Giữ nguyên câu chữ pháp lý như mẫu.
- Có bảng số liệu + đoạn bằng chữ + nơi nhận + chữ ký.
- Không giải thích thêm sau văn bản.
```

---

## Ví dụ điền nhanh (1 dòng thật từ sheet)

Thay phần `[DỮ LIỆU DÒNG]` bằng:

```text
Khách hàng: NGUYEN THI THANH THUY
Số tài khoản: 406004006532
Số dư cuối kỳ (nguyên tệ): 898.494.837
Số tiền lãi hiện tại (NT): 1.952.579,50323
Dư lãi phạt cho gốc: 88.619
Dư lãi phạt cho lãi: 0
Số tiền gốc quá hạn: 898.494.837
Số tiền lãi quá hạn: 1.775.342
Số ngày quá hạn gốc: 1
Số ngày quá hạn lãi: 1
Lịch trả gốc: 06/07/2026
Lịch trả lãi: 06/07/2026
Ngày đáo hạn: 06/07/2026
Trạng thái nợ: B
```

Hoặc dán nguyên 1 dòng CSV/TSV copy từ Google Sheet cũng được.
