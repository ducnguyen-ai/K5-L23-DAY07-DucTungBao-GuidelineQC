# Guideline gán nhãn — v1.1 (Individual Draft) — 138

* Phiên bản: v1.1 (Individual Draft — Pha 1, đã đồng bộ QC Cheatsheet)
* Ngày: 16/11/2026
* Mã người viết: 138 (Khảo sát độc lập Pha 1)
* Trạng thái: Chờ họp thống nhất nhóm / Reviewer (Pha 2)
* Loại nhãn: Bounding Box (hộp chữ nhật) trên ảnh đường phố
* Công cụ: CVAT, xuất COCO 1.0

## 1. Mục tiêu

Guideline này quy định cách gán nhãn Bounding Box cho các đối tượng người và phương tiện xuất hiện trong ảnh đường phố, nhằm khắc phục các định nghĩa định tính mơ hồ của bản khởi đầu (`guideline_v0_starter.md`) và đồng bộ với bộ tiêu chuẩn kiểm soát chất lượng của lab (`docs/QC_CHEATSHEET.md`).

Nhãn được sử dụng để huấn luyện và đánh giá mô hình phát hiện đối tượng (Object Detection), phục vụ các ứng dụng như camera giao thông và xe tự lái.

Mục tiêu:
* Đảm bảo các annotator xác định class thống nhất thông qua định nghĩa rõ ràng và danh sách phản ví dụ cụ thể.
* Đảm bảo mỗi đối tượng hợp lệ được gán một Bounding Box đạt chuẩn độ chính xác hình học của lab ($\text{IoU} \ge 0.85$ với box cao $\ge 50\text{ px}$ và $\text{IoU} \ge 0.7$ với box nhỏ hơn).
* Chốt các ngưỡng đo định lượng cho thuộc tính che khuất (`occluded_level`), cắt mép (`truncated`) và ngưỡng vật nhỏ (`cao < 20 px`).
* Tách bạch rạch ròi giữa **Ca loại trừ theo quy tắc (`exclude`)** và **Ca biên cần hỏi Reviewer (`can_review`)** trong buổi họp Pha 2.
* Đảm bảo chất lượng lô 40 ảnh đạt chuẩn nghiệm thu (tỷ lệ ảnh lỗi $\le 2\%$, không có lỗi hệ thống lặp lại).

## 2. Lớp và thuộc tính

### 2.1. Lớp

Dataset sử dụng 6 label được cấu hình sẵn trong CVAT, gồm 5 class đối tượng và 1 label vùng bỏ qua.

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô con dùng để vận chuyển người (thường từ 4–7 chỗ, thiết kế khoang hành khách liền khối hoặc có cốp). | Sedan, hatchback, SUV, MPV gia đình | Tượng xe bán tải (`img_027.jpg`), xe mô hình đồ chơi (`img_038.jpg`), xe phản chiếu trong gương (`img_020.jpg`), xe tải, xe van, xe buýt (`img_009.jpg`) |
| `truck` | Phương tiện cơ giới được thiết kế chủ yếu để vận chuyển hàng hóa, có thùng hàng tách biệt hoặc kết cấu chịu tải nặng. | Xe tải thùng, xe ben, xe đầu kéo chở ô tô (`img_002.jpg`) | Ô tô con, xe van, xe bán tải gắn nắp thùng cao (`img_037.jpg` — ca biên cần review) |
| `van` | Phương tiện dạng xe thùng kín cỡ nhỏ/trung bình dùng chở hàng nhẹ hoặc chở khách dưới 16 chỗ (đầu ngắn, thân hộp). | Xe van chở hàng, xe khách 12–16 chỗ | Sedan, xe tải, xe buýt cỡ lớn (`img_009.jpg` — ca biên cần review) |
| `motorcycle` | Phương tiện cơ giới hai bánh có động cơ thuộc nhóm xe máy, mô tô. | Xe máy số, xe tay ga, xe mô tô phân khối lớn | Xe đạp không động cơ (`img_006.jpg`, `img_029.jpg`), xích lô (`img_039.jpg`), xe ba bánh tuk-tuk (`img_004.jpg`, `img_035.jpg`), người lái xe |
| `person` | Con người thật bằng xương bằng thịt xuất hiện trực tiếp trong không gian ảnh, bao gồm người đi bộ, người lái xe hoặc người ngồi trên phương tiện. | Người đi bộ, người lái xe máy, người gánh hàng rong (`img_003.jpg`) | Tượng đồng/tượng đá (`img_011.jpg`, `img_017.jpg`), ma-nơ-canh trong tủ kính (`img_033.jpg`), chân dung trên biển quảng cáo (`img_018.jpg`), gánh hàng/thúng hàng tách rời |
| `ignore_region` | Vùng được đánh dấu để bỏ qua việc gán nhãn từng đối tượng bên trong, áp dụng cho cụm vật nhỏ (`cao < 20 px`) hoặc đám đông dày đặc không thể tách rời. | Cụm người/xe ở quá xa có chiều cao $< 20\text{ px}$, bãi đỗ xe máy chồng chéo ở nền xa | Không sử dụng thay thế tùy tiện cho một object đơn lẻ đủ kích thước nhưng khó phân loại |

