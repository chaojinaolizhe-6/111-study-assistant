# -*- coding: utf-8 -*-
import io
def fix(path,pairs):
    s=io.open(path,encoding='utf-8').read()
    for o,n in pairs:
        c=s.count(o); print(('OK   ' if c>=1 else 'MISS ')+path+' '+o[:26])
        s=s.replace(o,n)
    io.open(path,'w',encoding='utf-8',newline='\n').write(s)
fix('progress.md',[('（30 页，tex 同目录；2026-11-06 修订版）','（28 页，tex 同目录；2026-11-06 三次修订，答案已压到 50 词）')])
fix('INDEX.md',[('**讲义已备**（30 页，2026-11-06 编译，当日修订）','**讲义已备**（28 页，2026-11-06 编译，当日修订两轮）')])
fix(r'讲义\INDEX.md',[('（30 页）','（28 页；§7/§8 答案压到约 50 词）')])
fix(r'实验\INDEX.md',[('- 讲义（30 页，2026-11-06 修订）：','- 讲义（28 页，2026-11-06 修订两轮）：'),
 ('  - 修订记录：v1 漏读了讲义 p1 的 Experimental Objectives','  - 修订记录：v1 漏读 p1 的 Experimental Objectives')])
print('done')
