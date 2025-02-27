# ベースイメージとしてPython 3.8を使用
FROM python:3.8-slim

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    pkg-config \ 
    default-libmysqlclient-dev \
    gcc \ 
    build-essential \ 
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /code

# Python仮想環境のセットアップ
RUN python -m venv /venv

# 仮想環境のPATHを設定
ENV PATH="/venv/bin:$PATH"

# Python依存関係のインストール
COPY ./requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# MySQL用のPythonパッケージをインストール
RUN pip install mysqlclient

# アプリケーションコードをコピー
COPY ./hackathonbasic /code/
