#!/usr/bin/env bash

# 必要なパッケージを更新・インストール
apt-get update
apt-get install -y build-essential python3-dev

# Python関連ツールを最新版にアップグレード
pip install --upgrade pip setuptools wheel
