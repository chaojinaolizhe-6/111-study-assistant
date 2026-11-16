# -*- coding: utf-8 -*-
"""生成马原口试 PPT 的纸纹背景（大工红金版式，参照上次‘底线思维’汇报模板）。"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
import os

SRC_WALL = r"D:\aaa_D_usual\DSH\111学习助手\马原口试-七大思维-20261115\_tpl-src\media\0fecdeb3ad73e02d62bef4fe.png"
OUT = r"D:\aaa_D_usual\DSH\111学习助手\马原口试-七大思维-20261115\deck\media"
W, H = 1920, 1080

CREAM_TOP = np.array([252, 246, 236], dtype=np.float32)
CREAM_BOT = np.array([244, 233, 214], dtype=np.float32)


def base_canvas():
    t = np.linspace(0, 1, H)[:, None, None]
    return CREAM_TOP[None, None, :] * (1 - t) + CREAM_BOT[None, None, :] * t


def wall_plate():
    im = Image.open(SRC_WALL).convert("RGB")
    w, h = im.size
    band = im.crop((0, int(h * 0.72), w, h))
    bw, bh = band.size
    scale = W / bw
    band = band.resize((W, max(1, int(bh * scale))), Image.LANCZOS)
    plate = Image.new("RGB", (W, H), (247, 238, 223))
    plate.paste(band, (0, H - band.size[1]))
    # 降低对比与饱和，压成“纸纹”而不是插图
    plate = ImageEnhance.Color(plate).enhance(0.45)
    plate = ImageEnhance.Contrast(plate).enhance(0.70)
    plate = Image.blend(Image.new("RGB", (W, H), (248, 240, 226)), plate, 0.55)

    ys = np.arange(H)[:, None].astype(np.float32)
    band_top = H - band.size[1]
    v = np.clip((ys - band_top) / (band.size[1] * 0.75), 0, 1) ** 1.5
    v = np.repeat(v, W, axis=1)
    xs = np.arange(W)[None, :].astype(np.float32)
    hz = 1.0 - 0.55 * np.clip((W * 0.45 - xs) / (W * 0.45), 0, 1)
    hz = np.repeat(hz, H, axis=0)
    return plate, v * hz


def build(cover=False):
    out = base_canvas()
    plate, mask = wall_plate()
    strength = 0.55 if cover else 0.34
    a = (mask * strength)[..., None]
    out = out * (1 - a) + np.array(plate, dtype=np.float32) * a

    if cover:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W * 0.15) / (W * 0.62)) ** 2 + ((yy - H * 0.05) / (H * 0.70)) ** 2)
        glow = np.clip(1 - d, 0, 1) ** 2
        out = out + (255 - out) * glow[..., None] * 0.28

    rng = np.random.default_rng(7)
    noise = rng.normal(0, 1.6, (H, W, 1)).repeat(3, axis=2)
    out = np.clip(out + noise, 0, 255)
    img = Image.fromarray(out.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4))
    return img


os.makedirs(OUT, exist_ok=True)
build(False).save(os.path.join(OUT, "bg-page.png"), "PNG")
build(True).save(os.path.join(OUT, "bg-cover.png"), "PNG")
print("saved", OUT)

