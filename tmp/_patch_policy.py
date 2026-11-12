# -*- coding: utf-8 -*-
import io
p = r"D:\aaa_D_usual\CODEX\gemini-knowledge-bridge\src\policy.mjs"
s = io.open(p, encoding="utf-8").read()
start = s.index("export function buildPrompt")
old = s[start:]
new = '''export function buildPrompt({ question, context = '', purpose = 'research', id, date = new Date().toISOString().slice(0, 10) }) {
  // 2026-11-12: 原来的模板带着「请作为知识研究顾问」「任务：」「请使用中文…不要声称某个模型必然更强」
  // 这类机器味的包装，Gemini 网页会把它当成自动化脚本，直接回一句「我只是一个语言模型」。
  // 现在整段按正常人说话来写，只在最后留一行对号标记。
  const body = context ? `${question}\\n\\n${context}` : question;
  return `${body}\\n\\n（写完在最后单独附一行 [DSH_GEMINI_DONE:${id}]，我靠这行认出你的回复，谢谢。）`;
}
'''
s = s[:start] + new
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("policy.mjs rewritten")
