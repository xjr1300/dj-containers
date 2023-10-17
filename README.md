# `dj-containers`

## 概要

`Django`の開発または運用に必要なコンテナを構築するプロジェクトです。

## `poetry`プロジェクトの作成

```sh
mkdir dj-containers && cd dj-containers
poetry init
poetry install
```

> 以降、`dj-containers`ディレクトリを`poetry`ディレクトリと呼びます。
> また、以降、特に記述のない限り、`dj-containers`ディレクトリがカレントディレクトリとして説明します。

## リポジトリの作成

### `.gitignore`ファイルの作成

```.gitignore
# Path: .gitignore
.mypy_cache/
.venv/
__pycache__/
assets/
build/
dist/
eggs/
sdist/
.DS_Store
.cache
.coverage
db.sqlite3
.env
*.log
*.pot
*.pyc
*.py[cod]
*.so
```

> `django`の`collectstatic`コマンドで、`assets`ディレクトリに静的ファイルを収集するため、`assets`ディレクトリを追跡対象にしています。

### リポジトリの初期化

```sh
git init
git add .
git commit -m "Initial commit"
```

### [参考] 現在のディレクトリ構成

```text
.
├── .gitignore
├── README.md
├── poetry.lock
└── pyproject.toml
```

## `Django`プロジェクトの作成

### `Django`プロジェクトの作成

```sh
poetry add django psycopg djangorestframework gunicorn uvicorn python-dotenv
poetry run django-admin startproject <django-project-name>
```

`django-project-name`は任意の`django`プロジェクト名を指定してください。
リポジトリでは`my-site`としています。

### 開発用環境変数ファイルの作成

開発用に環境変数を設定する`.env`ファイルを次のとおり作成します。
なお、`DJANGO_SECRET_KEY`には、`dj-containers/<django-project-name>/settings.py`の`SECRET_KEY`の値を設定してください。

```.env
# Path: .env
DEBUG=True

DJANGO_SECRET_KEY=<django-secret-key>
```

### `Django`プロジェクト設定ファイルの編集

`dj-containers/<django-project-name>/settings.py`を次の通り編集します。

```python
# Path: <django-project-name>/settings.py
+import os
 from pathlib import Path

+from dotenv import load_dotenv

+load_dotenv()

 # Build paths inside the project like this: BASE_DIR / 'subdir'.
 BASE_DIR = Path(__file__).resolve().parent.parent

 [...]

 # SECURITY WARNING: keep the secret key used in production secret!
 # cspell: disable-next-line
-SECRET_KEY = 'django-insecure-)*@k@1^inm%fe%9hm0)p7a+0v8+skdegu@apcwy25q%&0ze8+='
+SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

 # SECURITY WARNING: don't run with debug turned on in production!
-DEBUG = True
+DEBUG = os.environ["DEBUG"]

 [...]

-LANGUAGE_CODE = 'en-us'
+LANGUAGE_CODE = 'ja'

-TIME_ZONE = 'UTC'
+TIME_ZONE = 'Asia/Tokyo'

 [...]

 # Static files (CSS, JavaScript, Images)
 # https://docs.djangoproject.com/en/4.2/howto/static-files/

-STATIC_URL = 'static/'
+STATIC_URL = 'assets/'
+STATIC_ROOT = os.path.join(BASE_DIR, "assets")
```

### [参考] 現在のディレクトリ構成

```text
.
├── .env
├── .gitignore
├── README.md
├── <django-project-name>
│   ├── manage.py
│   └── <django-project-name>
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── poetry.lock
└── pyproject.toml
```

### `manage.py`の移動と編集

`dj-containers/<django-project-name>/manage.py`を`dj-containers/manage.py`に移動して、内容を編集します。

```sh
git mv <django-project-name>/manage.py .
```

```python
# Path: manage.py
 def main():
     """Run administrative tasks."""
-    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<django-project-name>.settings')
+    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<django-project-name>.<django-project-name>.settings')
     try:
         from django.core.management import execute_from_command_line
     except ImportError as exc:
```

