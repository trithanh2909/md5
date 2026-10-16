# Kịch bản thuyết trình tổng thể (gợi ý 10-12 phút + demo)

Điều chỉnh thời lượng theo yêu cầu giảng viên. Mỗi thành viên cần đọc toàn bộ kịch bản và có thể trả lời câu hỏi ngoài phần được giao.

## Slide 1 — Đề tài và mục tiêu (Thành viên 1, 30-40 giây)

“Nhóm em trình bày về hàm băm MD5, tập trung vào cấu trúc Merkle–Damgård, bốn vòng 64 bước, cách tự cài đặt và lý do MD5 không còn phù hợp cho các ứng dụng mật mã cần chống va chạm. Nhóm không xem MD5 là thuật toán được khuyến nghị cho hệ thống mới; mục tiêu là hiểu nguyên lý và kiểm chứng bằng chương trình.”

## Slide 2 — Khái niệm hàm băm (Thành viên 1, 50 giây)

“Hàm băm nhận byte đầu vào dài tùy ý và tạo digest có độ dài cố định. MD5 tạo 128 bit, tương đương 32 ký tự hex. Hàm băm khác mã hóa vì không có quy trình giải mã để khôi phục duy nhất thông điệp. Ba tính chất cần phân biệt là kháng tiền ảnh, kháng tiền ảnh thứ hai và kháng va chạm.”

## Slide 3 — Lịch sử và đặc tả (Thành viên 1, 40 giây)

“MD5 do Ronald Rivest thiết kế và được mô tả trong RFC 1321 tháng 4 năm 1992. RFC này là nguồn chính để nhóm triển khai padding, trạng thái, 64 bước và test vector. Về an toàn, nhóm đối chiếu RFC 6151 và RFC 9155.”

## Slide 4 — Merkle–Damgård và padding (Thành viên 2, 60 giây)

“Thông điệp được đệm trước rồi chia thành khối 512 bit. Padding gồm bit 1, các bit 0 cho đến độ dài 448 modulo 512, sau đó nối 64 bit độ dài ban đầu little-endian. Mỗi khối đi cùng trạng thái băm hiện tại vào hàm nén; trạng thái kết quả được dùng cho khối sau. Đây là ý tưởng nối trạng thái của cấu trúc Merkle–Damgård.”

## Slide 5 — Thanh ghi và dữ liệu khối (Thành viên 2, 50 giây)

“Một khối 512 bit gồm 16 từ 32 bit. Trạng thái gồm A, B, C và D, mỗi từ 32 bit, với giá trị khởi tạo theo RFC 1321. Byte order rất quan trọng: code đọc từ dữ liệu theo little-endian và xuất digest theo cùng quy ước.”

## Slide 6 — Bốn vòng, 64 bước (Thành viên 2, 75 giây)

“Bốn vòng lần lượt sử dụng F, G, H và I. Mỗi vòng có 16 bước. Mỗi bước chọn một từ trong 16 từ, kết hợp hàm logic, một hằng số và trạng thái, cộng modulo 2 mũ 32 rồi xoay trái một số bit quy định. Cuối mỗi khối, trạng thái làm việc được cộng trở lại trạng thái tích lũy. Chương trình có tùy chọn trace để hiển thị A/B/C/D.”

## Slide 7 — Kiến trúc và code (Thành viên 3, 60 giây)

“Nhóm chia module để dễ kiểm tra. `md5_core.py` chứa thuật toán tự viết. `integrity.py` làm việc với tệp và digest tham chiếu. `main.py` là menu, không chứa phép biến đổi MD5. `test_md5.py` kiểm thử bằng test vector và đối chiếu với thư viện chuẩn. Đặc biệt, `hashlib.md5` không được dùng trong phần lõi.”

## Slide 8 — Kiểm thử (Thành viên 3, 45 giây)

“Bộ test gồm các vector RFC như chuỗi rỗng và `abc`, các độ dài quanh biên 55/56 và 63/64 byte, dữ liệu nhiều khối, UTF-8 và trace 64 bước. Điều này giúp kiểm tra cả kết quả đầu ra lẫn các lỗi dễ xảy ra ở padding và thứ tự byte. Sau khi có thay đổi code, nhóm chạy lại lệnh unittest.”

## Slide 9 — Điểm yếu va chạm (Thành viên 4, 75 giây)

“Va chạm có nghĩa là hai thông điệp khác nhau nhưng digest giống nhau. Với hàm băm lý tưởng 128 bit, birthday bound cho mức xấp xỉ 2 mũ 64 phép thử, nhưng các cuộc tấn công chuyên biệt vào MD5 khai thác cấu trúc thuật toán và hiệu quả hơn vét cạn. RFC 6151 khẳng định MD5 không còn chấp nhận được khi cần chống va chạm, ví dụ chữ ký số.”

## Slide 10 — So sánh và kết luận (Thành viên 4, 60 giây)

“SHA-256 tạo digest 256 bit và thuộc SHA-2; NIST khuyến nghị SHA-256 tối thiểu cho những ứng dụng hash cần tương tác. Tuy nhiên, độ dài đầu ra không phải yếu tố duy nhất; cần xem thuật toán có bị tấn công hiệu quả và mục đích cụ thể. Kết luận của nhóm: cài đặt MD5 đúng là bài tập học thuật hữu ích, nhưng không nên dùng MD5 cho bảo mật mới.”

## Chuyển sang demo trực tiếp (Thành viên 3 hoặc 4, 5-7 phút)

Dùng nguyên kịch bản trong `DEMO_SCRIPT.md`: hash chuỗi `abc`, hiện trace, hash tệp, kiểm tra với digest cũ trước/sau khi sửa tệp, chạy test. Nói rõ demo tệp minh họa thay đổi dữ liệu chứ không phải collision attack.

## Câu hỏi mọi thành viên cần trả lời

1. Tại sao output MD5 có 32 ký tự hex?
2. Padding dừng ở 448 modulo 512 bit để làm gì?
3. Vì sao MD5 dùng little-endian trong từng từ và digest?
4. Một khối có bao nhiêu bước và vì sao tổng là 64?
5. Collision resistance khác preimage resistance thế nào?
6. Vì sao hash giống nhau có thể gây rủi ro cho chữ ký số?
7. Vì sao `hashlib.md5` được phép trong test nhưng không được dùng trong core?
8. Vì sao “file thay đổi => hash khác” không chứng minh MD5 an toàn chống kẻ tấn công?
9. SHA-256 có được chọn chỉ vì đầu ra dài gấp đôi không? (Không; cần xét nghiên cứu bảo mật và tiêu chuẩn.)
10. Nếu hash tham chiếu bị thay cùng với file, demo kiểm tra còn đáng tin không? (Không.)
