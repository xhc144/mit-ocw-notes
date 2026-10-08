#!/usr/bin/env python3
"""Resolve reviewed source decisions, verify every PDF, and freeze selection."""
import hashlib, json
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'sources/graph-theory'
SUBJECT = ROOT / 'subjects/graph-theory'
MAPPING = {
 '18315-lec01': ('Ramsey; 不含多面体刚性', [17]),
 '18315-lec03': ('超图二染色思想; 不含加法数论或凸点集版', [17]),
 '18315-lec04': ('重配置与概率二染色; 不含矩形高度函数', [6,17]),
 '18315-lec05': ('贪心与 Brooks; 不含特定相交超图界', [6]),
 '18315-lec06': ('五色与 Vizing', [7,8]),
 '18315-lec07': ('二部图边染色、Heawood 上界', [7,8]),
 '18315-lec08': ('重配置与染色界; 不含 Glauber 速度/二次直径', [6]),
 '18315-lec09': ('染色多项式、包含排除、NBC', [9]),
 '18315-lec10': ('Stanley 无圈定向与 Tutte 定义', [9]),
 '18315-lec11': ('Tutte 特殊值、活动展开', [9]),
 '18315-lec12': ('圈的多项式和树计数; 不含 Gessel 完全图活动公式', [9,13]),
 '18315-lec19': ('Hamilton 必要条件; 不含专门平面图长路径界', [4]),
 '18315-lec20': ('Grinberg、Dirac; 顶点传递图猜想不作已证结论', [4]),
 '18315-lec21': ('奇度 Hamilton 奇偶、S_n 相邻交换; Tutte 平面四连通仅提及', [4,8]),
 '18315-lec22': ('路分离与 Chvátal–Erdős; 不含三对合一般群构造', [3,17]),
 '18315-lec23': ('Menger; 不含 Gallai–Milgram 路径覆盖', [3,12]),
 '18315-lec24': ('Hall、Dilworth、Mirsky、Erdős–Szekeres', [5,17]),
 '18315-lec25': ('Sperner、Mantel、递增迹平均度', [16,17]),
 '18315-lec27': ('Turán 与随机次序独立数', [16,17]),
 '18433-l123': ('匹配/增广路; 不含花算法', [5]),
 '18433-l78': ('流、割、最短增广路; 条件与完整证明补齐', [12]),
 '18433-l9': ('最小割与随机收缩', [11]),
 '18212-mit18_212s19_lec22': ('仅 PDF4–5 页 Cayley 引入; 分拆不收入', [2]),
 '18212-mit18_212s19_lec23': ('Cayley、Prüfer、度数出现计数', [2]),
 '18212-mit18_212s19_lec26': ('Laplace 与矩阵树指定部分', [13]),
 '18212-mit18_212s19_lec27': ('矩阵树指定讨论; 非全部变体', [13]),
 '18212-mit18_212s19_lec28': ('关联矩阵/Cauchy–Binet/树子式', [13]),
 '18212-mit18_212s19_lec29': ('有向矩阵树命题; 替代完整证明', [13]),
 '18212-mit18_212s19_lec30': ('有向权树与电网络', [13,14]),
 '18212-mit18_212s19_lec31': ('Kirchhoff、电阻/二根森林、命中概率', [14]),
 '18212-mit18_212s19_lec32': ('Euler/BEST; 固定首弧约定', [4,13]),
 '18217-mit18_217f19_ch2': ('PDF1–4 Mantel/Turán, 6–8 KST, 12起仅无四圈代数构造思想', [16]),
 '18217-mit18_217f19_ch4': ('PDF1–8 指定稠密谱/扩张混合; 只证正则限制版, 不含研究级后续', [15]),
 '6042-mit6_042js15_textbook': ('PDF332–353 有向图指定理论; 402–442 简单图主干, 稳定婚姻除外; 482–501 平面图; 非图论不收入', [1,2,3,6,8,10]),
}

