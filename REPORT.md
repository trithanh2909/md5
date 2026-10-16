# BÁO CÁO BÀI TẬP NHÓM

## HÀM BĂM MD5: CẤU TRÚC MERKLE–DAMGÅRD, BỐN VÒNG 64 BƯỚC VÀ GIỚI HẠN AN TOÀN

**Học phần:** An toàn và bảo mật thông tin / Mạng máy tính *(điền tên học phần đúng theo lớp)*  
**Giảng viên:** [Họ tên giảng viên]  
**Lớp học phần:** [Mã lớp]  
**Nhóm:** [Số nhóm]  
**Thành viên:** [Họ tên – mã sinh viên từng thành viên]  
**Trường/Khoa:** [Tên trường/khoa]  
**Ngày hoàn thành:** [Ngày/tháng/năm]

> **Lưu ý trước khi nộp:** Điền thông tin nhóm; bổ sung ảnh chụp kết quả chạy trên máy của nhóm; cập nhật bảng phân công/tỷ lệ đóng góp đã được tất cả thành viên xác nhận. Không giữ nguyên các ô hướng dẫn trong bản cuối.

---

## TÓM TẮT

MD5 (Message-Digest Algorithm 5) là hàm băm mật mã nhận đầu vào có độ dài tùy ý và tạo ra giá trị băm dài 128 bit. Thuật toán xử lý thông điệp theo từng khối 512 bit; mỗi khối gồm 16 từ 32 bit và được biến đổi qua bốn vòng, mỗi vòng 16 bước. Cấu trúc lặp này có thể được giải thích qua mô hình Merkle–Damgård: kết quả xử lý một khối trở thành trạng thái đầu vào cho khối tiếp theo.

Báo cáo trình bày khái niệm hàm băm, cấu trúc MD5, quy tắc đệm dữ liệu, bốn hàm logic, phép cộng modulo và phép xoay trái. Nhóm triển khai phần lõi MD5 bằng Python theo đặc tả RFC 1321, tách riêng tiện ích kiểm tra tệp và giao diện dòng lệnh. Độ đúng đắn được kiểm tra bằng các test vector của RFC 1321 và đối chiếu với thư viện chuẩn Python trong module kiểm thử; thư viện chuẩn không được sử dụng để tính hash trong phần lõi.

Kết quả nghiên cứu cho thấy MD5 không còn phù hợp với các ứng dụng yêu cầu khả năng chống va chạm, đặc biệt là chữ ký số. Các tài liệu IETF đã mô tả những cuộc tấn công va chạm và khuyến cáo không dùng MD5 khi cần collision resistance. Vì vậy, chương trình trong báo cáo chỉ nhằm mục đích học tập và minh họa nguyên lý; với hệ thống mới, cần lựa chọn hàm băm hiện đại như SHA-256 hoặc giải pháp xác thực thông điệp phù hợp với mô hình đe dọa.

**Từ khóa:** MD5, hàm băm, Merkle–Damgård, collision resistance, SHA-256, Python, kiểm tra tính toàn vẹn.

## MỤC LỤC

| Nội dung | Trang |
|---|---:|
| Tóm tắt | 2 |
| Chương 1. Mở đầu | 3 |
| Chương 2. Cơ sở lý thuyết | 5 |
| Chương 3. Phân tích thuật toán MD5 | 8 |
| Chương 4. Phân tích độ an toàn của MD5 | 11 |
| Chương 5. Thiết kế và cài đặt chương trình | 13 |
| Chương 6. Kiểm thử, demo và đánh giá | 15 |
| Chương 7. Kết luận và hướng phát triển | 17 |
| Khai báo sử dụng công cụ AI | 17 |
| Tài liệu tham khảo | 18 |
| Phụ lục A. Hướng dẫn chạy chương trình | 19 |
| Phụ lục B. Phân công công việc | 20 |

---

# CHƯƠNG 1. MỞ ĐẦU

## 1.1. Lý do chọn đề tài

Hàm băm là thành phần quan trọng trong nhiều hệ thống công nghệ thông tin. Một hàm băm ánh xạ dữ liệu đầu vào có độ dài khác nhau thành một giá trị đầu ra có độ dài cố định. Giá trị này có thể được dùng làm dấu vết dữ liệu để so sánh, kiểm tra lỗi truyền tải hoặc làm một thành phần trong các cơ chế mật mã như chữ ký số và mã xác thực thông điệp.

MD5 là thuật toán có ý nghĩa lịch sử và vẫn xuất hiện trong các hệ thống cũ, công cụ kiểm tra tệp hoặc tài liệu kỹ thuật. Tuy nhiên, MD5 đã mất khả năng chống va chạm cần thiết cho các mục đích mật mã quan trọng. Nghiên cứu MD5 vì thế vừa giúp hiểu một cấu trúc hàm băm phổ biến, vừa minh họa sự khác biệt giữa việc thuật toán vẫn có thể tính toán đúng theo đặc tả và việc thuật toán không còn an toàn cho một mục đích cụ thể.

## 1.2. Mục tiêu nghiên cứu

Báo cáo hướng đến các mục tiêu sau:

