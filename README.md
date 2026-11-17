# Day07 — DucTungBao — L2

**Trạng thái hiện tại: Hold — vòng QC 2.** Kết luận Release vòng 1 đã được thay vì phát hiện lỗi nhãn và hồ sơ checksum. Link repo nộp bài giữ nguyên.

- Thành viên: 178, 144, 138; đủ 80/80 lượt gán độc lập trên 40 ảnh.
- IAA: 268 cặp, IoU 0,882; cùng lớp 96,6%. Không phải ground truth accuracy.
- Nhãn làm việc sau sửa: 450 annotations; còn ca review, chưa đủ điều kiện Release.
- QC vòng 2: có kết quả 9/40 ảnh, 4 ảnh lỗi; 31 ảnh chưa kết luận. Chi tiết và phạm vi trong [QC_REPORT.md](submission/qc/QC_REPORT.md).
- Giữ nguyên [vòng 1 của 144](submission/qc/reviews/round-01/) và [vòng 2](submission/qc/reviews/round-02/) để truy vết.
- [Lịch sử sửa box](submission/qc/calibration_applied.csv), [ca còn kiểm](submission/qc/review_triage.csv), [nhãn hiện tại](submission/qc/labels_calibrated.json).

Kiểm tra bản hiện tại:

```powershell
$env:PYTHONUTF8 = "1"
python scripts/validate_labels.py --all
python scripts/check_submission.py --round 2
python -m unittest discover -s tests -v
```

Kiểm tra cấu trúc thành công không có nghĩa nhãn đạt Release. Vòng 2 có trợ lý hỗ trợ theo ủy quyền 178; không ghi thành review mới của 144. Theo SUBMISSION.md, có thể bàn giao bằng chứng Hold để coach xem.

---

**Nhóm 2–5 người · 4 giờ · 40 ảnh đường phố · gán box bằng CVAT**

Bạn nhận một guideline **sơ sài** và 40 ảnh chứa nhiều tình huống mà nó không nói tới.
Nhóm **viết lại guideline cho đủ dùng**, gán nhãn độc lập, đo độ đồng thuận, họp calibration,
rồi bàn giao nhãn kèm quyết định **Release / Hold / Rework**.

![Mẫu ảnh trong bộ dữ liệu](docs/assets/sample_grid.jpg)

*Tuk-tuk, xe chở xe, tượng, xe giả tưởng, tượng pickup, ma-nơ-canh… Guideline của bạn phải xử lý được chúng.*

## Quy trình

```mermaid
flowchart LR
  A[1. Guideline<br/>cá nhân] --> B[2. Thống nhất<br/>guideline]
  B --> C[3. Chia ảnh<br/>và gán nhãn]
  C --> D[4. So sánh<br/>đo IAA]
  D --> E[5. Calibration]
  E --> F[6. QC<br/>và bàn giao]
```

Trọng tâm là **guideline**: nhãn chỉ tốt khi mọi người hiểu quy tắc giống nhau.

## Bắt đầu

1. Clone [repo lab](https://github.com/VinUni-AI20k/K5-L23-Day07-Guideline-Taxonomy-QC). Nộp bài bằng repo riêng tư hoặc gói nén theo hướng dẫn của coach.
2. Cài Python 3.9+ và `python -m pip install -r requirements.txt`. Dùng tài khoản CVAT của lớp.
3. Mỗi người nhận một **mã thành viên** ba chữ số (ví dụ `101`). Đọc **[GUIDE.md](GUIDE.md)** rồi **[RULES.md](RULES.md)**.

## Tài liệu

| Bạn cần | Xem |
|---|---|
| Các pha làm việc và lệnh | [GUIDE.md](GUIDE.md) |
| Mốc tiến độ 4 giờ | [CHECKPOINTS.md](CHECKPOINTS.md) |
| Quy tắc làm bài | [RULES.md](RULES.md) |
| Chấm điểm (100 điểm) | [RUBRIC.md](RUBRIC.md) |
| Gói phải nộp, cách nộp, checklist | [SUBMISSION.md](SUBMISSION.md) |
| Thông tin nhóm, kết quả tóm tắt | [TEAM.md](TEAM.md) |
| Dùng CVAT và COCO | [docs/CVAT_SETUP.md](docs/CVAT_SETUP.md) |
| Công thức, ngưỡng, cây quyết định QC | [docs/QC_CHEATSHEET.md](docs/QC_CHEATSHEET.md) |
| Mẫu báo cáo QC, ghi chú cá nhân | [docs/QC_REPORT_TEMPLATE.md](docs/QC_REPORT_TEMPLATE.md), [docs/INDIVIDUAL_NOTE_TEMPLATE.md](docs/INDIVIDUAL_NOTE_TEMPLATE.md) |
| Các lệnh và file đầu ra | [scripts/README.md](scripts/README.md) |
| Guideline khởi đầu (v0), khung viết guideline | [guideline/](guideline/) |
| Nguồn và giấy phép ảnh | [data/README.md](data/README.md) |
| **Coach:** chuẩn bị lớp, ma trận kiểm thử | [docs/COACH_GUIDE.md](docs/COACH_GUIDE.md), [docs/TEST_MATRIX.md](docs/TEST_MATRIX.md) |
