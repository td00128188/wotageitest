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

        # 如果 Google 順利吐出資料，我們開始解析它
        if response.status_code == 200:
            # 將下載下來的文字按行拆開
            lines = response.text.split("\n")

            name_list = []
            # 遍歷每一行，抓出暱稱欄位
            for line in lines:
                # CSV 是用逗號分開每一欄的，我們用逗號切開
                columns = line.split(",")

                # 🎯 暱稱在 C 欄（也就是第三欄，程式世界陣列索引為 2）
                if len(columns) > 2:
                    name = columns[2].strip()

                    # 過濾掉空白格子、含有換行符號的髒資料，並排除掉標題
                    name = re.sub(r'[\r\n"]', "", name)
                    if name and name != "請輸入您的暱稱" and name != "":
                        name_list.append(name)

            print(f"【Python 連線成功】目前即時人數：{len(name_list)} 人")
            return name_list
        else:
            return ["錯誤：無法讀取 Google 試算表"]

    except Exception as e:
        return [f"後端發生異常：{str(e)}"]