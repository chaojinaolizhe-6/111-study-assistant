import fitz
d = fitz.open(r"subjects\01-理论力学\讲义\Topic8-刚体运动学P1-精讲-20261025.pdf")
print("pages", d.page_count)
for i in range(d.page_count):
    t = d[i].get_text()
    for key in ("HW8.01", "HW8.02", "HW8.03", "E8.01"):
        if key in t:
            print("p%d: %s" % (i + 1, key))
