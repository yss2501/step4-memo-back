#!/bin/bash
# FastAPIサーバーを仮想環境で起動するスクリプト

cd "$(dirname "$0")"

# 仮想環境をアクティベート
source venv/bin/activate

echo "=== 環境確認 ==="
echo "Python: $(which python)"
echo "仮想環境: $VIRTUAL_ENV"

echo -e "\n=== 依存関係確認 ==="
python -c "import bcrypt; print('bcrypt: OK')"
python -c "import jose; print('jose: OK')"
python -c "import fastapi; print('fastapi: OK')"

echo -e "\n=== FastAPIサーバー起動 ==="
uvicorn main:app --host 0.0.0.0 --port 8000 --reload