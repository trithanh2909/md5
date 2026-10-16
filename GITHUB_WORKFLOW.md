# Hướng dẫn Git và GitHub cho nhóm mới bắt đầu

## 1. Tạo repository trên GitHub

1. Đăng nhập GitHub và bấm nút **New repository**.
2. Đặt tên, ví dụ `computer-network-md5`.
3. Chọn **Private** trong lúc nhóm làm bài nếu muốn giới hạn người xem; thêm giảng viên sau nếu cần.
4. Nếu đã có project ở máy, có thể bỏ chọn tạo README/.gitignore để tránh xung đột lúc push lần đầu.
5. Bấm **Create repository**. Sao chép URL HTTPS của repo.

## 2. Cấu hình Git lần đầu (mỗi thành viên thực hiện trên máy của mình)

```bash
git --version
git config --global user.name "Tên của bạn"
git config --global user.email "email-git-hub-của-bạn"
```

Cài Git từ <https://git-scm.com/downloads> nếu chưa có. Với Windows, Git Bash là lựa chọn dễ theo hướng dẫn dòng lệnh.

## 3. Đẩy project ban đầu lên GitHub (một thành viên phụ trách)

Mở terminal tại thư mục gốc `MD5_Project`:

```bash
git init
git add .
git status
git commit -m "chore: initialize MD5 coursework project"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

Thay `USERNAME/REPOSITORY` bằng địa chỉ thực tế. Khi GitHub yêu cầu xác thực, làm theo luồng đăng nhập/token hiện hành của Git; không ghi token, mật khẩu hoặc khóa vào mã nguồn.

## 4. Thành viên khác tải project

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
python -m unittest discover -s tests -v
```

Nếu repository private, chủ repo cần mời từng thành viên trong **Settings → Collaborators** (giao diện có thể đổi tên đôi chút).

## 5. Quy trình nhánh và commit

Mỗi thành viên tạo nhánh cho phần việc của mình:

```bash
git switch -c feature/md5-core
```

Sau khi chỉnh sửa:

```bash
git status
git diff
git add src/md5_core.py
git commit -m "feat: implement MD5 compression rounds"
git push -u origin feature/md5-core
```

Vào GitHub, mở **Compare & pull request**, mô tả phần thay đổi, gắn người review, rồi merge sau khi test qua. Thành viên khác làm nhánh riêng, ví dụ `test/md5-vectors`, `docs/report`, `feat/integrity-demo`.

## 6. Các lệnh Git cần biết

```bash
git status                 # xem file đã sửa/chưa được theo dõi
git diff                   # xem chính xác dòng thay đổi
git log --oneline --graph  # xem lịch sử commit
git pull                   # lấy thay đổi mới của nhánh hiện tại
git switch main            # chuyển về main
git switch -c ten-nhanh    # tạo và chuyển sang nhánh mới
git add file               # đưa thay đổi vào staging
git commit -m "message"   # tạo commit
git push                   # đẩy commit lên remote
```

## 7. Đừng làm các việc này

- Không đưa mật khẩu, access token, file cá nhân hoặc dữ liệu nhạy cảm lên GitHub.
- Không commit `.venv/`, `__pycache__/` hoặc file output không cần thiết.
- Không để một người làm hết rồi các thành viên khác commit tài liệu cho có. Lịch sử commit cần phản ánh đóng góp thật.
- Không nhận code AI hoặc code trên mạng là hoàn toàn do mình tự viết. Ghi rõ đã dùng công cụ AI hỗ trợ ở khâu nào và bảo đảm thành viên giải thích được mã.
- Không sửa trực tiếp `main` khi nhóm đã thống nhất quy tắc review; dùng nhánh và Pull Request.

## 8. Checklist trước khi nộp

- [ ] Clone repo vào một thư mục khác và chạy lại theo README.
- [ ] Test pass trên ít nhất một máy khác máy lập trình chính.
- [ ] README nêu phiên bản Python, lệnh chạy, lệnh test và giới hạn bảo mật.
- [ ] Mã lõi không gọi `hashlib.md5`.
- [ ] Có commit/PR thực tế của từng thành viên.
- [ ] Report có bảng phân công và tỉ lệ đóng góp được mọi thành viên xác nhận.
- [ ] Nêu rõ nguồn tham khảo và phạm vi sử dụng AI.
