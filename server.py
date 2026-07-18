import json
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

# 1. 初始化 FastAPI 後端伺服器
app = FastAPI()

# 2. 解鎖跨網域限制（CORS）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許任何地方（包括你的本機網頁）連線進來
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get-names")
def get_live_names():
    try:
        # 🎯 終極修復：一字不差的 Google 原生 C 欄純文字匯出專用密令網址！
        csv_url = "https://docs.google.com/spreadsheets/d/13HfjqYz7bmSWPlc0EMIz1iQ3i6yR9qEUoROUq0RqJ7w/export?format=csv"
        
        # 叫 Python 發出網路請求去抓資料
        response = requests.get(csv_url, timeout=10)

        response.encoding = "utf-8"
        # 如果 Google 順利吐出資料，我們開始解析它
        if response.status_code == 200:
            # 將下載下來的文字按行拆開
            lines = response.text.split("\n")

            name_list = []
            # 遍歷每一行，抓出暱稱欄位
            for line in lines:
                columns = line.split(",")

                if len(columns) > 2:
                    name = columns[2].strip()  # 確保精準抓取第三欄

                    # 移除多餘的換行符號與雙引號
                    name = re.sub(r'[\r\n"]', "", name)

                    # 🎯 終極修正：只要開頭是「請輸入您的暱稱」，或者整格是空的，一律不加入名單！
                    if name and not name.startswith("請輸入您的暱稱") and name != "":
                        name_list.append(name)

            print(f"【Python 連線成功】目前即時人數：{len(name_list)} 人")
            return name_list
        else:
            return ["錯誤：無法讀取 Google 試算表"]

    except Exception as e:
        return [f"後端發生異常：{str(e)}"]