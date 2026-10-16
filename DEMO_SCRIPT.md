# Kịch bản chạy demo MD5 từ A đến Z (5-7 phút)

## A. Chuẩn bị trước buổi thuyết trình

1. Cài Python 3.10+ và mở thư mục repository.
2. Chạy `python -m unittest discover -s tests -v`; chụp lại terminal có dòng `OK` sau khi cả nhóm tự xác nhận test thành công trên máy trình bày.
3. Đảm bảo `sample_data/demo.txt` tồn tại và còn nội dung gốc.
4. Chuẩn bị một bản sao của `demo.txt` nếu không muốn sửa file mẫu.
5. Mở sẵn terminal ở thư mục gốc `MD5_Project`.
6. Chuẩn bị video dự phòng theo yêu cầu môn học. Video phải do nhóm ghi từ chương trình thực chạy, không thay bằng animation giả.

## B. Lời dẫn và thao tác

### 0:00-0:40 — Mở đầu

**Người nói:** “Chương trình này minh họa MD5 theo RFC 1321. Đây là hàm băm cho ra 128 bit, không phải mã hóa nên không có khóa hay chức năng giải mã. Nhóm tự cài đặt phần lõi; thư viện chuẩn chỉ dùng để đối chiếu trong test.”

**Thao tác:**

```bash
python src/main.py
```

### 0:40-1:30 — Băm văn bản

Chọn `1`, nhập `abc`.

Kết quả mong đợi:

```text
MD5 = 900150983cd24fb0d6963f7d28e17f72
```

**Người nói:** “Chuỗi được mã hóa UTF-8 thành bytes. MD5 luôn cho digest 128 bit, thường biểu diễn bằng 32 ký tự hex.”

### 1:30-2:20 — Trace 64 bước

Chọn `4`.

**Người nói:** “Sau padding, `abc` nằm trong một khối 512 bit. Mỗi khối xử lý qua bốn vòng, mỗi vòng 16 bước. Trace thể hiện A, B, C, D sau từng bước; chương trình in tám bước đầu cho dễ quan sát nhưng có thể ghi nhận đủ 64 bước.”

### 2:20-4:20 — Kiểm tra tệp

1. Chọn `2`, nhập `sample_data/demo.txt` và ghi digest hiện ra.
2. Chọn `3`, nhập cùng đường dẫn và dán digest vừa ghi. Kết quả mong đợi: **KHỚP**.
3. Mở file trong editor, sửa một ký tự rồi lưu.
4. Chọn `3`, nhập lại đường dẫn nhưng dán digest cũ. Kết quả mong đợi: **KHÔNG KHỚP**.

**Người nói:** “Đây là minh họa phát hiện dữ liệu khác với bản tham chiếu. Nó chỉ có ý nghĩa nếu digest tham chiếu được bảo vệ. Nếu kẻ tấn công thay được cả file và digest, phép kiểm tra không chứng minh nguồn gốc của file.”

### 4:20-5:20 — Kiểm thử đối chiếu

Thoát menu bằng `0`, chạy:

```bash
python -m unittest discover -s tests -v
```

**Người nói:** “Bộ kiểm thử dùng vector trong RFC 1321 và các trường hợp biên. `hashlib.md5` chỉ làm đối chiếu ở test, không phải là thuật toán lõi.”

### 5:20-6:30 — Kết luận bảo mật

**Người nói:** “MD5 không còn phù hợp cho ứng dụng cần chống va chạm, đặc biệt là chữ ký số. Kiểm tra tệp ở đây chỉ để giảng giải checksum, không nên diễn giải thành cơ chế bảo mật. Ứng dụng mới nên dùng SHA-256 hoặc giải pháp xác thực phù hợp.”

## C. Khôi phục demo

- Khôi phục `sample_data/demo.txt` về bản gốc từ Git: `git checkout -- sample_data/demo.txt` (chỉ chạy nếu file đã được commit và bạn muốn bỏ mọi chỉnh sửa cục bộ của chính file này).
- Hoặc chép lại nội dung gốc dưới đây:

```text
Demo kiểm tra tính toàn vẹn dữ liệu cho bài tập nhóm MD5.
Bước 1: tính hash tệp gốc.
Bước 2: sửa một ký tự rồi tính hash lần nữa.
Lưu ý: MD5 chỉ dùng minh họa; không dùng để bảo vệ dữ liệu trong ứng dụng mới.
```

## D. Nếu demo lỗi

- `python is not recognized`: cài Python và chọn **Add Python to PATH**, hoặc dùng `py` trên Windows / `python3` trên macOS/Linux.
- `ModuleNotFoundError`: chạy lệnh từ thư mục gốc repository, không phải từ `src` hoặc `tests`.
- Đường dẫn không tồn tại: dán đường dẫn đầy đủ, hoặc dùng đường dẫn tương đối `sample_data/demo.txt` từ thư mục gốc.
- Test sai: không trình diễn kết quả trước khi khắc phục. Kiểm tra thay đổi mới nhất, chạy test, và dùng video dự phòng có ghi từ phiên bản đã được xác nhận.
- Không có Internet: dự án không cần tải gói Python; chỉ cần cài Python trước.
