# Thông tin nhóm

- Tên nhóm: **DucTungBao**
- Lớp: **L2**
- Mã thành viên (ba chữ số): **178, 144, 138**
- Người điều phối và chốt calibration: **178** (xác nhận phân công ngày 17/11/2026).
- Người review QC bản cuối: **144** (đã phân công, chưa xác nhận đã review).
- Commit chốt bài (điền ở kênh nộp sau khi commit): **Chưa chốt; đã tính IAA, đang calibration**.

| Mã thành viên | Số ảnh được giao | Lớp | Vai trò thêm (đề xuất) |
|---|---:|---|---|
| 178 | 27 | L2 | Điều phối checkpoint, hỗ trợ chạy script và tổng hợp artifact sau pha độc lập. |
| 144 | 27 | L2 | Phối hợp tổng hợp guideline và ghi quyết định calibration. |
| 138 | 26 | L2 | Phối hợp review QC và kiểm tra gói bàn giao. |

Mỗi ảnh có đúng 2 người gán độc lập, tổng 80 lượt gán trên 40 ảnh. Pha 1 mỗi người tự xem đủ 40 ảnh; Pha 3 chỉ gán ảnh trong danh sách riêng. Guideline và nhãn cá nhân gửi riêng trước khi cả nhóm nộp xong. Bảng đối chiếu mã với danh tính gửi qua kênh lớp có giới hạn quyền.

## Kết quả tóm tắt

- Lượt gán nộp hợp lệ / được giao: **80 / 80**, 40 ảnh (138: 26, 144: 27, 178: 27).
- IAA trước calibration: **268 cặp ghép**, IoU TB **0,882**, cùng lớp **96,6%**, trên cặp ghép IoU>=0,5. Đạt ngưỡng tổng; cặp 138/144 và 144/178 chưa đạt riêng.
- Đồng thuận thuộc tính: occluded_level **33,2%**, truncated **88,4%**.
- Box chưa ghép: **239**; chưa kết luận bỏ sót hay thừa trước khi đọc ảnh.
- Số ảnh cần calibration: **34 / 40**, tổng **837** dòng cần xem, gồm 337 cờ can_review của 178.
- Calibration: **178** chốt; review QC: **144**. Bảng quyết định còn chờ điền bằng công việc thực tế.
- Vòng QC và số ảnh đã duyệt / cả lô: **Chưa mở vòng / 40**.
- Tỉ lệ lỗi QC theo ảnh và theo đối tượng: **Chưa đo**.
- **Trạng thái: Hold**, chờ calibration, nhãn cuối, manifest và review QC. Đây là tiến độ nội bộ, chưa phải quyết định do qc_report.py sinh.

Kết quả chi tiết: [iaa_summary.md](submission/qc/iaa_summary.md), [calibration_decisions.csv](submission/qc/calibration_decisions.csv), [QC_REPORT.md](submission/qc/QC_REPORT.md).
