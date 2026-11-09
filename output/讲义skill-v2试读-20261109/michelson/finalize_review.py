from pathlib import Path
import hashlib, json, re, sys, unicodedata
import fitz
import sympy

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[2]
tex_path = ROOT / 'michelson-excerpt-v2.tex'
pdf_path = ROOT / 'michelson-excerpt-v2.pdf'
tex = tex_path.read_text(encoding='utf-8-sig')
doc = fitz.open(pdf_path)
lecture_path = PROJECT / 'subjects/14-大物实验/课件/Exp.11TheAdjustmentofMichelsonInterferometer.pdf'
preview_path = PROJECT / 'subjects/14-大物实验/实验/PreviewforMichelsoninterferometer-2025.pdf'
old_path = PROJECT / 'subjects/14-大物实验/讲义/实验3.11-迈克尔逊干涉仪-原理与流程精讲-20261106.pdf'
preview = fitz.open(preview_path)
lecture = fitz.open(lecture_path)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def normalized(text):
    return ''.join(c.lower() for c in unicodedata.normalize('NFKC', text) if c.isalnum())

question_specs = [
    ('II-1', '§4.2', 1, [12]), ('II-2', '§4.3', 1, [12, 13]),
    ('II-3', '§4.4', 1, [13]), ('II-6', '§4.5', 1, [13]),
    ('II-7', '§4.6', 1, [14]), ('II-8', '§4.7', 1, [14]),
    ('II-9', '§4.8', 1, [15]), ('报告问题 (1)', '§4.9', 3, [15]),
    ('报告问题 (2)', '§4.10', 3, [15]),
]
questions = []
for ident, section, source_page, output_pages in question_specs:
    segment = tex.split('\\subhdr{' + section + ' ', 1)[1].split('\\subhdr{', 1)[0]
    stem = re.search(r'\\textit\{([^{}]+)\}', segment).group(1)
    if normalized(stem) not in normalized(preview[source_page-1].get_text()):
        raise AssertionError('Source stem mismatch: ' + ident)
    if '\\textbf{中文理解。}' not in segment or 'English short answer' not in segment:
        raise AssertionError('Bilingual answer missing: ' + ident)
    # Page list is explicit, then validated against the rendered heading/start.
    if section not in doc[output_pages[0]-1].get_text():
        raise AssertionError('Output page mismatch: ' + ident)
    questions.append(dict(id=ident, source='preview', source_pdf_pages=[source_page],
                          output_section=section, output_pdf_pages=output_pages,
                          original_english_stem=stem,
                          source_stem_check='PASS: Unicode/whitespace/punctuation normalized',
                          answer_languages=['中文', 'English']))

objectives_segment = tex.split('\\subhdr{§1.1', 1)[1].split('\\subhdr{§1.2', 1)[0]
objective_rows = re.findall(r'^\(([1-7])\) & (.+?) &', objectives_segment, re.M)
if [int(i) for i, _ in objective_rows] != list(range(1, 8)):
    raise AssertionError('The seven experimental objectives are not complete')
for i, english in objective_rows:
    if normalized(english) not in normalized(lecture[0].get_text()):
        raise AssertionError('Objective source mismatch: ' + i)
app_segment = tex.split('\\subhdr{§1.3', 1)[1].split('\\subhdr{§1.4', 1)[0]
app_rows = re.findall(r'^(\d+) & (.+?) &', app_segment, re.M)
if [int(i) for i, _ in app_rows] != list(range(1, 15)):
    raise AssertionError('Figure 11-1 apparatus numbers 1-14 are not complete')

log = (ROOT / 'michelson-excerpt-v2.log').read_text(encoding='utf-8', errors='replace')
log_checks = {
    'latex_errors': len(re.findall(r'^!', log, re.M)),
    'overfull_boxes': len(re.findall(r'Overfull \\[hv]box', log)),
    'missing_glyphs': len(re.findall(r'Missing character:', log)),
    'unresolved_references': len(re.findall(r'(?:Reference|Citation).+undefined|There were undefined references', log)),
    'rerun_required': len(re.findall(r'Rerun to get cross-references right|Label\(s\) may have changed', log)),
}
if any(log_checks.values()) or 'Output written on michelson-excerpt-v2.pdf (17 pages).' not in log:
    raise AssertionError('Final compilation log is incomplete or has blocking issues')

