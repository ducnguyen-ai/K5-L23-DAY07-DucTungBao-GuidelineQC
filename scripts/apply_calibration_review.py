"""Apply the recorded Day07 image review without editing independent labels.

Run after qc_compare.py. Source hashes prevent applying index-based edits to a
new annotation export. Decisions retain pending cases; this is not a Release.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
from calibration import DECISION_COLUMNS, calibration_export_path, calibration_scope, require_iaa
from common import (ROOT, QC_DIR, FINAL_GUIDELINE_PATH, GUIDELINE_PATH, load_taxonomy,
                    make_ann, build_coco, digest, read_csv, write_csv)


def main():
    require_iaa()
    patch = json.loads((QC_DIR / 'calibration_patch.json').read_text(encoding='utf-8'))
    sets = {}
    for member, expected in patch['input_sha256'].items():
        source = ROOT / 'submission/labels' / f'{member}.json'
        if digest(source) != expected:
            raise ValueError(f'Input changed: {member}; review the patch again before applying.')
        sets[member] = json.loads(source.read_text(encoding='utf-8'))
    selected = {}
    for member in ['178', '138', '144']:
        data = sets[member]
        for im in data['images']:
            name = Path(im['file_name']).name
            if name not in selected:
                selected[name] = (member, im, [a for a in data['annotations'] if a['image_id'] == im['id']])
    if set(selected) != set(patch['images']):
        raise ValueError('Patch must explicitly cover every image.')
    tax = load_taxonomy()
    images, annotations, log = [], [], []
    for iid, (name, (member, im, source_anns)) in enumerate(sorted(selected.items()), 1):
        rule = patch['images'][name]
        if member != rule['source']:
            raise ValueError(f'Source changed for {name}.')
        cats = {c['id']: c['name'] for c in sets[member]['categories']}
        images.append(dict(id=iid, file_name=name, width=im['width'], height=im['height']))
        for index, original in enumerate(source_anns, 1):
            if index in rule['delete']:
                log.append(dict(image=name, source=member, source_id=original['id'], action='delete', final_id='', reason=rule['note']))
                continue
            a = copy.deepcopy(original)
            update = rule['update'].get(str(index), {})
            cls = update.get('class', cats[a['category_id']])
            box = update.get('bbox', a['bbox'])
            attrs = {n: tax.norm_attr(n, a.get('attributes', {}).get(n)) for n in tax.attrs}
            # Retain uncertainty on unclosed images; never clear flags merely to pass QC.
            attrs.update({n: tax.norm_attr(n, update[n]) for n in tax.attrs if n in update})
            attrs['can_review'] = 'false' if rule['resolved_first_pass'] else 'true'
            x,y,w,h = box
            if not (0 <= x < x+w <= im['width'] and 0 <= y < y+h <= im['height']):
                raise ValueError(f'Invalid bbox: {name} #{index}')
            ann = make_ann(tax,len(annotations)+1,iid,cls,(x,y,x+w,y+h),attrs)
            annotations.append(ann)
            log.append(dict(image=name, source=member, source_id=original['id'], action='update' if update else 'retain', final_id=ann['id'], reason=rule['note']))
        for extra in rule['add']:
            x,y,w,h = extra['bbox']
            attrs = {n: tax.default(n) for n in tax.attrs}
            attrs.update(occluded_level=extra['occluded_level'],truncated=extra['truncated'],can_review='false' if rule['resolved_first_pass'] else 'true')
            ann = make_ann(tax,len(annotations)+1,iid,extra['class'],(x,y,x+w,y+h),attrs)
            annotations.append(ann)
            log.append(dict(image=name, source='new', source_id='', action='add', final_id=ann['id'], reason=rule['note']))
    final_review = patch.get('final_review', {})
    final_ready = final_review.get('status') == 'reviewed' and all(v['resolved_first_pass'] for v in patch['images'].values())
    # Existing R-14/R-16 already require review for evidence-poor display objects.
    # This version makes the image decisions explicit without adding classes/rules.
    guideline = GUIDELINE_PATH.read_text(encoding='utf-8')
    guideline = guideline.replace('# Guideline gán nhãn — v1.0 — Nhóm DucTungBao', '# Guideline sau calibration — v1.1 — Nhóm DucTungBao', 1)
    guideline = guideline.replace('- Phiên bản: v1.0, đã chốt.', '- Phiên bản áp dụng: v1.1; giữ nguyên phạm vi và taxonomy v1.0.', 1)
    guideline = guideline.replace('- Trạng thái: nhóm đã duyệt guideline chung, theo xác nhận của 178 ngày 16/11/2026.', '- Trạng thái: bản v1.0 đã được nhóm duyệt; phần calibration v1.1 dưới đây là lượt rà theo ủy quyền 178, còn các ca Hold. Chưa có xác nhận review QC của 144.', 1)
    guideline += '\n\n## 6. Calibration ngày 17/11/2026\n\n'
    guideline += 'Giữ nguyên R-01–R-16, taxonomy và mọi ngưỡng. Không lấy đồng thuận làm ground truth. Quyết định từng ảnh và ID nhãn sửa truy vết trong calibration_patch.json và calibration_applied.csv. Các dòng IAA cùng ảnh được liên kết tới quyết định ảnh; liên kết này không có nghĩa đã giải quyết hết mọi box trong ảnh.\n\n'
    guideline += 'Thực hiện: trợ lý theo ủy quyền 178. Người phụ trách chốt: 178; người được phân công QC độc lập: 144, chưa xác nhận hoàn tất. Bản này dùng để bàn giao có điều kiện Hold.\n\n'
    for name, rule in sorted(patch['images'].items()):
        state='đã rà lượt đầu, chờ QC độc lập' if rule['resolved_first_pass'] else 'còn review, giữ can_review'
        guideline += f'- `{name}` ({state}): {rule["note"]}\n'
    if final_ready:
        guideline = guideline.replace('còn các ca Hold. Chưa có xác nhận review QC của 144.', 'đã sửa và kiểm lại các ca mở; xác nhận 31 ảnh của 178 được ghi tại calibration_patch.json. Không phải review mới của 144.')
        guideline = guideline.replace('Bản này dùng để bàn giao có điều kiện Hold.', 'Bản này được đưa vào vòng QC cuối; quyết định dùng kết quả qc_report.py.')
        guideline = guideline.replace('đã rà lượt đầu, chờ QC độc lập', 'đã kiểm theo bằng chứng vòng cuối')
        guideline += '\nCơ sở kiểm cuối: ' + final_review['basis'] + '\n'
    FINAL_GUIDELINE_PATH.write_text(guideline+'\n',encoding='utf-8')
    (ROOT/'submission/guideline_change.json').write_text(json.dumps({'kind':'editorial','summary':'Làm rõ cách áp dụng các rule v1.0 trên 40 ảnh; giữ taxonomy và ngưỡng. Các ca chưa giải quyết được ghi Hold, không đổi nghĩa để loại khó khăn.','actor':patch['actor'],'pending_images':[n for n,v in patch['images'].items() if not v['resolved_first_pass']]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    decisions=[]
    for case in read_csv(QC_DIR/'calibration_candidates.csv'):
        name=case['image'];rule=patch['images'][name]
        decisions.append(dict(case_id=case['case_id'],image=name,quyet_dinh=('Giữ quyết định ảnh sau rà lượt đầu. ' if rule['resolved_first_pass'] else 'Chưa đóng toàn bộ bất đồng; giữ cờ review/Hold. ')+rule['note'],quy_tac_ghi_vao_guideline=patch['rules'],phien_ban_guideline='v1.1',nguoi_chot=patch['actor'],phieu_sua='submission/qc/calibration_applied.csv#'+name,kiem_lai=final_review['basis'] if final_ready else 'Đã đối chiếu ảnh lượt đầu; chưa phải QC độc lập của 144.',pham_vi='lo'))
    write_csv(QC_DIR/'calibration_decisions.csv',DECISION_COLUMNS,decisions)
    write_csv(QC_DIR/'calibration_applied.csv',['image','source','source_id','action','final_id','reason'],log)
    _,_,scope,_=calibration_scope()
    target=calibration_export_path(scope)
    data=build_coco(tax,images,annotations,{'description':'Calibration reviewed handoff' if final_ready else 'Calibration working handoff; HOLD pending independent QC','actor':patch['actor']})
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(images)} images, {len(annotations)} annotations; {len(decisions)} IAA cases linked (pending cases explicitly retained).')
    print(target)

if __name__ == '__main__':
    main()
