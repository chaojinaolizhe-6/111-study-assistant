# -*- coding: utf-8 -*-
"""Score XOR key candidates by HEVC start-code structure, then verify by decoding."""
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
    return pt + bytes(b ^ key for b in tail)


def std_of(hevc, w=180, h=320):
    with tempfile.NamedTemporaryFile(suffix=".hevc", delete=False) as f:
        f.write(hevc)
        path = f.name
    try:
        r = subprocess.run([FF, "-v", "error", "-f", "hevc", "-i", path, "-frames:v", "1",
                            "-vf", "scale=%d:%d" % (w, h), "-f", "rawvideo", "-pix_fmt",
                            "rgb24", "-"], capture_output=True)
        buf = r.stdout
        if len(buf) < w * h * 3:
            return -1.0
        arr = np.frombuffer(buf[:w * h * 3], dtype=np.uint8).reshape(h, w, 3).astype(np.float32)
        return float(arr.std())
    finally:
        os.unlink(path)


def main():
    dat = open(sys.argv[1], "rb").read()
    scores = []
    for key in range(256):
        pt = plaintext_with_key(dat, key)
        n = pt.count(b"\x00\x00\x01")
        scores.append((n, key))
    scores.sort(reverse=True)
    print("top start-code counts:")
    for n, key in scores[:8]:
        print("  key=0x%02X count=%d" % (key, n))
    cands = [k for _, k in scores[:6]] + [0x88, 0x00]
    print("decode std:")
    for key in dict.fromkeys(cands):
        pt = plaintext_with_key(dat, key)
        start = pt.find(b"\x00\x00\x00\x01")
        print("  key=0x%02X std=%.2f" % (key, std_of(pt[start:])))


if __name__ == "__main__":
    main()