1. Giải thích vai trò của hàm băm và các tính chất bảo mật cơ bản.
2. Trình bày cấu trúc Merkle–Damgård, quá trình padding, xử lý khối 512 bit và bốn vòng 64 bước của MD5.
3. Tự cài đặt thuật toán MD5 bằng Python mà không sử dụng hàm băm có sẵn trong phần lõi.
4. Xây dựng bộ kiểm thử, đối chiếu kết quả với test vector tiêu chuẩn và thư viện chuẩn.
5. Demo tính hash của văn bản/tệp và minh họa giới hạn của việc dùng MD5 để kiểm tra tính toàn vẹn.
6. Phân tích các điểm yếu bảo mật, so sánh MD5 với SHA-256 và đưa ra kết luận sử dụng phù hợp.

## 1.3. Phạm vi nghiên cứu

Đề tài tập trung vào thuật toán MD5 theo RFC 1321, cách triển khai trong Python, kiểm tra tính đúng đắn bằng test vector và phân tích an toàn. Chương trình không triển khai chữ ký số, mã hóa/giải mã hay tấn công tạo va chạm. Demo kiểm tra tệp chỉ minh họa cách tính và đối chiếu digest; không được xem là hệ thống xác thực an toàn trước đối thủ chủ động.

## 1.4. Phương pháp nghiên cứu

Nhóm sử dụng bốn phương pháp chính: (i) đọc và đối chiếu đặc tả MD5 RFC 1321; (ii) phân tích các tài liệu an toàn như RFC 6151 và RFC 9155; (iii) triển khai thuật toán bằng Python theo mô tả chuẩn; và (iv) kiểm thử bằng test vector, trường hợp biên padding, dữ liệu nhiều khối, dữ liệu UTF-8 và dữ liệu nhị phân.

## 1.5. Cấu trúc báo cáo

Báo cáo gồm bảy chương. Chương 1 giới thiệu đề tài; Chương 2 trình bày cơ sở lý thuyết; Chương 3 phân tích thuật toán MD5; Chương 4 thảo luận điểm yếu bảo mật; Chương 5 mô tả thiết kế và cài đặt; Chương 6 trình bày kiểm thử và kịch bản demo; Chương 7 tổng kết và đề xuất hướng phát triển.

# CHƯƠNG 2. CƠ SỞ LÝ THUYẾT

## 2.1. Khái niệm hàm băm

Hàm băm là hàm ánh xạ một đầu vào có độ dài biến đổi thành một đầu ra có độ dài cố định, thường được gọi là giá trị băm, hash value hoặc message digest. Với một hàm băm H, có thể viết:

`H : {0,1}* -> {0,1}^n`

Trong đó `{0,1}*` là tập các chuỗi bit có độ dài tùy ý và `n` là độ dài đầu ra cố định. Đối với MD5, `n = 128` bit. Một digest 128 bit thường được biểu diễn bằng 32 chữ số hệ thập lục phân, bởi mỗi chữ số hex biểu diễn 4 bit.

Hàm băm không phải là mã hóa. Mã hóa thường dùng khóa và được thiết kế để người có khóa giải mã có thể khôi phục bản rõ. Hàm băm không có thao tác giải mã để khôi phục duy nhất thông điệp gốc từ digest. Nhiều thông điệp khác nhau về nguyên tắc có thể ánh xạ tới cùng một đầu ra vì đầu vào có miền lớn hơn không gian đầu ra hữu hạn.

## 2.2. Các tính chất quan trọng

- **Tính xác định:** cùng byte đầu vào luôn cho cùng digest.
- **Kháng tiền ảnh (preimage resistance):** khi biết digest `y`, khó tìm `x` sao cho `H(x)=y`.
- **Kháng tiền ảnh thứ hai (second-preimage resistance):** với một thông điệp `x` đã cố định, khó tìm `x' != x` sao cho `H(x')=H(x)`.
- **Kháng va chạm (collision resistance):** khó tìm bất kỳ hai đầu vào khác nhau `x` và `x'` sao cho `H(x)=H(x')`.
- **Hiệu ứng avalanche:** thay đổi nhỏ ở đầu vào thường làm nhiều bit đầu ra thay đổi. Đây là đặc trưng mong muốn nhưng tự nó không chứng minh thuật toán an toàn.

Ba tính chất kháng tiền ảnh, kháng tiền ảnh thứ hai và kháng va chạm là các khái niệm khác nhau. Với MD5, điểm yếu nổi bật là những cuộc tấn công va chạm thực tế; vì vậy, việc đầu ra trông ngẫu nhiên hoặc thay đổi nhiều khi sửa thông điệp không đủ để xem MD5 là an toàn.

## 2.3. Tổng quan về MD5

MD5 do Ronald Rivest thiết kế và được mô tả trong RFC 1321, công bố tháng 4 năm 1992. Mục đích của đặc tả là cung cấp một thuật toán message digest có thể xử lý thông điệp dài tùy ý và trả về digest 128 bit. MD5 chia thông điệp thành các khối 512 bit; các từ dữ liệu và trạng thái được thao tác theo 32 bit.

Các thông số chính:

| Thuộc tính | MD5 |
|---|---|
| Đầu vào | Chuỗi byte có độ dài tùy ý trong phạm vi triển khai |
| Đệm | Bit 1, các bit 0, sau đó độ dài ban đầu 64 bit |
| Kích thước khối | 512 bit = 64 byte |
| Từ dữ liệu trong mỗi khối | 16 từ × 32 bit |
| Trạng thái tích lũy | 4 từ 32 bit: A, B, C, D |
| Số vòng mỗi khối | 4 |
| Số bước mỗi vòng | 16 |
| Tổng số bước | 64 |
| Đầu ra | 128 bit = 16 byte = 32 ký tự hex |

## 2.4. Mô hình Merkle–Damgård