Quy tắc:
* Mỗi object thực tế thuộc một class phù hợp trong 5 class đối tượng.
* Mỗi object được gán một Bounding Box riêng.
* Không tự tạo class mới ngoài danh sách label có sẵn.
* **Phương tiện không động cơ / ngoài taxonomy** (xe đạp `img_006.jpg`, `img_029.jpg`; xe xích lô `img_039.jpg`; xe đẩy tay): Không tạo box thuộc 5 class trên. Bỏ qua coi như nền (background), trừ khi nằm trong cụm cần phủ `ignore_region`.
* Không gán tượng, ma-nơ-canh, đồ chơi, hình ảnh phản chiếu hoặc hình in 2D thành `person` hay phương tiện thật.

### 2.2. Thuộc tính

Năm class đối tượng (`car`, `truck`, `van`, `motorcycle`, `person`) đều có cùng ba thuộc tính.

| Thuộc tính | Giá trị | Ngưỡng định lượng & Ý nghĩa |
|---|---|---|
| `occluded_level` | `0` | **0%**: Không bị object khác che khuất. |
| `occluded_level` | `1` | **1% – 30%**: Bị che khuất nhẹ (ví dụ: che một phần bánh xe, tay lái hoặc bàn chân). |
| `occluded_level` | `2` | **31% – 70%**: Bị che khuất trung bình đến nhiều, nhưng vẫn nhìn rõ cấu trúc chính của đối tượng. |
| `occluded_level` | `3` | **Trên 70%**: Bị che khuất nghiêm trọng nhưng vẫn còn đủ bằng chứng cấu trúc đặc trưng để nhận dạng chắc chắn class và vị trí. |
| `truncated` | `no` | Object nằm trọn vẹn bên trong khung hình ảnh, không bị cắt bởi biên ảnh. |
| `truncated` | `yes` | Một phần object nằm ngoài khung ảnh do bị cắt ở biên ảnh. |
| `can_review` | `false` | Đối tượng rõ ràng, không có điểm phân vân về class, vị trí box hoặc quy tắc áp dụng. |
| `can_review` | `true` | Tình huống biên chưa có quy định rõ trong taxonomy (ví dụ: xe buýt, xe tuk-tuk, bán tải nắp thùng cao) cần đưa ra họp Pha 2. |

Quy tắc áp dụng:
* `occluded_level` phản ánh phần diện tích object bị che bởi object/vật thể khác trong ảnh, không cộng dồn phần nằm ngoài biên ảnh.
* `truncated` phản ánh việc object bị cắt bởi biên ảnh, không phụ thuộc vào mức độ bị che khuất.
* Nếu object vừa bị che khuất vừa bị cắt mép ảnh, đồng thời đặt `occluded_level` khác `0` và `truncated = yes`.
* Object bị che khuất hoặc bị cắt **không quá 70%** bắt buộc phải annotate.
* Object bị che khuất hoặc bị cắt **trên 70%** chỉ annotate khi nhìn thấy **ít nhất một bộ phận cấu trúc đặc trưng đủ để định danh chắc chắn class và ranh giới** (ví dụ: đầu/vai người, hoặc cụm đầu xe/yên xe/bánh xe hoàn chỉnh). Nếu chỉ thấy một mảnh nhỏ rời rạc (ví dụ: một góc gương chiếu hậu, chỏm mũ, hoặc một vệt lốp xe), **không annotate** để tránh lỗi `thua` (False Positive).

