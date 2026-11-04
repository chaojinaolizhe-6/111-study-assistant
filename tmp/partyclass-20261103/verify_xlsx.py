from openpyxl import load_workbook
p=r"D:\aaa_D_usual\DSH\111学习助手\入党\党的常用名词规范表-20261104.xlsx"
wb=load_workbook(p)
print(wb.sheetnames)
for ws in wb.worksheets:
    print(ws.title, ws.max_row, ws.max_column)
ws=wb["名词表"]
for r in [1,2,20,50,96]:
    print([ws.cell(row=r,column=c).value for c in (1,3,6)])
