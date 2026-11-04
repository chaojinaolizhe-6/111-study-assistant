import struct, glob, os
base=r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64"
for p in [base+r"\msg\attach\250ea1e712b1441663fd47be6fc3c833\2026-10\Img\5bcb153f7cc8fc39132f4ea8d055c101_t.dat",
          base+r"\cache\2026-10\Message\250ea1e712b1441663fd47be6fc3c833\Bubble\38b2ed83698f828714578f0b74145789_b.dat"]:
    d=open(p,"rb").read()
    print(os.path.basename(p), len(d), d[:16].hex())
    if d[:6]==b"\x07\x08\x56\x32\x08\x07":
        a,x=struct.unpack_from("<LL",d,6); print("  aes",a,"xor",x,"rest",len(d)-15-((a+15)//16*16) - x)
