# Quy ước đóng góp cho bài tập nhóm MD5

## Quy ước nhánh

- `feature/md5-core`: `src/md5_core.py` và tài liệu giải thích thuật toán.
- `feature/integrity-cli`: `src/integrity.py`, `src/main.py` và kịch bản demo.
- `test/md5-vectors`: `tests/test_md5.py`, test vector và kiểm thử biên.
- `docs/report-security`: `docs/REPORT.md`, nguồn tham khảo và phân tích an toàn.
- `docs/github-readme`: README, hướng dẫn Git/GitHub, trình bày và khai báo AI.

Tên nhánh chỉ là gợi ý; thay đổi theo số lượng thành viên. Commit phản ánh đúng việc thành viên thực sự làm.

## Trước mỗi commit

```bash
git status
git diff
python -m unittest discover -s tests -v
```

Không commit nếu test đang lỗi mà chưa giải thích nguyên nhân. Không commit token, mật khẩu hoặc dữ liệu riêng tư.

## Quy ước commit message

Dùng tiền tố ngắn để lịch sử dễ đọc:

- `feat:` thêm tính năng
- `fix:` sửa lỗi
- `test:` thêm/sửa kiểm thử
- `docs:` sửa tài liệu
- `chore:` cấu hình dự án

Ví dụ:

```bash
git add src/md5_core.py
git commit -m "feat: implement MD5 compression rounds"
```

## Yêu cầu review

Pull Request nên ghi:

1. Vấn đề hoặc yêu cầu đang giải quyết.
2. File/hàm được sửa và lý do.
3. Lệnh kiểm thử đã chạy cùng kết quả thật.
4. Hạn chế hoặc câu hỏi cần người review xác nhận.

Người review cần tự giải thích được logic thay đổi trước khi merge. Vì giảng viên yêu cầu mọi thành viên giải thích được mã nguồn, không chấp nhận việc chỉ tạo commit tên mình mà không hiểu phần code đó.
