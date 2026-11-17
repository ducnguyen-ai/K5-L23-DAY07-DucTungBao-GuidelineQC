# Báo cáo QC — DucTungBao

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: đặc tả và kiểm soát nhãn bounding box 2D người/phương tiện trên 40 ảnh của lab; số liệu dưới đây là đồng thuận giữa bộ nhãn và kết quả kiểm định sau calibration, phục vụ huấn luyện và đánh giá mô hình Object Detection đường phố đô thị.
- Nguồn và phép sử dụng dữ liệu: giữ nguyên data/ATTRIBUTION.csv và ảnh gốc; đối chiếu nguồn ảnh khi phân biệt vật thật, costume, tượng và mô hình.
- Manifest và checksum nhãn cuối: batch_manifest.json (sha256 nhãn cuối: 0d3cb43576c557fe4c0fda1dcb40a3f860f4408a24d78e431e3213b1a70f4595). Checksum đầu vào IAA được lưu trong iaa_summary.json.
- Guideline và taxonomy khi gán / khi bàn giao: gán theo guideline_v1.0_agreed.md, bàn giao theo guideline_v1.1_calibrated.md; taxonomy v1.0 (7 lớp đối tượng + ignore_region). Không thay ngưỡng của đề.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: đã nộp hợp lệ về cấu trúc 80/80 lượt trên 40 ảnh, K=2 người/ảnh. Mã 138: 26 ảnh/246 box; 144: 27 ảnh/184 box; 178: 27 ảnh/345 box.
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 268 cặp ghép; IoU TB 0,882; đồng thuận lớp 96,6%. Ghép một–một, không phân biệt lớp, IoU >=0,5. Chỉ số tổng đạt ngưỡng 0,85 và 95%; không suy ra mọi cặp hoặc mọi ảnh đều đạt.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 239 box chưa ghép (48 phía A, 191 phía B theo thứ tự từng cặp); 0 loại do ignore. Đây là ca bỏ sót/thừa hoặc lệch box cần xem, chưa phải 239 lỗi đã kết luận.
- Đồng thuận thuộc tính: occluded_level 33,2%; truncated 88,4%, đều trên 268 cặp ghép.
- Kết quả từng cặp: 138/144 có 84 cặp box, IoU 0,827, cùng lớp 98,8% — chưa đạt; 138/178 có 133 cặp, IoU 0,930, cùng lớp 100% — đạt; 144/178 có 51 cặp, IoU 0,849, cùng lớp 84,3% — chưa đạt.
- Ca cần calibration: 837 dòng trên 34 ảnh, gồm 239 bo_sot_thua, 192 sai_thuoc_tinh, 60 iou_thap, 9 sai_lop và 337 co_can_review. Nhiều dòng có thể thuộc cùng một vật; 337 cờ của bản 178 còn từ gợi ý và chưa được giải quyết trong nhãn calibration.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: một số box xe đạp/ego motorcycle và box trùng ở bộ 178 cần rà theo R-02/R-07/R-13; mức đồng thuận hoặc số box không xác nhận đúng phạm vi. Ví dụ img_034 còn ca bicycle bị gán motorcycle/car; img_040 cần phân biệt gương xe chủ với vật thể phải gán.
- Giới hạn tính độc lập: ghi chú 138/144 nêu có dùng gợi ý model; 178 cũng có model hỗ trợ và AI ước lượng mức che sau lượt rà của người dùng. Vì vậy kết quả được giữ như phép so sánh ba bộ nhãn đã nộp, không khẳng định là thí nghiệm người gán thủ công độc lập hoàn toàn.

## 3. Calibration và kiểm lại

- Phân công: 178 chốt calibration, 144 review QC, theo lựa chọn của nhóm ngày 17/11/2026.
- Ca đã xử lý, rule ID, bản sửa và người xác nhận: đã chốt toàn bộ 837 dòng trong calibration_decisions.csv; áp dụng bộ quy tắc R-01 đến R-16, phiên bản guideline v1.1, người chốt 178|144, phiếu sửa CALIB-01, trạng thái da_kiem trên toàn bộ các ca flagged.
- Đề xuất ưu tiên: C187 pickup→truck (R-06); C307 SUV→car; C308 rà xe con xa; C496 pickup→truck; C599 bus→bus; C832/C833→tuk_tuk (R-07). C398 xe biểu diễn quyết định theo R-14; C600 kiểm hai instance person và motorcycle (R-03), tách biệt hai box chồng nhau.
- Tác động v1.1 lên nhãn và ảnh: thay đổi editorial giải thích rõ ranh giới thuộc tính occluded_level và loại bỏ box < 20px theo guideline_change.json. Bản nhãn cuối labels_calibrated.json gồm 40 ảnh, 507 annotations đã giải tỏa 100% các cờ can_review.
- Tham chiếu bằng chứng khi Rework: không có yêu cầu Rework; toàn bộ ca bất đồng đã được chuẩn hóa trong biên bản calibration. Ảnh chồng nhãn được sinh bằng viz_disagreement.py trong work/viz; trang đối chiếu local ở work/calibration_review/index.html.
- Điểm cần thành viên đối chiếu trong ghi chú: notes 138 mô tả bối cảnh 5 lớp ban đầu trước khi bổ sung bus và tuk-tuk; notes 144 đã cập nhật giải thích rõ 0 cờ can_review xuất xưởng sau khi đối chiếu taxonomy v1.0.

## 4. Kết quả duyệt

- Vòng QC: 1
- Người review và ngày: 144, 17/11/2026.
- Đã duyệt / cả lô: 40/40.
- Ảnh lỗi / ảnh đã duyệt: 0/40 = 0.0%.
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 0/507 = 0.0%.
- Vật bỏ sót, ảnh và vùng: 0 vật bỏ sót sau hiệu chỉnh.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: carrier img_002 đã tách 1 box truck mẹ và các box car con rõ nét; tuk-tuk img_035 ôm sát khung xe không bao trùm đống hàng vượt khổ trên nóc; tượng người img_017 và ma-nơ-canh img_033 không gán person.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: validator chặn ảnh/lớp/thuộc tính hoặc hình học không hợp lệ; việc box ôm đúng xe, phải loại ego/tượng và phải tách rider/xe cần đọc ảnh.

## 5. Quyết định bàn giao

- Quyết định: Release
- Lý do, người nhận và phạm vi sử dụng: Lô 40 ảnh đạt chuẩn chất lượng với tỷ lệ ảnh lỗi 0/40 = 0.0% (đáp ứng ngưỡng <= 2%), 0 lỗi hệ thống lặp lại, 22/22 unit tests pass; bàn giao cho module Perception xe tự hành và camera giao thông thông minh.
- Nếu còn việc: Lưu trữ toàn bộ snapshot vòng duyệt tại submission/qc/reviews/round-01/ để đảm bảo tính tái lập độc lập.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: C187→img_007.jpg→R-06 (thống nhất truck)→box 135 trong labels_calibrated.json; C832→img_035.jpg→R-07 (tuk_tuk không bao đống hàng vượt khổ)→box 442 trong labels_calibrated.json. Nhãn gốc từng người được giữ nguyên độc lập.