### 2.3. Label ignore_region

* `ignore_region` không có thuộc tính `occluded_level`, `truncated` hoặc `can_review`. Không gán các thuộc tính này cho `ignore_region`.
* **Áp dụng cho vật nhỏ theo chuẩn lab:** Các đối tượng hoặc cụm đối tượng ở xa có chiều cao **`< 20 px`** được xử lý bằng vùng `ignore_region` (đối chiếu quy tắc vật nhỏ của lab).
* Nếu trong quá trình rà soát hoặc đối chiếu chéo (IAA), chỉ một người đặt vùng `ignore_region` phủ lên box của người khác thì ca đó bắt buộc được đưa vào buổi **calibration** để thống nhất.

## 3. Quy tắc vẽ box

### 3.1. Nguyên tắc chung & Chuẩn độ chính xác (IoU)

* Mỗi object hợp lệ phải có một Bounding Box riêng biệt.
* Box phải là hình chữ nhật bao sát 4 điểm cực trị (`left`, `right`, `top`, `bottom`) của phần object nhìn thấy.
* **Yêu cầu độ chính xác hình học theo chuẩn QC của lab:**
  * Với các box có chiều cao **$\ge 50\text{ px}$**: đường viền phải ôm sát để đạt ngưỡng **$\text{IoU} \ge 0.85$** so với chuẩn (không để hở nền rộng, không cắt lẹm vào thân xe/người).
  * Với các box có chiều cao **$< 50\text{ px}$** (nhưng $\ge 20\text{ px}$): cần đạt ngưỡng **$\text{IoU} \ge 0.70$**.
* Không gộp nhiều object thành một box. Các Bounding Box được phép chồng lấn (overlap) khi các object ở gần nhau hoặc che khuất lẫn nhau.

### 3.2. Đối tượng bị che khuất

* Box chỉ bao quanh **phần object nhìn thấy**, không tự suy đoán và kéo giãn đường viền của phần bị che khuất hoàn toàn.
* Gán `occluded_level` theo đúng ngưỡng định lượng tại Mục 2.2 (`1–30%`, `31–70%`, `>70%`).
* Nếu mức che khuất lớn hơn 70% nhưng vẫn xác định được cấu trúc chính của object, khuyến khích annotate và đặt `occluded_level = 3`.
* Nếu rơi vào vùng ranh giới gây phân vân giữa việc vẽ hay bỏ qua (không đủ bằng chứng), đánh dấu `can_review = true` hoặc bỏ qua nếu chỉ là mảnh vỡ quá nhỏ.

### 3.3. Đối tượng bị cắt bởi biên ảnh

* Object bị cắt bởi cạnh ảnh vẫn phải được annotate nếu còn đủ bằng chứng nhận diện.
* Box chỉ bao phần object nằm trong khung ảnh, tuyệt đối không mở rộng box ra ngoài kích thước ảnh.
* Gán `truncated = yes`.
* Nếu phần nằm trong khung ảnh quá nhỏ (chiều cao $< 20\text{ px}$ hoặc tương đương mức che khuất $>70\%$ làm mất đặc trưng nhận diện), bỏ qua không annotate.

### 3.4. Người đi xe máy / Dắt xe

* Người lái xe máy, người ngồi sau và xe máy là các object riêng biệt.
* Gán một box cho mỗi `person` và một box cho `motorcycle`.
* Box `person` bao phần cơ thể người nhìn thấy (tính cả mũ bảo hiểm/nón lá đang đội, quần áo đang mặc và balo đeo sát lưng), không bao gồm toàn bộ xe máy.
* Box `motorcycle` bao phần xe máy nhìn thấy (tính cả gương chiếu hậu, giỏ xe gắn cố định trên xe), không bao gồm cơ thể người.
* Hai box được phép chồng lấn tại vị trí người và xe tiếp xúc hoặc che khuất nhau.
* Nếu có nhiều người trên cùng xe máy, mỗi người được gán một box `person` riêng.
* Nếu người đang dắt hoặc đạp xe đạp/xích lô không động cơ (`img_003.jpg`, `img_006.jpg`, `img_029.jpg`, `img_039.jpg`), chỉ vẽ box `person` cho người, bỏ qua phương tiện không động cơ.

