# Bài tập nhóm: Hàm băm MD5

> **Cảnh báo học thuật:** MD5 đã không còn an toàn cho các ứng dụng cần khả năng chống va chạm. Repository này dùng để học thuật toán và kiểm thử, không dùng để thiết kế cơ chế bảo mật mới.

## 1. Mục tiêu

- Tự cài đặt lõi MD5 theo đặc tả RFC 1321, không gọi `hashlib.md5()` trong phần lõi.
- Tính digest MD5 cho văn bản và tệp.
- Minh họa kiểm tra tính toàn vẹn bằng digest tham chiếu.
- In trace các thanh ghi A/B/C/D ở từng bước để hỗ trợ thuyết trình.
- Đối chiếu với test vector RFC 1321 và `hashlib.md5()` chỉ trong bộ kiểm thử.

## 2. Yêu cầu

- Python 3.10 trở lên (chỉ dùng thư viện chuẩn, không cần cài gói ngoài).
- Terminal/Command Prompt/PowerShell.
- Git tùy chọn nếu làm việc nhóm qua GitHub.

Kiểm tra phiên bản Python:

```bash
python --version
```

Nếu máy dùng lệnh `python3`, thay `python` bằng `python3` trong các lệnh dưới đây.

## 3. Cấu trúc thư mục

```text
MD5_Project/
├── README.md
├── CONTRIBUTING.md
├── requirements.txt
├── .gitignore
├── .github/workflows/tests.yml  # tự chạy test khi push / mở Pull Request
├── src/
│   ├── md5_core.py       # lõi MD5 tự cài đặt
│   ├── integrity.py      # băm tệp và so sánh digest
│   └── main.py           # menu demo CLI
├── tests/
│   └── test_md5.py       # test vector + kiểm thử biên
├── sample_data/
│   └── demo.txt          # tệp dùng trong demo
└── docs/
    ├── REPORT.md         # bản nội dung báo cáo dạng Markdown
    ├── CODE_WALKTHROUGH.md
    ├── DEMO_SCRIPT.md
    ├── PRESENTATION_SCRIPT.md
    └── GITHUB_WORKFLOW.md
```

## 4. Chạy chương trình từ đầu

### Windows

1. Tải ZIP từ GitHub hoặc chọn **Code → Download ZIP**, rồi giải nén.
2. Mở thư mục `MD5_Project`.
3. Bấm thanh địa chỉ của File Explorer, nhập `cmd` rồi Enter (hoặc mở PowerShell tại thư mục này).
4. Chạy kiểm thử:

```powershell
python -m unittest discover -s tests -v
```

5. Chạy menu demo:

```powershell
python src/main.py
```

Không có bước `pip install` bắt buộc vì dự án chỉ dùng thư viện chuẩn.

### macOS/Linux

```bash
cd MD5_Project
python3 -m unittest discover -s tests -v
python3 src/main.py
```

## 5. Các lựa chọn trong menu

1. **Tính MD5 cho văn bản:** nhập thông điệp; chương trình chuyển chuỗi sang UTF-8 bytes rồi băm.
2. **Tính MD5 cho tệp:** nhập đường dẫn file; đường dẫn có dấu cách nên đặt trong dấu ngoặc kép khi dán ở terminal.
3. **Kiểm tra toàn vẹn tệp:** nhập digest tham chiếu 32 ký tự hex, chương trình tính lại digest của tệp và so sánh.
4. **Hiển thị trace:** in 8 bước đầu của thông điệp `abc`; mã nguồn ghi lại đủ 64 bước của một khối.
5. **Hướng dẫn chạy test:** in lệnh kiểm thử để người demo chạy ở terminal.
0. Thoát.

## 6. Demo kiểm tra tính toàn vẹn của tệp

1. Chạy `python src/main.py`.
2. Chọn `2`, nhập `sample_data/demo.txt` (Windows có thể nhập `sample_data\demo.txt`). Ghi lại MD5 32 ký tự được in ra.
3. Chọn `3`, nhập cùng đường dẫn và dán digest vừa ghi. Kết quả phải là **KHỚP**.
4. Mở `sample_data/demo.txt`, thêm hoặc sửa một ký tự, lưu file.
5. Chọn `3` lần nữa, nhập đường dẫn và vẫn dán digest cũ. Kết quả phải là **KHÔNG KHỚP**.
6. Khôi phục nội dung file ban đầu nếu cần.

