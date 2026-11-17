# Báo cáo QC — DucTungBao

## 1. Mục đích và đầu vào

- Mục đích và giới hạn sử dụng: Tôi bàn giao lô thực hành 40 ảnh để đánh giá guideline và chất lượng annotation; chưa đủ cơ sở dùng cho xe tự hành hoặc hệ thống giao thông vận hành thật. IAA không phải độ chính xác so với ground truth.
- Nguồn và phép sử dụng dữ liệu: Giữ data/ATTRIBUTION.csv và giấy phép gốc.
- Manifest và checksum nhãn cuối: submission/qc/batch_manifest.json; SHA256 labels_calibrated.json = 312ee71df053010d1def19b244e94885db220cae2ccd60c632bf8cc3609d753a.
- Guideline và taxonomy khi gán / khi bàn giao: v1.0 agreed khi gán; v1.1 ghi cách áp dụng rule khi calibration; taxonomy v1.0 và mọi ngưỡng giữ nguyên.

## 2. IAA và sửa nhãn

- Lượt hoàn thành / được giao: 80/80 lượt trên 40 ảnh, K=2; 138 có 26 ảnh/246 box, 144 có 27 ảnh/184 box, 178 có 27 ảnh/345 box.
- IAA: 268 cặp ghép, mean IoU 0,882; cùng lớp 96,6%; occluded_level 33,2%; truncated 88,4%. Có 239 box chưa ghép. Chỉ số tổng không chứng minh từng box đúng.
- Truy vết calibration: 837 dòng IAA được liên kết tới quyết định từng ảnh trong calibration_decisions.csv; không đồng nghĩa 837 ca đã đóng. Còn 26 ảnh được giữ cờ review trong calibration_patch.json/review_triage.csv.
- Bản nhãn làm việc hiện tại: 450 annotations/40 ảnh. Chọn bản 178 nếu được giao, nếu không thì 138 làm nền sửa; đây là cách dựng bản làm việc, không phải kết luận người nào chính xác hơn. Các ca chưa chắc vẫn can_review.
- Sửa có truy vết: 13 box loại, 5 box sửa class/geometry, 7 box bổ sung; 438 box giữ từ bản nền. Đây không phải phép đếm chênh lệch với 507 box consensus. Xem calibration_applied.csv để tra source_id và final_id.
- Ví dụ: img_007 bỏ box cabin trùng pickup; img_012 bỏ box pickup trùng; img_028 đổi pickup car sang truck; img_040 bỏ ego motorcycle và sửa extent taxi; img_005 thêm van và person bỏ sót. Không sửa nhãn độc lập để tăng IAA.
- Trạng thái guideline: ca rooftop car img_024 cần chốt phạm vi R-14/R-16; các ảnh đông cần kiểm instance/extent/thuộc tính, không thay định nghĩa để hợp thức hóa box.

## 3. Bằng chứng QC

- Vòng QC: 2
- Người review và ngày: 178 là mã phụ trách; lượt đối chiếu mới do trợ lý thực hiện theo ủy quyền ngày 17/11/2026. 144 đã nộp vòng 1, không quy kết người này đã review vòng 2.
- Đã duyệt / cả lô: Phiếu QC vòng 2 có kết quả 9/40 ảnh; đã xem toàn bộ 40 ảnh ở lượt triage, nhưng triage không thay QC hoàn chỉnh. 31 ảnh chưa có kết luận QC.
- Ảnh lỗi / ảnh đã duyệt: 4/9 = 44,4%; không suy rộng thành tỷ lệ lỗi toàn bộ 40 ảnh.
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 1/49 = 2,0%; không bao gồm ba vật bỏ sót.
- Vật bỏ sót, ảnh và vùng: 3 ca ghi riêng ở img_005, img_014, img_021; chi tiết vùng trong reviews/round-02/qc_review.csv.
- Lỗi đã ghi: truck img_001 có extent lấn cảnh quán; các ca bỏ sót phương tiện/người nêu trên. Các ca chưa chắc giữ can_review, không tính là lỗi đã xác nhận.
- Một lỗi máy chặn được và một lỗi cần đọc ảnh: checksum ngăn dùng nhãn/phiếu khác phiên bản; phát hiện bicycle nhầm motorcycle hoặc box trùng phải đối chiếu ảnh.

## 4. Sửa kết luận vòng 1

- Lưu lịch sử: Giữ nguyên reviews/round-01 và nhãn revision ab5bebe6ba91a115. Bản đó không còn dùng để ra quyết định cho nhãn hiện tại.
- Lý do thay kết luận: Tại commit 08f93c6, tọa độ và class của cả 507 box giống consensus_draft; pickup img_028 vẫn car, ego motorcycle img_040 vẫn tồn tại. Báo cáo 0 lỗi/40 ảnh không phù hợp các lỗi đối chiếu được. check_submission khi đó báo lệch checksum và đầu vào IAA.
- Chốt calibration: Phân công 178 chốt/144 QC vẫn giữ; không ghi có phiên họp hoặc xác nhận nhóm mới khi chưa có bằng chứng.

## 5. Bàn giao

- Quyết định: Hold
- Lý do, người nhận và phạm vi sử dụng: Nộp bằng chứng thực hành cho coach với trạng thái Hold theo SUBMISSION.md. Còn cờ review, một ca phạm vi guideline và QC chưa đủ 40 ảnh; không công bố Release hoặc 0 lỗi.
- Nếu còn việc: Xử lý các ca trong review_triage.csv, sửa các lỗi vòng 2; chốt rooftop car; kiểm lại đủ 40 ảnh rồi mở vòng 3 trên bản nhãn đã sửa. Không điền khong hàng loạt để vượt kiểm tra.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: img_028→R-06→calibration_patch.json update 1→calibration_applied.csv source_id/final_id→labels_calibrated.json. img_001→R-02→phiếu QC vòng 2 object_id 7. Snapshot và checksum khóa từng vòng.