### 3.5. Vật dụng mang vác, gánh hàng rong và hàng hóa trên xe

* **Đối với `person` (`img_003.jpg`):** Box chỉ bao quanh phần cơ thể người và trang phục/phụ kiện ôm sát người (mũ, nón lá, túi đeo chéo nhỏ sát người). **Không kéo rộng box** để bao gồm các vật dụng cồng kềnh tách rời khỏi trục cơ thể như: đòn gánh, thúng/mẹt hàng rong, xe đẩy hàng, ô/dù cầm tay mở rộng (tránh lỗi `sai_vi_tri_kich_thuoc` do box lỏng).
* **Đối với phương tiện (`motorcycle`, `truck`, `van`, `car`):** Box bao gồm phần khung xe và các bộ phận gắn liền. Không kéo giãn box quá mức cho các hàng hóa cồng kềnh chất vượt khổ ra ngoài thân xe quá nhiều (nếu hàng hóa che khuất thân xe khiến khó xác định ranh giới xe, đánh dấu `can_review = true`).

### 3.6. Phương tiện chở phương tiện (`img_002.jpg`)

* Phương tiện vận chuyển và phương tiện được chở là các object riêng biệt (ví dụ: xe tải chuyên dụng chở 8 ô tô con trên hai sàn ở `img_002.jpg`).
* Nếu cả hai đều thuộc taxonomy và có thể nhận diện, mỗi object có một box riêng (1 box `truck` cho xe chở + tối đa 8 box `car` riêng biệt cho từng xe con trên sàn).
* Box của phương tiện vận chuyển ôm toàn bộ khung xe chở, không gộp chung các xe được chở thành một object duy nhất mà bỏ quên các box con bên trong (tránh lỗi `bo_sot`).

### 3.7. Đối tượng ở xa / Vật nhỏ (`cao < 20 px`)

* Theo ngưỡng định lượng của lab (`docs/QC_CHEATSHEET.md`), các đối tượng có chiều cao **`< 20 px`** được xếp vào nhóm **Vật nhỏ** và xử lý bằng vùng `ignore_region` (không cố vẽ box đơn lẻ cho từng vật thể li ti ở đường chân trời).
* Với các đối tượng có chiều cao **$\ge 20\text{ px}$** nhưng ở xa/mờ đến mức không phân biệt được là `person` hay vật thể tĩnh (cột điện, biển báo), **không tự đoán nhãn** (bỏ qua hoặc dùng `ignore_region` nếu cả cụm đám đông ở xa đều mờ).

### 3.8. Reflection, shadow, tượng và hình ảnh mô phỏng

Không annotate các trường hợp sau thành object thật (xem như phản ví dụ và loại bỏ để tránh lỗi `thua`):
* **Hình ảnh phản chiếu (reflection):** Phản chiếu trên gương chiếu hậu (`img_020.jpg`), kính cửa hàng hoặc mặt nước.
* **Bóng đổ (shadow):** Bóng của người hoặc phương tiện đổ xuống mặt đường/tường.
* **Hình ảnh 2D in ấn/hiển thị:** Chân dung người hoặc hình phương tiện trên billboard, poster quảng cáo (`img_018.jpg`), màn hình hoặc in trên thân xe buýt/xe tải.
* **Tượng, ma-nơ-canh và đồ chơi:** Tượng đồng, tượng đá hình người (`img_011.jpg`, `img_017.jpg`), tượng xe bán tải (`img_027.jpg`), ma-nơ-canh và xe mô hình đồ chơi trong tủ kính (`img_033.jpg`, `img_038.jpg`).
* Nếu không thể phân biệt chắc chắn giữa object thật và vật thể mô phỏng ở khoảng cách xa, đánh dấu `can_review = true`.

