#!/usr/bin/env python3
"""Tự kiểm bài nộp trước khi push lần cuối (giảng viên cũng dùng để chấm sơ bộ).

    python scripts/check_submission.py

Kiểm: tiêu đề README có đủ MSHV - Họ tên, guideline cá nhân của mọi thành viên,
guideline thống nhất, nhãn từng người, các file CSV/JSON của calibration, báo cáo QC,
và (nếu có git) mọi thành viên đều có commit.
Chỉ kiểm CÓ/ĐỦ, không chấm chất lượng nội dung.
"""
from __future__ import annotations

import csv
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUB = ROOT / "submission"
errs, warns = [], []
DEFAULT_RULES = {"min_box_height_px": 20, "iou_thr_large": 0.85, "iou_thr_small": 0.7, "large_px": 50,
                 "iaa_iou": 0.85, "iaa_class": 0.95, "error_rate_img_max": 0.02, "match_iou": 0.5}


def err(m): errs.append(m)
def warn(m): warns.append(m)


def members() -> list:
    p = SUB / "qc" / "assignment.csv"
    if not p.exists():
        err("Thiếu submission/qc/assignment.csv (chạy scripts/split_assign.py).")
        return []
    ids = set()
    with p.open(encoding="utf8") as f:
        for r in csv.DictReader(f):
            ids.update(x for x in r["annotators"].split("|") if x)
    return sorted(ids)


def readme_has_member(title: str, member: str) -> bool:
    """Cho phép mã 3 chữ số khớp duy nhất đuôi MSHV đầy đủ trên README.

    Nhóm DucTung dùng 178/144 trong assignment, giữ 2A202603xxx ở tiêu đề.
    Không thay đổi yêu cầu có nhãn, guideline hay bất kỳ ngưỡng QC nào.
    """
    ids = re.findall(r"(?<![A-Za-z0-9_])([A-Za-z0-9]+)\s*-\s*\S", title)
    matches = [sid for sid in ids if sid == member or
               (len(member) == 3 and member.isdigit() and len(sid) > 3
                and sid.endswith(member))]
    return len(matches) == 1


def main() -> int:
    team = members()
    print(f"Thành viên (theo assignment.csv): {', '.join(team) or '(chưa có)'}")

    # README
    rd = ROOT / "README.md"
    title = ""
    if rd.exists():
        for line in rd.read_text(encoding="utf8").splitlines():
            if line.startswith("# "):
                title = line
                break
    if not title:
        err("README.md không có dòng tiêu đề `# ...`.")
    else:
        if "<" in title and ">" in title:
            err("Tiêu đề README còn placeholder `<...>`: hãy điền tên nhóm và danh sách MSHV - Họ tên.")
        for m in team:
            if not readme_has_member(title, m):
                err(f"Tiêu đề README thiếu `{m} - Họ và tên`.")

    # guideline cá nhân
    ind = SUB / "guidelines" / "individual"
    v0 = hashlib.md5((ROOT / "guideline" / "guideline_v0_starter.md").read_bytes()).hexdigest()
    for m in team:
        fs = list(ind.glob(f"guideline_{m}_*.md"))
        if not fs:
            err(f"Thiếu guideline cá nhân của {m}: submission/guidelines/individual/guideline_{m}_<HoTen>.md")
        elif hashlib.md5(fs[0].read_bytes()).hexdigest() == v0:
            err(f"Guideline của {m} giống hệt bản v0 (chưa sửa gì).")
    agreed = SUB / "guidelines" / "guideline_v1.0_agreed.md"
    if not agreed.exists():
        err("Thiếu submission/guidelines/guideline_v1.0_agreed.md")
    elif hashlib.md5(agreed.read_bytes()).hexdigest() == v0:
        err("guideline_v1.0_agreed.md giống hệt v0.")
    if not (SUB / "guidelines" / "guideline_v1.1_calibrated.md").exists():
        warn("Chưa có guideline_v1.1_calibrated.md. Nếu calibration không đổi quy tắc nào, hãy nói rõ trong QC_REPORT.md.")

    # ghi chú cá nhân
    for m in team:
        if not list((SUB / "individual_notes").glob(f"{m}_*.md")):
            err(f"Thiếu ghi chú cá nhân của {m}: submission/individual_notes/{m}_<HoTen>.md")

    # TEAM.md
    tm = ROOT / "TEAM.md"
    if not tm.exists() or "| 1 | | |" in tm.read_text(encoding="utf8"):
        err("TEAM.md chưa điền (bảng thành viên còn trống).")

    # ngưỡng không được đổi
    try:
        import json
        rules = json.loads((SUB / "taxonomy.json").read_text(encoding="utf8")).get("rules", {})
        for k, v in DEFAULT_RULES.items():
            if rules.get(k) != v:
                err(f"taxonomy.json: rules.{k} = {rules.get(k)} (mặc định {v}). Không đổi các ngưỡng QC.")
    except Exception as e:
        err(f"Không đọc được submission/taxonomy.json: {e}")

    # nhãn
    for m in team:
        if not list((SUB / "labels").glob(f"{m}_*.json")):
            err(f"Thiếu nhãn của {m}: submission/labels/{m}_<HoTen>.json")

    # calibration + QC
    for f in ["assignment.csv", "calibration_candidates.csv", "calibration_decisions.csv",
              "labels_calibrated.json", "labels_calibrated.csv", "iaa_summary.md",
              "qc_sample.csv", "qc_review.csv", "qc_report_auto.md", "QC_REPORT.md"]:
        if not (SUB / "qc" / f).exists():
            err(f"Thiếu submission/qc/{f}")
    rep = SUB / "qc" / "QC_REPORT.md"
    if rep.exists():
        t = rep.read_text(encoding="utf8")
        if "<<" in t or "TODO" in t:
            err("QC_REPORT.md còn chỗ `<<...>>` / TODO chưa điền.")
        if not re.search(r"\b(Release|Hold|Rework)\b", t):
            err("QC_REPORT.md chưa có quyết định Release / Hold / Rework.")
    dec = SUB / "qc" / "calibration_decisions.csv"
    if dec.exists():
        with dec.open(encoding="utf8") as f:
            rows = list(csv.DictReader(f))
        if not any((r.get("quyet_dinh") or "").strip() for r in rows):
            err("calibration_decisions.csv chưa có quyết định nào.")

    # git
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "log", "--format=%an <%ae>"],
                             capture_output=True, text=True, check=True).stdout.splitlines()
        authors = sorted(set(out))
        print(f"Số tác giả commit khác nhau: {len(authors)}")
        if team and len(authors) < len(team):
            warn(f"Chỉ có {len(authors)} tác giả commit nhưng nhóm có {len(team)} người: mỗi thành viên phải có commit của mình.")
    except Exception:
        warn("Không đọc được git log (chưa `git init` / chưa commit?).")

    for w in warns:
        print("CẢNH BÁO:", w)
    for e in errs:
        print("LỖI:", e)
    print(f"\nTổng kết: {len(errs)} lỗi, {len(warns)} cảnh báo.")
    print("Script này chỉ kiểm có/đủ. Nội dung (guideline rõ không, QC đúng không) vẫn do người đọc đánh giá.")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
