# Giải thích mã nguồn MD5 - dùng để học và chuẩn bị bảo vệ

Tài liệu này giải thích **vai trò**, **đầu vào/đầu ra**, và **cách nói khi thuyết trình** cho từng module. Cả nhóm nên đọc tất cả, không chỉ phần mình commit.

## 1. Bản đồ chương trình

```text
main.py
  ├── md5_core.py  -> tính hash và trace các bước
  └── integrity.py -> đọc tệp, so sánh hash tham chiếu

test_md5.py -> gọi md5_core.py và so kết quả với test vector/hashlib
```

- `md5_core.py`: thuật toán chính. Đây là phần bắt buộc tự viết.
- `integrity.py`: lớp tiện ích cho demo file.
- `main.py`: giao diện menu; không chứa thuật toán mật mã lõi.
- `test_md5.py`: kiểm tra tính đúng đắn; thư viện chuẩn chỉ được dùng làm oracle trong test.

## 2. `src/md5_core.py`

### 2.1. Hằng số và trạng thái

- `_MASK32 = 0xFFFFFFFF`: mặt nạ 32 bit. Python cho số nguyên có thể lớn tùy ý, trong khi MD5 cần phép toán như trên từ 32 bit; `& _MASK32` giữ lại 32 bit thấp.
- `_SHIFT`: lịch xoay trái 64 số, bốn cụm tương ứng bốn vòng.
- `_K`: 64 hằng số, theo RFC 1321: `T[i] = floor(2^32 × abs(sin(i)))` với `i = 1..64`. Trong Python chỉ số mảng bắt đầu từ 0 nên code dùng `sin(i + 1)`.
- `_INITIAL_STATE`: bốn giá trị trạng thái chuẩn của RFC 1321. Lưu ý đối chiếu: slide Chương 4 được cung cấp có một dòng ghi A/B/C/D khác các giá trị chuẩn này. Vì chương trình được kiểm tra theo test vector RFC, code dùng IV chuẩn `67452301`, `EFCDAB89`, `98BADCFE`, `10325476`. Hỏi giảng viên để xác nhận cách hiểu slide trước khi bảo vệ; không thay IV chuẩn nếu vẫn tuyên bố đây là MD5 theo RFC 1321.

### 2.2. `_left_rotate(value, amount)`

Xoay trái không giống dịch trái thông thường. Các bit bị đẩy ra bên trái được đưa vòng lại từ bên phải. Sau đó áp dụng mặt nạ 32 bit.

Công thức:

```text
ROL(x, s) = ((x << s) OR (x >> (32 - s))) AND 0xffffffff
```

### 2.3. `_pad(message)`

1. Tính độ dài ban đầu tính bằng bit.
2. Thêm byte `0x80`, bắt đầu bằng bit 1 theo quy tắc padding.
3. Thêm byte 0 đến khi số byte còn lại modulo 64 bằng 56. Vì 56 byte = 448 bit, còn 8 byte cuối dành cho độ dài.
4. Nối 8 byte biểu diễn độ dài ban đầu bằng little-endian (`<Q`).

Kết quả là độ dài bội số của 64 bytes, tương ứng khối 512 bit. Điều này giải thích trường hợp 55/56 byte: ở đầu vào dài 56 byte, không còn đủ chỗ cho 8 byte length trong khối hiện tại nên phải sinh thêm một khối padding.

### 2.4. `md5(message, trace=False)`

- Nhận bytes, không nhận trực tiếp `str`. Vì hash là của byte đầu vào, chuỗi văn bản phải được mã hóa trước; hàm `md5_text` dùng UTF-8.
- Padding xong, từng khối 64 bytes được đọc bằng `struct.unpack('<16I', block)` thành 16 số nguyên 32 bit little-endian.
- Khởi tạo working registers `a,b,c,d` bằng trạng thái trước khi xử lý khối.
- Lặp `i=0..63`. Chọn hàm logic và vị trí từ dữ liệu theo từng vòng:
  - Bước 0-15: F, `g=i`.
  - Bước 16-31: G, `g=(5*i+1) mod 16`.
  - Bước 32-47: H, `g=(3*i+5) mod 16`.
  - Bước 48-63: I, `g=(7*i) mod 16`.
- Cộng working state, kết quả hàm logic, hằng số, từ dữ liệu; cắt về 32 bit.
- Xoay trái số bit quy định; cập nhật thanh ghi.
- Hết 64 bước: cộng working state vào trạng thái tích lũy (feed-forward).
- Hết tất cả các khối: đóng gói 4 từ 32 bit theo little-endian và đổi thành hex 32 ký tự.

### 2.5. Vì sao `trace=True`?

Khi trace bật, hàm vẫn tính kết quả hash bình thường nhưng đồng thời lưu số khối, số bước, vòng, chỉ số từ dữ liệu và giá trị A/B/C/D sau mỗi bước. Menu chỉ in 8 bước đầu để output dễ đọc; có thể thay `rows[:8]` thành `rows` nếu muốn xem đủ 64 bước của thông điệp ngắn `abc`.

