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
     
    
3. 프로젝트를 실행합니다(가상환경 자동 세팅):
    ```bash
    sh script/run-project.sh
    ```

## 프로젝트 구조
```
notion-retrospect-upload/
├── intermediate_output/  # 실행 과정 중간 출력 파일들
├── script/
│   └── run-project.sh    # 프로젝트 실행 스크립트
├── .env                  # 환경 변수 파일
├── .gitignore
├── gpt_prompt.py         # GPT 프롬프트 파일
├── main.py               # 메인 실행 파일
├── poetry.lock           # Poetry lock 파일
├── pyproject.toml        # Poetry 설정 파일
├── read_pages.py         # 노션 페이지 읽기 관련 함수 모음
└── README.md             # 프로젝트 설명
```


