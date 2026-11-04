# -*- coding: utf-8 -*-
"""Brute force the single-byte XOR key of a WeChat V2 wxgf image.

For each candidate key, rebuild the HEVC stream and let ffmpeg decode it to
270x480 RGB; score = fraction of pure-green (concealed) pixels. Correct key
gives the lowest score.
"""
import struct
import subprocess
import sys
import tempfile
import os

import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

FF = r"C:\Program Files (x86)\ACLOS\Cross\recorder-release\ffmpeg.exe"
AES_KEY = b"893b57bf6f96b718"


def plaintext_with_key(dat, key):
    aes_size, xor_size = struct.unpack_from("<LL", dat, 6)
    blk = aes_size + (16 - aes_size % 16 if aes_size % 16 else 16)
    pt = Cipher(algorithms.AES(AES_KEY), modes.ECB()).decryptor().update(dat[15:15 + blk])
    pad = pt[-1]
    if 1 <= pad <= 16 and all(b == pad for b in pt[-pad:]):
        pt = pt[:-pad]
    tail = dat[15 + blk:]
    if key is not None:
        tail = bytes(b ^ key for b in tail)
    return pt + tail


def score(hevc, w=270, h=480):
    with tempfile.NamedTemporaryFile(suffix=".hevc", delete=False) as f:
        f.write(hevc)
        path = f.name
    try:
        r = subprocess.run([FF, "-v", "error", "-f", "hevc", "-i", path, "-frames:v", "1",
                            "-vf", "scale=%d:%d" % (w, h), "-f", "rawvideo", "-pix_fmt",
                            "rgb24", "-"], capture_output=True)
        buf = r.stdout
        if len(buf) < w * h * 3:
            return 1.0, r.stderr.decode("utf-8", "ignore")[:200]
        arr = np.frombuffer(buf[:w * h * 3], dtype=np.uint8).reshape(h, w, 3)
        g = ((arr[:, :, 1] > 180) & (arr[:, :, 0] < 80) & (arr[:, :, 2] < 80)).mean()
        return float(g), ""
    finally:
        os.unlink(path)


def main():
    dat_path = sys.argv[1]
    dat = open(dat_path, "rb").read()
    best = []
    for key in range(256):
        pt = plaintext_with_key(dat, key)
        start = pt.find(b"\x00\x00\x00\x01")
        g, err = score(pt[start:])
        best.append((g, key))
    best.sort()
    for g, key in best[:6]:
        print("key=0x%02X green=%.3f" % (key, g))


if __name__ == "__main__":
    main()
