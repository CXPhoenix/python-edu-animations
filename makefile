.PHONY: run_container_and_cleanup help


default: help


# 執行 Manim 相關變數
IMAGE_NAME ?= custom-manim
ROOT_DIR ?= $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
HOST_DIR ?= $(ROOT_DIR)$(PROJECT_NAME)
CONTAINER_DIR ?= /manim
MANIM_FILE_NAME ?= main
MANIM_TARGET ?= OutputScene
QUALITY_FLAG ?= l

ifeq ($(QUALITY_FLAG), l)
	QUALITY = 480p15
else
	ifeq ($(QUALITY_FLAG), m)
		QUALITY = 720p30
	else
		ifeq ($(QUALITY_FLAG), h)
			QUALITY = 1080p60
		else
			ifeq ($(QUALITY_FLAG), p)
				QUALITY = 1440p60
			else
				ifeq ($(QUALITY_FLAG), k)
					QUALITY = 2160p60
				else
					QUALITY = 480p30
				endif
			endif
		endif
	endif
endif

MANIM_EXE ?= manim -q$(QUALITY_FLAG) $(MANIM_FILE_NAME).py $(MANIM_TARGET)
FILES_TO_DELETE ?= $(HOST_DIR)/media/videos/$(MANIM_FILE_NAME)/$(QUALITY)/partial_movie_files

# 目標：新增一個新的影片專案資料夾
create:
	@if [ -z "$(PROJECT_NAME)" ]; then \
		echo "Error: Environment variable PROJECT_NAME is not set or is empty."; \
		exit 1; \
	fi
	@echo "正在建立 Manim 專案..."
	mkdir -p $(ROOT_DIR)$(PROJECT_NAME)
	@echo "正在建立必要目錄..."
	mkdir -p $(ROOT_DIR)$(PROJECT_NAME)/audio
	mkdir -p $(ROOT_DIR)$(PROJECT_NAME)/images
	@echo "正在複製 example"
	cp main.py.example $(ROOT_DIR)$(PROJECT_NAME)/main.py
	@echo "正在建立 README..."
	touch $(ROOT_DIR)$(PROJECT_NAME)/README.md
	@echo "建立完成！"

# 目標：執行 Docker 容器並在結束後清理
build:
	@if [ -z "$(PROJECT_NAME)" ]; then \
		echo "Error: Environment variable PROJECT_NAME is not set or is empty."; \
		exit 1; \
	fi
	@echo "正在啟動 Manim 容器..."
	docker run --rm -v "$(HOST_DIR):$(CONTAINER_DIR)" $(IMAGE_NAME) $(MANIM_EXE)
	@echo "Manim 製作完成。"
	@echo "正在清理綁定掛載目錄下的檔案：$(FILES_TO_DELETE)..."
	rm -rf $(FILES_TO_DELETE)
	@echo "清理完成。"

gif:
	@if [ -z "$(PROJECT_NAME)" ]; then \
		echo "Error: Environment variable PROJECT_NAME is not set or is empty."; \
		exit 1; \
	fi
	@echo "正在啟動 Manim 容器..."
	docker run --rm -v "$(HOST_DIR):$(CONTAINER_DIR)" $(IMAGE_NAME) manim --format gif $(MANIM_FILE_NAME).py $(MANIM_TARGET)
	@echo "Manim 製作完成。"
	@echo "正在清理綁定掛載目錄下的檔案：$(FILES_TO_DELETE)..."
	rm -rf $(FILES_TO_DELETE)
	@echo "清理完成。"

instructs:
	@echo "查詢 Manim 指令集"
	docker run --rm $(IMAGE_NAME) manim $(MANIM_COMMAND) --help

# 目標：顯示幫助訊息
help:
	@echo "可用命令："
	@echo "  make help					- 顯示此幫助訊息。"
	@echo "	---------- ******** make TARGET ******** ----------"
	@echo "  make instructs [MANIM_COMMAND=MANIM_COMMAND]	- 查詢 manim 相關指令。"
	@echo "  make create PROJECT_NAME=YOUR_PROJECT_NAME	- 建立新的 Manim 影片專案。"
	@echo "  make build PROJECT_NAME=YOUR_PROJECT_NAME   	- 啟動 Manim Container 製作影片，並在結束後清理暫存的 Frames。"
	@echo "  make gif PROJECT_NAME=YOUR_PROJECT_NAME   	- 啟動 Manim Container 製作 GIF，並在結束後清理暫存的 Frames。"

