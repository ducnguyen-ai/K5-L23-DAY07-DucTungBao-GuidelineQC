# Guideline gán nhãn — v1.0 — 178

- Phiên bản: v1.0, đã chốt.
- Ngày: 16/11/2026.
- Người phụ trách: 178; lớp L2.
- Bản áp dụng của 178 sau khi thống nhất guideline chung v1.0. Quy tắc và mã R-01–R-16 giữ đồng nhất với bản chung.

## 1. Mục tiêu và phạm vi

Gán bounding box 2D cho người và phương tiện thật quan sát trực tiếp trong 40 ảnh gốc. Nhãn phục vụ object detection; không suy ra danh tính, khả năng vận hành, số ghế không nhìn thấy hoặc chuyển động từ một ảnh tĩnh. Giữ nguyên ảnh và ATTRIBUTION.csv.

Các lỗi ưu tiên tránh: bỏ sót người/xe, gộp nhiều vật vào một box, nhầm lớp phương tiện, gán tượng/đồ chơi/hình in thành vật thật và suy đoán phần bị che. Mức đồng thuận cao không chứng minh nhóm đã gán đúng thực tế; reviewer vẫn cần xem ảnh và ca tham chiếu.

Phân công hiện tại:178 gán 27 ảnh,144 gán 27 ảnh,138 gán 26 ảnh; mỗi ảnh 2 người, tổng 80 lượt gán. Pha 1 mỗi người xem đủ 40 ảnh; Pha 3 chỉ gán danh sách riêng. Chỉ tập hợp nhãn khi mọi người đã hoàn tất lượt độc lập, theo GUIDE/RULES mới.

## 2. Taxonomy và thuộc tính

### 2.1. Danh sách lớp: 7 lớp đối tượng + 1 vùng bỏ qua

Bộ lớp thống nhất gồm 7 lớp đối tượng và 1 vùng bỏ qua. Dùng `bus` và `tuk_tuk` cho đúng loại phương tiện; không ép sang car/truck/van/motorcycle.

| Class | Định nghĩa / dấu hiệu quan sát | Ví dụ | Loại trừ / dễ nhầm |
|---|---|---|---|
| `car` | Sedan, hatchback, wagon, SUV, MPV dạng ô tô con. | Xe trên carrier img_002; wagon thật img_024. | Pickup→truck; đồ chơi img_038 không gán. Không phân loại bằng kích thước hoặc số ghế suy đoán. |
| `truck` | Xe có kết cấu chở hàng riêng: pickup, xe tải thùng, đầu kéo/carrier. Pickup giữ lớp kể cả gắn nắp thùng cao. | img_001,img_002,img_012,img_036; pickup img_037. | Van nguyên khối khác truck. Tượng pickup img_027 không gán. |
| `van` | Thân hộp kín liền cabin, kiểu xe hàng/xe khách nhỏ, không có cấu trúc pickup hoặc cabin-thùng riêng. | Chỉ dùng khi đủ dấu hiệu nhìn thấy. | img_037 là pickup gắn cap theo attribution, không lấy làm ví dụ van. Không ép minibus kiểu xe khách vào van chỉ vì xe nhỏ. |
| `bus` | Xe buýt/xe khách, gồm minibus có thân xe khách và dãy cửa sổ/khoang hành khách. | Minibus img_009; bus nền img_037, bus img_040. | Không dùng ngưỡng 16 ghế nếu không quan sát được; ca van/bus chưa chắc cần review. |
| `tuk_tuk` | Xe ba bánh có động cơ kiểu tuk-tuk, auto-rickshaw hoặc xe lam chở người/hàng. | img_004,img_016,img_035,img_040. | Xích lô đạp chân ngoài phạm vi; motorcycle + sidecar theo quy tắc tổ hợp dưới đây. |
| `motorcycle` | Xe máy/mô tô hai bánh có động cơ, kể cả scooter; mô tô gắn sidecar tính một tổ hợp motorcycle. | img_005,img_006,img_026; sidecar img_022. | Bicycle/xích lô không phải motorcycle; người ngồi xe là person riêng. |
| `person` | Người thật nhìn trực tiếp, kể cả rider/hành khách và người mặc costume khi có căn cứ nhận biết. | img_003,img_014,img_026; ca costume img_011. | Tượng img_017, mannequin img_033, người in trên biển img_018 không gán. |
| `ignore_region` | Vùng bỏ qua theo quy tắc vật nhỏ hoặc không tách được, không phải vật thể. | Vùng chứa các vật dưới 20 px; cụm không thể tách sau xem ảnh. | Không dùng vì model không phát hiện, khó phân loại hoặc muốn che một vật rõ của người khác. Không có 3 thuộc tính dưới đây. |

