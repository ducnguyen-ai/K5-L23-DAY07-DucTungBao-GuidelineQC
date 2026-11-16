# Guideline gán nhãn — v0.1-draft — 144

- Phiên bản: v0.1-draft
- Ngày: 2026-11-16
- Người viết: 144 (Lớp L2)

## 1. Mục tiêu
Tập dữ liệu bounding box 2D phục vụ huấn luyện và kiểm thử mô hình phát hiện đối tượng đa lớp trong môi trường giao thông đô thị phức tạp (ADAS / Xe tự hành / Camera giám sát). Lỗi phân loại sai người thành chướng ngại vật tĩnh hoặc bỏ sót phương tiện di chuyển có thể gây ra tai nạn thảm khốc.

## 2. Lớp và thuộc tính

### Lớp
| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con chở người dưới 9 chỗ ngồi (sedan, SUV, hatchback, coupe). | Xe sedan chở khách `img_015.jpg`, wagon `img_024.jpg` | Không gán xe bán tải thùng rời (xếp vào `truck`); không gán mô hình xe đồ chơi trong tủ kính `img_038.jpg`. |
| `truck` | Phương tiện chuyên dụng chở hàng có cabin và thùng tải tách biệt, xe bán tải (pickup), hoặc đầu kéo container. | Xe chở ô tô `img_002.jpg`, xe bán tải `img_001.jpg`, `img_012.jpg`, xe tải nhẹ Kaifeng `img_036.jpg` | Xe van chở khách nguyên khối (xếp vào `van`). |
| `van` | Xe thùng kín nguyên khối cỡ nhỏ hoặc vừa chở người/hàng (như Ford Transit, minivan). | Xe van bưu chính, xe minivan gia đình | Xe SUV lớn (xếp `car`), xe tải cabin rời (xếp `truck`). |
| `bus` | Phương tiện giao thông công cộng chở khách cỡ lớn có trên 16 chỗ ngồi. | Xe buýt nội đô `img_009.jpg`, `img_031.jpg`, `img_040.jpg` | Xe van 12 chỗ cỡ nhỏ. |
| `tuk_tuk` | Xe ba bánh có động cơ dùng để chở khách hoặc chở hàng (auto-rickshaw, tuk-tuk). | Xe tuk-tuk Thái Lan `img_004.jpg`, auto-rickshaw `img_035.jpg` | Xe xích lô đạp chân (không có động cơ cơ giới). |
| `motorcycle` | Xe máy hai bánh có động cơ, xe gắn máy, xe mô tô phân khối lớn. | Xe máy lưu thông `img_005.jpg`, `img_026.jpg` | Xe đạp thô sơ hoặc xe xích lô. |
| `person` | Con người thực tế còn sống (người đi bộ, người lái xe, hành khách ngồi trên xe). | Người đi bộ `img_001.jpg`, người cưỡi xe máy `img_005.jpg` | Tượng đá/đồng `img_017.jpg`, ma-nơ-canh `img_033.jpg`, hình in áp phích `img_018.jpg`. |
| `ignore_region` | Vùng không cần gán nhãn chi tiết từng vật thể đơn lẻ (đám đông quá dày đặc, cụm vật thể nhỏ phía xa). | Đám đông khách bộ hành phía xa `img_025.jpg` | Đối tượng đơn lẻ rõ nét ở tiền cảnh. |

Vật thể ngoài taxonomy (xe đạp không động cơ, xe xích lô, động vật, rào chắn): không gán box, trừ khi tạo thành cụm gây nhiễu thì khoanh `ignore_region`.

