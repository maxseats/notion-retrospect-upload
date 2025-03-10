# 프로젝트 설명

이 프로젝트는 노션에 1주일 단위로 회고를 작성 후 업로드하는 기능을 제공합니다.

## 실행 방법

1. 저장소 클론:
    ```bash
    git clone https://github.com/maxseats/notion-retrospect-upload.git
    cd notion-retrospect-upload
    ```
2. `.env` 파일 작성:

    - 다음 링크에서 다운로드할 수 있습니다. ([`.env 파일`](https://www.notion.so/1b20c76f6ccb8058bf97f75cbde32610?pvs=4) / 문의: maxseats)
    
    <br>


3. 디스크 접근 권한 허용:

    - [참고 링크(Case 2)](https://23log.tistory.com/171)

    <br>

    
4. 스크립트 실행(run-project 스크립트 생성 및 Crontab 등록):
    ```bash
    sh script/run-this-for-everything.sh
    ```

## 프로젝트 구조
```
notion-retrospect-upload/
├── intermediate_output/            # 실행 과정 중간 출력 파일들
├── script/
│   ├── crontab-register.sh         # Crontab 등록 스크립트(중간에 생성)
│   ├── run-project.sh              # 프로젝트 실행 스크립트(중간에 생성)
│   └── run-this-for-everything.sh  # 최종 실행 스크립트
├── .env                            # 환경 변수 파일
├── .gitignore
├── gpt_prompt.py                   # GPT 프롬프트 파일
├── main.py                         # 메인 실행 파일
├── make_crontab_sh_file.py         # Crontab 스크립트 파일 생성 코드
├── poetry.lock                     # Poetry lock 파일
├── pyproject.toml                  # Poetry 설정 파일
├── read_pages.py                   # 노션 페이지 읽기 관련 함수 모음
└── README.md                       # 프로젝트 설명
```