### `Django`プロジェクト設定ファイルの編集

```python
# Path: <django-project-name><django-project-name>/settings.py
 [...]

 load_dotenv()

 # Build paths inside the project like this: BASE_DIR / 'subdir'.
-BASE_DIR = Path(__file__).resolve().parent.parent
+BASE_DIR = Path(__file__).resolve().parent.parent.parent

 [...]

-ROOT_URLCONF = '<django-project-name>.urls'
+ROOT_URLCONF = '<django-project-name>.<django-project-name>.urls'

 [...]

-WSGI_APPLICATION = '<django-project-name>.wsgi.application'
+WSGI_APPLICATION = '<django-project-name>.<django-project-name>.wsgi.application'
```

### `WSGI`設定ファイルの編集

```python
# Path: <django-project-name>/<django-project-name>/wsgi.py
 [...]

 from django.core.wsgi import get_wsgi_application

-os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<django-project-name>.settings')
+os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<django-project-name>.<django-project-name>.settings')

 application = get_wsgi_application()
```

### `ASGI`設定ファイルの編集

```python
# Path: <django-project-name>/<django-project-name>/asgi.py
 [...]

 from django.core.asgi import get_asgi_application

-os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<django-project-name>.settings')
+os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<django-project-name>.<django-project-name>.settings')

 application = get_asgi_application()
```

### [参考] 現在のディレクトリ構成

```text
.
├── .env
├── .gitignore
├── README.md
├── manage.py
├── <django-project-name>
│   └── <django-project-name>
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── poetry.lock
└── pyproject.toml
```

### [試行] `Django`開発用サーバの起動

`Django`プロジェクトが適切に設定されているか確認するために、`Django`開発用サーバーを次の通り起動して、ブラウザで`http://localhost:8000`にアクセスします。

`Django`のインストール画面が**日本語**で表示されれば、`Django`プロジェクトの設定は適切です。

```sh
poetry run python manage.py runserver 0.0.0.0:8000
```

## `Django`開発用コンテナのビルドと起動

### `.dockerignore`ファイルの作成

```text
# Path: .dockerignore
.devcontainer/
.mypy_cache/
.ruff_cache/
.venv/
__pycache__/
assets/
.dockerignore
```

### Django開発用コンテナ起動スクリプトの作成

次の`entrypoint.sh`ファイルを作成して、実行権限を付与します。

```sh
# Path: entrypoint.sh
#!/usr/bin/env bash

# データベースのマイグレーションを作成
python manage.py makemigrations --noinput
# データベースのマイグレーションを適用
python manage.py migrate --noinput
# 静的ファイルを収集
python manage.py collectstatic --noinput
# Djangoアプリ起動
if [ $DEBUG = "True" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    # TODO: プロダクション環境の場合はuvicornを起動して、WebサーバーとDjangoアプリを連携
    :
fi
```

```sh
chmod +x entrypoint.sh
```

### Django開発用コンテナイメージの定義

```sh
mkdir -p containers/django
vi containers/django/Dockerfile
```

```dockerfile
# Path: containers/django/Dockerfile
# Pythonのイメージを指定
# Pythonのイメージを指定
FROM python:3.12-slim-bookworm
# パッケージの更新及びインストール
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    vim git \
    sudo \
    curl \
    wget \
    locales \
    tzdata \
    ca-certificates \
    gcc \
    build-essential \
    libgdal-dev \
    libgeos-dev \
    libproj-dev
RUN apt-get -y clean && apt-get -y autoclean && apt-get -y autoremove
RUN rm -rf /var/lib/apt/lists/*
# 日本語環境の設定
RUN sed -i -e 's/# \(ja_JP.UTF-8\)/\1/' /etc/locale.gen && locale-gen
ENV LANG=ja_JP.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
# モジュールインポート次に.pycファイルを作成しない
ENV PYTHONDONTWRITEBYTECODE=1
# 標準出力と標準エラー出力ストリームをバッファしないように強制
ENV PYTHONUNBUFFERED=1
# コンテナのワークディレクトリを/workspaceに指定
WORKDIR /workspace
# ローカルのプロジェクトディレクトリの内容を、コンテナの/workspaceディレクトリの配下に配置
COPY . /workspace/
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
```