### Thuộc tính
| Thuộc tính | Kiểu | Các mức cố định | Ý nghĩa và ngưỡng định lượng |
|---|---|---|---|
| `occluded_level` | select | `0`, `1`, `2`, `3` | Mức độ bị che khuất diện tích nhìn thấy:<br>- `0`: Thấy rõ hoàn toàn, bị che khuất < 10% diện tích.<br>- `1`: Bị che khuất ít, từ 10% đến 35% diện tích.<br>- `2`: Bị che khuất vừa, từ 36% đến 70% diện tích.<br>- `3`: Bị che khuất nặng, > 70% diện tích nhưng vẫn nhận diện được. |
| `truncated` | select | `no`, `yes` | Vật thể bị cắt đứt bởi mép khung ảnh:<br>- `no`: Toàn bộ vật thể nằm trong biên ảnh.<br>- `yes`: Một phần vật thể bị cắt bởi rìa mép ảnh. |
| `can_review` | checkbox | `false`, `true` | Cờ đánh dấu tình huống biên cần xem lại (bật `true` khi còn phân vân). |

## 3. Quy tắc vẽ box
1. **Ôm sát phần nhìn thấy (R-01)**: Box bao khít các pixel biên ngoài cùng của phần vật thể nhìn thấy được. Tuyệt đối không ước lượng phần thân xe bị chìm dưới lòng đường hoặc khuất sau tường.
2. **Người đi xe máy (R-02)**: Luôn tách thành 2 box độc lập: 1 box `person` cho cơ thể người điều khiển/người ngồi sau và 1 box `motorcycle` cho toàn bộ thân xe máy.
3. **Xe chở xe (R-03)**: Với xe tải chuyên dụng chở ô tô con (`img_002.jpg`), gán 1 box `truck` cho xe tải mẹ và gán riêng từng box `car` cho các xe con được chở trên sàn nếu nhìn thấy rõ.
4. **Vật thể không thật (R-04)**: Tượng nghệ thuật (`img_017.jpg`, `img_027.jpg`), ma-nơ-canh trưng bày (`img_033.jpg`), đồ chơi mô hình (`img_038.jpg`), hình in áp phích (`img_018.jpg`) và ảnh phản chiếu qua gương (`img_020.jpg`) KHÔNG được gán nhãn đối tượng thật. Các ảnh chỉ chứa các vật thể này được giữ nguyên trong COCO với 0 annotation.
5. **Vật nhỏ và ngưỡng cắt (R-05)**: Vật thể có chiều cao dưới 20 pixel không gán box đơn lẻ; nếu nằm trong cụm đông đúc thì khoanh vùng `ignore_region`.
6. **Xe bán tải / Pickup (R-06)**: Xe bán tải (dù thùng hở hay có nắp thùng như `img_001.jpg`, `img_012.jpg`, `img_037.jpg`) thống nhất xếp vào lớp `truck`.

## 4. Ca khó
| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_002.jpg` | Xe tải chở 8 ô tô con trên hai tầng giá đỡ | R-03 | Gán 1 box `truck` và 8 box `car` | Các xe con là thực thể giao thông độc lập cần nhận diện tránh va chạm. |
| `img_017.jpg` | Tượng công tước Wellington cưỡi ngựa bằng đồng | R-04 | Không gán box `person` (0 annotation) | Tượng đồng là chướng ngại tĩnh kiến trúc, không phải người thật. |
| `img_027.jpg` | Bia mộ hình xe bán tải khắc bằng đá | R-04 | Không gán box `truck` (0 annotation) | Bia mộ đá không phải phương tiện vận hành. |
| `img_033.jpg` | Ma-nơ-canh trong tủ kính cửa hàng | R-04 | Không gán box `person` | Ma-nơ-canh nhựa/sáp không phải người. |
| `img_035.jpg` | Xe auto-rickshaw chở bao tải cao ngất ngưởng | R-07 | Box `tuk_tuk` chỉ ôm thân xe, không ôm bao tải | Đảm bảo tính nhất quán về hình học và đặc trưng xe 3 bánh. |
| `img_037.jpg` | Xe bán tải gắn nắp thùng cao Master 75 | R-06 | Gán `truck` | Xe bán tải giữ nguyên lớp `truck` dù có nắp thùng. |

## 5. QC và phiên bản
| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0.1-draft | Khởi tạo từ khảo sát 40 ảnh: đề xuất bổ sung bus, tuk_tuk, quy tắc xe chở xe, quy tắc loại bỏ tượng | Khắc phục các thiếu sót của guideline v0 starter. |
