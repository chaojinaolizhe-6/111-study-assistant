# 微信发送链路就绪检查（仅 dry-run，未发送）

检查时间：2026-11-11 04:44（本地）；入口：`社交信息整理助手/scripts/wechat_push.py`
样本：`inputs/old-handout.pdf`（0.34 MiB，%PDF-，非空，远低于 25 MiB 通道上限）

## 结论

| 环节 | 状态 | 依据 |
|---|---|---|
| 网关 | **就绪** | 127.0.0.1:18869 正在监听（openclaw-weixin） |
| 绑定 | **就绪** | 已存在 1 个绑定本人，收件人落在 `@im.wechat` 且带凭据；标识与凭据未落盘、未打印 |
| 文件能力 | **就绪** | 样本非空、PDF、0.34 MiB ≤ 25 MiB，工具自身 `validate()` 通过 |
| 窗口期 | **就绪** | 距上次入站约 0.14 小时，远小于 20 小时告警线，无拒收预警 |
| 补发队列 | **干净** | pending 0 条；sent 16 条（文件 10 / 文字 6），最近一条为今日 01:22 的真实发送（status=sent 且带 messageId） |
| 端到端 dry-run | **未完成** | `wechat_push.py -f … --dry-run --json` 在 staging 处被文件沙箱拒绝（WinError 5），未拿到 `dryRun=true` 回执 |

## 需要本人参与的实际阻断（一项）

**发送执行侧的目录写权限，不是微信链路本身的问题。**

- 原因：`--dry-run` 仍会把样本复制到 `社交信息整理助手/data/openclaw/media/outbox/<时间戳>/`；当前会话是 workspace-write 沙箱，只对本工作区可写。我按规则重试申请更宽权限一次，但本会话没有审批通道，申请被拒。
- 后果：**若最终讲义也由同样受限的会话直接调用 `wechat_push.py`，发送会在 staging 处失败，消息发不出去**。若由桌面端/主服务（本就拥有该 data 目录）执行，则不受此限。
- 需要的动作：交付时确认执行发送的会话能写 `社交信息整理助手/data/openclaw`，或改由桌面端上下文发送。**不需要重新扫码绑定，也不需要重启网关。**

## 边界说明

- 本次未发送任何文字或文件，未改绑定、凭据、网关或脚本，未使用微信 GUI；staging 失败时连目录都没建出来，没有残留（outbox 最新仍为 01:22，pending 仍为 0）。
- dry-run 只校验本地参数与文件，**不等于发送成功**；历史 01:22 的 `sent` 也只是过去证据，不能保证下一次必达。

## 复验命令（在具备该目录写权限的环境执行）

```powershell
python "D:\aaa_D_usual\DSH\社交信息整理助手\scripts\wechat_push.py" `
  -f "D:\aaa_D_usual\DSH\111学习助手\output\讲义skill-张量并矢-DS试生成-20261111\inputs\old-handout.pdf" `
  --dry-run --json
```

期望看到 `"ok": true`、每条 `"status": "dry-ok"`；真发时则要求每条 `deliveryStatus == "sent"` 且带 `messageId`。

附带产物：`readiness_probe.py`（复用发送器自身函数的只读探针）、`wechat-push-readiness.json`（机器可读结果，标识已脱敏）。