Ngoài taxonomy: bicycle, xích lô đạp chân, động vật, biển/cột, đồ vật/hàng hóa rời không gán class đối tượng. Người trên phương tiện ngoài taxonomy vẫn gán person khi đủ điều kiện. Không khoanh ignore chỉ vì một vật rõ nằm ngoài taxonomy; ghi issue nếu phạm vi chưa rõ.

### 2.2. Thuộc tính chung cho7 class đối tượng

Tỷ lệ che `q` là ước lượng phần hình chiếu của vật bị vật khác che **trong khung ảnh**; không cộng phần ngoài ảnh do truncated. Không tính q từ tỷ lệ diện tích bbox so với ảnh. Đây là ước lượng dựa trên cấu trúc nhận ra, không phải đo pixel chính xác.

| Thuộc tính | Giá trị | Quy tắc |
|---|---|---|
| `occluded_level` | `0` | Không quan sát thấy phần nào bị vật khác che: q=0%. |
| | `1` | 0%<q≤30%. Ví dụ q 30% thuộc mức 1. |
| | `2` | 30%<q≤70%. Ví dụ q 30,5% và 70% thuộc mức 2. |
| | `3` | q>70%, nhưng vẫn đủ cấu trúc để nhận biết class/box theo quy tắc. |
| `truncated` | `yes/no` | yes nếu hình dạng vật tiếp tục ra ngoài khung; no nếu toàn phần vật nằm trong khung. Chạm biên là dấu hiệu cần xem, không tự động chứng minh truncated. |
| `can_review` | `true/false` | true nếu chưa chắc class, mức che, extent hoặc áp dụng rule; ghi câu hỏi cụ thể. false khi đã xác định đủ. |

Các khoảng q liên tục, không có khe tại 30,5%. Mức 3 chỉ biểu thị che trên 70%, không biểu thị “không biết”. Nếu chưa xác định được thuộc tính, bật can_review và xử lý trước bàn giao.

Chưa vẽ được box do không xác định vật/extent: ghi `image_issues.csv` sau khóa bản độc lập, với `image,annotator,region,note`; không tạo box/class tạm ngẫu nhiên. Nếu đã có box hợp lý nhưng ca biên, bật can_review. Ghi nhật ký và bản cá nhân riêng cho đến khi hết pha độc lập.

## 3. Quy tắc bounding box có mã cố định

