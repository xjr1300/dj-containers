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