Merkle–Damgård là cấu trúc xây dựng hàm băm từ một hàm nén xử lý dữ liệu theo khối. Trạng thái ban đầu được khởi tạo theo quy tắc của thuật toán. Mỗi khối thông điệp cùng trạng thái trước đó đi vào hàm nén và tạo ra trạng thái mới. Trạng thái mới được dùng khi xử lý khối kế tiếp. Sau khi xử lý tất cả các khối, trạng thái cuối được xuất thành digest.

Sơ đồ khái quát:

```text
Thông điệp M -> padding + độ dài ban đầu -> M1, M2, ..., Mn

IV + M1       -> hàm nén -> H1
H1 + M2       -> hàm nén -> H2
...                         ...
H(n-1) + Mn   -> hàm nén -> Hn -> digest 128 bit

Mỗi Mi dài 512 bit; Hi là trạng thái băm sau khối i.
```

Sơ đồ nhóm nêu là mô hình khái niệm để diễn giải chuỗi trạng thái, không phải sơ đồ kiến trúc của một giao thức mạng cụ thể. MD5 sử dụng dạng xử lý khối nối tiếp này, với hàm nén gồm 64 bước.

## 2.5. Padding trong MD5

Theo RFC 1321, việc đệm được thực hiện theo ba thao tác:

1. Thêm một bit `1` ở cuối thông điệp gốc.
2. Thêm các bit `0` cho đến khi độ dài đạt 448 theo modulo 512, tức phần trước trường độ dài dài 56 byte trong khối cuối.
3. Nối biểu diễn 64 bit của độ dài thông điệp ban đầu, tính bằng bit, theo thứ tự little-endian.

Sau padding, tổng độ dài luôn là bội số của 512 bit. Trường độ dài là độ dài của thông điệp gốc trước khi padding, không phải độ dài sau padding. Với thông điệp 56 byte, padding bit và trường độ dài không cùng vừa trong một khối, nên thuật toán tạo thêm khối 512 bit nữa.

## 2.6. Biểu diễn byte và endianness

MD5 diễn giải mỗi nhóm 4 byte thành một từ 32 bit theo little-endian: byte đầu tiên là byte ít quan trọng nhất. Đặc tả cũng xuất trạng thái cuối dưới dạng byte little-endian. Vì vậy, khi cài đặt bằng ngôn ngữ có quy ước đóng gói byte khác, phải chủ động định nghĩa thứ tự byte. Trong chương trình Python của nhóm, `struct.unpack('<16I', block)` đọc 16 số nguyên 32 bit little-endian và `struct.pack('<4I', ...)` tạo 16 byte kết quả theo little-endian.

## 2.7. Ứng dụng và hạn chế khái niệm

Giá trị băm có thể phục vụ so sánh dữ liệu, phát hiện thay đổi ngẫu nhiên, làm đầu vào cho chữ ký số hoặc các cơ chế xác thực. Tuy nhiên, tính phù hợp phụ thuộc vào thuật toán và mô hình đe dọa. Với MD5, không nên dùng làm nền cho chữ ký số hoặc những nơi cần chống đối thủ cố tình tạo va chạm. Một giá trị hash không tự chứng minh nguồn gốc dữ liệu nếu giá trị tham chiếu không được bảo vệ.

# CHƯƠNG 3. PHÂN TÍCH THUẬT TOÁN MD5

## 3.1. Quy trình tổng quát

MD5 được mô tả theo các giai đoạn:

1. Đệm thông điệp và nối trường độ dài 64 bit.
2. Chia thông điệp đã đệm thành các khối 512 bit.
3. Khởi tạo bốn thanh ghi trạng thái A, B, C, D.
4. Với mỗi khối, chia thành 16 từ 32 bit và thực hiện bốn vòng với tổng cộng 64 bước.
5. Cộng trạng thái làm việc vào trạng thái tích lũy của khối trước đó.
6. Sau khi hết các khối, xuất A, B, C, D theo thứ tự byte quy định để tạo digest 128 bit.

## 3.2. Khởi tạo trạng thái

RFC 1321 định nghĩa các từ trạng thái ban đầu là:

| Thanh ghi | Giá trị khởi tạo (hex) |
|---|---|
| A | `67452301` |
| B | `EFCDAB89` |
| C | `98BADCFE` |
| D | `10325476` |

Mỗi thanh ghi dài 32 bit nên trạng thái có tổng cộng 128 bit. Khi xử lý một khối, chương trình sao chép trạng thái tích lũy hiện tại vào bốn biến làm việc `a`, `b`, `c`, `d`. Sau 64 bước, trạng thái làm việc được cộng với trạng thái tích lũy theo modulo `2^32`.

**Lưu ý đối chiếu tài liệu:** trong một dòng của slide Chương 4 được nhóm cung cấp có ghi các giá trị A/B/C/D khác với bộ khởi tạo trong RFC 1321. Do bài tập yêu cầu cài đặt MD5 chuẩn và đối chiếu test vector RFC, mã nguồn trong báo cáo sử dụng bộ khởi tạo của RFC 1321 nêu ở bảng trên. Nhóm nên xác nhận với giảng viên liệu các giá trị trong slide là ví dụ minh họa hay lỗi trình bày trước khi bảo vệ; không nên trộn hai bộ giá trị trong cùng một cài đặt.

## 3.3. Bốn hàm logic

Các hàm phi tuyến thao tác bit trên ba từ 32 bit:

**Vòng 1:**

