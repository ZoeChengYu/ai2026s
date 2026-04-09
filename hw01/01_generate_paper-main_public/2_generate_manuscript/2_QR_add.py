# ADD_QRCODE
import os
import json
import qrcode
import qrcode.image.svg
import sys
from pathlib import Path

# 為了抓 config.py，設定 sys.path 在 ROOT
sys.path.append(str(Path(__file__).resolve().parents[1]))
import config # 在 config.py 中填入所有路徑

with open(config.PATH_INFO_JSON,'r', encoding='utf-8') as f:
    info = json.load(f)

title = info["TITLE"]
dir_title = config.DIR_GEN_MANUSCRIPT / title  # 該稿紙的專用資料夾

# 建立資料夾
table_folder = dir_title / f"{title}-Table"
qrcode_folder = dir_title / f"{title}-qrcode"
merge_folder = dir_title / f"{title}-Merge"

os.makedirs(qrcode_folder, exist_ok=True)
os.makedirs(merge_folder, exist_ok=True)

for i in range(info["TOTAL_PAGES"]):
    page_num = i + 1
    filename = f"{page_num:03d}.svg"
    
    # 讀取原本的 SVG
    source_svg = table_folder / filename
    with open(source_svg, "r", encoding="utf-8") as file:
        svg_content = file.read()

    # 產生 QR Code 圖片
    factory = qrcode.image.svg.SvgPathImage
    qr_code = qrcode.make(str(page_num), image_factory=factory)

    # 將 QR Code 存成檔案
    qr_path = str(qrcode_folder / f"qrcode_{page_num:03d}.svg")
    qr_code.save(qr_path)

    # 讀取 QR Code SVG 檔案
    with open(qr_path, "rb") as qr_file:
        qr_code_svg_str = qr_file.read().decode('utf-8')

    # 找到最後一個 </svg> 標籤的位置
    last_svg_index = svg_content.rfind('</svg>')

    # 在最後一個 </svg> 之前插入 QR Code SVG 字串，並加入 transform 屬性
    updated_svg_content = (
        svg_content[:last_svg_index] +
        f'<g transform="translate(498,772) scale(0.6)">{qr_code_svg_str[qr_code_svg_str.find("<svg"):].strip()}</g>'
        + svg_content[last_svg_index:]
    )

    # 將更新後的 SVG 寫回檔案
    output_path = merge_folder / filename
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(updated_svg_content)

print("QR Code 已成功插入 SVG 中")
