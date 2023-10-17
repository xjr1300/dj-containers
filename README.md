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
├── my_site
│   ├── manage.py
│   └── my_site
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

-ROOT_URLCONF = 'my_site.urls'
+ROOT_URLCONF = 'my_site.my_site.urls'

 [...]

-WSGI_APPLICATION = 'my_site.wsgi.application'
+WSGI_APPLICATION = 'my_site.my_site.wsgi.application'
```

### `WSGI`設定ファイルの編集

```python
# Path: <django-project-name>/<django-project-name>/wsgi.py
 [...]

 from django.core.wsgi import get_wsgi_application

-os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.settings')
+os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.my_site.settings')

 application = get_wsgi_application()
```

### `ASGI`設定ファイルの編集

```python
# Path: <django-project-name>/<django-project-name>/asgi.py
 [...]

 from django.core.asgi import get_asgi_application

-os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.settings')
+os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.my_site.settings')

 application = get_asgi_application()
```

### [参考] 現在のディレクトリ構成

```text
.
├── .env
├── .gitignore
├── README.md
├── db.sqlite3
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

### [試行] `Django`開発用サーバの起動

`Django`プロジェクトが適切に設定されているか確認するために、`Django`開発用サーバーを次の通り起動して、ブラウザで`http://localhost:8000`にアクセスします。

`Django`のインストール画面が**日本語**で表示されれば、`Django`プロジェクトの設定は適切です。

```sh
poetry run python manage.py runserver 0.0.0.0:8000
```
