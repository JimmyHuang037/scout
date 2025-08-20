print("hello")
import pandas as pd

# 读取 CSV
df = pd.read_csv("scores.csv")

# 转换并保存为 Excel
df.to_excel("scores.xlsx", index=False, engine="openpyxl")
print("转换完成: scores.xlsx")