| Rule ID | Quy tắc thao tác |
|---|---|
| R-01 | **Phần nhìn thấy:** box là hình chữ nhật nhỏ nhất bao các phần thấy được và nhận ra thuộc cùng vật. Không kéo ra phần bị che hoàn toàn hoặc ngoài ảnh. Nếu thấy nhiều phần rời của cùng vật, một box bao các phần ấy; không tách thành nhiều instance. |
| R-02 | **Một vật/một box:** không gộp các vật đứng sát nhau; không tạo box trùng cùng vật. Box khác instance được chồng nhau khi che khuất, kể cả khác class. |
| R-03 | **Người và xe:** với n người phân biệt được trên một xe, gán n box person và một box phương tiện, không chỉ luôn “2 box”. Mỗi người ngồi sau là một person riêng. Mũ/quần áo/balo đeo sát người thuộc extent người; xe không thuộc extent người. |
| R-04 | **Phụ kiện/hàng:** phương tiện bao cấu trúc và bộ phận gắn liền như gương xe; không mở box theo bao tải/hàng rời vượt thân. Person không bao đòn gánh, thúng hàng, ô hoặc vật dụng cồng kềnh tách xa cơ thể. |
| R-05 | **Carrier:** một truck cho tổ hợp đầu kéo-rơ-moóc chở xe khi nhận ra cùng tổ hợp; từng xe trên sàn có box riêng nếu đủ rõ/cao 20 px. Không ép ảnh phải có đúng8 car nếu thực tế phần thấy/độ rõ khác; không gán các mảnh rời của một xe thành nhiều xe. |
| R-06 | **Pickup và nắp thùng:** pickup thuộc truck, có hoặc không cap. Xe tải nhẹ cabin/thùng riêng cũng truck. Không đổi class chỉ vì xe nhỏ hoặc lắp vỏ kín. img_037 dùng truck theo cấu trúc và attribution. |
| R-07 | **Bus/tuk-tuk/sidecar:** dùng lớp mới bus,tuk_tuk đúng định nghĩa, không class gần nhất tùy người. Mô tô có sidecar giữ một motorcycle bao cả phần tổ hợp thấy được; sidecar không thành motorcycle thứ hai. Người ngồi trên tổ hợp vẫn person riêng. |
| R-08 | **Che/cắt:** cần đủ bằng chứng class và ranh giới phần thấy. Không suy ra tỷ lệ bị cắt bằng bbox hoặc bắt người gán đo phần ngoài ảnh. Phần thấy hợp lệ và cao ≥ 20 px vẫn xét dù mức che lớn; mảnh quá mơ hồ ghi issue, không đoán class. |
| R-09 | **Mép ảnh:** tọa độ giới hạn trong ảnh; `0≤x1<x2≤W`, `0≤y1<y2≤H`. Truncated theo vật thật, không chỉ vị trí box. |
| R-10 | **Vật nhỏ:** h=y2−y1<20px trên ảnh gốc không gán từng vật; tạo ignore_region gọn quanh vùng vật nhỏ theo cheatsheet. h=20 px đủ ngưỡng, h=50 px vào nhóm box lớn. Không phóng to box để vượt ngưỡng và không dùng mức zoom màn hình để tính pixel. |
| R-11 | **Ignore/dày đặc:** tách từng vật rõ khi được; vùng ignore không phủ tùy tiện cả ảnh hoặc người/xe rõ≥20px. Nếu vật rõ và cụm nhỏ khó tách khỏi một ignore chữ nhật, ghi issue. Ignore chỉ một phía che box phía khác là ca calibration, không mặc định hai người đã đồng ý bỏ vật đó. |
| R-12 | **Vật giả/hình in:** không gán tượng, mannequin, đồ chơi, shadow, hình 2D hoặc ảnh trên màn hình thành vật thật. Chỉ loại vùng mô phỏng; người/xe thật khác cùng ảnh vẫn phải xét. Không gọi mọi ảnh có tượng là ảnh 0 annotation. |
| R-13 | **Reflection/ego:** không gán vật chỉ nhìn qua gương hoặc phản chiếu; vật thật nhìn trực tiếp qua kính trong suốt vẫn xét. Không gán nắp capo/gương/thân xe chủ quay phim làm một instance riêng. |
| R-14 | **Costume/xe độ/trưng bày:** ngoại hình lạ, đứng yên hoặc trưng bày không tự chứng minh là đồ giả. Người mặc costume vẫn person nếu xác định được; xe thật độ/trưng bày vẫn class theo kết cấu. Không suy ra xe thật/giả hoặc khả năng hoạt động chỉ từ confidence hoặc hình dáng. Nếu không phân biệt được vỏ xe/mô hình/xe biểu diễn, giữ review và dẫn bằng chứng. |
| R-15 | **Ảnh âm tính:** vẫn có dòng images trong COCO dù không có box, chỉ xác nhận0annotation sau kiểm hết ảnh. Không tạo ignore cả ảnh cho tượng/đồ chơi rõ. |
| R-16 | **Chưa chắc và khóa phiên bản:** biết rõ ngoài phạm vi→exclude theo rule, không bật cờ chỉ vì đã exclude; chưa rõ có thuộc phạm vi→review/issue. Không tự thêm class/đổi threshold giữa Pha 3. Quy tắc ảnh hưởng nhãn phải được xử lý qua calibration có version và phạm vi làm lại. |