`F(B,C,D) = (B AND C) OR ((NOT B) AND D)`

Hàm chọn bit từ C khi bit tương ứng của B là 1, ngược lại lấy từ D.

**Vòng 2:**

`G(B,C,D) = (B AND D) OR (C AND (NOT D))`

**Vòng 3:**

`H(B,C,D) = B XOR C XOR D`

**Vòng 4:**

`I(B,C,D) = C XOR (B OR (NOT D))`

Các phép `NOT` cần được hiểu trong phạm vi từ 32 bit. Trong Python, số nguyên có độ chính xác tùy ý và `~x` có biểu diễn bù vô hạn về mặt toán học; các phép cộng và xoay trong triển khai đều được cắt về 32 bit bằng mặt nạ `0xFFFFFFFF`. Kết quả này giúp mô phỏng phép toán trên từ 32 bit của MD5.

## 3.4. Bốn vòng và 64 bước

Mỗi khối thực hiện 64 bước. Chỉ số bước trong mã nguồn bắt đầu từ 0; khi trình bày với người xem, bước được hiển thị từ 1 đến 64.

| Vòng | Chỉ số bước trong code | Hàm | Chỉ số từ dữ liệu `g` |
|---|---|---|---|
| 1 | 0–15 | F | `g = i` |
| 2 | 16–31 | G | `g = (5*i + 1) mod 16` |
| 3 | 32–47 | H | `g = (3*i + 5) mod 16` |
| 4 | 48–63 | I | `g = (7*i) mod 16` |

Trong mỗi bước, thuật toán cộng từ trạng thái, kết quả hàm logic, hằng số `T[i]` và từ thông điệp `M[g]`; lấy phần dư theo `2^32`, xoay trái số bit `s[i]`, rồi cộng vào thanh ghi B và luân chuyển các thanh ghi. Các hằng số `T[i]` được xác định theo công thức trong RFC 1321 dựa trên phần nguyên của `2^32 × |sin(i)|`, với i đếm từ 1 đến 64.

Dạng công thức cốt lõi của một bước có thể diễn giải như sau:

`B_new = (B + ROL32(A + f(B,C,D) + T[i] + M[g], s[i])) mod 2^32`

Sau đó các thanh ghi được luân chuyển theo thứ tự: `A <- D`, `D <- C`, `C <- B`, `B <- B_new`, xét trên các giá trị cũ phù hợp. Trong code, biến `a,b,c,d` được cập nhật đồng thời bằng giá trị đã lưu trước bước để tránh dùng nhầm trạng thái mới giữa chừng.

## 3.5. Phép toán modulo và xoay trái

Máy tính Python không tự tràn số nguyên ở 32 bit như một số ngôn ngữ cấp thấp. Vì MD5 định nghĩa phép cộng trên từ 32 bit, code áp dụng:

`value_32 = value & 0xFFFFFFFF`

Phép xoay trái `ROL32(x,s)` dịch các bit của x sang trái s vị trí và đưa các bit vượt khỏi đầu trái vòng lại từ đầu phải. Phép này khác với dịch trái đơn thuần vì không làm mất các bit bị đẩy ra. Số bit xoay thay đổi theo bước, theo lịch `S` trong RFC.

## 3.6. Ví dụ kiểm tra bằng thông điệp `abc`

Một test vector chuẩn trong RFC 1321 là thông điệp byte ASCII `abc`. Kết quả mong đợi:

```text
Input:  abc
MD5:    900150983cd24fb0d6963f7d28e17f72
```

Độ dài thông điệp ban đầu là 3 byte = 24 bit. Sau khi thêm byte `0x80`, cần thêm các byte 0 sao cho độ dài đạt 56 byte; sau đó nối 8 byte lưu độ dài 24 bit theo little-endian. Vì vậy, thông điệp đã đệm dài đúng 64 byte (512 bit), tạo thành một khối. Khối đó được phân thành 16 từ 32 bit; 64 bước biến đổi bốn thanh ghi và tạo digest cuối.

Đối với việc tính tay, nhóm có thể ghi chi tiết byte padding và 16 từ đầu vào, sau đó chọn một bước cụ thể để trình diễn cách chọn hàm logic, chỉ số từ, hằng số, phép cộng modulo và xoay trái. Việc liệt kê toàn bộ số hex sau mỗi bước có thể đưa vào phụ lục dạng trace do chính chương trình sinh. Trước khi nộp, cần đính kèm ảnh hoặc bảng trace được tạo từ chương trình của nhóm và xác nhận giá trị cuối khớp với test vector.

## 3.7. Độ phức tạp tính toán

Với thông điệp dài n bit, quá trình padding và xử lý các khối cần thời gian tỷ lệ tuyến tính theo độ dài đầu vào, tức `O(n)` trong mô hình thông thường. Mỗi khối xử lý đúng 64 bước, vì vậy phần xử lý khối có chi phí tuyến tính theo số khối. Bộ nhớ của phiên bản demo hiện tại tỷ lệ với kích thước tệp đầu vào do đọc toàn bộ tệp vào bộ nhớ; đây là lựa chọn đơn giản cho minh họa, không phải thiết kế tối ưu cho các tệp rất lớn.

# CHƯƠNG 4. PHÂN TÍCH ĐỘ AN TOÀN CỦA MD5

## 4.1. Phân biệt va chạm và kiểm tra thay đổi thông thường

Va chạm xảy ra khi có hai thông điệp khác nhau nhưng cùng digest:

`M != M'` và `MD5(M) = MD5(M')`.

