---
name: schedule-review
description: 处理记忆到期复习和延迟能力再测，保持同日重做与跨日证据分离。
---

# schedule-review

运行 tutor_context.py 查看到期项，或读 plan/schedule.md。记忆保持与能力再测是两个队列，不能互相替代。
记忆复习先回忆后反馈；质量分依据首次表现，提示后答对不能给无帮助的高分。
已有带 id 的概念卡，用 python -B tools/record_review.py --concept <id> --quality <0-5>。同日重做不增加间隔成功次数；脚本记录后更新 frontmatter。
能力再测使用新的 task_id、相应 kind 和验收条件，遵守 not_before/min_delay_days；用 append_attempt.py 入账。
课程尚未建记忆卡时明确尚未启用，不能用「到期 0」证明无需复习。收尾跑 session-close.py。
