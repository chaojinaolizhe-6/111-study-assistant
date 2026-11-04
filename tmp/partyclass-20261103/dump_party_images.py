# -*- coding: utf-8 -*-
"""Decrypt WeChat 4.x .dat images for the 党课 group chat.

Standalone: scans Weixin.exe memory for the 16-byte AES image key, derives the
single-byte XOR key from thumbnail tails, then decrypts every V2 .dat found in
the chat's attach folder.
"""
import ctypes
import ctypes.wintypes as wt
import glob
import os
import re
import struct
import sys
import time

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

V2_MAGIC = b"\x07\x08\x56\x32\x08\x07"
k32 = ctypes.WinDLL("kernel32", use_last_error=True)


class MBI(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", wt.DWORD),
        ("PartitionId", wt.WORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wt.DWORD),
        ("Protect", wt.DWORD),
        ("Type", wt.DWORD),
    ]


k32.OpenProcess.restype = wt.HANDLE
k32.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
k32.VirtualQueryEx.restype = ctypes.c_size_t
k32.VirtualQueryEx.argtypes = [wt.HANDLE, ctypes.c_void_p, ctypes.POINTER(MBI), ctypes.c_size_t]
k32.ReadProcessMemory.restype = wt.BOOL
k32.ReadProcessMemory.argtypes = [wt.HANDLE, ctypes.c_void_p, ctypes.c_void_p,
                                  ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
k32.CloseHandle.argtypes = [wt.HANDLE]


def weixin_pids():
    import subprocess
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Weixin.exe", "/FO", "CSV", "/NH"],
                         capture_output=True, text=True, encoding="gbk", errors="ignore").stdout
    pids = []
    for line in out.splitlines():
        parts = [p.strip('"') for p in line.split('","')]
        if len(parts) >= 2 and parts[0].lower().startswith("weixin.exe"):
            try:
                pids.append(int(parts[1]))
            except ValueError:
                pass
    return pids


def read_mem(h, addr, n):
    buf = ctypes.create_string_buffer(n)
    br = ctypes.c_size_t(0)
    if k32.ReadProcessMemory(h, ctypes.c_void_p(addr), buf, n, ctypes.byref(br)) and br.value:
        return buf.raw[: br.value]
    return None


ASCII32 = re.compile(rb"[^a-zA-Z0-9]([a-zA-Z0-9]{32})[^a-zA-Z0-9]")
U16_32 = re.compile(rb"(?:[a-zA-Z0-9]\x00){32}")


def aes_ecb_decrypt(key: bytes, data: bytes) -> bytes:
    d = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    return d.update(data) + d.finalize()


def img_like(pt: bytes) -> bool:
    return pt[:3] == b"\xff\xd8\xff" or pt[:4] in (b"\x89PNG", b"GIF8", b"RIFF") or pt[:4] == b"wxgf"


def find_key(probe: bytes, log):
    pids = weixin_pids()
    log("Weixin pids: %s" % pids)
    for pid in pids:
        h = k32.OpenProcess(0x0010 | 0x0400, False, pid)
        if not h:
            log("open failed pid=%s err=%s" % (pid, ctypes.get_last_error()))
            continue
        try:
            addr = 0
            scanned = 0
            while True:
                mbi = MBI()
                r = k32.VirtualQueryEx(h, ctypes.c_void_p(addr), ctypes.byref(mbi), ctypes.sizeof(mbi))
                if r == 0:
                    break
                if (mbi.State == 0x1000 and (mbi.Protect & 0xFF) & 0xE6
                        and not (mbi.Protect & 0x100) and 0 < mbi.RegionSize < 0x2000000):
                    buf = read_mem(h, mbi.BaseAddress or 0, mbi.RegionSize)
                    if buf:
                        scanned += len(buf)
                        for m in ASCII32.finditer(buf):
                            key = m.group(1)[:16]
                            if img_like(aes_ecb_decrypt(key, probe)):
                                return key.decode()
                        for m in U16_32.finditer(buf):
                            key = bytes(b for i, b in enumerate(m.group()) if i % 2 == 0)[:16]
                            if img_like(aes_ecb_decrypt(key, probe)):
                                return key.decode()
                addr = (mbi.BaseAddress or 0) + mbi.RegionSize
            log("pid %s scanned %.1f MB, no hit" % (pid, scanned / 1e6))
        finally:
            k32.CloseHandle(h)
    return None


