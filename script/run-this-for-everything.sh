# 현재 스크립트가 위치한 디렉토리 기준으로 경로 설정
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# PROJECT_DIR로 이동
cd "$SCRIPT_DIR/.."

pip install poetry

poetry install

poetry run python make_crontab_sh_file.py

sh script/crontab-register.sh