manifest = {
    'schema_version': 1,
    'review_date': '2026-11-09',
    'artifact_type': '实验原理与预习节选；不是完整实验讲义',
    'output': {'tex': str(tex_path), 'pdf': str(pdf_path), 'pdf_pages': len(doc),
               'tex_sha256': sha(tex_path), 'pdf_sha256': sha(pdf_path)},
    'provenance': {
        'draft_generator': 'DSH',
        'draft_status': '2026-11-09 13:13:06 达到 1200 秒时限退出；没有自然完成的最终验收答复',
        'draft_archive': str(ROOT.parent / 'dsh-初稿-审核前留档.zip'),
        'draft_pdf_pages': 16,
        'reviewed_revision': 'DSH 初稿经独立来源、数学与图示审核后修订；当前 PDF 为审核修订稿',
        'old_full_handout': str(old_path), 'old_full_handout_pages': 28,
        'old_full_handout_unchanged': True,
    },
    'sources': [
        {'id': 'lecture', 'path': str(lecture_path), 'sha256': sha(lecture_path), 'pdf_pages': len(lecture)},
        {'id': 'preview', 'path': str(preview_path), 'sha256': sha(preview_path), 'pdf_pages': len(preview)},
    ],
    'page_convention': 'All source and output pages are PDF physical pages, starting at 1.',
    'coverage': {
        'objectives': {'source': 'lecture', 'source_pdf_pages': [1], 'source_ids': list(range(1, 8)),
                       'optional_ids': [3, 4, 6, 7], 'output_section': '§1.1', 'output_pdf_pages': [2, 3],
                       'status': '7/7 complete; English source phrases checked; Chinese translations retained'},
        'preview_objectives': {'source': 'preview', 'source_pdf_pages': [1], 'source_ids': [1, 2, 3],
                              'output_section': '§1.2', 'output_pdf_pages': [3]},
        'apparatus': {'source': 'lecture', 'source_pdf_pages': [1, 2], 'figure': '11-1',
                     'source_ids': list(range(1, 15)), 'output_section': '§1.3', 'output_pdf_pages': [3, 4],
                     'status': '14/14 named apparatus entries and Chinese descriptions present; separate auxiliary equipment and carried materials'},
        'selected_questions_count': len(questions), 'selected_questions': questions,
        'excluded': [
            {'source': 'preview', 'source_pdf_pages': [1], 'ids': ['II-4', 'II-5', 'II-10', 'II-11'],
             'reason': '完整调环步骤、环心调整、空气折射率操作与注意事项超出本节选'},
            {'source': 'preview', 'source_pdf_pages': [1, 2], 'ids': ['III-1', 'III-2', 'III-3', 'III-4', 'III-5', 'III-6', 'III-7', 'III-8', 'III-9'],
             'reason': '全部九道口试思考题不覆盖；其中前两题在 p1，其余在 p2'},
            {'source': 'preview', 'source_pdf_pages': [2], 'ids': ['IV-1', 'IV-2', 'IV-3', 'IV-4'], 'reason': '四道扩展题不覆盖'},
            {'source': 'preview', 'source_pdf_pages': [3], 'ids': ['完整记录与处理表'],
             'reason': '仅解释波长表的 20:1 与 ΔN=160，未提供完整数据处理表或实测结果'},
            {'source': 'lecture', 'source_pdf_pages': [6, 7, 8, 9],
             'ids': ['完整操作', '定域/等厚条纹全部内容', '白光完整操作', 'F-P', '空气/薄片折射率实验完整处理'],
             'reason': '仅在目的、器材、来源冲突及选题需要处提及，不声称完整覆盖'},
        ],
    },
    'content_map': [
        {'output_section': '§2.1-§2.2', 'output_pdf_pages': [5, 6, 7], 'source': 'lecture', 'source_pdf_pages': [3, 4, 6, 7],
         'additions': '自行重建局部 AB/BC/AC/AD/CD 几何，明确同一比较波面与 Snell 推导；p7 续页复述点、长度与目标'},
        {'output_section': '§3.1-§3.3', 'output_pdf_pages': [7, 8, 9, 10], 'source': 'lecture', 'source_pdf_pages': [3, 4, 5, 7],
         'additions': '连续相位级次与整数亮纹分开；亮环半径例设 phi0=0, K=3000, d0=0.9492 mm, lambda=632.8 nm, z=0.500 m；全为教学示例'},
        {'output_section': '§3.4-§3.5', 'output_pdf_pages': [10, 11], 'source': ['lecture', 'preview'], 'source_pdf_pages': {'lecture': [2, 5, 8], 'preview': [3]},
         'additions': '数环/镜位移/鼓轮表逐项验证；明确 50/550 与 40/160 两套来源口径'},
    ],
    'verification': {
        'math_script': 'verify_michelson.py', 'math_output': 'verify_michelson.out.txt',
        'math_assertions_passed': 50, 'math_exit_code': 0, 'deliberate_failure_probe_exit_code': 1,
        'final_xelatex_pass_exit_codes': [0, 0], 'final_log_checks': log_checks,
        'handout_checker': {'mode': 'lab', 'log_provided': True, 'exit_code': 0, 'errors': 0, 'review_clues': 0},
        'source_stems_checked': 9, 'objective_phrases_checked': 7, 'apparatus_number_sequence_checked': 14,
        'rendered_pages': list(range(1, 18)), 'visual_overview': 'review-pages/overview-after.png',
        'visual_detail_pages': [6, 7, 8, 9, 12, 13, 15],
        'visual_result': '关键几何图、续页、两张数值表、双语答案及全页缩览未见重叠、截断或缺字；字体为 SimSun/SimHei 等已嵌入字体',
    },
    'comparison_images': [
        {'subject': '局部光程差图', 'before': 'review-pages/before-dsh-06.png', 'after': 'review-pages/after-06.png', 'comparison_type': 'DSH 初稿 vs 独立审核修订稿'},
        {'subject': '整机光路与往返箭头', 'before': 'review-pages/before-dsh-12.png', 'after': 'review-pages/after-12.png', 'comparison_type': 'DSH 初稿 vs 独立审核修订稿'},
        {'subject': '旧讲义等倾条纹示意与新局部投影推导', 'before': 'review-pages/before-full-10.png', 'after': 'review-pages/after-06.png',
         'comparison_type': '2026-11-06 的 28 页完整旧讲义 vs 新节选；范围不同，不能按页数评价覆盖'},
    ],
    'limitations': [
        '本文件仅为上述范围的节选；未覆盖内容继续查原 PDF 与旧完整讲义，旧稿未在本轮逐页重新审计。',
        '真实镀膜相位、实际膜厚、激光波长与气室长度未知；示例不替代现场测量。',
        '固定附加相位、相干与偏振条件是所用亮纹/数环模型的前提；近轴半径式还要求 2d<<z 和 m lambda/d<<1。',
        'II-6 原题观察目标含糊，已区分固定一圈外扩与整套条纹变疏；课堂预期口径仍应说明。',
        '钠光源称谓、数环间隔、空气测量次数在两份原资料中存在差异，未替教师作选择。',
        '公式断言与静态检查不能自动证明所有文字物理解释正确；本次另做了限定范围的独立语义和视觉审核。',
    ],
}
(ROOT / 'source-map.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
verification = f'''迈克尔逊原理与预习节选：独立审核修订验收记录
日期：2026-11-09

产物：{pdf_path}
页数：{len(doc)}；不是完整实验讲义。
PDF SHA256：{sha(pdf_path)}
TEX SHA256：{sha(tex_path)}

来源与范围
- 两份原始 PDF 的物理页码、文件 SHA256、各题映射见 source-map.json。
- 7 项实验目的完整中英对照，选做标记为 (3)(4)(6)(7)；7 条英文逐项匹配源文。
- 图 11-1 的 14 个编号部件完整列出，单独区分辅助器材与携带材料。
- 只收 9 问：II-1、II-2、II-3、II-6、II-7、II-8、II-9，及预习 p3 报告问题 (1)(2)。
- 9 个英文题干经 Unicode/空白/标点归一化逐一匹配源 PDF，均保留题号与中英答案。
- 不覆盖 II-4/5/10/11、III-1 至 III-9、IV-1 至 IV-4、完整记录表与完整操作；不以这 17 页替代旧 28 页讲义。

来源沿革
- DSH 初稿在 1200 秒时限退出，未自然完成最终验收；初稿 PDF 为 16 页。
- 原稿已封存于 ../dsh-初稿-审核前留档.zip；本目录当前 TEX/PDF 是独立审核后修订版。
- 旧完整讲义为 2026-11-06 的 28 页版本，未改动；它与 DSH 本轮初稿是不同对象。

修正与人工验收
- p6：比较波面 CD 真正通过 C、D，且垂直出射光；AD 在光束 1 上；AB、BC、AC 与投影的几何数值一致，标注无重叠。
- p7：续页重述 A/B/C/D、AB/BC/AD 和推导目标；非空气膜先加权膜内光程、再用 Snell 定律；补偿玻璃不等于总光程差为零。
- p8-p9：相位差与连续级次 q 明确，整数才是亮纹；理想特例 phi0=0、K=3000、d0=0.9492 mm，重算半径 12.91/18.26/22.36/25.82 mm。
- p9-p10：固定附加相位在数环时相消；说明完整周期及起止相位条件；20:1、6 行数环表和反推波长已验证。
- p12：整机光路保留扩束镜，分开往返箭头；E/FG 标签与图注分离；虚像位置与 45 度分光板一致。
- p13：II-2 英文短答完整且带题号；II-6 中英均区分“固定一圈外扩”和“整套条纹变疏”。
- p16：来源章节不再作为孤立标题留在前页页尾。
- 已渲染全 17 页并看全页缩览；重点放大核查 p6、7、8、9、12、13、15。图像位于 review-pages/。

自动验证
1. python -B verify_michelson.py：exit 0，50 条强断言通过。
   覆盖膜几何、Snell/折射率式、固定相位数环、整数亮中心、新半径、角度表、鼓轮/逐差与气室双程关系。
   记录：verify_michelson.out.txt；Python {sys.version.split()[0]}，SymPy {sympy.__version__}。
2. 故意调用 require_equal(1, 2, 'deliberate failure probe')：AssertionError，exit 1。
   证明验证脚本不会仅打印 False 后仍成功退出。
3. 最终修改后 XeLaTeX 连续两遍：exit 0、exit 0；最终交叉引用稳定。
   记录：compile-pass-1.txt、compile-pass-2.txt、michelson-excerpt-v2.log。
4. check_handout.py TEX --mode lab --log LOG：exit 0，错误 0，人工复核线索 0。
5. 最终 log：{json.dumps(log_checks, ensure_ascii=False)}。
   字体实际为 SimSun/SimHei 等；没有 Missing character。MiKTeX 的更新提醒不影响本次编译。

对照图
- DSH 初稿 p6 -> 修订 p6：review-pages/before-dsh-06.png / after-06.png。
- DSH 初稿 p12 -> 修订 p12：review-pages/before-dsh-12.png / after-12.png。
- 旧完整讲义 p10 的等倾示意 -> 新节选 p6 的局部投影推导：review-pages/before-full-10.png / after-06.png。
- 三者范围不同，不用页数作覆盖或质量结论。

剩余限制
- 镀膜相位、真实膜厚、波长与气室长度未给，不用教学数值冒充实际参数。
- II-6 的口头目标、钠光源称谓、计数档位与空气测量次数仍有源材料口径问题，文内已列明。
- 数学断言只验证指定恒等式与例值；本次并非对旧完整讲义或全部实验内容的重新审计。
'''
(ROOT / 'verification.txt').write_text(verification, encoding='utf-8')
print('PASS: 9 source question stems; 7 objective phrases; apparatus IDs 1-14; final log clean.')
print('Wrote source-map.json and verification.txt with final artifact hashes.')
