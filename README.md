# Python 程式設計技巧系列
![Docker](https://img.shields.io/badge/docker-custom%20image-8574bd.svg?style=flat&logo=docker&logoColor=white&labelColor=%230db7ed)
![Google Gemini](https://img.shields.io/badge/google%20gemini-8E75B2?style=flat&logo=google%20gemini&logoColor=white)
![Python](https://img.shields.io/badge/python-with%20manim-3670A0?style=flat&logo=python&logoColor=ffdd54)

## ABSTRACT
這個專案是利用 Manim 來製作一系列關於 Python 程式設計技巧的動畫影片。我們整合了 Google Gemini 2.5 Pro 作為輔助工具，用來生成動畫內容，並使用 Gemini 2.5 Pro preview TTS 功能來產生語音介紹，讓影片更具互動性和教育性。專案目標是為學習者提供視覺化且易懂的 Python 教學資源，涵蓋基礎技巧到進階應用。

## INSTALLATION AND CONFIGURATIONS
要運行這個專案，您需要先安裝必要的依賴項目。請確保您的系統符合以下要求：

### REQUIREMENTS
- Python 3.12.9（已設定於 .python-version 檔案）。
- Manim 圖形庫（可透過 pip 安裝）。

> [!TIP]
> 詳細的 [Manim 安裝](https://docs.manim.community/en/stable/installation.html)請見 [Manim Official Documentation](https://docs.manim.community/en/stable/index.html)
>
> 這邊為了不麻煩，所以此專案預設使用 `Docker` 來處理影片產生問題。詳情可見此[說明](https://docs.manim.community/en/stable/installation/docker.html)
>
> 當然，此專案也十分適合使用 `Jupyter Notebook` 或是 `Google Colab`。詳情請見此[說明](https://docs.manim.community/en/stable/installation/jupyter.html)

### INSTALLATION
1. 克隆這個儲存庫：
   ```
   git clone https://github.com/CXPhoenix/python-edu-animations.git  # 替換為實際儲存庫 URL
   cd python_explain_video
   ```

2. 建立虛擬環境（推薦）：
   ```
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate  # Windows
   ```

3. 安裝依賴：
   使用 uv 作為套件管理器：
   ```
   uv pip install -r requirements.txt  # 如果有 requirements.txt 檔案
   uv pip install manim  # 如果未包含在 requirements.txt
   ```

## USAGE
> [!WARNING]
> 在開始前，請確保您已安裝 Docker 和 make。如果尚未安裝，請先執行以下命令：
> - 安裝 make（如果您的系統未有）：在 macOS 上，使用 `brew install make`；在 Linux 上，使用適當的套件管理器。
> - 安裝 Docker：從官方網站下載並安裝。
> - 建置 Docker 映像檔：執行 `docker build -t custom-manim -f Dockerfile.custom-manim .`。

一旦安裝完成，您可以開始生成影片。以下是基本步驟：

1. 使用 make 建立新專案：
   - 執行 `make create PROJECT_NAME=YOUR_PROJECT_NAME` 來設定新專案。

> [!WARNING]
> 這邊要注意，記得要帶入 `PROJECT_NAME` 喔！

2. 編輯腳本：
   - 開啟 `YOUR_PROJECT_NAME/main.py`，修改影片內容、Python 技巧範例。
   - 這邊你可以搭配 Google Gemini 或其他任何 LLM 製作。

> [!NOTE]
> 詳細 Prompt 尚在實驗。
> 
> 若想知道最新的 Prompt 進度，可以看[這個 repository](https://github.com/CXPhoenix/prompt-engineer)。

3. 運行 Manim 來生成動畫：
   ```
   make build PROJECT_NAME=YOUR_PROJECT_NAME
   ```

4. 觀看輸出：
   - 生成的影片會儲存在 `YOUR_PROJECT_NAME/media/` 目錄。您可以使用任何媒體播放器開啟檔案。

## CONTRIBUTE
歡迎大家貢獻！如果您想參與：
- 提出問題或 Pull Request。
- 新增更多 Python 技巧的場景。
- Prompt 產生 Manim 與 TTS 文本技巧。

請遵守我們的程式碼規範，並在提交前測試您的變更。

## LICENCE
這個專案使用 Apache License 2.0 授權。詳情請見 LICENSE 檔案。

## 致謝
感謝 Manim 社區和 Google Gemini 團隊提供的工具，讓教育內容製作變得更簡單。
