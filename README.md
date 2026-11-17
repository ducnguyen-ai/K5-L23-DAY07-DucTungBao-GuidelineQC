# Day 07 Lab — Nhóm DucTungBao — mã 178, 144, 138

## Setup nhóm sau khi cập nhật đề

- Repo: `K5-L23-DAY07-DucTungBao-GuidelineQC`; lớp **L2**, 3 thành viên, mỗi ảnh **K = 2 người gán độc lập**.
- Đã hoàn tất toàn bộ các Checkpoint từ CP1 đến CP6. Đã calibration 34 ảnh, xuất lô nhãn cuối 40 ảnh và hoàn thành QC Vòng 1 với kết luận **RELEASE**.
- Bản đề mới chỉ dùng mã trong tên file, Task và nhật ký. Không đưa họ tên, MSHV đầy đủ hay email vào artifact nộp; bảng đối chiếu gửi riêng qua kênh lớp.
- Fork này vẫn public. Gửi guideline/nhãn cá nhân riêng cho đến khi cả nhóm hoàn thành pha độc lập; không push sớm lên repo chung. Nộp cuối qua repo private có quyền coach hoặc ZIP qua LMS theo [SUBMISSION.md](SUBMISSION.md).
- Lịch sử fork có thông tin thành viên từ setup trước; việc sửa nội dung hiện tại không xóa lịch sử đó. Không dùng link fork public thay cho kênh nộp riêng tư mới.

## Guideline chung đã chốt

Áp dụng [guideline v1.0](submission/guidelines/guideline_v1.0_agreed.md) cho cả nhóm. [Taxonomy v1.0](submission/taxonomy.json) và [cấu hình CVAT](cvat/labels_generated.json) có 7 lớp đối tượng (`car`, `truck`, `van`, `bus`, `tuk_tuk`, `motorcycle`, `person`) cùng `ignore_region`. Ngưỡng QC giữ nguyên theo đề.

[Bản áp dụng của 178](submission/guidelines/individual/guideline_178.md) theo đủ 5 phần của mẫu. Các nguồn cá nhân 138/144 giữ nguyên để đối chiếu. Ghi chú sử dụng công cụ và tiến độ của 178 nằm trong [ghi chú cá nhân](submission/individual_notes/178.md).

## Tiến độ & Kết quả bàn giao — 17/11/2026 (RELEASE)

- [Báo cáo IAA](submission/qc/iaa_summary.md): 80/80 lượt gán hoàn thành; 268 cặp box ghép, IoU TB 0,882 (vượt ngưỡng >= 0,85), đồng thuận lớp 96,6% (vượt ngưỡng >= 95%).
- [Bảng calibration](submission/qc/calibration_decisions.csv): 837 dòng đã xử lý và chốt quyết định 100%; áp dụng bộ quy tắc R-01–R-16 và guideline v1.1; toàn bộ 337 cờ can_review đã được giải tỏa trong nhãn hiệu chỉnh.
- [Đặc tả hiệu chỉnh](submission/guideline_change.json) & [Guideline v1.1](submission/guidelines/guideline_v1.1_calibrated.md): chuẩn hóa ranh giới thuộc tính occluded_level và loại bỏ nhiễu < 20px.
- [Lô nhãn cuối](submission/qc/labels_calibrated.json) & [Manifest](submission/qc/batch_manifest.json): 40 ảnh, 507 annotations, bảo đảm đầy đủ checksum SHA-256.
- [Báo cáo QC bàn giao](submission/qc/QC_REPORT.md): **RELEASE** — Duyệt toàn bộ 40/40 ảnh trong [qc_review.csv](submission/qc/reviews/round-01/qc_review.csv), 0 ảnh lỗi (0.0% <= 2% ngưỡng đề ra), 0 vật bỏ sót.
- Kiểm định tự động: `scripts/check_submission.py --round 1` đạt **0 lỗi**; bộ kiểm thử `tests/test_workflow.py` vượt qua **22/22 unit tests**.

## Cài và tái lập phân công

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe scripts/split_assign.py --members 178,144,138 --seed 42 --copy-images
```

| Mã | Số ảnh gán | Thư mục ảnh | Guideline cá nhân | Nhãn COCO 1.0 |
|---|---:|---|---|---|
| 178 | 27 | `work/178/images/` | `guideline_178.md` | `178.json` |
| 144 | 27 | `work/144/images/` | `guideline_144.md` | `144.json` |
| 138 | 26 | `work/138/images/` | `guideline_138.md` | `138.json` |

- Pha 1: mỗi người xem đủ 40 ảnh gốc, tự viết guideline theo `guideline/TEMPLATE_guideline.md`, gửi riêng. Sau khi tất cả nộp, mới mở bản của nhau để họp.
- Pha 2: nhóm khóa `guideline_v1.0_agreed.md` và taxonomy v1.0; giữ nguyên mục `rules`; chạy `scripts/make_cvat_labels.py` trước tạo task.
- Pha 3: chỉ upload ảnh được giao theo `submission/qc/assignments/<mã>.txt`; task tên `Day07-178`, `Day07-144`, `Day07-138`. Gán độc lập, export và gửi riêng trước khi tổng hợp.
- File guideline đặt ở `submission/guidelines/individual/`; nhãn ở `submission/labels/`; ghi chú cá nhân ở `submission/individual_notes/178.md`, `144.md`, `138.md`.
- Các bước calibration, manifest và QC theo vòng dùng nguyên script mới; chưa tạo artifact đánh giá khi chưa review thật.

## Kiểm tra môi trường / script

```powershell
$env:PYTHONUTF8 = "1"
.venv/Scripts/python.exe -m unittest discover -s tests -v
```

Bộ test dùng dữ liệu tạm, không phải nhãn thực tế của nhóm. `check_submission.py --round 1` chỉ kiểm bài hoàn chỉnh khi có đầy đủ đầu vào; setup xong chưa đồng nghĩa bài đã hoàn thành.

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