**Diễn giải quan trọng:** kiểm tra này chỉ có giá trị nếu digest tham chiếu được tin cậy. Nếu kẻ tấn công sửa được cả tệp và digest tham chiếu, phép so sánh đơn thuần không xác thực được nguồn gốc. MD5 còn có điểm yếu chống va chạm nên không dùng để chống đối thủ chủ động.

## 7. Chạy bộ kiểm thử

```bash
python -m unittest discover -s tests -v
```

Bộ test bao gồm:

- 7 test vector MD5 chuẩn trong RFC 1321.
- Nhiều độ dài quanh ranh giới padding 55/56 bytes và biên khối 64 bytes.
- Dữ liệu có toàn bộ giá trị byte, kéo dài qua nhiều khối.
- Văn bản tiếng Việt được mã hóa UTF-8.
- Kiểm tra trace đủ 64 bước cho một khối.
- Kiểm tra API lõi từ chối chuỗi Unicode chưa mã hóa thành bytes.

Ở thời điểm đóng gói, lệnh trên chạy thành công **7 phương thức test**. Khi thay đổi mã, hãy chạy lại test và ghi nhận kết quả thật.

## 8. Nguyên tắc kỹ thuật

- `src/md5_core.py` không gọi `hashlib.md5()`, `Crypto` hay OpenSSL để tính hash.
- `hashlib.md5()` chỉ được dùng trong `tests/test_md5.py` làm kết quả đối chiếu, theo yêu cầu hướng dẫn bài tập.
- Thuật toán dùng state khởi tạo theo RFC 1321: `67452301`, `EFCDAB89`, `98BADCFE`, `10325476`, và quy ước little-endian của RFC.
- Đây là bản triển khai phục vụ giáo dục. Không dùng mã này trong hệ thống sản xuất hoặc cho nhu cầu bảo mật.

## 9. GitHub và làm việc nhóm

Hướng dẫn chi tiết: [`docs/GITHUB_WORKFLOW.md`](docs/GITHUB_WORKFLOW.md).

Quy tắc nhóm:

1. Mỗi thành viên làm trên nhánh riêng, ví dụ `feature/md5-core`, `feature/tests`, `docs/report`.
2. Commit nhỏ, thông điệp nói rõ thay đổi.
3. Tạo Pull Request để thành viên khác review.
4. Không commit file `.venv`, `__pycache__`, hoặc thông tin riêng tư.
5. Trong báo cáo, ghi rõ phần tự viết, phần tham khảo đặc tả, và việc dùng AI nếu có; mọi thành viên cần hiểu toàn bộ chương trình.

## 10. Khai báo sử dụng công cụ AI

Hướng dẫn học phần cho phép sử dụng AI nhưng yêu cầu ghi rõ mục đích sử dụng. Vì bộ tài liệu này được tạo với sự hỗ trợ của ChatGPT, nhóm nên ghi trung thực các phần đã dùng, chẳng hạn: “Nhóm sử dụng ChatGPT để hỗ trợ lập kế hoạch báo cáo, diễn giải đặc tả MD5, tạo bản nháp code/test và tài liệu hướng dẫn. Nhóm tự kiểm tra nguồn trích dẫn, đọc và chỉnh sửa mã nguồn, chạy lại bộ kiểm thử, và chịu trách nhiệm về mọi nội dung trong sản phẩm.” Chỉ giữ các câu về việc đã làm thực tế; không khẳng định đã review/chạy trên máy nhóm nếu chưa thực hiện.

## 11. Tài liệu kỹ thuật chính

1. R. Rivest, **RFC 1321: The MD5 Message-Digest Algorithm**, April 1992: <https://www.rfc-editor.org/rfc/rfc1321>
2. S. Turner and L. Chen, **RFC 6151: Updated Security Considerations for the MD5 Message-Digest and the HMAC-MD5 Algorithms**, March 2011: <https://www.rfc-editor.org/rfc/rfc6151>
3. IETF, **RFC 9155: Deprecating MD5 and SHA-1 Signature Hashes in TLS 1.2 and DTLS 1.2**: <https://www.rfc-editor.org/rfc/rfc9155>
4. NIST, **Secure Hash Standard (FIPS 180-4)**: <https://csrc.nist.gov/pubs/fips/180-4/upd1/final>
