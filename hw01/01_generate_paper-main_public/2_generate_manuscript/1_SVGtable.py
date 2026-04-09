# -*- coding: utf-8 -*-
import json
import numpy as np
from tqdm import tqdm
import multiprocessing as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os
import matplotlib.font_manager as fm
from fontTools.ttLib import TTFont
import sys
from pathlib import Path
# 為了抓 config.py，設定 sys.path 在 ROOT
sys.path.append(str(Path(__file__).resolve().parents[1]))
import config # 在 config.py 中填入所有路徑


# 讀取 info.json 稿紙字元數 及 頁數
with open(config.PATH_INFO_JSON,'r', encoding='utf-8') as f:
    info = json.load(f)

total_characters = info["TOTAL_CHARACTERS"]
total_pages = info["TOTAL_PAGES"]
title = info["TITLE"]

dir_title = config.DIR_GEN_MANUSCRIPT / title # 該稿紙的專用資料夾
table_folder = dir_title / f"{title}-Table"

font_setting = [
    {"name": "NotoSansTC", "path": f"{config.DIR_FONTS}/NotoSansTC-ExtraLight.ttf"},
    {"name": "FreeSans", "path": f"{config.DIR_FONTS}/FreeSans.ttf"}
]

font_objects = []
for setting in font_setting:
    if os.path.exists(setting["path"]):
        fm.fontManager.addfont(setting["path"])
        prop = fm.FontProperties(fname=setting["path"])
        # 使用 fontTools 讀取字元表
        ttfont = TTFont(setting["path"])
        cmap = ttfont.getBestCmap()
        font_objects.append({
            "prop": prop,
            "cmap": cmap,
            "name": setting["name"]
        })

noto_prop = next((obj["prop"] for obj in font_objects if obj["name"] == "NotoSansTC"), None)

def get_best_font_prop(char):
    """回傳第一個支援該字元的字體屬性"""
    target_unicode = ord(char)
    for obj in font_objects:
        if target_unicode in obj["cmap"]:
            return obj["prop"]
    return None


def decimal_to_binary(number, digits):
    index = digits - 1
    binaries = [0] * digits
    while number > 0:
        binaries[index] = number % 2  # True / False
        index -= 1
        number >>= 1
    return binaries  # list of booleans


def create_plot(page):
    # figure
    fig = plt.figure(
        num=page, figsize=(8.27, 11.69), dpi=72, facecolor="white"
    )  # figure size (inches)
    axes = plt.subplot(111)

    plt.text(125, 7, "生成式人工智慧導論", fontsize=12.5, color="black", fontproperties=noto_prop)
    student = info["ID"] + "_" + info["NAME"]
    plt.text(85, 7, student, fontsize=12.5, color="black", fontproperties=noto_prop)
    number = info["NUMBER"]
    plt.text(55, 7,"114年度第二學期", fontproperties=noto_prop)

    table_square(axes)

    # page number
    temp_page = page + 1

    plt.text(
        175,
        7,
        "第 {}/{} 頁".format(temp_page, total_pages),
        fontsize=12.5,
        color="black",
        fontproperties=noto_prop
    )
    plt.text(
        10,
        8,
        "字順 {}-{}".format(100 * (temp_page - 1) + 1, 100 * temp_page),
        fontsize=17,
        color="black",
        fontproperties=noto_prop
    )
    plt.text(88, 285, "頁碼", fontsize=11, color="black", fontproperties=noto_prop)
    rect = patches.Rectangle(
        (98, 279), 58, 9, linewidth=1, edgecolor="black", facecolor="black", fill=False
    )
    axes.add_patch(rect)
    plt.text(158, 285, str(temp_page), fontsize=11, color="black", fontproperties=noto_prop)

    # decimal to binary
    binaries = decimal_to_binary(temp_page, 8)

    # square
    for j, fill in enumerate(binaries):
        rect = patches.Rectangle(
            (100 + 7 * j, 281),
            5,
            5,
            linewidth=1,
            edgecolor="black",
            facecolor="black",
            fill=fill,
        )
        axes.add_patch(rect)

    plt.text(8, 285, "編號", fontsize=11, color="black", fontproperties=noto_prop)
    rect = patches.Rectangle(
        (18, 279), 58, 9, linewidth=1, edgecolor="black", facecolor="black", fill=False
    )
    axes.add_patch(rect)
    plt.text(78, 285, str(number), fontsize=11, color="black", fontproperties=noto_prop)

    # decimal to binary
    binaries = decimal_to_binary(number, 8)

    # number square
    for j, fill in enumerate(binaries):
        rect = patches.Rectangle(
            (20 + 7 * j, 281),
            5,
            5,
            linewidth=1,
            edgecolor="black",
            facecolor="black",
            fill=fill,
        )
        axes.add_patch(rect)

def read_json(file):
    if not os.path.exists(file):
        print(f"找不到 JSON 檔案: {file}")
        return []
    with open(file, 'r', encoding='utf-8') as f:
        try:
            p = json.load(f)
            v = [""] * total_characters
            for i in range(total_characters):
                try:
                    # 確保抓取的是 JSON 裡的 unicode
                    code = p["CP950"][i]["UNICODE"][2:6]
                    v[i] = "\\u{}".format(code)
                except:
                    v[i] = ""
            return v
        except Exception as e:
            print(f"解析 JSON 失敗: {e}")
            return []

