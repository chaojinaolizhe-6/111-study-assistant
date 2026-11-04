import glob, os, struct
folder = r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64\msg\attach\250ea1e712b1441663fd47be6fc3c833\2026-10\Img"
for f in sorted(glob.glob(os.path.join(folder, "*.dat"))):
    if f.endswith("_t.dat"): continue
    d = open(f, "rb").read()
    aes_size, xor_size = struct.unpack_from("<LL", d, 6)
    blk = aes_size + (16 - aes_size % 16 if aes_size % 16 else 16)
    print(os.path.basename(f)[:8], "total", len(d), "aes", aes_size, "xor", xor_size, "raw", len(d)-15-blk-xor_size, "blk", blk)
