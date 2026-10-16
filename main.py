"""Interactive command-line demo for the coursework MD5 project."""
from __future__ import annotations

import sys
from pathlib import Path

from md5_core import md5, md5_text
from integrity import hash_file, verify_file


def ask_path() -> Path | None:
    raw = input("Nhập đường dẫn tệp (có thể kéo-thả tệp vào cửa sổ terminal): ").strip().strip('"')
    path = Path(raw).expanduser()
    if not path.is_file():
        print("Không tìm thấy tệp. Hãy kiểm tra đường dẫn và thử lại.")
        return None
    return path


def show_trace() -> None:
    sample = "abc".encode("utf-8")
    digest, rows = md5(sample, trace=True)
    print("\nMinh họa trace MD5 cho thông điệp bytes của 'abc' (một khối sau padding).")
    print("Chỉ hiển thị 8 bước đầu; mã nguồn ghi lại đủ 64 bước cho mỗi khối.")
    print("Bước | Vòng | từ X[g] |       A |       B |       C |       D")
    for row in rows[:8]:
        print(
            f"{row['step']:>4} | {row['round']:>4} | {row['word_index']:>7} | "
            f"{row['A']} | {row['B']} | {row['C']} | {row['D']}"
        )
    print(f"MD5('abc') = {digest}")


def menu() -> None:
    while True:
        print("\n========== DEMO HÀM BĂM MD5 (PHỤC VỤ HỌC TẬP) ==========")
        print("1. Tính MD5 cho văn bản")
        print("2. Tính MD5 cho một tệp")
        print("3. Kiểm tra toàn vẹn tệp với MD5 tham chiếu")
        print("4. Hiển thị trace 8 bước đầu của MD5('abc')")
        print("5. Xem lệnh chạy bộ kiểm thử")
        print("0. Thoát")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            text = input("Nhập văn bản: ")
            print(f"UTF-8 bytes length: {len(text.encode('utf-8'))} byte")
            print(f"MD5 = {md5_text(text)}")
        elif choice == "2":
            path = ask_path()
            if path:
                print(f"Tệp: {path}")
                print(f"Kích thước: {path.stat().st_size} byte")
                print(f"MD5 = {hash_file(path)}")
        elif choice == "3":
            path = ask_path()
            if path:
                expected = input("Nhập MD5 tham chiếu 32 ký tự hex: ").strip()
                matched, actual = verify_file(path, expected)
                print(f"MD5 tính được: {actual}")
                print("KẾT QUẢ: KHỚP (trùng digest tham chiếu)." if matched else
                      "KẾT QUẢ: KHÔNG KHỚP (hoặc digest tham chiếu không hợp lệ).")
                print("Lưu ý: đây không phải cơ chế xác thực an toàn trước kẻ tấn công chủ động.")
        elif choice == "4":
            show_trace()
        elif choice == "5":
            print("Lệnh chạy: python -m unittest discover -s tests -v")
            print("Hãy chạy lệnh đó từ thư mục gốc của repository.")
        elif choice == "0":
            print("Kết thúc demo.")
            return
        else:
            print("Lựa chọn không hợp lệ. Hãy nhập 0, 1, 2, 3, 4 hoặc 5.")


def main() -> None:
    menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")
        sys.exit(130)