def print_font(count, page, unicode_list, fnip):
    index = 0
    X = np.arange(7.5, 192.5, 20)
    Y = np.arange(21, 281, 26)
    
    for j in range(10):
        for i in range(10):
            if count >= total_characters:
                continue
            
            char_code = unicode_list[count]
            if char_code == "123" or not char_code:
                fnip[page][index] = ""
            else:
                # 解碼 Unicode 字串 (例如 \u0370 -> 實際字元)
                actual_char = char_code.encode("ascii").decode("unicode-escape")
                
                # 取得該字元最適合的字體
                best_prop = get_best_font_prop(actual_char)
                
                # 畫出文字
                plt.text(
                    X[i] + 1,
                    Y[j] - 3,
                    actual_char,
                    fontsize=14,
                    color="black",
                    alpha=0.7,
                    fontproperties=best_prop  # 重點：手動指定字體屬性
                )
                
                # 畫出 Unicode 編碼小字
                plt.text(
                    X[i] + 8.5,
                    Y[j] - 3,
                    char_code[2:6],
                    fontsize=8,
                    color="black",
                    alpha=0.7,
                    fontproperties=noto_prop
                )
                fnip[page][index] = char_code[2:6]
            
            index += 1
            count += 1
            
            
def table_square(axes):
    X = np.arange(7.5, 192.5, 20)
    Y = np.arange(21, 281, 26)
    for j in range(10):
        for i in range(10):
            rect = patches.Rectangle(
                (X[i], Y[j]),
                15,
                15,
                linewidth=1,
                #edgecolor="#9ACD32",
                edgecolor="#000000",
                alpha=1,
                #facecolor="black",
                facecolor="#3C3C3C",
                fill=False,
            )
            axes.add_patch(rect)

            # 書寫輔助虛線
            # axes.plot([X[i]+7.5, X[i]+7.5], [Y[j], Y[j]+15], linewidth=0.4, color='#9ACD32', alpha=0.6, linestyle='--', dashes=(8, 8))
            # axes.plot([X[i], X[i]+15], [Y[j]+7.5, Y[j]+7.5], linewidth=0.4, color='#9ACD32', alpha=0.6, linestyle='--', dashes=(8, 8))
            # axes.plot([X[i], X[i]+15], [Y[j]+12, Y[j]+12], linewidth=0.4, color='#9ACD32', alpha=0.6, linestyle='--', dashes=(8, 8))

            axes.plot(
                [X[i] + 0.5, X[i] + 2],
                [Y[j] - 7.5, Y[j] - 7.5],
                linewidth=0.4,
                color="black",
                alpha=0.4,
            )  ## v
            axes.plot(
                [X[i] + 5, X[i] + 6.5],
                [Y[j] - 7.5, Y[j] - 7.5],
                linewidth=0.4,
                color="black",
                alpha=0.4,
            )
            axes.plot(
                [X[i] + 0.5, X[i] + 2],
                [Y[j] - 1.5, Y[j] - 1.5],
                linewidth=0.4,
                color="black",
                alpha=0.4,
            )
            axes.plot(
                [X[i] + 5, X[i] + 6.5],
                [Y[j] - 1.5, Y[j] - 1.5],
                linewidth=0.4,
                color="black",
                alpha=0.4,
            )
            axes.plot(
                [X[i] + 0.5, X[i] + 0.5],
                [Y[j] - 7.5, Y[j] - 6],
                linewidth=0.4,
                color="black",
                alpha=0.4,
            )  ## h
            axes.plot(
                [X[i] + 0.5, X[i] + 0.5],
                [Y[j] - 3, Y[j] - 1.5],
                linewidth=0.4,
                color="black",
                alpha=0.4,
            )
            axes.plot(
                [X[i] + 6.5, X[i] + 6.5],
                [Y[j] - 7.5, Y[j] - 6],
                linewidth=0.4,
                color="black",
                alpha=0.4,
            )
            axes.plot(
                [X[i] + 6.5, X[i] + 6.5],
                [Y[j] - 3, Y[j] - 1.5],
                linewidth=0.4,
                color="black",
                alpha=0.4,
            )

        axes.plot(
            [5, 205],
            [Y[j] + 16.5, Y[j] + 16.5],
            linewidth=0.3,
            color="black",
            alpha=0.4,
        )  ## vvvv

def output_svg(filename):
    plt.axis("off")  # 刪除座標軸
    plt.xlim(0, 210)
    plt.ylim(297, 0)
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)  # 刪除白邊
    plt.margins(0, 0)
    plt.savefig(table_folder / f"{filename}.svg")

def pipeline(args):
    (page, count, unicode_list) = args # 包裹內容：頁碼, 起始位置, 完整清單
    # 子進程需要自己的 fnip 局部變數 (或直接忽略，因為主要是畫圖)
    local_fnip = [[""] * 100 for _ in range(total_pages)]
    try:
        create_plot(page)
        print_font(count, page, unicode_list, local_fnip)
        output_svg("{:03d}".format(page + 1))
    finally:
        plt.close('all')


# fnip = [[""] * 100 for _ in range(total_pages)]  # Font Number in Page (Unicode)


if __name__ == "__main__":
    cp950_path = config.DIR_CP950_JSON / f"CP950-{title}.json"
    unicode_data = read_json(cp950_path)

    if not unicode_data:
        print("錯誤：無法讀取 Unicode 資料，請確認是否先跑了 2_generate_CP950.py")
        sys.exit()

    cpus = mp.cpu_count()  # count of CPU cores
    
    worker_args = [
        (p, p * 100, unicode_data) 
        for p in range(total_pages)
    ]

    result_path = table_folder # 存放資料夾
    
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    print(f"Using {cpus = }")
    pool = mp.Pool(cpus)
    for _ in tqdm(pool.imap_unordered(pipeline, worker_args), total=total_pages):
        pass
    pool.close()
    pool.join()