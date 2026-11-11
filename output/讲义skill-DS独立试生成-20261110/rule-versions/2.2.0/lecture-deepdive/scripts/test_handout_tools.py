# -*- coding: utf-8 -*-
"""Focused regression checks; temporary fixtures never modify existing handouts.

Run: python -B .dsh/skills/lecture-deepdive/scripts/test_handout_tools.py
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker, reader = load("check_handout"), load("read_slides")
VALID = r"""\documentclass{article}
\newcommand{\practice}[5]{#3 \pageref{#5}}
\begin{document}
\subhdr{教学小例：方法示范}
给出一个完整示例。\textbf{关键一步}：先展开。
\hdr{§2}{独立练习}
\practice{p1}{课件 p2}{已知 $A=\begin{pmatrix}1&0\\0&2\end{pmatrix}$，求解。}{矩阵指数}{ans:p1}
\appendix
\answerstart{p1}{课件 p2}{矩阵 A 为题干中的对角矩阵。}
\textbf{详解}：按定义计算。
\answercontinue{p1}{仍为该对角矩阵。}
核对结果；见第 \pageref{ans:p1} 页。
\end{document}
"""


class HandoutChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="handout-check-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def tex(self, text):
        path = self.root / "test.tex"
        path.write_text(text, encoding="utf-8")
        return path

    def test_valid_pair_and_teaching_example(self):
        self.assertEqual(checker.check_file(self.tex(VALID), "appendix"), ([], []))

    def test_theme_commands_used_as_environments_fail(self):
        for name in ("callout", "qstem", "warnbox"):
            with self.subTest(name=name):
                path = self.tex("\\begin{document}\n" + f"\\begin{{{name}}}设条件成立。\\end{{{name}}}\n"
                                + "\\end{document}")
                errors, _ = checker.check_file(path)
                self.assertTrue(any(f"主题命令 \\{name} 当作环境" in e for e in errors), errors)
        path = self.tex(r"\begin{callout}设条件成立。\end{callout}")
        result = subprocess.run([sys.executable, "-B", str(HERE / "check_handout.py"), str(path)],
                                capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"[E]", result.stdout)

    def test_theme_command_check_ignores_comments_and_definitions(self):
        text = r"""\begin{document}
% \begin{callout} 注释里的示范不算调用。
\newcommand{\demo}[1]{
  \begin{qstem}#1\end{qstem}
}
\providecommand{\otherdemo}{\begin{warnbox}示范\end{warnbox}}
\callout{设条件成立。}
\qstem{（课件 p1）已知条件，求解。}
\warnbox{注意适用范围。}
\begin{quote}正常环境不受这项专门检查影响。\end{quote}
\end{document}"""
        self.assertEqual(checker.check_file(self.tex(text)), ([], []))

    def test_nested_braces_and_multiline_stem(self):
        text = VALID.replace("已知 $A=", "已知\\textbf{如下条件}\n$A=")
        self.assertEqual(checker.check_file(self.tex(text), "appendix"), ([], []))

    def test_hint_inside_practice_rejected(self):
        errors, _ = checker.check_file(self.tex(VALID.replace("矩阵指数}{", "关键一步：先算特征值}{")), "appendix")
        self.assertTrue(any("解题提示" in e for e in errors), errors)

    def test_hint_after_practice_rejected(self):
        errors, _ = checker.check_file(self.tex(VALID.replace(r"\appendix", r"\textbf{关键一步}：先求逆。" + "\n" + r"\appendix")), "appendix")
        self.assertTrue(any("后紧跟" in e for e in errors), errors)

    def test_definitions_and_comments_not_calls(self):
        text = r"""\begin{document}
\newcommand{\practice}[5]{#3 \pageref{#5}}
\newcommand{\answerstart}[3]{\label{ans:#1}}
% \practice{x}{p1}{题干}{考点}{ans:x}
只有说明，没有练习调用。
\end{document}"""
        errors, _ = checker.check_file(self.tex(text), "appendix")
        self.assertTrue(any("未发现真实" in e for e in errors), errors)
        self.assertFalse(any("#" in e for e in errors), errors)

    def test_empty_missing_and_definition_only_fail(self):
        for value in ("", "  % comment\n", r"\newcommand{\hello}[1]{#1}", r"\begin{document}\end{document}"):
            with self.subTest(value=value):
                self.assertTrue(checker.check_file(self.tex(value))[0])
        self.assertTrue(checker.check_file(self.root / "missing.tex")[0])
        result = subprocess.run([sys.executable, "-B", str(HERE / "check_handout.py"), str(self.root / "missing.tex")], capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"[E]", result.stdout)

    def test_wrong_answer_id_or_label_fails(self):
        for text in (VALID.replace("{ans:p1}", "{ans:p2}", 1), VALID.replace(r"\answerstart{p1}", r"\answerstart{p2}")):
            self.assertTrue(checker.check_file(self.tex(text), "appendix")[0])

    def test_boundary_and_continuation_order(self):
        errors, _ = checker.check_file(self.tex(VALID.replace(r"\appendix", "")), "appendix")
        self.assertTrue(any("附录" in e for e in errors), errors)
        errors, _ = checker.check_file(self.tex(VALID.replace(r"\answercontinue{p1}", r"\answercontinue{unknown}")), "appendix")
        self.assertTrue(any("前没有" in e for e in errors), errors)

    def test_legacy_qstem_is_compatible_without_break_noise(self):
        text = r"""\begin{document}
\hdr{§1}{作业}
\qbreak
\qstem{（课件 p3）已知条件，求解。}
详解见附录第 \pageref{old:answer} 页。
\hdr{附录 A}{解答}
\subhdr{第 1 题}
\label{old:answer}
\qbreak
\qstem{（课件 p3）已知条件，求解。}
详解：运算与核对。
\end{document}"""
        errors, warns = checker.check_file(self.tex(text), "appendix")
        self.assertEqual(errors, [])
        self.assertTrue(warns)
        self.assertFalse(any("qbreak" in w for w in warns))
        errors, _ = checker.check_file(self.tex(text.replace("详解见附录", "关键一步：先设未知量。\n详解见附录")), "appendix")
        self.assertTrue(errors)

    def test_lab_drawing_is_review_hint(self):
        text = r"\subhdr{Q1 画出电路图？}" + "\n" + "题目：画图并解释。\n答案：说明见正文。"
        errors, warns = checker.check_file(self.tex(text), "lab")
        self.assertEqual(errors, [])
        self.assertTrue(any("未见图" in w for w in warns))

    def test_practice_drawing_checked_in_its_answer(self):
        text = VALID.replace("，求解。", "，求解并画图。")
        errors, warns = checker.check_file(self.tex(text), "appendix")
        self.assertEqual(errors, [])
        self.assertTrue(any("对应附录解答未见图" in w for w in warns))
        text = text.replace("按定义计算。", r"按定义计算。\begin{tikzpicture}\end{tikzpicture}")
        self.assertEqual(checker.check_file(self.tex(text), "appendix"), ([], []))

    def test_log_errors_and_success(self):
        log = self.root / "test.log"
        for issue in ("! Undefined control sequence.", r"Overfull \hbox (2pt too wide)",
                      "Missing character: There is no x in font f!", "LaTeX Warning: There were undefined references.",
                      "LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right."):
            with self.subTest(issue=issue):
                log.write_text(issue + "\nOutput written on test.pdf (2 pages).", encoding="utf-8")
                self.assertTrue(checker.check_log(log)[0])
        log.write_text("Output written on test.pdf (2 pages).", encoding="utf-8")
        self.assertEqual(checker.check_log(log), ([], []))
        self.assertTrue(checker.check_log(self.root / "absent.log")[0])
        log.write_text("Compilation stopped", encoding="utf-8")
        self.assertTrue(checker.check_log(log)[0])

    def test_proof_shape_is_a_hint_and_existing_derivation_is_respected(self):
        fixture = HERE / "fixture-example-as-proof.tex"
        errors, warns = checker.check_file(fixture)
        self.assertEqual(errors, [])
        self.assertEqual(len(warns), 1)
        self.assertIn("仅为复核线索", warns[0])
        text = r"""\subhdr{一般推导}
由定义展开，先推导。
\[ X=Y+Z \]
\[ Y+Z=K \]
例如取一个数字核对。
\[ 1+2=3 \]
上述一般关系汇总如下。
\[ \boxed{X=K} \]
"""
        self.assertEqual(checker.check_file(self.tex(text)), ([], []))


class ReaderChecks(unittest.TestCase):
    def test_page_ranges_reject_invalid_values(self):
        self.assertEqual(reader._parse_pages("1-3, 2,5", 5), [0, 1, 2, 4])
        for spec in ("", "0", "6", "3-2", "1-7", "1,,2", "a", "-1"):
            with self.subTest(spec=spec), self.assertRaises(ValueError):
                reader._parse_pages(spec, 5)

    def test_full_text_and_explicit_truncation_in_real_pdf(self):
        import fitz
        with tempfile.TemporaryDirectory(prefix="slide-reader-") as temp:
            pdf = Path(temp) / "slides.pdf"
            with fitz.open() as doc:
                page = doc.new_page()
                page.insert_textbox(fitz.Rect(30, 30, 550, 790), ("A complete sentence for extraction. " * 70), fontsize=10)
                doc.save(pdf)
            command = [sys.executable, "-B", str(HERE / "read_slides.py"), str(pdf)]
            result = subprocess.run(command + ["--json"], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            row = json.loads(result.stdout)["pages"][0]
            self.assertGreater(row["chars"], 1200)
            self.assertEqual(row["chars"], len(row["text"]))
            self.assertFalse(row["truncated"])
            limited = subprocess.run(command + ["--json", "--max-chars", "40"], capture_output=True, text=True, encoding="utf-8")
            row = json.loads(limited.stdout)["pages"][0]
            self.assertTrue(row["truncated"])
            self.assertEqual(row["returned_chars"], 40)
            self.assertEqual(row["omitted_chars"], row["chars"] - 40)
            human = subprocess.run(command + ["--max-chars", "40"], capture_output=True, text=True, encoding="utf-8")
            self.assertIn("已截断", human.stdout)
            bad = subprocess.run(command + ["--pages", "2"], capture_output=True, text=True, encoding="utf-8")
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("越界", bad.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