Ảnh 11: ATTRIBUTION mô tả *costumed Predator character* và *custom motorcycles*. Đối chiếu bối cảnh cùng ảnh gốc, không loại người mặc costume hoặc xe độ chỉ vì hình dáng. Ảnh 19/24 áp dụng R-14; trường hợp chưa đủ bằng chứng chuyển reviewer theo R-16.

## 4. Ca khó và hướng áp dụng trong bản chung

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_001,img_012 | Pickup, người/hàng bị che. | R-01,R-04,R-06 | Pickup→truck; person riêng; không gộp hàng vào extent người. | Theo dấu hiệu quan sát và R-01,R-04,R-06. |
| img_002 | Carrier chở nhiều xe. | R-02,R-05 | Truck tổ hợp + từng car thật đủ rõ; số box theo vật quan sát, không chép số 8 như định mức. | Theo dấu hiệu quan sát và R-02,R-05. |
| img_003 | Người gánh hàng, xe đạp và xe máy nền. | R-03,R-04,R-07 | Person ôm cơ thể/trang phục, bỏ thúng/đòn gánh; bicycle ngoài phạm vi, motorcycle thật vẫn xét. | Theo dấu hiệu quan sát và R-03,R-04,R-07. |
| img_004,img_016,img_035,img_040 | Tuk-tuk, có ca chở hàng lớn. | R-04,R-07 | Tuk_tuk riêng; box thân phương tiện và bộ phận gắn liền, không bao bao tải vượt thân; person riêng. | Theo dấu hiệu quan sát và R-04,R-07. |
| img_005,img_006,img_010,img_026 | Nhiều người trên cùng xe. | R-03 | n người + một xe; kiểm không gộp hai người thành một, kể cả khi box người chồng nhau. | Theo dấu hiệu quan sát và R-03. |
| img_007,img_036 | Pickup và xe tải nhỏ/thùng riêng. | R-06,R-08 | Truck; vẫn xét trong ảnh tối, không tự đổi van theo kích thước. | Theo dấu hiệu quan sát và R-06,R-08. |
| img_009 | Minibus/xe khách có dãy cửa sổ. | R-07,R-16 | Bus theo cấu trúc; không đoán số ghế hoặc ép van/truck. | Theo dấu hiệu quan sát và R-07,R-16. |
| img_011 | Costume Predator, xe máy độ và người/xe nền. | R-12,R-14 | Không tự loại như tượng; xác minh từng vật thật/giả và extent, các đối tượng chưa chắc bật review. | Theo dấu hiệu quan sát và R-12,R-14. |
| img_014,img_015,img_031 | Nhòe chuyển động, tối/mưa và phản chiếu. | R-08,R-13,R-16 | Vật rõ vẫn gán; không gán phản chiếu trên đường; chưa rõ ghi issue thay vì đoán. | Theo dấu hiệu quan sát và R-08,R-13,R-16. |
| img_017,img_027 | Tượng người cưỡi ngựa / monument pickup. | R-12,R-15 | Không gán tượng thành person/truck. Vẫn kiểm phần ảnh khác trước kết luận ảnh âm tính. | Theo dấu hiệu quan sát và R-12,R-15. |
| img_018 | Người in trên billboard, xe thật phía dưới. | R-12 | Không gán hình in; xe thật nền không bị loại theo billboard. | Theo dấu hiệu quan sát và R-12. |
| img_019 | Xe biểu diễn hình phô-mai, nhân vật hoạt hình, người lái/khán giả thật. | R-12,R-14,R-16 | Person thật được gán; nhân vật mô phỏng không gán. Class của xe biểu diễn cần nhóm quyết theo phạm vi R-14; giữ issue nếu chưa chắc. | Theo dấu hiệu quan sát và R-12,R-14,R-16. |
| img_020 | Gương chiếu hậu, phản chiếu và thân xe chủ. | R-13,R-15 | Không gán vật chỉ trong gương hoặc phần ego; giữ ảnh trong COCO. | Theo dấu hiệu quan sát và R-13,R-15. |
| img_021,img_025,img_030,img_032,img_039 | Nhiều vật nhỏ/dày đặc. | R-10,R-11 | Gán vật đủ rõ/cao, ignore gọn phần dưới 20 px hoặc không tách được theo rule; không xóa cả đám đông. | Theo dấu hiệu quan sát và R-10,R-11. |
| img_022 | Mô tô có sidecar. | R-07 | Một motorcycle cho tổ hợp; không hai motorcycle cho xe chính và thùng sidecar. | Theo dấu hiệu quan sát và R-07. |
| img_023,img_029 | Xích lô/xe đạp và người thật. | R-03,R-07 | Phương tiện không động cơ ngoài phạm vi; person thật vẫn gán. | Theo dấu hiệu quan sát và R-03,R-07. |
| img_024 | Xe trưng bày và vỏ/xe nhỏ màu vàng trên nóc. | R-02,R-14,R-16 | Xe thật phía dưới vẫn car. Vật trên nóc cần chốt có phải vỏ/mô hình ngoài phạm vi không; chưa khẳng định loại bỏ bằng suy đoán. | Theo dấu hiệu quan sát và R-02,R-14,R-16. |
| img_033,img_038 | Mannequin và ô tô đồ chơi trong cửa kính. | R-12,R-13 | Không gán vật giả; không nhầm vật thật sau kính trong suốt với ảnh phản chiếu. | Theo dấu hiệu quan sát và R-12,R-13. |
| img_034 | Người băng qua trước nhiều xe ngược sáng. | R-01,R-03,R-08 | Người và xe riêng, kiểm mép ảnh và vật nền đủ 20 px. | Theo dấu hiệu quan sát và R-01,R-03,R-08. |
| img_037 | GO Transit pickup có Master 75 truck cap; bus nền. | R-06,R-07 | Pickup→truck kể cả nắp cao; bus nền→bus. Không lấy pickup làm ví dụ van. | Theo dấu hiệu quan sát và R-06,R-07. |