MD5 có đầu ra 128 bit, do đó số giá trị băm tối đa là `2^128`. Do không gian các thông điệp là vô hạn còn số digest hữu hạn, va chạm phải tồn tại theo nguyên lý chuồng bồ câu. Điều cần có từ hàm băm an toàn là việc tìm va chạm phải khó về mặt tính toán.

Đối với một hàm băm lý tưởng có n bit đầu ra, nghịch lý ngày sinh gợi ý rằng chi phí tìm va chạm ngẫu nhiên có bậc khoảng `2^(n/2)`. Với 128 bit, mức lý tưởng là xấp xỉ `2^64` lần thử. Tuy nhiên, đây chỉ là mốc so sánh lý thuyết, không phải chi phí thực tế của tấn công MD5: các kỹ thuật phân tích mật mã đã khai thác cấu trúc của MD5 để tìm va chạm hiệu quả hơn vét cạn ngẫu nhiên.

Việc sửa một ký tự làm digest thay đổi trong demo là hiện tượng thông thường và phù hợp với hiệu ứng avalanche. Nhưng điều đó không chứng minh rằng không thể tạo hai thông điệp khác nhau có cùng digest. Phát hiện thay đổi thông thường và chống tấn công va chạm là hai bài toán khác nhau.

## 4.2. Những dạng tấn công liên quan

- **Birthday attack:** mô hình lý thuyết dùng để hiểu tại sao collision resistance của hàm n bit có mức an toàn tối đa gần n/2 bit khi xét tìm va chạm ngẫu nhiên.
- **Tấn công va chạm dựa trên cấu trúc MD5:** dùng các điều kiện và quan hệ nội bộ của quá trình nén để tạo ra các cặp thông điệp cùng digest với chi phí thấp hơn vét cạn.
- **Chosen-prefix collision:** trong một số điều kiện và với kỹ thuật chuyên biệt, kẻ tấn công có thể chọn hai tiền tố khác nhau rồi xây dựng phần nối thêm sao cho hai thông điệp hoàn chỉnh có cùng MD5. Loại tấn công này đáng quan tâm khi hash được dùng để ký hoặc xác thực tài liệu.

Báo cáo không triển khai công cụ tạo va chạm. Phần phân tích chỉ giải thích hệ quả và dẫn nguồn chính thống, tránh coi một ví dụ hash khác nhau sau khi chỉnh file là bằng chứng của một cuộc tấn công va chạm.

## 4.3. Hậu quả đối với chữ ký số và chứng chỉ

Nếu một hệ thống ký số chỉ ký digest của tài liệu, tính chống va chạm là yêu cầu quan trọng: người ký chấp thuận một tài liệu nhưng kẻ tấn công có thể tìm hoặc xây dựng tài liệu khác cùng digest trong điều kiện phù hợp. Nếu có thể chuyển một chữ ký hợp lệ sang tài liệu khác mà không phát hiện được sự khác biệt ở digest, ý nghĩa của chữ ký bị suy giảm nghiêm trọng.

RFC 6151 cập nhật các cân nhắc bảo mật cho MD5 và nêu rõ MD5 không còn chấp nhận được trong những ứng dụng cần collision resistance, chẳng hạn chữ ký số. RFC 9155 cũng quy định MD5 và SHA-1 không được dùng cho chữ ký số trong TLS 1.2/DTLS 1.2. Đây là căn cứ tiêu chuẩn để giải thích vì sao MD5 bị loại khỏi nhiều ứng dụng mật mã hiện đại.

## 4.4. MD5 còn phù hợp cho mục đích nào?

Không nên diễn giải “MD5 đã bị phá” thành việc mọi phép tính MD5 đều vô ích. MD5 vẫn có thể xuất hiện trong hệ thống cũ, định danh nội bộ hoặc một số quy trình phát hiện lỗi ngẫu nhiên khi không có đối thủ chủ động. Tuy nhiên, nếu cần bảo đảm chống giả mạo, không thể chỉ dựa vào MD5.

Một digest có ý nghĩa kiểm tra tính toàn vẹn nếu giá trị tham chiếu được lấy từ nguồn đáng tin và đối thủ không thể thay cả dữ liệu lẫn digest. Nếu cần xác thực nguồn gốc, cần cơ chế bổ sung như HMAC với hàm băm còn được khuyến nghị, chữ ký số hoặc kênh phân phối tin cậy; lựa chọn đúng phụ thuộc vào yêu cầu của hệ thống.

## 4.5. So sánh MD5 với SHA-256

| Tiêu chí | MD5 | SHA-256 |
|---|---|---|
| Họ thuật toán | MD5 | SHA-2 |
| Độ dài đầu ra | 128 bit | 256 bit |
| Kích thước khối | 512 bit | 512 bit |
| Cấu trúc vòng | 4 vòng × 16 bước | 64 vòng |
| Khả năng chống va chạm | Bị phá vỡ trong thực tế | Được khuyến nghị cho nhiều ứng dụng cần hash mật mã |
| Khuyến nghị cho ứng dụng bảo mật mới | Không dùng khi cần collision resistance | Phù hợp hơn; cần chọn theo tiêu chuẩn và mô hình đe dọa |

Không nên kết luận chỉ từ độ dài đầu ra. SHA-256 có đầu ra dài hơn và vẫn được NIST liệt kê trong họ SHA-2 được dùng cho các ứng dụng dùng secure hash algorithms. NIST khuyến nghị tối thiểu SHA-256 cho các ứng dụng hàm băm yêu cầu khả năng tương tác. Tốc độ thực tế nên được đo nếu báo cáo muốn so sánh hiệu năng: giữ cùng máy, cùng dữ liệu, cùng thư viện/môi trường và ghi rõ phương pháp đo.

