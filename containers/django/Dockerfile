# Pythonのイメージを指定
FROM python:3.12-slim-bookworm
# パッケージの更新及びインストール
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    build-essential \
    libgdal-dev \
    libgeos-dev \
    libproj-dev
RUN apt-get -y clean && apt-get -y autoclean && apt-get -y autoremove
RUN rm -rf /var/lib/apt/lists/*
# モジュールインポート次に.pycファイルを作成しない
ENV PYTHONDONTWRITEBYTECODE=1
# 標準出力と標準エラー出力ストリームをバッファしないように強制
ENV PYTHONUNBUFFERED=1
# コンテナのワークディレクトリを/projectに指定
WORKDIR /project
# ローカルのプロジェクトディレクトリの内容を、コンテナの/projectディレクトリの配下に配置
COPY . /project/
RUN pip install --upgrade pip && pip install poetry
# poetryが仮想環境を作成しないように設定
RUN poetry config virtualenvs.create false
# コンテナ側でパッケージをインストール
RUN poetry install
# コンテナのpipのキャッシュをクリア
RUN pip cache purge
# コンテナのpoetryのキャッシュをクリア
RUN poetry cache clear pypi --all
# entrypoint.shに実行権限を付与
RUN chmod 755 entrypoint.sh
