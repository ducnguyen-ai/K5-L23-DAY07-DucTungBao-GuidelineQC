# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 3
- Lượt gán đủ **80/80**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 268 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 268 | 0.882 | 96.6% | 33.2% | 88.4% | 48/191 | 0 | ĐẠT |
| 138 / 144 | 13 | 84 | 0.827 | 98.8% | 42.9% | 94.0% | 27/30 | 0 | CHƯA ĐẠT |
| 138 / 178 | 13 | 133 | 0.930 | 100.0% | 22.6% | 85.7% | 2/94 | 0 | ĐẠT |
| 144 / 178 | 14 | 51 | 0.849 | 84.3% | 45.1% | 86.3% | 19/67 | 0 | CHƯA ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 837 ({'sai_thuoc_tinh': 192, 'bo_sot_thua': 239, 'co_can_review': 337, 'iou_thap': 60, 'sai_lop': 9}), trên 34 ảnh cần calibration.