def main():
    target = SOURCE/'source-manifest.json'
    data = json.loads(target.read_text())
    if data.get('selection_frozen'):
        raise SystemExit('Already frozen; use verify_sources.py, not another freeze.')
    hashes = set()
    for item in data['selected_resources']:
        path = SOURCE/item['path']
        value = hashlib.sha256(path.read_bytes()).hexdigest()
        with fitz.open(path) as doc:
            pages = len(doc)
        assert value == item['sha256'] and pages == item['pages']
        assert value not in hashes
        hashes.add(value)
        scope, chapters = MAPPING[item['id']]
        item.update(archive_allowed=True, license_review='resolved',
                    scope=scope, book_chapters=chapters,
                    authors_evidence='Official course lecture directory; author metadata is secondary',
                    year_evidence='Official course semester; PDF creation/modification dates are not lecture years',
                    rights_review_method=('All 34 scanned main-source pages visually inspected; all-page OCR searched' if item['course']=='18315' else 'All-page extracted text or repaired OCR searched; official resource and course attribution checked'),
                    rights_findings='No separate restrictive notice identified; references/removed/OCR © flags are not third-party permission statements',
                    license_evidence_url='https://ocw.mit.edu/pages/privacy-and-terms-of-use/')
        if item['course'] in ['18315','18212','18217']:
            item['attribution_note'] = 'Official directory attributes student notes and says used with permission. This is preserved as provenance, not treated as an independent sublicense. No item-specific CC exclusion found; default OCW license applied.'
        if item['course']=='18315':
            item['date_discrepancy'] = 'Official Spring 2005 label retained; several handwritten pages carry September–November 2005 dates.'
        if item['course']=='6042':
            item['license']='CC BY-NC-SA 3.0 Unported, explicit PDF page 2; original notice preserved'
            item['rights_findings']='PDF page 2 names authors, revision 2015-05-18 and CC BY-NC-SA 3.0. Other removed hits describe graph operations. Full original is preserved; only selected graph content adapted.'
            item['adaptation_license']='CC BY-NC-SA 4.0, permitted later same-elements version under 3.0 legalcode section 4(b)'
            item['adaptation_license_evidence_url']='https://creativecommons.org/licenses/by-nc-sa/3.0/legalcode'
    held=json.loads(Path('/tmp/graph-2023-metadata.json').read_text())
    held.update(id='18225-author-version',course='18.225 Fall 2023',authors=['Yufei Zhao'],
                author_version_updated='2024-06-18',year=2023,archive_allowed=False,
                disposition='link_only; no PDF, OCR, pages or images retained in repository or source ZIP',
                reason='PDF page 2 explicit author copyright 2023 and Anne Ma image courtesy/permission. No assumption that a generic OCW footer overrides individual notices.',
                resource_url='https://ocw.mit.edu/courses/18-225-graph-theory-and-additive-combinatorics-fall-2023/pages/lecture-notes/')
    data.update(selection_frozen=True,frozen_on='2026-10-08',selected_count=len(hashes),
                selected_pdf_pages=sum(x['pages'] for x in data['selected_resources']),
                byte_duplicates=[],semantic_dedup='Repeated definitions and results merged in book chapters; scope maps distinguish omitted material.',
                held_resources=[held],book_language='Simplified Chinese native LaTeX; English originals only in sources archive',
                book_adaptation_license='CC BY-NC-SA 4.0',
                comparisons=[{'course':'18.314 Fall 2014','decision':'not main; graph syllabus exists but main readings use commercial textbook, only isolated supplementary handouts','url':'https://ocw.mit.edu/courses/18-314-combinatorial-analysis-fall-2014/pages/readings/'},
                             {'course':'6.042J Spring 2015','decision':'supplement only; not a specialized graph book'},
                             {'course':'18.315 Spring 2005','decision':'classical graph main; 19 selected lecture PDFs, not full course translation'},
                             {'course':'18.217 Fall 2019','decision':'selected advanced supplement only'},
                             {'course':'18.225 Fall 2023','decision':'link-only author book due individual rights notices'}])
    encoded=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    target.write_text(encoded)
    (SUBJECT/'source-manifest.json').write_text(encoded)
    rows=['# 图论逐文件来源冻结清单','', '34 份原件，共 1062 个 PDF 物理页；仅声明下表指定内容采用。下载/核查日期：2026-10-08。', '', '|文件|页数|作者与授课年|采用范围|许可|SHA-256|', '|---|---:|---|---|---|---|']
    for x in data['selected_resources']:
        rows.append(f"|[{x['id']}]({x['url']})|{x['pages']}|{'; '.join(x['authors'])}, {x['year']}|{x['scope']}|{'CC BY-NC-SA 3.0' if x['course']=='6042' else 'OCW 默认 CC BY-NC-SA 4.0'}|`{x['sha256']}`|")
    rows+=['','英文原件保持完整原许可，只作为出处档案；中文书没有英文原页。数学阅读依赖原图，OCR不是可信公式转录。', '', '[18.225 作者版书稿仅链接]('+held['url']+')：344页；2023作者版权，2024-06-18更新；有图片单独许可。已核查但不归档正文、OCR或图片。','', '18.315部分原页标9–11月，与官网Spring标签不一致；保留两类证据，不把PDF制作日期作为授课日期。第三方商业教材、课网首页照片和受限题面未复用。']
    (SOURCE/'SOURCE_MAP.md').write_text('\n'.join(rows)+'\n')
    print(f'Frozen {len(hashes)} originals / {data["selected_pdf_pages"]} pages; one held link-only resource.')

if __name__=='__main__': main()
