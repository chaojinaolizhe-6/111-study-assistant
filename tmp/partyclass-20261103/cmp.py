a = open(r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\images\20261103-121604_38b2ed83.bin","rb").read()
b = open(r"D:\aaa..D盘常用文件夹\xwechat_files\wxid_4g9cekhsy71c22_9d64\cache\2026-10\Message\250ea1e712b1441663fd47be6fc3c833\ImageTemp\28_1793426482_mid_temp_convert","rb").read()
print(len(a), len(b))
diff = [i for i in range(min(len(a),len(b))) if a[i]!=b[i]]
print("first diff", diff[:5], "count", len(diff))
if diff:
    print("diff region", diff[0], diff[-1])
    # derive xor key from diff
    ks = set(a[i]^b[i] for i in diff[:50])
    print("xor keys seen", ks)
