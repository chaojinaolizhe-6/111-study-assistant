import fitz
want16 = {5,6,7,9,10,17,18,21,22,23,28,29,32,40,41,42,43}
want17 = {4,6,9,11,12,13,18,20,23,24,25,27,28}
for f, want in [(r"subjects\03-微分方程\课件\16_17_matrix_exponential.pdf", want16),
                (r"subjects\03-微分方程\课件\17_18_Nonhomogeneous-linear-systems.pdf", want17)]:
    d = fitz.open(f); print("#"*80); print(f)
    for i in range(d.page_count):
        if (i+1) in want:
            print(f"\n===== p{i+1} =====")
            print(" ".join(d[i].get_text().split())[:1200])
