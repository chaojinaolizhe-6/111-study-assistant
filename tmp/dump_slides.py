import fitz, re
for f in [r"subjects\03-微分方程\课件\16_17_matrix_exponential.pdf",
          r"subjects\03-微分方程\课件\17_18_Nonhomogeneous-linear-systems.pdf"]:
    d = fitz.open(f)
    print("="*70)
    print(f, "pages:", d.page_count)
    for i, p in enumerate(d):
        t = " ".join(p.get_text().split())
        print(f"--- p{i+1}: {t[:180]}")