## 4.6. Kết luận về an toàn

MD5 vẫn có thể được triển khai đúng theo đặc tả, nhưng điều đó không đồng nghĩa nó còn an toàn cho mọi ứng dụng. Điểm yếu va chạm khiến nó không phù hợp cho chữ ký số và các mục đích mà một đối thủ có thể chủ động lựa chọn thông điệp. Vì vậy, việc cài đặt MD5 trong đề tài chỉ nên được xem là bài tập hiểu thuật toán và kiểm thử; mọi hệ thống mới cần chọn hàm băm hoặc cơ chế xác thực còn phù hợp với khuyến nghị hiện hành.

# CHƯƠNG 5. THIẾT KẾ VÀ CÀI ĐẶT CHƯƠNG TRÌNH

## 5.1. Môi trường triển khai

- Ngôn ngữ: Python 3.10 trở lên.
- Phụ thuộc ngoài: không có; sử dụng thư viện chuẩn Python.
- Giao diện: menu dòng lệnh (CLI).
- Kiểm thử: `unittest` và thư viện chuẩn `hashlib` chỉ dùng đối chiếu.
- Nền tảng: Windows, macOS hoặc Linux có Python.

## 5.2. Kiến trúc module

| Module | Trách nhiệm | Có thực hiện thuật toán MD5 lõi? |
|---|---|---|
| `src/md5_core.py` | Padding, chia khối, hàm logic, 64 bước, xuất digest và trace | Có |
| `src/integrity.py` | Đọc file, tính digest, so sánh digest tham chiếu | Gọi lõi, không tự cài lại vòng |
| `src/main.py` | Menu, nhập dữ liệu, in kết quả | Không |
| `tests/test_md5.py` | Test vector, trường hợp biên, đối chiếu | Không; gọi lõi để test |

Tách module giúp kiểm tra thuật toán riêng biệt với giao diện và làm lịch sử commit rõ ràng. Phần lõi từ chối chuỗi `str` để tránh mơ hồ về cách mã hóa; hàm `md5_text` chuyển văn bản sang UTF-8 trước khi băm.

## 5.3. Triển khai padding

Hàm `_pad(message)` ghi nhớ độ dài ban đầu tính bằng bit. Sau đó thêm byte `0x80`, tương ứng bit đầu tiên bằng 1 tiếp theo là các bit 0. Vòng lặp thêm byte 0 cho đến khi độ dài modulo 64 bằng 56; cuối cùng nối 8 byte độ dài theo little-endian. Kết quả có độ dài bội số 64 byte.

## 5.4. Triển khai hàm nén

Mỗi khối 64 byte được tách bằng `struct.unpack('<16I', block)`. Bốn biến làm việc khởi đầu bằng bốn từ trạng thái hiện tại. Vòng lặp 64 bước quyết định hàm F/G/H/I, chỉ số từ g và số vòng; kết hợp các giá trị với hằng số và phép xoay trái; sau đó cập nhật bốn thanh ghi. Khi kết thúc khối, trạng thái làm việc được cộng vào trạng thái tích lũy modulo `2^32`.

Hàm cho phép bật `trace=True`, khi đó trả thêm danh sách các trạng thái sau từng bước. Trace phục vụ việc giải thích nội bộ thuật toán, không phải bằng chứng độc lập về tính an toàn.

## 5.5. Triển khai chức năng kiểm tra tệp

`hash_file(path)` đọc nội dung tệp ở dạng bytes và gọi MD5 tự cài đặt. `verify_file(path, expected_digest)` tính lại digest, chuẩn hóa giá trị tham chiếu và so sánh hai chuỗi. Kết quả gồm trạng thái khớp/không khớp và digest vừa tính để người dùng quan sát.

Phiên bản demo đọc toàn bộ tệp vào bộ nhớ để giữ code đơn giản. Phần này phù hợp với tệp nhỏ dùng trong lớp; nếu mở rộng để xử lý tệp lớn, nên thiết kế API incremental, cập nhật hash theo từng chunk, đồng thời vẫn đảm bảo tự triển khai lõi chứ không gọi hàm MD5 có sẵn.

## 5.6. Giao diện dòng lệnh

Menu có các chức năng: (1) tính hash văn bản; (2) tính hash tệp; (3) kiểm tra tính toàn vẹn với digest tham chiếu; (4) hiển thị trace tám bước đầu của thông điệp `abc`; (5) nhắc lệnh chạy test; và (0) thoát. Giao diện cố tình đơn giản để người thuyết trình tập trung vào thuật toán và kết quả.

## 5.7. Giới hạn của chương trình

- Mục tiêu là học tập, không phải triển khai mật mã trong môi trường sản xuất.
- MD5 không an toàn cho mục đích chống va chạm.
- Băm tệp hiện tại nạp toàn bộ tệp vào bộ nhớ.
- Digest tham chiếu do người dùng nhập; chương trình không quản lý kho tham chiếu an toàn.
- Chương trình không triển khai tấn công va chạm hoặc chữ ký số.

# CHƯƠNG 6. KIỂM THỬ, DEMO VÀ ĐÁNH GIÁ

## 6.1. Chiến lược kiểm thử

