# 收尾核对

1. 真实作答用 append_attempt.py 追加；帮助史逐目标与事件级一致。订正走 record_correction.py。
2. 用户的新遗漏/时间反馈已进入 observations 队列，并有处理产物或暂缓理由。
3. 若有真实记忆复习，用 record_review.py 更新已有概念卡；不手工改能力分数。
4. 运行 `python -B tools/session-close.py`，以输出为准。任一 FAIL 就报告未完整同步。
5. 一句说明当前障碍、下次首个动作；暂停要保留最后有效步骤。不把受助完成说成独立掌握。

旧模板 refresh-status/validate-study 与 state/mastery.json 不属于当前收尾链。
