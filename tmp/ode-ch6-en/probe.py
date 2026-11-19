import sys, io, os
p = os.path.join('subjects', '03-微分方程', '讲义', 'ODE-期中之后-完整讲义-L13-L23-20261118.tex')
b = open(p, 'rb').read()
print('bytes', len(b))
print('crlf', b.count(b'\r\n'), 'lf', b.count(b'\n'), 'bom', b[:3])
s = b.decode('utf-8')
print('chars', len(s))
print('ascii_dq', s.count('"'), 'cn_lq', s.count('\u201c'), 'cn_rq', s.count('\u201d'))
print('en_macro', s.count('\\EN{'))
