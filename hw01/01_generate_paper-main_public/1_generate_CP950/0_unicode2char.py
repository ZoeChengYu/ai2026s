# 定義 Unicode 區段及其範圍
unicode_ranges = {
    "Basic Latin": (0x0000, 0x007F),
    "Latin-1 Supplement": (0x0080, 0x00FF),
    "Latin Extended-A": (0x0100, 0x017F),
    "Latin Extended-B": (0x0180, 0x024F),
    "Greek and Coptic": (0x0370, 0x03FF),
    "Currency Symbols": (0x20A0, 0x20CF),
    "Mathematical Operators": (0x2200, 0x22FF),
    "CJK Radicals Supplement": (0x2E80, 0x2EFF),
    "Kangxi Radicals": (0x2F00, 0x2FDF),
    "CJK Symbols and Punctuation": (0x3000, 0x303F),
    "Hiragana": (0x3040, 0x309F),
    "Katakana": (0x30A0, 0x30FF),
    "Bopomofo": (0x3100, 0x312F),
    "Hangul Compatibility Jamo": (0x3130, 0x318F),
    "Kanbun": (0x3190, 0x319F),
    "Bopomofo Extended": (0x31A0, 0x31BF),
    "CJK Strokes": (0x31C0, 0x31EF),
    "Katakana Phonetic Extensions": (0x31F0, 0x31FF),
    "Enclosed CJK Letters and Months": (0x3200, 0x32FF),
    "CJK Compatibility": (0x3300, 0x33FF),
    "Yijing Hexagrams Symbols": (0x4DC0, 0x4DFF),
    "CJK Compatibility Forms": (0xFE30, 0xFE4F),
    "全形標點符號及英文和數字":(0xFF01,0xFF65),
    "中日韓統一表意文字擴充區B列表":(0x20000,0x2A6DD)
}

# 產生 Unicode 文字內容
def generate_unicode_text():
    text_content = ""
    for category, (start, end) in unicode_ranges.items():
        #text_content += f"{category} (U+{start:04X} ~ U+{end:04X}):\n"
        text_content += f"{category} (U+{start:05X} ~ U+{end:05X}):\n"
        text_content += "".join(chr(code) for code in range(start, end + 1) if chr(code).isprintable())
        text_content += "\n\n"
    return text_content

# 將內容寫入 TXT 檔案
def save_to_file(filename="unicode_characters.txt"):
    text = generate_unicode_text()
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Unicode 文字已成功寫入 {filename}")

# 執行程式
save_to_file()
