import os
import json
import math
import sys
from pathlib import Path
# 為了抓 config.py，設定 sys.path 在 ROOT
sys.path.append(str(Path(__file__).resolve().parents[1]))
import config # 在 config.py 中填入所有路徑

with open(config.PATH_MANUSCRIPT_PAPER, "r", encoding="utf-8") as file:
    text = file.read()

# 輸入稿紙標題
title = input("請輸入稿紙標題 (ex. 千字文)：")

# 依據空白字元分割
raw_clean_text = "".join(text.lstrip('\ufeff').split())

is_specified = input("是否刪除標點符號(y/n)： ")

if is_specified == 'y':
    exclude_chars = "，。；「」：！？《》、"  # <填入指定刪除的字元>
    clean_text = "".join([char for char in raw_clean_text if char not in exclude_chars])
else:
    clean_text = raw_clean_text

not_repeated = input("是否去除重複字元(y/n)： ")

if not_repeated == 'y':
    unique_characters = set(clean_text)
    with open(config.PATH_CHARACTER_HISTORY, "r", encoding="utf-8") as f:
        history_characters = set(f.read())
    unique_characters = unique_characters - history_characters
else:
    unique_characters = clean_text

# 建立一個txt檔案並將字元寫入其中
output_file = config.PATH_CHARACTER_PAPER
with open(output_file, "w", encoding="utf-8") as file:
    for char in unique_characters:
        file.write(char)

# 計算稿紙字元的數量
count = len(unique_characters)
pages = math.ceil(count/100)

# 將 總字元數 + 稿紙頁數 寫入 info.json 方便稿紙生成調用
paper_info_path = config.PATH_INFO_JSON
os.makedirs(os.path.dirname(paper_info_path), exist_ok=True)

with open(paper_info_path, 'r', encoding='utf-8') as f:
    info = json.load(f)

info["TITLE"] = title
info["TOTAL_CHARACTERS"] = count
info["TOTAL_PAGES"] = pages

with open(paper_info_path, 'w', encoding="utf-8") as f:
    json.dump(info, f, indent=4, ensure_ascii=False)

print("----------已處理完畢----------")
print("稿紙名稱：", title)
print("字元的數量：", count)
print(f"已保存到 {output_file}")
print("info.json 更新完畢")


