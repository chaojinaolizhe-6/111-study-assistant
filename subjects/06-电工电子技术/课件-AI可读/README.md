# 电工电子技术 · 课件 AI 可读层（生成物，勿手改）

这一层是 `../课件/` 里 12 个老师课件 PDF 的**忠实转写**，目的是让网页 AI
不打开 PDF 也能读到页码级内容，并把每句话回指到具体页。

## 目录

| 路径 | 内容 |
|---|---|
| `index/INDEX.md` | **入口**：导航、字段说明、页码→小节快查、例题清单 |
| `index/manifest.json` | 构建元数据（源文件 sha256、页数、图区数、token 估算） |
| `index/pages.jsonl` | 一行一页的机器可读索引（`grep` 用） |
| `index/figure-descriptions.json` | 逐页图区 AI 视觉通读结果（原始产物） |
| `chapters/<deck>.md` | 整册串读全文（含本册目录表） |
| `text/<deck>-p###.md` | 逐页正文（引用单元） |
| `assets/<deck>/p###.jpg` | 整页扫描图 150 dpi（Git LFS） |

课件 id：`C1-1 C1-2 C1-3 C1-4 C2-1 C2-2 C3-1 C3-2 C3-3 C4-1 C4-2 C4-3`，
分别对应 `../课件/` 里按章排序的 12 个 PDF。**页码 = PDF 物理页 = 文件名编号**。

## 怎么再生成

这些脚本在仓库 `tools/` 下，都是幂等的：

```powershell
# 1. 版面解析（MinerU hybrid-engine，本地 GPU；约 4.5 s/页，547 页≈46 min）
python tools/ee-slides-run-mineru.py                 # 跳过已完成的册
python tools/ee-slides-run-mineru.py --decks C4-2 --force

# 2. 组装 AI 可读层（逐页 markdown / 整册全文 / JSONL / INDEX / 整页渲染图）
python tools/ee-slides-build.py build

# 3. 图区视觉通读（可选；需要能看图的 agent）
python tools/ee-slides-merge-descriptions.py tasks --batches 6
#    → index/describe-tasks.json，每批 6 页，交给读图 agent
python tools/ee-slides-merge-descriptions.py merge --result <agent结果.json>
python tools/ee-slides-build.py refresh           # 把描述回填进正文并重建 INDEX

# 4. 登记资料读取事实（learning/materials.json）
python tools/ee-materials-register.py
```

## 已知边界

- MinerU 会把画在图里的短标注（`＋`、`−`、`uO`、`RL`）判成页眉/页脚丢掉，
  因此逐页 markdown 里另有一节「页面文字层补充（图上标注）」，来自 PDF 文字层原样碎片。
- 图区裁切图**不入库**（重复且含装饰块）；版面事实以整页扫描图为准。
- 图区描述里凡属推断的读法标在「读图要点」中，供教学核对，
  **不构成任何掌握证据**；公式与页面图不一致时以页面图为准。
