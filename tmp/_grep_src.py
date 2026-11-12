import io, re, sys
files = {
 "NUM": r"tmp\src\1_оди_н_2_два_3_три_4_четы_ре_5_пять_6_шесть_7_семь_8_во_сем.txt",
 "PAST": r"tmp\src\Глагол_Прошедшее_время.txt",
 "NAST": r"tmp\src\ГЛАГОЛ_НАСТОЯЩЕЕ_ВРЕМЯ.txt",
 "POVT": r"tmp\src\ПОВТОРЕНИЕ.txt",
 "BUD": r"tmp\src\_ГЛАГОЛ_БУДУЩЕЕ_ВРЕМЯ.txt",
}
pats = {
 "NUM": ["юан", "Сколько сто", "час", "Порядков", "недел", "Месяц", "минут"],
 "PAST": ["был", "БЫТЬ", "учил", "игра", "занят", "болен"],
 "NAST": ["-ся", "занима", "учит", "зовут", "по-русски", "язык", "тихо"],
 "POVT": ["зовут", "Союз", " но ", " а ", "меня"],
 "BUD": ["пить", "есть", "буду"],
}
for k, path in files.items():
    txt = io.open(path, encoding="utf-8").read()
    pages = re.split(r"===== PDFPAGE (\d+) \(\d+ chars\) =====", txt)
    page_text = {}
    for i in range(1, len(pages), 2):
        page_text[int(pages[i])] = pages[i+1]
    print("#####", k, "pages:", len(page_text))
    for p in pats[k]:
        hits = [n for n, t in page_text.items() if p.lower() in t.lower()]
        print(f"  {p!r}: {hits[:14]}")