Áp dụng cùng một phiên bản cho tất cả thành viên. Ca vật thể chưa đủ bằng chứng được ghi issue/can_review để xử lý trong calibration; không tự thêm lớp.

## 5. QC và phiên bản

### 5.1. Ngưỡng cố định và mẫu số

Giữ nguyên mục rules của đề: min_box_height_px 20; large_px 50; iou_thr_large 0.85; iou_thr_small 0.70; match_iou 0.50; iaa_iou 0.85; iaa_class 0.95; error_rate_img_max 0.02. Đây là ngưỡng QC của lab, không phải accuracy model hoặc sự bảo đảm box đúng thực tế.

- Đủ 80/80 lượt gán được giao trước khi tính IAA. Nhãn gợi ý chưa được duyệt không được tính là nhãn người gán đã hoàn tất.
- Ghép một-một theo IoU≥0.5, không phân biệt lớp khi tìm cặp; IoU TB và class agreement chỉ trên cặp ghép được. Box chưa ghép được thống kê riêng; không có cặp→N/A.
- Với assignment hiện tại mỗi ảnh 2 người, mỗi ảnh có 1 cặp người; không mặc định 3 cặp chỉ vì nhóm có 3 thành viên. Nếu một ảnh thật sự có 3 người gán thì có 3 cặp.
- IoU lớn/nhỏ 0.85/0.70 là ngưỡng so sánh hình học theo lab; không tự gọi là đo với ground truth nếu chưa có reference.
- Lỗi theo ảnh = số ảnh review có ≥ 1 lỗi / số ảnh đã review. Lỗi theo đối tượng = số annotation đối tượng hiện có bị lỗi / số annotation đối tượng đã duyệt, mỗi đối tượng chỉ tính một lần dù có nhiều loại lỗi. Bỏ sót ghi số vật/vùng riêng, không thêm đối tượng chưa tồn tại vào mẫu số một cách tùy ý.
- Duyệt đủ 40 ảnh mới bàn giao Release; 1/40=2,5% đã vượt 2%. Vòng demo/lấy mẫu luôn Hold. Giữ IAA trước calibration, không sửa số đo cho đạt.

