---
name: curate-notes
description: 根据已核读课程资料与真实辅导整理概念笔记，保留来源和未确认项。
---

# curate-notes

按当前主题整理，不自动通读教材库。原文、教学归纳、用户解释分别保留来源。
资料页是否读图/核公式记 materials.json；笔记不再维护另一份页数计数。
不要把已教或上传自动标 mastered。创建记忆卡时用稳定 id 和初始 SM-2 字段，实际复习交 record_review.py。
更新必要索引，不把历史纠错长篇复制到冷启动入口。