## 4. Ca khó

Để đảm bảo tính nhất quán trước buổi họp Pha 2, toàn bộ tình huống biên phát hiện được khi rà soát bộ 40 ảnh được phân tách rõ thành 2 nhóm: **Nhóm A (Ca loại trừ theo quy tắc — `Exclude`)** và **Nhóm B (Ca biên cần hỏi Reviewer — `can_review = true`)**.

### Phân loại xử lý ca khó

* **Nhóm A — `exclude` (Loại bỏ theo quy tắc):** Đối tượng chắc chắn không thuộc 5 lớp vật lý thực tế dựa trên định nghĩa lớp và phản ví dụ (xe đạp, xích lô, thúng hàng, tượng, ma-nơ-canh, đồ chơi, ảnh in 2D, ảnh phản chiếu qua gương). **Không tạo box và không bật `can_review`.**
* **Nhóm B — `can_review = true` (Ca biên cần chốt ở Pha 2):** Phương tiện giao thông có động cơ thực tế nhưng nằm ở ranh giới giữa các lớp trong taxonomy hiện tại (xe buýt cỡ lớn, xe ba bánh tuk-tuk, xe bán tải gắn nắp thùng cao). **Tạo box theo lớp gần nhất, bật `can_review = true` và ghi lại image ID + lý do để thống nhất trong buổi họp Pha 2.**
* Không dùng `can_review` để thay thế cho một quy tắc đã rõ ràng ở Nhóm A.

### Bảng tổng hợp các ca khó thực tế trong bộ 40 ảnh

| Ảnh | Tình huống thực tế | Nhóm / Rule ID | Quyết định thao tác | Lý do |
|---|---|---|---|---|
| `img_002.jpg` | Xe tải chở 8 ô tô con trên hai sàn | Quy tắc chuẩn (Mục 3.6) | 1 box `truck` + tối đa 8 box `car` riêng biệt | Phương tiện vận chuyển và phương tiện được chở là các object độc lập, không gộp chung |
| `img_003.jpg` | Người gánh hàng rong (thúng trái cây treo thấp) + người dắt xe đạp | Nhóm A & Quy tắc (Mục 3.4, 3.5) | Vẽ `person` ôm sát cơ thể người và nón lá; **bỏ qua** thúng hàng và chiếc xe đạp | Thúng hàng làm méo tỷ lệ `person` (gây lỗi `sai_vi_tri_kich_thuoc`); xe đạp ngoài taxonomy |
| `img_004.jpg`, `img_035.jpg` | Xe ba bánh có động cơ (tuk-tuk) | Nhóm B — `can_review` (Mục 2.1) | Vẽ box tạm (gán `motorcycle` hoặc `car`), bật `can_review = true` | Phương tiện cơ giới 3 bánh nằm giữa `motorcycle` và `car`/`truck`, cần chốt quy tắc nhóm |
| `img_006.jpg`, `img_029.jpg`, `img_039.jpg` | Xe đạp và xe xích lô không động cơ | Nhóm A — `exclude` (Mục 2.1, 3.4) | Chỉ vẽ box `person` (nếu có người lái/dắt), **không** vẽ box cho xe | Ngoài phạm vi phương tiện cơ giới của taxonomy |
| `img_009.jpg`, `img_037.jpg` | Xe buýt cỡ lớn | Nhóm B — `can_review` (Mục 2.1) | Vẽ box tạm (gán `van` hoặc `truck`), bật `can_review = true` | Taxonomy hiện tại chưa có lớp `bus`, cần chốt cách ánh xạ tại Pha 2 |
| `img_037.jpg` | Xe bán tải gắn nắp thùng cao (Master 75) | Nhóm B — `can_review` (Mục 2.1) | Vẽ box tạm (gán `car`), bật `can_review = true` | Ca biên hình dáng dễ nhầm giữa `car` (bán tải gốc), `van` (thùng kín) và `truck` |
| `img_011.jpg`, `img_017.jpg`, `img_027.jpg` | Tượng đồng/tượng đá hình người và tượng xe bán tải | Nhóm A — `exclude` (Mục 3.8) | Không annotate (bỏ qua hoàn toàn) | Phản ví dụ vật thể điêu khắc tĩnh, tránh lỗi `thua` |
| `img_018.jpg` | Chân dung người in trên biển quảng cáo | Nhóm A — `exclude` (Mục 3.8) | Không annotate (bỏ qua hoàn toàn) | Hình ảnh 2D trên biển hiệu, tránh lỗi `thua` |
| `img_020.jpg` | Ô tô con và thân xe phản chiếu qua gương chiếu hậu | Nhóm A — `exclude` (Mục 3.8) | Không annotate (bỏ qua hoàn toàn) | Ảnh ảo phản chiếu trên mặt gương, không phải vật thể vật lý trực tiếp |
| `img_033.jpg`, `img_038.jpg` | Ma-nơ-canh và xe mô hình đồ chơi trong tủ kính | Nhóm A — `exclude` (Mục 3.8) | Không annotate (bỏ qua hoàn toàn) | Vật thể mô phỏng kích thước/chất liệu giả trong cửa hàng |

