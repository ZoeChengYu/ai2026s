from tqdm import tqdm
from pikepdf import Pdf
import json
import os
import sys
from pathlib import Path
# 為了抓 config.py，設定 sys.path 在 ROOT
sys.path.append(str(Path(__file__).resolve().parents[1]))
import config # 在 config.py 中填入所有路徑

with open(config.PATH_INFO_JSON,'r', encoding='utf-8') as f:
    info = json.load(f)
title = info["TITLE"]
stu_id = info['ID']
stu_name = info['NAME']

dir_title = config.DIR_GEN_MANUSCRIPT / title # 該稿紙的專用資料夾
pdf_folder = dir_title / f"{title}-PDF"
output = Pdf.new()

print(f"正在合併 {title} 的所有頁面...")
for i in tqdm(range(1, info["TOTAL_PAGES"] + 1)):
    pdf_filename = f"{i:03d}.svg.pdf"
    pdf_path = pdf_folder / pdf_filename
    
    # 使用 with 確保檔案讀取後會釋放資源
    with Pdf.open(pdf_path) as src:
        output.pages.extend(src.pages)

result_path = config.DIR_FINAL_PDF
result_path.mkdir(parents=True, exist_ok=True)

final_filename = f"{stu_id}_{stu_name}_{title}.pdf"
final_output_path = result_path / final_filename

output.save(final_output_path)

print("合併完成")
print(f"檔案儲存於：{final_output_path}")