### 5.2. Phiếu QC và quyết định đúng script hiện tại

Phiếu theo vòng `submission/qc/reviews/round-NN/qc_review.csv`: `image,object_id,error_type,reviewer,rule_id,region,note`.

| error_type | Cách ghi |
|---|---|
| bo_sot | Để trống object_id, ghi region phân biệt vật bỏ sót, rule_id và note. |
| thua | ID box có thật trong ảnh, rule_id và note vì sao loại. |
| sai_lop | ID box, class đang có và class cần sửa trong note, dẫn rule. |
| sai_vi_tri_kich_thuoc | ID box, dẫn rule và mô tả hướng sửa. |
| sai_thuoc_tinh | ID box, thuộc tính cần sửa/giá trị đúng và rule. |
| khong | Chỉ sau review toàn ảnh; không ghi object_id, rule_id hoặc region, không vừa sạch vừa lỗi cho cùng ảnh. |

Không ghi mã thành viên vào cột reviewer nếu người đó chưa review. Thay nhãn/quyết định calibration phải mở vòng đúng phiên bản; không dùng lại review cũ cho checksum nhãn mới. Script gắn kết review với labels, manifest và calibration decisions; không sửa tay báo cáo sinh tự động.

Theo `qc_report.py` hiện tại: Hold khi thiếu/sai bằng chứng, còn issue guideline/data, còn can_review hoặc chỉ demo; Rework khi tỉ lệ ảnh lỗi>2% hoặc một error_type có ít nhất 3 lỗi và chiếm≥50% tổng lỗi; Release khi không còn điều kiện trên và reviewer xác nhận. IAA trước calibration dùng để chẩn đoán, không tự thêm điều kiện trái script để sửa số hoặc ép kết quả.

### 5.3. Xử lý ca chưa chắc và lịch sử phiên bản

Người gán ghi mã ảnh, vùng, Rule ID và câu hỏi cụ thể. Reviewer của vòng QC quyết định trên ảnh gốc, ghi mã người quyết và lý do trong nhật ký calibration. Nếu quyết định làm thay đổi quy tắc chung, tăng phiên bản và xác định các ảnh cần rà lại; không sửa âm thầm guideline đã khóa.

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| v0 | Bộ quy tắc khởi đầu của lab. | Điểm xuất phát để rà các ca khó. |
| v1.0 — 16/11/2026 | Thống nhất 7 lớp đối tượng + ignore; khoảng che 0 / (0,30] / (30,70] / >70%; R-01–R-16; pickup gắn cap→truck, sidecar→một motorcycle, n người→n person. | Thống nhất cách xử lý carrier, tuk-tuk, bus, costume, vật giả, người trên xe và ranh giới box. Nhóm đã chốt theo xác nhận của 178. |

Taxonomy áp dụng: `submission/taxonomy.json`; cấu hình CVAT: `cvat/labels_generated.json`. Không thay các ngưỡng trong mục rules của đề.

Tham chiếu: GUIDE.md, RULES.md, docs/QC_CHEATSHEET.md, scripts/qc_report.py, schemas/taxonomy.schema.json; ảnh gốc và data/ATTRIBUTION.csv.