def xor_key_from_thumbs(folder):
    tails = {}
    for p in glob.glob(os.path.join(folder, "*_t.dat")):
        try:
            with open(p, "rb") as f:
                f.seek(-2, 2)
                t = f.read(2)
        except OSError:
            continue
        if len(t) == 2:
            tails[(t[0], t[1])] = tails.get((t[0], t[1]), 0) + 1
    for (x, y), _ in sorted(tails.items(), key=lambda kv: -kv[1]):
        k = x ^ 0xFF
        if y ^ 0xD9 == k:
            return k
    return None


def decrypt_v2(data, aes_key, xor_key):
    aes_size, xor_size = struct.unpack_from("<LL", data, 6)
    blk = aes_size + (16 - aes_size % 16 if aes_size % 16 else 16)
    off = 15
    aes_data = data[off:off + blk]
    off += blk
    raw = data[off:len(data) - xor_size] if xor_size else data[off:]
    xor = data[len(data) - xor_size:] if xor_size else b""
    pt = aes_ecb_decrypt(aes_key.encode(), aes_data)
    pad = pt[-1] if pt else 0
    if 1 <= pad <= 16 and all(b == pad for b in pt[-pad:]):
        pt = pt[:-pad]
    out = pt + raw + bytes(b ^ (xor_key & 0xFF) for b in xor)
    if out.startswith(b"\xff\xd8"):
        i = out.rfind(b"\xff\xd9")
        if i > 0 and len(out) - i - 2 <= 32:
            out = out[:i + 2]
    elif out.startswith(b"\x89PNG"):
        i = out.rfind(b"IEND\xaeB`\x82")
        if i > 0:
            out = out[:i + 8]
    return out


def main():
    folder = sys.argv[1]
    outdir = sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    logf = open(os.path.join(outdir, "decrypt.log"), "w", encoding="utf-8")

    def log(msg):
        logf.write(msg + "\n")
        logf.flush()

    dats = sorted(glob.glob(os.path.join(folder, "*.dat")))
    dats = [d for d in dats if not d.endswith("_t.dat") and not d.endswith("_h.dat")]
    log("dat files: %d" % len(dats))
    with open(dats[0], "rb") as f:
        head = f.read(32)
    assert head[:6] == V2_MAGIC, head[:6]
    probe = head[15:31]
    xor_key = xor_key_from_thumbs(folder)
    log("xor key from thumbs: %s" % xor_key)

    key = None
    for attempt in range(3):
        key = find_key(probe, log)
        if key:
            break
        log("retry %d: asking user to open an image in WeChat..." % attempt)
        time.sleep(5)
    if not key:
        log("FAILED to locate AES key")
        return 1
    log("AES key: %s" % key)

    ok = 0
    for d in dats:
        with open(d, "rb") as f:
            data = f.read()
        try:
            if xor_key is None:
                xor_key = 0x88
            img = decrypt_v2(data, key, xor_key)
        except Exception as exc:
            log("ERR %s %r" % (os.path.basename(d), exc))
            continue
        name = os.path.basename(d)[:-4]
        ext = ".jpg" if img[:2] == b"\xff\xd8" else ".png" if img[:4] == b"\x89PNG" else ".bin"
        mtime = time.strftime("%Y%m%d-%H%M%S", time.localtime(os.path.getmtime(d)))
        dst = os.path.join(outdir, "%s_%s%s" % (mtime, name[:8], ext))
        with open(dst, "wb") as f:
            f.write(img)
        ok += 1
        log("OK %s -> %s (%d bytes)" % (os.path.basename(d), os.path.basename(dst), len(img)))
    log("decrypted %d/%d" % (ok, len(dats)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
