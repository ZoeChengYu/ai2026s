from tqdm import tqdm
from os import listdir
import multiprocessing as mp
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import os
import json
import sys
from pathlib import Path
# 為了抓 config.py，設定 sys.path 在 ROOT
sys.path.append(str(Path(__file__).resolve().parents[1]))
import config # 在 config.py 中填入所有路徑

with open(config.PATH_INFO_JSON,'r', encoding='utf-8') as f:
    info = json.load(f)
title = info["TITLE"]

dir_title = config.DIR_GEN_MANUSCRIPT / title # 該稿紙的專用資料夾
merge_folder = dir_title / f"{title}-Merge"
pdf_folder = dir_title / f"{title}-PDF"

def svg2pdf(file):
    input_svg = merge_folder / file
    output_pdf = pdf_folder / f"{file}.pdf"
    
    drawing = svg2rlg(str(input_svg))
    renderPDF.drawToFile(drawing, str(output_pdf))

if __name__ == "__main__":
    cpus = mp.cpu_count()  # count of CPU cores
    result_path = f'{dir_title}/{title}-PDF' # 存放資料夾
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    print(f"Using {cpus = }")
    pool = mp.Pool(cpus)
    files = listdir(str(merge_folder))
    for _ in tqdm(pool.imap_unordered(svg2pdf, files), total=info["TOTAL_PAGES"]):
        ...
    pool.close()
    pool.join()
