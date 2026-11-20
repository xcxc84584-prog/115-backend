# 115-backend — Week 1

本專案依照 [Agent Runtime 教材](https://gloomcheng.github.io/115-backend/agent-runtime/) 完成第一週單次模型 API 呼叫作業。

## 安裝與執行

1. 安裝 Python 3。
2. 安裝套件：`python -m pip install -r requirements.txt`
3. 到 [NVIDIA API Catalog](https://build.nvidia.com/) 建立 API key。
4. 在 PowerShell 設定目前工作階段環境變數：
   `$env:NVIDIA_API_KEY = Read-Host 'NVIDIA_API_KEY'`
5. 執行：`python week1_single_call.py`

程式透過 HTTP POST 呼叫 `https://integrate.api.nvidia.com/v1/chat/completions`，
使用模型 `minimaxai/minimax-m3.1-flash`，設定
`max_tokens=512`、`temperature=1`、`top_p=0.95` 與 60 秒 timeout。

會顯示 HTTP status 與 JSON response。正常回應時從
`choices[0].message.content` 擷取模型回答；非 2xx 時輸出 API error。

**安全提醒：** 不要將 NVIDIA API key 或 `.env` 提交至 GitHub，
分享 `curl -v` 觀察紀錄前須遮蔽 Authorization Bearer Token。

依教材，`curl -v` 成功與失敗觀察記錄屬自行練習，不需繳交。