## 5. QC và phiên bản

### 5.1. Danh mục mã lỗi QC chuẩn (đồng bộ `qc_review.csv`)

Khi tự kiểm tra và khi reviewer chấm điểm trong file `qc_review.csv`, hệ thống sử dụng 5 mã lỗi chính và 1 trạng thái sạch:

| Mã `error_type` | Loại lỗi | Mô tả & Ví dụ áp dụng trên bộ 40 ảnh |
|---|---|---|
| `bo_sot` | Bỏ sót (False Negative) | Vật thật hợp lệ thuộc 5 class nhưng không có box (ví dụ: bỏ sót các xe `car` nằm trên sàn xe chở xe ở `img_002.jpg`). Khi ghi phiếu QC để trống `object_id` và ghi vùng `region`. |
| `thua` | Thừa (False Positive) | Gán box lên đối tượng thuộc Nhóm A (`exclude` như tượng ở `img_011.jpg`/`img_027.jpg`, ảnh phản chiếu qua gương ở `img_020.jpg`, biển quảng cáo ở `img_018.jpg`, ma-nơ-canh/đồ chơi ở `img_033.jpg`/`img_038.jpg`, xe đạp) hoặc chi tiết bị che $>70\%$ không đủ nhận diện. |
| `sai_lop` | Sai lớp (Wrong Class) | Gán nhầm class cho đối tượng (ví dụ: xe con `car` gán thành `truck` hoặc `van`, hoặc nhầm người với xe). |
| `sai_vi_tri_kich_thuoc` | Sai vị trí, kích thước | Box vẽ lỏng (bao cả đòn gánh/thúng hàng rong ở `img_003.jpg` hoặc chứa nhiều nền làm $\text{IoU} < 0.85$), box quá chặt cắt mất đuôi xe/nón lá, hoặc gộp chung người và xe máy thành 1 box. |
| `sai_thuoc_tinh` | Sai thuộc tính | Gán sai mức `occluded_level` (`1–30%`, `31–70%`, `>70%`), quên bật `truncated = yes` ở biên ảnh, hoặc quên bật `can_review = true` cho các ca biên Nhóm B (`img_004.jpg`, `img_009.jpg`, `img_035.jpg`, `img_037.jpg`). |
| `khong` | Không lỗi | Ảnh đã được duyệt toàn bộ đối tượng và sạch lỗi. |

*(Lưu ý: Một ảnh có thể phát sinh nhiều lỗi khác nhau; mỗi lỗi được ghi thành một dòng độc lập theo quy định của `scripts/README.md`).*

### 5.2. Ngưỡng nghiệm thu, Quy trình QC & Quy chuẩn nộp bài