> `GeoDjango`を利用することを想定しているため、`libgdal-dev`、`libgeos-dev`、`libproj-dev`をインストールしています。

### `docker-compose.yml`ファイルの作成

```yaml
# Path: docker-compose.yml
version: "3.8"

services:
  app:
    # コンテナ名
    container_name: django-app
    # ビルドコンテキストをカレントディレクトリに設定
    # Dockerfileのパスを指定
    build:
      context: .
      dockerfile: containers/django/Dockerfile
    # ローカルのカレントディレクトリを、コンテナの/workspaceにマウント
    volumes:
      - .:/workspace
    # ローカルの8000ポートを、コンテナの8000ポートにマッピング
    ports:
      - 8000:8000
    # 環境変数ファイルを設定
    env_file:
      - .env
    # コンテナ起動時に実行するコマンドを設定
    entrypoint: /workspace/entrypoint.sh
```

### Django開発用コンテナイメージのビルドと起動

```sh
# コンテナのビルド
docker-compose build
# コンテナの起動
docker-compose up -d
```

### Django開発用アプリケーションコンテナの起動確認

ブラウザで`http://localhost:8000`にアクセスして、`Django`のインストール画面が**日本語**で表示されれば、正常に`Django`プロジェクトは適切に設定されています。

### [参考] 現在のディレクトリ構成

```text
├── .dockerignore
├── .env
├── .gitignore
├── README.md
├── containers
│   └── django
│       └── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── manage.py
├── <django-project-name>
│   └── <django-project-name>
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── poetry.lock
└── pyproject.toml
```

## `PostgreSQL`コンテナのビルドと起動

### 開発用環境変数ファイルの作成

```.env
# Path: .env
 DEBUG=True

 DJANGO_SECRET_KEY=<django secret key>

+POSTGRES_USER=<postgres-user>
+POSTGRES_PASSWORD=<postgres-user-password>
+POSTGRES_DB=<database-name>
+POSTGRES_HOST=postgres-db
+POSTGRES_PORT=5432
+PGPASSWORD="${POSTGRES_PASSWORD}"
```

