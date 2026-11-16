# Day 07 Lab — Nhóm DucTung: 2A202603178 - Nguyễn Cao Ngọc Đức, 2A202603144 - Nguyễn Khánh Tùng

## Nhóm và trạng thái setup

- Repo public: https://github.com/ducnguyen-ai/DucTung
- Lớp: **L2**; nhóm **2 người**, mỗi ảnh **K = 2 người gán độc lập**.
- Nguyễn Cao Ngọc Đức: **178**, GitHub [ducnguyen-ai](https://github.com/ducnguyen-ai), email Git `26ai.ducncn@vinuni.edu.vn`.
- Nguyễn Khánh Tùng: **144**, GitHub [sfpcshch](https://github.com/sfpcshch). Tùng tự cấu hình Git bằng tên và email của mình.
- Dùng MSHV đầy đủ trên tiêu đề README; dùng **178/144** trong TEAM, assignment và tên file cá nhân.
- Đã chuẩn bị môi trường Python và chia 40 ảnh cho mỗi người. **Chưa hoàn thành guideline cá nhân, chưa chốt v1.0, chưa gán nhãn hoặc đo IAA.**

Tên repo **DucTung** theo yêu cầu của nhóm, khác mẫu `K5-L23-DAY07-[TenNhom]-GuidelineQC` trong đề; cần đối chiếu yêu cầu tên khi nộp. Fork và lịch sử đề gốc được giữ nguyên.

## Bắt đầu trên máy mỗi thành viên

```powershell
git clone https://github.com/ducnguyen-ai/DucTung.git
cd DucTung
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe scripts/split_assign.py --members 178,144 --seed 42 --copy-images
```

- Đức mở `work/178/images/`; Tùng mở `work/144/images/`. Mỗi thư mục có đúng 40 ảnh; cùng ảnh nhưng làm độc lập, không xem guideline hoặc nhãn của nhau trong Pha 1/Pha 3.
- **Việc đầu tiên:** mỗi người tự xem 40 ảnh, đọc `guideline/guideline_v0_starter.md`, dùng `guideline/TEMPLATE_guideline.md` để tự viết bản cá nhân. Chưa bắt đầu gán box.
- File Đức: `submission/guidelines/individual/guideline_178_NguyenCaoNgocDuc.md`; file Tùng: `submission/guidelines/individual/guideline_144_NguyenKhanhTung.md`.
- Sau khi mỗi người đã commit bản cá nhân, họp chốt `guideline_v1.0_agreed.md` và `submission/taxonomy.json`, rồi chạy `scripts/make_cvat_labels.py` và tạo CVAT task riêng.
- Tên task đề xuất: `Day07-DucTung-178` và `Day07-DucTung-144`. Mỗi người giữ nhãn riêng đến hết pha gán độc lập.
- Export COCO 1.0: `submission/labels/178_NguyenCaoNgocDuc.json` hoặc `submission/labels/144_NguyenKhanhTung.json`.
- Theo RULES.md, AI được hỗ trợ giải thích/script/chính tả; không gán box hoặc quyết định ca ảnh thay người làm. Không tạo kết quả QC khi chưa thực hiện.

### Tương thích ID rút gọn

`check_submission.py` được điều chỉnh riêng bước kiểm tiêu đề: chấp nhận mã 3 chữ số khi khớp duy nhất đuôi MSHV đầy đủ trên README. Lý do: TEAM/assignment dùng 178/144 nhưng README giữ 2A202603178/2A202603144 theo yêu cầu nhóm. Các kiểm tra nội dung bắt buộc, script nhãn và toàn bộ ngưỡng QC vẫn giữ nguyên. Ghi chú thay đổi này vào báo cáo QC cuối bài.

---

**Nhóm 2–5 người · 4 giờ · 40 ảnh đường phố châu Á · gán box bằng CVAT**

Bạn nhận một guideline gán nhãn **sơ sài** và 40 ảnh chứa nhiều tình huống mà nó không nói tới.
Việc của nhóm: **viết lại guideline cho đủ dùng**, chia việc, gán nhãn độc lập, đo độ đồng thuận, họp calibration,
rồi quyết định **Release / Hold / Rework** cho lô nhãn.

![Mẫu ảnh trong bộ dữ liệu](docs/assets/sample_grid.jpg)

*Có gì lạ trong ảnh? Tuk-tuk, xe chở xe, tượng, xe giả tưởng, tượng pickup, ma-nơ-canh… Guideline của bạn phải xử lý được chúng.*

## Quy trình

```mermaid
flowchart LR
  A[1. Guideline<br/>cá nhân] --> B[2. Thống nhất<br/>guideline]
  B --> C[3. Chia ảnh<br/>và gán nhãn]
  C --> D[4. So sánh<br/>đo IAA]
  D --> E[5. Calibration]
  E --> F[6. QC mẫu<br/>và báo cáo]
```

Trọng tâm là **guideline**: nhãn chỉ tốt khi mọi người hiểu quy tắc giống nhau.

## Bắt đầu

1. **Fork** repo thành repo **public** của nhóm, mời các bạn làm collaborator, mỗi người `git clone`.
2. Đọc **[GUIDE.md](GUIDE.md)** (từng pha, lệnh chạy) và **[RULES.md](RULES.md)**.
3. `pip install -r requirements.txt` (Python 3.9+).

> Tiêu đề đã điền đủ hai thành viên. Trước khi nộp, đối chiếu [SUBMISSION.md](SUBMISSION.md).

## Tài liệu

| Bạn cần | Xem |
|---|---|
| Các pha làm việc và lệnh | [GUIDE.md](GUIDE.md) |
| Mốc tiến độ 4 giờ | [CHECKPOINTS.md](CHECKPOINTS.md) |
| Quy tắc làm bài | [RULES.md](RULES.md) |
| Chấm điểm (100 điểm) | [RUBRIC.md](RUBRIC.md) |
| Sản phẩm phải nộp, tên repo, checklist | [SUBMISSION.md](SUBMISSION.md) |
| Thông tin nhóm và kết quả tóm tắt | [TEAM.md](TEAM.md) |
| Cài và dùng CVAT | [docs/CVAT_SETUP.md](docs/CVAT_SETUP.md) |
| Công thức, ngưỡng, cây quyết định QC | [docs/QC_CHEATSHEET.md](docs/QC_CHEATSHEET.md) |
| Mẫu báo cáo QC, ghi chú cá nhân | [docs/QC_REPORT_TEMPLATE.md](docs/QC_REPORT_TEMPLATE.md), [docs/INDIVIDUAL_NOTE_TEMPLATE.md](docs/INDIVIDUAL_NOTE_TEMPLATE.md) |
| Các script | [scripts/README.md](scripts/README.md) |
| Guideline khởi đầu (v0), khung viết guideline | [guideline/](guideline/) |
| Nguồn và giấy phép ảnh | [data/README.md](data/README.md), [data/ATTRIBUTION.csv](data/ATTRIBUTION.csv) |
