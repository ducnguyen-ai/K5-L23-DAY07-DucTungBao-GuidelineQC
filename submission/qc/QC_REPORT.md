# Báo cáo QC — DucTungBao

## 1. Mục tiêu và dữ liệu

- Mục đích và giới hạn sử dụng: Tôi bàn giao bộ nhãn thực hành Day07, gồm 40 ảnh đường phố. Release áp dụng cho bài lab này; không chứng nhận dữ liệu đủ cho xe tự hành hoặc hệ thống giao thông vận hành thực tế. Các tỷ lệ dưới đây là lỗi được ghi nhận trong lượt review, không phải accuracy so với ground truth.
- Nguồn và phép sử dụng dữ liệu: Giữ nguyên data/ATTRIBUTION.csv và giấy phép gốc.
- Manifest và checksum nhãn cuối: submission/qc/batch_manifest.json; SHA256 labels_calibrated.json = 76ffd0fd0e8a123a269913b675b5ad2d1daa802e80dc15f253946741eeeb068d.
- Guideline và taxonomy khi gán / khi bàn giao: Guideline v1.0 agreed khi gán, v1.1 sau calibration; taxonomy v1.0, giữ nguyên R-01–R-16 và các ngưỡng của đề.

## 2. Gán độc lập và IAA

- Lượt hoàn thành / được giao: 80/80 lượt, mỗi ảnh hai người; 138 có 26 ảnh/246 box, 144 có 27 ảnh/184 box, 178 có 27 ảnh/345 box. Giữ nguyên nhãn độc lập.
- IAA trước calibration: 268 cặp ghép; mean IoU 0,882; cùng lớp 96,6%; occluded_level 33,2%; truncated 88,4%. Có 239 box chưa ghép. Ghép một-một không phân biệt class, IoU ≥0,5.
- Kết quả từng cặp: 138/144 IoU 0,827 và class 98,8%; 138/178 IoU 0,930 và class 100%; 144/178 IoU 0,849 và class 84,3%. Chỉ số tổng đạt không có nghĩa mọi ảnh hoặc mọi cặp đạt.
- Calibration: 837 dòng IAA liên kết tới quyết định ảnh, rule, source_id/final_id và bản sửa. Không dùng số dòng ứng viên làm số lỗi thực tế. Nguồn và lịch sử nhãn vẫn tra được qua calibration_applied.csv.
- Giới hạn độc lập: Các bộ nhãn có công cụ/model hỗ trợ; IAA là so sánh ba bộ đã nộp, không khẳng định nghiên cứu gán thủ công độc lập hoàn toàn.

## 3. Các sửa và căn cứ

- Nhãn cuối: 474 annotations/40 ảnh; 435 giữ từ bản nền, 13 loại, 8 sửa và 31 bổ sung. Đây là thao tác so với nguồn từng ảnh trong calibration_patch.json, không phải chênh lệch trực tiếp so với consensus 507 box.
- Nguồn bản nền: Chọn 178 nếu được giao ảnh, nếu không chọn 138 rồi sửa theo ảnh. Đây không phải xếp hạng độ chính xác giữa thành viên; giữ mapping tới nhãn nguồn và các sửa để kiểm lại.
- R-02/R-03: Sửa extent truck img_001; thêm van, người và motorcycle img_005; sửa box person áo xanh bao đủ mũ và phần thấy tới biên dưới. Tách person/motorcycle, không gộp rider vào xe.
- R-08: Bổ sung person/motorcycle nhòe ở trái, giữa và phải img_014 theo phần quan sát được; không loại chỉ vì nhòe.
- R-03/R-08: Bổ sung motorcycle tiền/trung cảnh và person còn thiếu ở img_021, sửa person 31 bao đầu; giữ các instance riêng trong cảnh chồng nhau.
- R-14: Giữ rooftop car img_024 vì thấy kết cấu thân ô tô và bánh; không yêu cầu xe trưng bày phải chứng minh động cơ hoạt động. Không loại chỉ vì khoang/cửa kính đã cắt.
- Các sửa trước đó: Loại box pickup trùng img_007/img_012; pickup img_028 thành truck; loại ego motorcycle img_040. Tượng/mannequin/đồ chơi và reflection được loại theo R-12/R-13.
- Phạm vi guideline: Chốt cách áp dụng rule hiện có cho các ảnh trên, không đổi schema hoặc threshold. Toàn bộ 40 ảnh nằm trong scope calibration và manifest.

## 4. Kiểm lại và bằng chứng

- Vòng QC: 5
- Người review và ngày: 178, ngày 17/11/2026. Người dùng xác nhận đã kiểm nhóm 31 ảnh còn trống ở vòng 2; trợ lý theo ủy quyền 178 sửa/kiểm các ảnh 001,005,014,021,024 và kiểm năm ảnh âm tính 017,020,027,033,038. 024 thuộc nhóm 31 ảnh nhưng được kiểm thêm. Không ghi đây là review độc lập mới của 144.
- Đã duyệt / cả lô: 40/40, theo cơ sở từng dòng trong reviews/round-05/qc_review.csv. Xác nhận của người dùng và phạm vi sửa được ghi tại calibration_patch.json.
- Ảnh lỗi / ảnh đã duyệt: 0/40 = 0,0% lỗi còn ghi nhận ở vòng 5 sau sửa; không phải tuyên bố tuyệt đối không thể còn sai sót.
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 0/474 = 0,0% lỗi còn ghi nhận. Vật bỏ sót được đếm riêng.
- Vật bỏ sót, ảnh và vùng: 0 ca còn ghi nhận ở vòng 5. Giữ các ca bỏ sót vòng 2 để đối chiếu lịch sử, không xóa bằng chứng cũ.
- Ca khó / phần còn lại: Crowded riders, xe độ và motion blur đã được xử lý theo bản v1.1; nếu có phát hiện mới thì mở vòng mới trên nhãn sửa, không sửa phiếu cũ. Mức che là ước lượng thị giác, không có ground truth lớp học để xác nhận accuracy.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Checksum khóa nhãn/manifest/phiếu cùng phiên bản; phát hiện box ôm bicycle, ego hoặc chi tiết trùng vẫn cần đối chiếu ảnh.
- Lịch sử: Vòng 1 của 144 được giữ nguyên; vòng 2 Hold được giữ nguyên. Vòng 3/4 là snapshot kiểm trung gian, không dùng ra quyết định. Vòng 5 là vòng bàn giao hiện tại.

## 5. Quyết định

- Quyết định: Release
- Lý do, người nhận và phạm vi sử dụng: qc_report.py --round 5 trả RELEASE với phiếu đủ 40 ảnh, không còn can_review, không còn guideline gap và không còn lỗi ghi nhận sau sửa. Bàn giao cho coach trong phạm vi bài lab Day07.
- Nếu còn việc: Không còn lỗi đang mở trong phiếu vòng 5; giữ lịch sử và mở vòng mới nếu có phát hiện bổ sung. Giữ nguồn ảnh và giới hạn sử dụng khi chia sẻ.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: img_001→R-02→calibration_patch.json update 7→calibration_applied.csv→labels_calibrated.json; img_021→R-03/R-08→các annotation bổ sung→snapshot vòng 5. Manifest ghi SHA256 các đầu vào và nhãn bàn giao.