> `POSTGRES_HOST`変数には、`docker-compose.yml`で後で定義する`PostgreSQL`コンテナのコンテナ名を指定しています。
>
> [`PGPASSWORD`](https://www.postgresql.org/docs/current/libpq-envars.html)変数は、後で定義する`PostgreSQL`コンテナの起動チェックで`psql`コマンドを実行する際に、この変数の値をパスワードとして使用するために設定しています。

### `Django`プロジェクトのデータベース設定

```python
# Path: <django-project-name>/<django-project-name>.settings.py
 [...]
 INSTALLED_APPS = [
     'django.contrib.admin',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.messages',
     'django.contrib.staticfiles',
+    'django.contrib.gis',
 ]

 [...]

 DATABASES = {
     'default': {
-        'ENGINE': 'django.db.backends.sqlite3',
-        'NAME': BASE_DIR / 'db.sqlite3',
+        'ENGINE': 'django.contrib.gis.db.backends.postgis',
+        'NAME': os.environ["POSTGRES_DB"],
+        'USER': os.environ["POSTGRES_USER"],
+        'PASSWORD': os.environ["POSTGRES_PASSWORD"],
+        'HOST': os.environ["POSTGRES_HOST"],
+        'PORT': os.environ["POSTGRES_PORT"],
     }
 }

 [...]
```

### `PostgreSQL`コンテナの定義

```yaml
 services:
   app:
     [...]
     # コンテナ起動時に実行するコマンドを設定
     entrypoint: /workspace/entrypoint.sh
+   # コンテナ間の依存関係を設定
+   depends_on:
+     # dbコンテナが起動してからappコンテナを起動
+     db:
+       condition: service_healthy
+
+  db:
+    # コンテナ名
+    container_name: postgres-db
+    # コンテナイメージを指定
+    image: xjr1300/postgres16-postgis34:latest
+    # ポート番号を設定
+    ports:
+      - 5432:5432
+    # ボリュームを永続化
+    volumes:
+      - postgres-db-data:/var/lib/postgresql/data
+    # 環境変数ファイルを指定
+    env_file:
+      - .env
+    # ヘルスチェック
+    healthcheck:
+      # コンテナ内で実行するコマンド
+      test: psql -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c '\q'
+      # ヘルスチェックの間隔
+      interval: 10s
+      # ヘルスチェックのタイムアウト
+      timeout: 5s
+      # ヘルスチェックのリトライ回数
+      retries: 5
+
+volumes:
+  postgres-db-data:
```

> `xjr1300/postgres16-postgis34:16`イメージは、`Docker Hub`で公開されている[`postgis/postgis`](https://registry.hub.docker.com/r/postgis/postgis/)の`Docker`ファイルを編集して、`adminpack`エクステンションを追加して、ビルドしています。
>
> [参考] `containers/postgres`ディレクトリ

### `PostgreSQL`コンテナの起動確認

```sh
# コンテナを起動
docker-compose up -d
# PostgreSQLコンテナのシェルに接続
docker exec -i -t <postgres-container-id> /bin/bash
# データベースのテーブルを表示
psql -U <postgres-user> -c '\dt'
```

上記を実行して、`django`のデフォルトテーブルが表示されていれば、`PostgreSQL`コンテナが正常に作成され、`Django`開発用アプリケーションコンテナからデータベースにアクセスできています。

## リンター、フォーマッター及び静的型チェッカーの設定

リンター、フォーマッター及び静的型チェッカーには次のパッケージを使用します。

* `isort`: インポートの整理
* `black`、`ruff`: リンター及びフォーマッター
* `mypy`: 静的型チェッカー
* `django-stubs`: `mypy`が使用する`django`用の型ヒント
* `pre-commit`: `git commit`の前に、リンター、フォーマッター及び静的型チェッカーなどを実行する設定を追加

### リンター、フォーマッター及び静的型チェッカーのインストール

```sh
poetry add isort black ruff mypy django-stubs pre-commit
```

### リンター、フォーマッター及び静的型チェッカーの設定

```yaml
# Path: pyproject.toml
 [...]

 [tool.poetry.dependencies]
 python = "^3.11"
 django = "^4.2.6"
 psycopg = "^3.1.12"
 djangorestframework = "^3.14.0"
 gunicorn = "^21.2.0"
 uvicorn = "^0.23.2"
 python-dotenv = "^1.0.0"
+isort = "^5.12.0"
+ruff = "^0.1.0"
+pre-commit = "^3.5.0"
+black = "^23.9.1"
+mypy = "^1.6.0"
+django-stubs = "^4.2.4"

 [build-system]
 requires = ["poetry-core"]
 build-backend = "poetry.core.masonry.api"
+
+[tool.isort]
+py_version = 311
+profile = "black"
+line_length = 120
+
+[tool.black]
+target-version = ["py311"]
+line-length = 120
+
+[tool.ruff]
+target-version = "py311"
+line-length = 120
+select = ["ALL"]
+ignore = [
+    "D104", # Missing docstring in public package
+    "D203", # 1 blank line required before class docstring
+    "D212", # Multi-line docstring summary should start at the first line
+]
+
+[tool.mypy]
+python_version = "3.11"
+plugins = ["mypy_django_plugin.main"]
+
+[tool.django-stubs]
+django_settings_module = "<django-project-name>.<django-project-name>.settings"
```

```Makefile
lint:
    poetry run isort <django-project-name> --check-only
    poetry run black <django-project-name> --check
    poetry run ruff <django-project-name>
fmt:
    poetry run isort <django-project-name>
    poetry run black <django-project-name>
    poetry run ruff <django-project-name> --fix
types:
    poetry run mypy <django-project-name>
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v3.2.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files
  - repo: https://github.com/astral-sh/ruff-pre-commit
    # Ruff version.
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix, <django-project-name>]
```

次の通り、コミット前の`git hook`スクリプトをインストールします。

```sh
poetry run pre-commit install
```

### リンター、フォーマッター及び静的型チェッカーの実行

```sh
# リンターの実行
make lint
# リンター及びフォーマッターの実行
make fmt
# 静的型チェッカーの実行
make types
```

### [参考] 現在のディレクトリ構成

```text
.
├── .dockerignore
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile
├── README.md
├── containers
│   ├── django
│   │   └── Dockerfile
│   └── postgis
│       ├── Dockerfile
│       ├── initdb-postgis.sh
│       └── update-postgis.sh
├── docker-compose.yml
├── entrypoint.sh
├── manage.py
├── <django-project-name>
│   └── <django-project-name>
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── poetry.lock
└── pyproject.toml
```

### `Docker`コンテナの再ビルド

リンター、フォーマッター及び静的型チェッカーをインストールしたり、ソースコードを整形したりしたため、`Docker`コンテナを再ビルドします。

```sh
docker-compose build
docker-compose up -d
```

## コンテナ開発環境の構築

`vscode`の拡張機能`Dev Containers`を使用して、先に作成した`Django`開発用コンテナで開発する環境を構築します。

### `Dev Containers`のインストール

`vscode`の拡張機能`Dev Containers`をインストールしてください。

### `Dev Containers`の設定

1. コマンドパレットを開いて(`Command + Shirt + P`)、`Dev Containers - Reopen in Container`を選択します。
2. 次に`From 'docker-compose.yml'`を選択します。
3. 次に`app`を選択します。
4. 次に`Select additional features to install`で次を選択します。
   1. `Python`
   2. `isort`
   3. `Black`
   4. `Ruff`
   5. `Mypy`
5. 最後に`Keep Defaults`を選択します。

しばらくすると`dj-containers`プロジェクトを開いている`vscode`が閉じられて、`Django`開発用コンテナにアタッチした`vscode`が開きます。
開いた`vscode`で次を実行します。

1. `Open Workspaces...`をクリックします。
2. `Open Folder`で、`/workspace`を指定して`OK`をクリックします。

これで、`Django`開発用コンテナにある本プロジェクトを`vscode`で開くことができました。
`Django`開発用コンテナで実行した内容は、ローカルの本プロジェクトのディレクトリに反映されます。

`vscode`のターミナルで次を実行して、ローカルのブラウザで`http://localhost:8080`にアクセスすると、`django`のインストール成功画面が表示されます。

```sh
python manage.py 0.0.0.0:8080
```

ここで、次に注意してください。

- `8000`番ポートは、`Django`開発用コンテナで使用しているため、`8080`番ポートを使用しています。
- `Django`開発用コンテナでは仮想環境を作成せずに、`Python`本体にパッケージを導入しているため、`poetry run python ...`のように実行できません。

ソースコードの実装は、`Django`開発用コンテナで実施します。

> ローカルで開発しようとすると、`GeoDjango`が要求する`gdal`がインストールされていないなど、エラーが発生する場合があります。

### [参考] 現在のディレクトリ構成

```text
.
├── .devcontainer
│   ├── devcontainer.json
│   └── docker-compose.yml
├── .dockerignore
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile
├── README.md
├── containers
│   ├── django
│   │   └── Dockerfile
│   └── postgis
│       ├── Dockerfile
│       ├── initdb-postgis.sh
│       └── update-postgis.sh
├── docker-compose.yml
├── entrypoint.sh
├── manage.py
├── my_site
│   └── my_site
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── poetry.lock
└── pyproject.toml
```
