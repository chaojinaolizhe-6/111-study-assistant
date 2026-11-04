import os, struct, subprocess, tempfile, numpy as np
ff = r"C:\Program Files (x86)\ACLOS\Cross\recorder-release\ffmpeg.exe"
src = r"D:\aaa_D_usual\DSH\111学习助手\tmp\partyclass-20261103\images\20261103-121602_24d96807.bin"
data = open(src, "rb").read()
assert data[:4] == b"wxgf"
# find first start code
start = data.find(b"\x00\x00\x00\x01")
aes_part = data[start:start+1024+16-16]  # placeholder
