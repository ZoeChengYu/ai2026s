from pathlib import Path

# 自動抓取本專案根目錄
ROOT = Path(__file__).resolve().parent

# ROOT底下的子資料夾
DIR_GEN_CP950 = ROOT / "1_generate_CP950"
DIR_GEN_MANUSCRIPT = ROOT / "2_generate_manuscript"

# 常用資料夾
DIR_FONTS = DIR_GEN_MANUSCRIPT / "font_type"    # 電腦字體包資料夾
DIR_CP950_JSON = DIR_GEN_MANUSCRIPT / "CP950"   # 各稿紙 CP950 資料夾
DIR_FINAL_PDF = DIR_GEN_MANUSCRIPT / "manuscripts-final"   # 生成稿紙成果儲存位置

# 常用檔案
PATH_MANUSCRIPT_PAPER = DIR_GEN_CP950 / "manuscript_paper.txt"   # 初始稿紙內容貼在此
PATH_CHARACTER_PAPER = DIR_GEN_CP950 / "character.txt"           # 清洗過的稿紙字元
PATH_INFO_JSON = DIR_GEN_MANUSCRIPT / "info.json"                # 印稿紙的資訊 ex. 姓名、學號、頁數、標題
PATH_ALL_MANUSCRIPT = DIR_GEN_CP950 / "all_manuscript.txt"       # 寫過的 稿紙 1~4 貼在此
PATH_CHARACTER_HISTORY = DIR_GEN_CP950/ "character_history.txt"  # 紀錄寫過的字元

