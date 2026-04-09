import json
import os
import sys
from pathlib import Path
# 為了抓 config.py，設定 sys.path 在 ROOT
sys.path.append(str(Path(__file__).resolve().parents[1]))
import config # 在 config.py 中填入所有路徑

with open(config.PATH_CHARACTER_PAPER, 'r', encoding='utf-8') as file:
    text = file.read()

with open(config.PATH_INFO_JSON,'r', encoding='utf-8') as f:
    info = json.load(f)
title = info["TITLE"]

# 使用列表推導式將字串分割為單個字元的列表
chinese_characters = [char for char in text]

unicode_characters = []

# 轉成 Unicode 編碼
for character in chinese_characters:
    unicode_code = "0x" + hex(ord(character))[2:].upper().zfill(4)
    unicode_characters.append({
        "Character": character,
        "UNICODE": unicode_code
    })

is_sorted = input("是否按照 unicode 排序(y/n)： ")
if is_sorted == 'y':
    unicode_characters = sorted(
        unicode_characters, 
        key=lambda x: int(x["UNICODE"][2:], 16)
    )


# CP950 清單 --> 繁體中文字集
data_dict = {"CP950": unicode_characters}

# 保存文件
folder_path = config.DIR_CP950_JSON
folder_path.mkdir(parents=True, exist_ok=True)

# 使用 / 拼接路徑，這樣就不用擔心反斜線 \ 的問題
final_path = folder_path / f"CP950-{title}.json"

with open(final_path, "w", encoding="utf-8") as json_file:
    json.dump(data_dict, json_file, ensure_ascii=False, indent=2)

print(f"已產生 CP950-{title}.json")