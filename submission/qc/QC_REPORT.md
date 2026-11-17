# Báo cáo QC — DucTungBao

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: đặc tả và kiểm soát nhãn bounding box 2D người/phương tiện trên 40 ảnh của lab; số liệu dưới đây là đồng thuận giữa bộ nhãn, không phải độ chính xác so với ground truth.
- Nguồn và phép sử dụng dữ liệu: giữ nguyên data/ATTRIBUTION.csv và ảnh gốc; đối chiếu nguồn ảnh khi phân biệt vật thật, costume, tượng và mô hình.
- Manifest và checksum nhãn cuối: chưa tạo batch_manifest.json vì calibration và bản nhãn cuối chưa chốt. Checksum đầu vào IAA được lưu trong iaa_summary.json.
- Guideline và taxonomy khi gán / khi bàn giao: dùng guideline_v1.0_agreed.md và taxonomy v1.0 (7 lớp đối tượng + ignore_region); bản v1.1 sau calibration chưa được chốt. Không thay ngưỡng của đề.

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

- Phân công: 178 chốt calibration, 144 review QC, theo lựa chọn của 178 ngày 17/11/2026. Phân công không đồng nghĩa hai người đã hoàn thành bước đó.
- Ca đã xử lý, rule ID, bản sửa và người xác nhận: mới tạo calibration_decisions.csv với 837 dòng từ script; các ô quyết định/kiểm lại còn chờ thực hiện. Không ghi người đã xác nhận khi chưa review.
- Đề xuất ưu tiên: C187 pickup→truck (R-06); C307 SUV→car; C308 rà xe con xa; C496 pickup→truck; C599 bus→bus; C832/C833→tuk_tuk (R-07). C398 xe biểu diễn cần quyết định theo R-14; C600 cần kiểm hai instance person và motorcycle (R-03), không chỉ ép một class cho hai box chồng nhau.
- Tác động v1.1 lên nhãn và ảnh: chưa đổi nghĩa guideline/taxonomy. Sau khi chốt từng ca, ghi loại thay đổi thật trong guideline_change.json và bản guideline v1.1. Nếu đổi nghĩa thì phạm vi lo và kiểm cả 40 ảnh theo script.
- Tham chiếu bằng chứng khi Rework: chưa có vòng QC cũ hay quyết định Rework. Ảnh chồng nhãn được sinh bằng viz_disagreement.py trong work/viz; trang đối chiếu local ở work/calibration_review/index.html.
- Điểm cần thành viên đối chiếu trong ghi chú: notes 138 mô tả bộ 5 lớp trong khi bản chung có 7 lớp đối tượng; notes 144 ghi đã tick can_review 3 lần nhưng file nộp hiện có 0 cờ true. Giữ nguyên bản cá nhân, đề nghị chủ bản cập nhật đúng việc đã làm, không tự sửa trải nghiệm của người khác.

## 4. Kết quả duyệt

- Vòng QC: chưa mở; cần có nhãn calibration và manifest trước khi tạo round-01.
- Người review và ngày: 144 được phân công; chưa có xác nhận review cuối. Ngày cập nhật tiến độ: 17/11/2026.
- Đã duyệt / cả lô: chưa thực hiện QC nhãn cuối / 40 ảnh.
- Ảnh lỗi / ảnh đã duyệt: chưa đo; không dùng 34 ảnh bị cờ IAA thay cho số ảnh lỗi QC.
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: chưa đo.
- Vật bỏ sót, ảnh và vùng: chưa kết luận; xem bo_sot_thua trong calibration_candidates.csv.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: carrier img_002 có các box xe con của hai bản lệch rõ trên ảnh; phạm vi person/vehicle trong cảnh đông và các lớp bus/tuk_tuk cần chốt.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: validator chặn ảnh/lớp/thuộc tính hoặc hình học không hợp lệ; việc box ôm đúng xe, phải loại ego/tượng và phải tách rider/xe cần đọc ảnh.

## 5. Quyết định bàn giao

- Quyết định: Hold
- Lý do, người nhận và phạm vi sử dụng: trạng thái tiến độ nội bộ, chưa phải quyết định do qc_report.py sinh. Chưa có 837 quyết định calibration được chốt, nhãn cuối, manifest hoặc review QC đủ 40 ảnh. Chưa nộp như bài đã hoàn tất.
- Nếu còn việc: 178 chốt calibration trên ảnh gốc, sửa đúng scope và lưu COCO theo tên revision do prepare_calibration.py in ra; build_final.py tạo nhãn cuối/manifest; 144 điền phiếu review thật rồi chạy qc_report.py/check_submission.py.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: C187→img_007.jpg→R-06→hai box pickup IoU 0,96 nhưng class car/truck khác; đề xuất truck chưa thay xác nhận calibration. Nhãn gốc từng người được giữ nguyên sau lần IAA này.
