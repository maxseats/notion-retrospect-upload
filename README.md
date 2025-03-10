# 프로젝트 설명

- 이 프로젝트는 노션 데이터베이스에 1주일 단위로 회고를 작성 후 업로드하는 기능을 제공합니다. 데이터베이스에 작성한 1주 치 개발일지를 모아 LLM에게 회고 작성을 맡깁니다.
- Crontab을 활용하여 1주일 간격으로 자동 업로드됩니다.(스케줄링 중지를 원할 경우, crontab -r 등의 조치 필요)
- 사전에 Notion API Key와 OpenAI API Key 발급이 필요합니다.

[`Notion API Key 발급 링크`](https://www.notion.so/my-integrations)
[`OpenAI API Key 발급 링크`](https://platform.openai.com/api-keys)


## 실행 방법

1. 저장소 클론:
    ```bash
    git clone https://github.com/maxseats/notion-retrospect-upload.git
    cd notion-retrospect-upload
    ```
2. `.env` 파일 작성:

    [`maxseats의 .env`](https://www.notion.so/1b20c76f6ccb8058bf97f75cbde32610?pvs=4) / 문의: @maxseats
    
    
    ```
    # Notion API Key
    NOTION_API_KEY = "ntn_o~"

    # 회고를 기록할 데이터베이스 ID - 해당 노션 데이터베이스 링크에서 얻기 -> https://www.notion.so/1b00c76f6ccb80599fa8f269f9bca1bb?v=1b00c76f6ccb80629a28000cd2fba0b2&pvs=4 / 여기서 "1b00c76f6ccb80599fa8f269f9bca1bb" 부분이 데이터베이스 ID
    DATABASE_ID = "1b00c76f6ccb80599fa8f269f9bca1bb"

    # OPENAI API Key
    OPENAI_API_KEY = "sk-p~"

    # 사용할 GPT 모델 / "4o-2024-08-06", 4o, 4, 3.5-turbo, 3.5, 3 등
    OPENAI_MODEL = "gpt-4o"

    # 현재 시간대 기준 위치
    TIME_ZONE = "Asia/Seoul"
    ```

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


