import struct, collections
dat = open(r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64\msg\attach\250ea1e712b1441663fd47be6fc3c833\2026-10\Img\24d9680778e11cf4218a87c1a5048f3d.dat","rb").read()
tail = dat[1055:]
c = collections.Counter(tail)
print("len", len(tail))
print("top bytes:", [(hex(b), n) for b, n in c.most_common(8)])
print("pct top:", c.most_common(1)[0][1]/len(tail))
# entropy
import math
H = -sum((n/len(tail))*math.log2(n/len(tail)) for n in c.values())
print("entropy", round(H,3))
