# -*- coding: utf-8 -*-
import io
def fix(path, pairs):
    s=io.open(path,encoding='utf-8').read()
    for o,n in pairs:
        c=s.count(o)
        print(('OK   ' if c>=1 else 'MISS ')+path+' :: '+o[:40])
        s=s.replace(o,n)
    io.open(path,'w',encoding='utf-8',newline='\n').write(s)

fix('progress.md', [
 ('（29 页，tex 同目录）','（30 页，tex 同目录；2026-11-06 修订版）'),
 ('- 材料里发现的口径冲突已写进 §10（13 条）','- 材料里发现的口径冲突已写进 §10（16 条）'),
])
fix('INDEX.md', [
 ('**讲义已备**（29 页，2026-11-06 编译）','**讲义已备**（30 页，2026-11-06 编译，当日修订）'),
])
fix(r'讲义\INDEX.md', [
 ('（29 页）','（30 页）'),
 ('11 道预习题 + 9 道口试 + 4 道扩展（中英）；§10 缺口 13 条',
  '讲义 p1 的 **Experimental Objectives 7 条**与目标—章节对照表、**SGM-2** 器材段；§5.8 第三项（定域条纹测钠光波长，含钠双线可见度消失判据）；11 道预习题 + 9 道口试 + 4 道扩展（中英）；§10 缺口 16 条'),
])
fix(r'实验\INDEX.md', [
 ('- 讲义（29 页）：','- 讲义（30 页，2026-11-06 修订）：'),
 ('§10 缺口（13 条）','§10 缺口（16 条）'),
 ('  - 补齐的推导：','  - 修订记录：v1 漏读了讲义 p1 的 Experimental Objectives（抽文本时被 1200 字上限截断）与 SGM-2 器材段；v2 已补 7 条目的、目标对照表、SGM-2、§5.8 第三项。\n  - 补齐的推导：'),
])
print('done')
