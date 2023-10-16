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

