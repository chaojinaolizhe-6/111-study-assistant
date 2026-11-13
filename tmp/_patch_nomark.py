# -*- coding: utf-8 -*-
import io, sys
base = r"D:\aaa_D_usual\CODEX\gemini-knowledge-bridge\src"

# 1) policy.mjs —— 提示词里不再出现任何标记
p1 = base + r"\policy.mjs"
s1 = io.open(p1, encoding="utf-8").read()
old1 = '''  const body = context ? `${question}\\n\\n${context}` : question;
  return `${body}\\n\\n（写完在最后单独附一行 [DSH_GEMINI_DONE:${id}]，我靠这行认出你的回复，谢谢。）`;'''
new1 = '''  // 2026-11-12 二次修改：连结束标记也去掉。连接器改按「页面上是否多出一条回答」对号，
  // 提示词就是纯粹的一句人话，不含任何脚本痕迹。
  return context ? `${question}\\n\\n${context}` : question;'''
if s1.count(old1) != 1:
    print("policy pattern:", s1.count(old1)); sys.exit(1)
s1 = s1.replace(old1, new1)
io.open(p1, "w", encoding="utf-8", newline="\n").write(s1)

# 2) page-programs.mjs —— 对号改成计数；发送前校验放宽
p2 = base + r"\page-programs.mjs"
s2 = io.open(p2, encoding="utf-8").read()
old2 = '''  const token = jobId ? `[DSH_GEMINI_DONE:${jobId}]` : '';
  const correlated = !!jobId && !!users.length && (users.at(-1).textContent || '').includes(token);'''
new2 = '''  const token = jobId ? `[DSH_GEMINI_DONE:${jobId}]` : '';
  // 提示词里已经没有结束标记，改用计数对号：提交前记下基线，页面上多出一条回答就是本次的。
  const correlated = !!jobId && responses.length > baselineCount;'''
if s2.count(old2) != 1:
    print("page-program correlated pattern:", s2.count(old2)); sys.exit(1)
s2 = s2.replace(old2, new2)

old3 = '''  const sameText = !!(editor && wanted && (draft === wanted || (draft.includes(token) && draft.startsWith(head))));'''
new3 = '''  // 没有结束标记做锚点，就用「开头 24 字一致」来确认这一段确实是我们刚打进去的。
  const sameText = !!(editor && wanted && (draft === wanted || (draft.startsWith(head) && draft.length >= wanted.length * 0.85)));'''
if s2.count(old3) != 1:
    print("page-program send pattern:", s2.count(old3)); sys.exit(1)
s2 = s2.replace(old3, new3)
io.open(p2, "w", encoding="utf-8", newline="\n").write(s2)

# 3) jobs.mjs —— 完成判定不再依赖结束标记
p3 = base + r"\jobs.mjs"
s3 = io.open(p3, encoding="utf-8").read()
old4 = '''        const complete = snapshot.correlated && !!text && !snapshot.generating && (snapshot.endMarker || (snapshot.completionToolbar && stableSince > 0 && Date.now() - stableSince >= this.settledMs));'''
new4 = '''        // 没有结束标记：文字停住 settledMs 秒且页面不在生成，就算答完。
        const settled = stableSince > 0 && Date.now() - stableSince >= this.settledMs;
        const complete = snapshot.correlated && !!text && !snapshot.generating && (snapshot.endMarker || settled);'''
if s3.count(old4) != 1:
    print("jobs pattern:", s3.count(old4)); sys.exit(1)
s3 = s3.replace(old4, new4)
io.open(p3, "w", encoding="utf-8", newline="\n").write(s3)
print("patched policy/page-programs/jobs")
