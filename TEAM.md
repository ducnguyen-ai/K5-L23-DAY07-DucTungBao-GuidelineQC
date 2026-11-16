# Thông tin nhóm

- Tên nhóm: **DucTungBao**
- Repo bài nộp (URL): https://github.com/ducnguyen-ai/K5-L23-DAY07-DucTungBao-GuidelineQC
- Commit chốt bài (hash): Chưa chốt; hiện mới setup.
- Số thành viên: **3** → số người gán mỗi ảnh (K): **2**.

| STT | MSHV | Họ và tên | Lớp (L2 / L3 / khác) | Tài khoản GitHub |
|---|---|---|---|---|
| 1 | 178 | Nguyễn Cao Ngọc Đức | L2 | [ducnguyen-ai](https://github.com/ducnguyen-ai) |
| 2 | 144 | Nguyễn Khánh Tùng | L2 | [sfpcshch](https://github.com/sfpcshch) |
| 3 | 138 | Hoàng Gia Bảo | L2 | [GBao294](https://github.com/GBao294) |

MSHV trong bảng, assignment và tên file cá nhân dùng 3 chữ số cuối; tiêu đề README giữ MSHV đầy đủ. Lệnh chia: `python scripts/split_assign.py --members 178,144,138 --seed 42 --copy-images`.

## Phân công (đề xuất, cả nhóm xác nhận khi bắt đầu)

| MSHV | Số ảnh gán độc lập | Phụ trách thêm |
|---|---:|---|
| 178 | 27 | Setup repo/môi trường; tổng hợp assignment; hỗ trợ chạy script IAA sau khi đủ nhãn. |
| 144 | 27 | Phối hợp review cấu trúc guideline và ghi nhận quyết định calibration sau pha độc lập. |
| 138 | 26 | Phối hợp kiểm mẫu QC và đối chiếu báo cáo sau calibration. |

Pha 1: mỗi người tự xem đủ 40 ảnh và viết guideline cá nhân. Pha 3: mỗi người chỉ gán số ảnh được giao; 40 ảnh có tổng 80 lượt gán độc lập, mỗi ảnh 2 người. Mỗi người tự viết ghi chú và commit sản phẩm của mình. Không khai commit hộ thành đóng góp của teammate. Guideline v1.0/calibration phải do nhóm thảo luận trước khi ghi quyết định.

## Kết quả tóm tắt (điền cuối bài)

- Số thành viên / số lần gán mỗi ảnh (K): **3 / 2**.
- IAA trước calibration: **Chưa đo**.
- Số ảnh phải calibration: **Chưa xác định** / 40.
- Tỉ lệ lỗi sau calibration: **Chưa đo**, cần ghi cả mẫu số theo ảnh và theo đối tượng.
- **Quyết định:** Chưa đánh giá Release / Hold / Rework; chưa có nhãn và kết quả QC.