Nhóm kiểm tra ba lớp: test vector đã công bố; các trường hợp biên có khả năng làm lộ lỗi padding/đọc khối; và các tình huống dữ liệu thực tế như UTF-8 hoặc dữ liệu nhị phân. `hashlib.md5()` được sử dụng trong module test làm kết quả đối chiếu, không nằm trong phần lõi thuật toán.

## 6.2. Test vector

Một số test vector chuẩn trong RFC 1321:

| Đầu vào | MD5 kỳ vọng |
|---|---|
| Chuỗi rỗng | `d41d8cd98f00b204e9800998ecf8427e` |
| `a` | `0cc175b9c0f1b6a831c399e269772661` |
| `abc` | `900150983cd24fb0d6963f7d28e17f72` |
| `message digest` | `f96b697d7cb7938d525a2f31aaf161d0` |
| `abcdefghijklmnopqrstuvwxyz` | `c3fcd3d76192e4007dfb496cca67e13b` |

Bộ kiểm thử trong repository chứa bảy vector RFC, kiểm thử độ dài 0, 1, 2, 3, 54, 55, 56, 57, 63, 64, 65, 127, 128, 129 và 1000 byte; kiểm thử dữ liệu byte 0-255 lặp nhiều lần; văn bản Unicode UTF-8; trace 64 bước; và trường hợp API nhận nhầm kiểu dữ liệu.

## 6.3. Kết quả kiểm thử

Trong lần kiểm tra tại môi trường xây dựng bộ nộp bài, lệnh:

```bash
python -m unittest discover -s tests -v
```

cho kết quả **7 phương thức kiểm thử thành công (OK)**. Các phép đối chiếu test vector và dữ liệu biên đều khớp. Khi nộp chính thức, nhóm cần chạy lại lệnh trên máy dùng demo và thay ảnh chụp minh chứng bằng kết quả thật từ máy nhóm.

| Nhóm kiểm thử | Mục đích | Kết quả trong lần kiểm tra |
|---|---|---|
| Test vector RFC 1321 | Kiểm tra các đầu ra đã biết | Đạt |
| Độ dài biên padding/khối | Phát hiện lỗi ở 55/56 và 63/64 byte | Đạt |
| Dữ liệu nhị phân nhiều khối | Kiểm tra xử lý bytes và nhiều block | Đạt |
| UTF-8 | Kiểm tra mã hóa văn bản sang bytes | Đạt |
| Trace | Kiểm tra đủ 64 bước cho một khối | Đạt |
| Kiểm tra kiểu đầu vào | Bảo đảm lõi yêu cầu bytes | Đạt |

> **Minh chứng cần thêm trước khi nộp:** chèn ảnh chụp terminal chạy test trên máy nhóm và ảnh demo menu. Không dùng ảnh giả lập; kết quả có thể khác nếu nhóm chỉnh sửa code.

## 6.4. Kịch bản demo tính toàn vẹn

1. Chạy chương trình và chọn tính hash cho `sample_data/demo.txt`.
2. Ghi lại digest.
3. Chọn kiểm tra tính toàn vẹn, nhập cùng tệp và digest vừa ghi; kết quả phải khớp.
4. Sửa một ký tự trong tệp, lưu lại và kiểm tra với digest cũ; kết quả phải không khớp.
5. Khôi phục nội dung tệp, chạy bộ test và trình bày kết luận.

Demo này minh họa thay đổi dữ liệu, không minh họa collision attack. Kết quả không khớp sau khi sửa tệp không chứng minh MD5 chống được va chạm; nó chỉ thể hiện digest của hai nội dung đang kiểm tra khác nhau trong trường hợp đó.

## 6.5. Đánh giá kết quả

Chương trình đáp ứng mục tiêu học tập: phần lõi tự triển khai, cấu trúc module tách biệt, đầu ra khớp với các test vector và có demo trên tệp thật. Trace cho phép nhìn giá trị thanh ghi sau bước biến đổi, từ đó kết nối phần công thức với kết quả chạy thực tế.

Hạn chế lớn nhất không phải lỗi triển khai mà là giới hạn của chính MD5: collision resistance không còn đủ cho ứng dụng bảo mật. Ngoài ra, việc đọc toàn bộ tệp vào RAM chưa tối ưu cho file lớn. Để tăng chất lượng, nhóm có thể cải thiện giao diện, thêm xử lý lỗi đường dẫn, hỗ trợ file lớn bằng incremental hashing tự cài đặt và thực hiện benchmark có kiểm soát với SHA-256.

# CHƯƠNG 7. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 7.1. Kết luận

Báo cáo đã trình bày cơ sở lý thuyết của hàm băm, mô hình Merkle–Damgård và cấu trúc MD5. Thuật toán xử lý thông điệp sau padding theo các khối 512 bit; mỗi khối gồm 16 từ 32 bit, được biến đổi qua bốn vòng 16 bước, tổng cộng 64 bước. Trạng thái gồm bốn thanh ghi 32 bit được cập nhật và xuất thành digest 128 bit theo quy tắc little-endian.

Nhóm xây dựng chương trình Python có phần lõi tự cài đặt, công cụ hash văn bản/tệp, kiểm tra digest tham chiếu và trace các bước. Bộ kiểm thử kiểm tra test vector chuẩn và các trường hợp biên, giúp xác nhận triển khai phù hợp với đặc tả đã chọn.

