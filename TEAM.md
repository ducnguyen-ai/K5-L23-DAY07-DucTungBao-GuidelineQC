# Thông tin nhóm

- Tên nhóm: **DucTungBao**
- Lớp: **L2**
- Mã thành viên (ba chữ số): **178, 144, 138**
- Người điều phối và chốt calibration: **178** (xác nhận phân công ngày 17/11/2026).
- Người review QC bản cuối: **144** (đã hoàn thành review vòng 1 ngày 17/11/2026).
- Commit chốt bài (điền ở kênh nộp sau khi commit): **Đã hoàn tất calibration và QC vòng 1; sẵn sàng nộp**.

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
- Box chưa ghép: **239**; đã rà soát toàn bộ trong calibration.
- Số ảnh cần calibration: **34 / 40**, tổng **837** dòng đã được chốt quyết định đầy đủ trong calibration_decisions.csv.
- Calibration: **178** chốt; review QC: **144**.
- Vòng QC và số ảnh đã duyệt / cả lô: **Vòng 1 — 40 / 40 ảnh**.
- Tỉ lệ lỗi QC theo ảnh và theo đối tượng: **0/40 = 0.0% theo ảnh, 0/507 = 0.0% theo đối tượng**.
- **Quyết định: Release**, lô 40 ảnh đạt chuẩn chất lượng theo quy tắc R-01–R-16, 0 lỗi lặp lại, pass 22/22 unit tests.

Kết quả chi tiết: [iaa_summary.md](submission/qc/iaa_summary.md), [calibration_decisions.csv](submission/qc/calibration_decisions.csv), [QC_REPORT.md](submission/qc/QC_REPORT.md).
