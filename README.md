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
# <django-project-name>/settings.py
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