* **Các ngưỡng đo định lượng bắt buộc của lab (`docs/QC_CHEATSHEET.md`):**
  * **Độ phủ (Coverage):** Phải đạt đủ **$100\%$** lượt gán hợp lệ trên tổng lượt trong `assignment.csv` trước khi đo IAA.
  * **Đồng thuận giữa người gán (IAA):** Tính trên các cặp box ghép 1–1 ($\text{IoU ghép} \ge 0.5$); yêu cầu đạt **$\text{IoU trung bình} \ge 0.85$** và **tỷ lệ cùng lớp $\ge 95\%$**. Bắt buộc lưu giữ chỉ số IAA **trước** calibration trong hồ sơ.
  * **Tỷ lệ lỗi theo ảnh:** Yêu cầu **$\le 2\%$** số ảnh đã duyệt mới đạt chuẩn **Release** (với lô 40 ảnh thực hành, chỉ cần **1 ảnh lỗi = $2.5\%$** là đã vượt ngưỡng và phải xử lý lại).
  * **Cách ghi số đo:** Luôn ghi đầy đủ dạng `tử số/mẫu số` (ghi `N/A` nếu không có cặp box ghép).
* **Cây quyết định xử lý lô dữ liệu (`Hold` $\rightarrow$ `Rework` $\rightarrow$ `Release`):**
  1. **Hold:** Tạm dừng bàn giao nếu thiếu bằng chứng đo lường, guideline/dữ liệu còn điểm mơ hồ chưa calibration, review lệch phiên bản, hoặc mới chỉ kiểm tra lấy mẫu (vòng demo luôn ở trạng thái **Hold**).
  2. **Rework:** Bắt buộc làm lại nếu tỷ lệ ảnh lỗi **$> 2\%$** hoặc phát hiện **lỗi hệ thống lặp lại cùng một kiểu** (dù số lượng ít). Khi Rework phải ghi rõ nguyên nhân (nếu do quy tắc mơ hồ thì sửa guideline; nếu do cá nhân lệch thì hướng dẫn lại; nếu cùng hiểu sai thì đối chiếu ca tham chiếu), người sửa và kết quả kiểm lại.
  3. **Release:** Chỉ xác nhận bàn giao khi reviewer duyệt toàn bộ lô 40 ảnh và mọi chỉ số đạt chuẩn.
* **Quy chuẩn lưu trữ Pha 1:**
  * File cá nhân lưu tại đường dẫn: `submission/guidelines/individual/guideline_138.md`.
  * Giữ nguyên bản cá nhân này sau khi gửi cho coach/nhóm trưởng để đối chiếu với bản hợp nhất ở Pha 2 (đảm bảo vượt qua kiểm tra mã băm SHA-256 của `check_submission.py` so với `guideline_v0_starter.md`).

### 5.3. Lịch sử phiên bản

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| v0 | Guideline khởi đầu (`guideline_v0_starter.md`) do giảng viên cung cấp | Bản ban đầu, định nghĩa sơ lược 5 lớp và dùng mô tả định tính ("che ít", "che nhiều"), còn thiếu quy tắc xử lý ca khó |
| v0.1 | Bổ sung quy tắc BBox, thuộc tính, che khuất, cắt mép ảnh, người đi xe máy và các trường hợp loại trừ cơ bản | Làm rõ các điểm mơ hồ nền tảng trước khi khảo sát sâu bộ dữ liệu |
| v1.0 (138) | Chốt ngưỡng định lượng `occluded_level` (`1–30%`, `31–70%`, `>70%`); tách bạch Nhóm A (`exclude`) và Nhóm B (`can_review = true`); bổ sung bảng kiểm chứng các ca thực tế (`img_002` đến `img_039`) | Hoàn thiện bản khảo sát độc lập cá nhân Pha 1 |
| v1.1 (138) | Đồng bộ 100% với `docs/QC_CHEATSHEET.md`: chốt ngưỡng vật nhỏ `< 20 px` (`ignore_region`), chuẩn $\text{IoU} \ge 0.85$ / $0.70$, chuyển mã lỗi sang 5 `error_type` của `qc_review.csv` (`bo_sot`, `thua`, `sai_lop`, `sai_vi_tri_kich_thuoc`, `sai_thuoc_tinh`) và tích hợp cây quyết định `Hold -> Rework -> Release` | Đảm bảo guideline cá nhân khớp hoàn toàn với hệ thống chấm điểm và nghiệm thu tự động của lab |