## 3. `src/integrity.py`

- `hash_file(path)`: đọc bytes nguyên trạng từ tệp và gọi `md5(data)`. Không decode thành văn bản vì file có thể chứa bất kỳ byte nào.
- `verify_file(path, expected_digest)`: tính hash hiện tại, chuẩn hóa digest nhập vào thành chữ thường và so sánh. Digest hợp lệ phải dài 32 ký tự.
- Hàm trả về cả trạng thái đúng/sai và digest mới, giúp giao diện giải thích vì sao mismatch.
- Giới hạn demo: file được đọc vào bộ nhớ một lần; dùng tệp nhỏ cho buổi học. Muốn hỗ trợ tệp rất lớn có thể viết API incremental MD5 riêng, nhưng không cần thiết cho bản đầu tiên.

**Điểm bảo mật phải nói ra:** so sánh hai digest chỉ nói rằng giá trị tính được có khớp với giá trị tham chiếu không. Nó không chứng minh ai tạo ra file. Nếu kẻ tấn công có thể thay cả file lẫn digest, kiểm tra này có thể bị đánh lừa; collision resistance của MD5 cũng đã bị phá.

## 4. `src/main.py`

Menu gọi các hàm ở hai module trên. Giao diện tách khỏi thuật toán để mã dễ kiểm thử và bảo trì.

- Mục 1: `md5_text(text)` chuyển văn bản sang UTF-8 rồi băm.
- Mục 2: yêu cầu đường dẫn, in kích thước và hash tệp.
- Mục 3: nhập digest tham chiếu và gọi `verify_file`.
- Mục 4: gọi `md5(..., trace=True)` trên `abc` và in 8 bước đầu.
- Mục 5: in hướng dẫn lệnh test; bộ test nên được chạy trực tiếp tại terminal.

## 5. `tests/test_md5.py`

- Test vector RFC 1321 xác nhận các kết quả kinh điển (chuỗi rỗng, `a`, `abc`, ...).
- Test biên so sánh với `hashlib.md5` ở các độ dài quanh 55/56 và 63/64 byte. Chỉ test mới dùng thư viện chuẩn để đối chiếu.
- Test byte 0..255 lặp nhiều lần xác nhận xử lý nhiều khối và dữ liệu nhị phân.
- Test UTF-8 xác nhận quy ước encode chuỗi.
- Test trace đảm bảo có 64 bản ghi cho một khối đã padding.
- Test lỗi kiểu dữ liệu nhắc lập trình viên rằng lõi thao tác trên bytes.

## 6. Bài nói mẫu cho phần code (khoảng 60-90 giây)

“Nhóm chia chương trình thành ba lớp. `md5_core.py` tự cài đặt theo RFC 1321, bao gồm padding, chia khối, bốn hàm logic và 64 bước. `integrity.py` là tiện ích băm và kiểm tra digest của tệp. `main.py` chỉ lo giao tiếp với người dùng nên không trộn logic thuật toán vào giao diện. Để tránh vô tình dùng thư viện có sẵn, phần lõi không gọi `hashlib.md5`; thư viện chuẩn chỉ xuất hiện trong test làm chuẩn đối chiếu. Bộ test gồm các test vector RFC, trường hợp biên padding, dữ liệu nhiều khối và UTF-8. Mục tiêu của chương trình là minh họa thuật toán, không phải khuyến nghị dùng MD5 cho ứng dụng bảo mật mới.”

## 7. Câu hỏi phản biện dễ gặp

- **MD5 là mã hóa hay hàm băm?** MD5 là hàm băm; không có khóa và không có thuật toán giải mã để khôi phục thông điệp từ digest.
- **Vì sao cần padding?** Để tổng dữ liệu sau đệm là bội số 512 bit và có thêm độ dài ban đầu theo đặc tả.
- **Tại sao đầu ra 128 bit có 32 ký tự?** Mỗi ký tự hex biểu diễn 4 bit, nên 128/4 = 32 ký tự.
- **Collision khác preimage thế nào?** Collision là tìm bất kỳ hai thông điệp khác nhau có cùng digest; preimage là tìm một đầu vào cho digest mục tiêu cho trước.
- **Nếu sửa một ký tự thì hash có luôn khác không?** Thông thường sẽ khác, nhưng không thể khẳng định mọi thay đổi đều cho digest khác; va chạm tồn tại.
- **Vì sao dùng `hashlib.md5` trong test?** Chỉ làm nguồn đối chiếu độc lập; lõi thuật toán vẫn do nhóm tự cài đặt.
- **Hash khớp có bảo đảm tệp an toàn không?** Không. Digest tham chiếu phải đáng tin và MD5 không phù hợp để chống đối thủ chủ động tạo va chạm.