Đồng thời, phân tích bảo mật cho thấy việc tính MD5 đúng không làm nó phù hợp cho mọi mục đích. Các cuộc tấn công va chạm đã làm mất khả năng chống va chạm cần thiết cho chữ ký số và các ứng dụng liên quan. MD5 trong dự án chỉ nên dùng làm ví dụ giáo dục; với ứng dụng mới, cần chọn SHA-256/SHA-3 hoặc cơ chế MAC/chữ ký phù hợp.

## 7.2. Hướng phát triển

- Bổ sung xử lý tệp theo từng khối nhưng vẫn tự triển khai thuật toán.
- Xây dựng giao diện trực quan hiển thị đầy đủ 64 trạng thái cho thông điệp ngắn.
- Cài đặt thêm SHA-256 để so sánh digest và tốc độ trong điều kiện đo giống nhau.
- Minh họa collision bằng một cặp mẫu MD5 đã được công bố và xác minh nguồn gốc, không chạy tệp không đáng tin cậy.
- Bổ sung tự động hóa CI trên GitHub để mỗi Pull Request đều chạy unit test.

# KHAI BÁO SỬ DỤNG CÔNG CỤ AI

Trong quá trình thực hiện, nhóm đã sử dụng ChatGPT hỗ trợ xây dựng dàn ý, diễn giải đặc tả kỹ thuật, tạo bản nháp mã nguồn Python/bộ kiểm thử và cấu trúc tài liệu. Nhóm có trách nhiệm đối chiếu nội dung với RFC 1321, RFC 6151 và các nguồn được trích dẫn; tự chạy và kiểm tra mã nguồn trên môi trường thực tế; chỉnh sửa nội dung theo kết quả xác minh; và bảo đảm mọi thành viên hiểu phần việc được giao. Trước khi nộp, nhóm cần chỉnh sửa tuyên bố này cho đúng chính xác với phần việc đã thực sự sử dụng AI và mức độ kiểm chứng.

# TÀI LIỆU THAM KHẢO

[1] R. Rivest, “The MD5 Message-Digest Algorithm,” RFC 1321, Internet Engineering Task Force, April 1992. https://www.rfc-editor.org/rfc/rfc1321

[2] S. Turner and L. Chen, “Updated Security Considerations for the MD5 Message-Digest and the HMAC-MD5 Algorithms,” RFC 6151, Internet Engineering Task Force, March 2011. https://www.rfc-editor.org/rfc/rfc6151

[3] L. Velvindron, K. Moriarty, and A. Ghedini, “Deprecating MD5 and SHA-1 Signature Hashes in TLS 1.2 and DTLS 1.2,” RFC 9155, Internet Engineering Task Force, December 2021. https://www.rfc-editor.org/rfc/rfc9155

[4] National Institute of Standards and Technology (NIST), “Secure Hash Standard (SHS),” FIPS PUB 180-4. https://csrc.nist.gov/pubs/fips/180-4/upd1/final

[5] NIST Computer Security Resource Center, “NIST Policy on Hash Functions,” updated page. https://csrc.nist.gov/projects/hash-functions/nist-policy-on-hash-functions

[6] Python Software Foundation, “hashlib — Secure hashes and message digests.” https://docs.python.org/3/library/hashlib.html

[7] ThS. Nguyễn Quốc Thái, “An toàn và bảo mật thông tin - Chương 4: Hàm băm và chữ ký điện tử,” bài giảng môn học, Đại học Kinh tế Quốc dân.

# PHỤ LỤC A. HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH

## A.1. Yêu cầu môi trường

Cài Python 3.10 trở lên. Mở terminal tại thư mục gốc repository. Dự án không yêu cầu cài thư viện bên ngoài.

## A.2. Chạy test

```bash
python -m unittest discover -s tests -v
```

## A.3. Chạy demo

```bash
python src/main.py
```

Chọn chức năng theo menu. Mô tả chi tiết và lời dẫn có trong `docs/DEMO_SCRIPT.md`; hướng dẫn giải thích mã có trong `docs/CODE_WALKTHROUGH.md`.

# PHỤ LỤC B. PHÂN CÔNG CÔNG VIỆC VÀ TỶ LỆ ĐÓNG GÓP

> Nhóm phải tự điền và cùng xác nhận. Tỷ lệ bên dưới là mẫu cấu trúc, không phải dữ liệu thực tế.

| STT | Họ tên | Mã sinh viên | Nhiệm vụ và sản phẩm cụ thể | Tỷ lệ đóng góp | Xác nhận |
|---:|---|---|---|---:|---|
| 1 | [Điền] | [Điền] | [Ví dụ: cơ sở lý thuyết, sơ đồ Merkle–Damgård] | [__%] | [Có/Chưa] |
| 2 | [Điền] | [Điền] | [Ví dụ: phân tích 4 vòng/64 bước, trace] | [__%] | [Có/Chưa] |
| 3 | [Điền] | [Điền] | [Ví dụ: lõi MD5, review thuật toán] | [__%] | [Có/Chưa] |
| 4 | [Điền] | [Điền] | [Ví dụ: kiểm thử, đối chiếu, demo tệp] | [__%] | [Có/Chưa] |
| 5 | [Điền] | [Điền] | [Ví dụ: phân tích bảo mật, SHA-256, tổng hợp report/slide] | [__%] | [Có/Chưa] |

Tổng tỷ lệ đóng góp phải bằng 100%. Ghi rõ công cụ AI đã dùng và dùng vào việc gì, theo yêu cầu hướng dẫn học phần. Mỗi thành viên phải có khả năng giải thích toàn bộ mã nguồn khi bảo vệ.
