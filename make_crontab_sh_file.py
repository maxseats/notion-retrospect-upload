"""crontab 파일 생성을 위한 코드입니다."""

import os


# 절대경로를 알아내는 함수
def get_absolute_path(executable):
    return os.popen(f"which {executable}").read().strip()


def make_run_project_sh():
    # 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = os.path.abspath(os.path.join(current_dir, "script"))

    # 절대경로 알아내기
    pip_path = get_absolute_path("pip")
    poetry_path = get_absolute_path("poetry")
    python_path = get_absolute_path("python")

    # sh 파일 내용
    sh_content = f"""

#!/bin/bash
# 현재 스크립트가 위치한 디렉토리 기준으로 경로 설정
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# PROJECT_DIR로 이동
cd "$SCRIPT_DIR/.."

# pip 절대경로로 poetry 설치
{pip_path} install poetry

# poetry 절대경로로 가상환경 세팅
{poetry_path} install

# run project
{poetry_path} run {python_path} main.py
    
    """

    # sh 파일 생성
    with open(os.path.join(script_dir, "run-project.sh"), "w") as file:
        file.write(sh_content)


def make_crontab_register_sh():
    # 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = os.path.abspath(os.path.join(current_dir, "script"))

    # 절대경로 알아내기
    bash_path = get_absolute_path("bash")

    # sh 파일 내용
    sh_content = f"""
    
chmod +x {script_dir}/run-project.sh

# crontab에 작업을 추가(매주 토요일 정오에 run-project.sh 실행)
echo "0 12 * * 6 {bash_path} {script_dir}/run-project.sh >> {script_dir}/cron.log 2>&1" | crontab -


    """

    # sh 파일 생성
    with open(os.path.join(script_dir, "crontab-register.sh"), "w") as file:
        file.write(sh_content)


if __name__ == "__main__":
    make_run_project_sh()
    make_crontab_register_sh()
