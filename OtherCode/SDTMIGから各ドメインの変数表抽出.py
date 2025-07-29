import email
from bs4 import BeautifulSoup
import pandas as pd

# === ステップ1：.mhtmlファイルを読み込んでHTMLを抽出 ===
with open("SDTMIG v3.3 _ CDISC.mhtml", "r", encoding="utf-8") as f:
    msg = email.message_from_file(f)

html = ""
for part in msg.walk():
    if part.get_content_type() == "text/html":
        html = part.get_payload(decode=True).decode("utf-8")
        break

soup = BeautifulSoup(html, "html.parser")

# === ステップ2：「Variable Name」を含む表だけを抽出 ===
tables = soup.find_all("table")
target_tables = []

for table in tables:
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    if any("Variable Name" in h for h in headers):
        target_tables.append(table)

# === ステップ3：表をDataFrameに変換して結合・保存 ===
def table_to_df(table):
    rows = []
    for row in table.find_all("tr"):
        cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
        rows.append(cells)
    return pd.DataFrame(rows[1:], columns=rows[0])

dfs = [table_to_df(t) for t in target_tables]
final_df = pd.concat(dfs, ignore_index=True)

# Excelに保存
final_df.to_excel("sdtmig_v3.3_variables.xlsx", index=False)
print("✅ 変数表を抽出して 'sdtmig_v3.3_variables.xlsx' に保存しました！")
