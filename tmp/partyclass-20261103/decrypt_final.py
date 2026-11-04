# -*- coding: utf-8 -*-
"""Decrypt WeChat V2 .dat (wxgf/HEVC) with the verified account keys and
convert to JPEG with ffmpeg."""
import glob
import os
import struct
import subprocess
import sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

AES_KEY = b"893b57bf6f96b718"
XOR_KEY = 0xA9
FF = r"C:\Program Files (x86)\ACLOS\Cross\recorder-release\ffmpeg.exe"
VPS = b"\x00\x00\x00\x01\x40\x01"


def decrypt(dat):
    aes_size, xor_size = struct.unpack_from("<LL", dat, 6)
    blk = aes_size + (16 - aes_size % 16 if aes_size % 16 else 16)
    pt = Cipher(algorithms.AES(AES_KEY), modes.ECB()).decryptor().update(dat[15:15 + blk])
    pad = pt[-1]
    if 1 <= pad <= 16 and all(b == pad for b in pt[-pad:]):
        pt = pt[:-pad]
    tail = dat[15 + blk:]
    if xor_size:
        tail = bytes(b ^ XOR_KEY for b in tail)
    return pt + tail


def stream_start(buf):
    i = buf.find(VPS)
    if i >= 0:
        return i
    i = buf.find(b"\x00\x00\x00\x01")
    return i if i >= 0 else 0


def main(folder, outdir):
    os.makedirs(outdir, exist_ok=True)
    files = [f for f in sorted(glob.glob(os.path.join(folder, "*.dat")))
             if not f.endswith("_t.dat") and not f.endswith("_h.dat")]
    ok = 0
    for f in files:
        name = os.path.basename(f)[:-4]
        dat = open(f, "rb").read()
        if dat[:6] != b"\x07\x08\x56\x32\x08\x07":
            print("SKIP (not v2)", name)
            continue
        plain = decrypt(dat)
        start = stream_start(plain)
        hevc = os.path.join(outdir, name + ".hevc")
        open(hevc, "wb").write(plain[start:])
        out = os.path.join(outdir, name + ".jpg")
        r = subprocess.run([FF, "-v", "error", "-y", "-f", "hevc", "-i", hevc,
                            "-frames:v", "1", "-c:v", "mjpeg", "-q:v", "2",
                            "-update", "1", out], capture_output=True, text=True)
        size = os.path.getsize(out) if os.path.exists(out) else 0
        print("%s rc=%d jpg=%d %s" % (name[:8], r.returncode, size, r.stderr.strip()[:100]))
        if size:
            ok += 1
    print("converted %d/%d" % (ok, len(files)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
