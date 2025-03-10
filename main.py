import requests
from datetime import datetime, timedelta
import pytz
from openai import OpenAI
from notion_client import Client
import os
from dotenv import load_dotenv
import logging

from md2notionpage.core import parse_md
from gpt_prompt import *
from read_pages import convert_block_to_markdown, query_notion_database

load_dotenv(override=True)

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")  # Default to "gpt-4o" if not set

TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Seoul")

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# 로거 설정
log_directory = "log"
os.makedirs(log_directory, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_directory, "main.log")),
        logging.StreamHandler(),
    ],
)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_current_time() -> datetime:
    seoul_tz = pytz.timezone(TIME_ZONE)
    current_date = datetime.now(seoul_tz).replace(tzinfo=None)
    return current_date


def make_notion_headers():
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    return headers


def make_notion_page_data(notion_block, today, title):
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "이름": {"title": [{"text": {"content": title}}]},
            "날짜": {"date": {"start": today}},
        },
        "children": notion_block,  # 마크다운을 변환한 블록 추가
    }
    return data


def create_daily_page(title, content):
    """
    주어진 콘텐츠를 사용하여 노션에 일일 페이지를 생성합니다.

    오늘 날짜를 설정하고, 콘텐츠를 마크다운 형식으로 파싱한 후,
    노션 API를 통해 페이지를 생성합니다.

    Args:
        content (str): 생성할 페이지의 콘텐츠를 포함한 md문자열.

    Returns:
        None: 함수는 페이지 생성 성공 여부를 출력합니다.
    """

    today = get_current_time().strftime("%Y-%m-%d")

    notion_block = parse_md(content)

    headers = make_notion_headers()
    data = make_notion_page_data(notion_block, today, title)

    response = requests.post(
        "https://api.notion.com/v1/pages", headers=headers, json=data
    )
    if response.status_code == 200:
        print(f"✅ {today} 페이지 생성 완료!")
    else:
        print("❌ 페이지 생성 실패:", response.text)


def make_weekly_retrospect_by_gpt(page_content):
    """
    주어진 페이지 내용을 바탕으로 GPT를 사용하여 주간 회고를 생성합니다.
    매개변수:
        page_content (str): 주간 회고를 생성할 페이지 내용.
    반환값:
        str: GPT가 생성한 주간 회고 내용.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": f"{GPT_WEEKLY_PERSONA_PROMPT}"},
            {"role": "user", "content": f"{page_content}"},
        ],
    )

    # Extract the response message
    gpt_response = completion.choices[0].message.content
    return gpt_response


def make_title_of_retrospect_by_gpt(gpt_retrospect):
    client = OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": f"{GPT_TITLE_MAKER_PROMPT}"},
            {"role": "user", "content": f"{gpt_retrospect}"},
        ],
    )

    # Extract the response message
    gpt_response = completion.choices[0].message.content
    return gpt_response


def make_page_content_md(page_id):
    """
    주어진 페이지 ID를 사용하여 노션 페이지의 콘텐츠를 생성합니다.

    Args:
        page_id (str): 노션 페이지의 ID.

    Returns:
        str: 페이지 제목과 변환된 마크다운 문자열을 포함한 페이지 콘텐츠.
    """
    notion = Client(auth=NOTION_API_KEY)

    block_info = notion.blocks.retrieve(block_id=page_id)
    title = f"# {block_info['child_page']['title']}\n"

    # 실행 예시
    markdown_string = convert_block_to_markdown(notion, page_id)
    page_content = title + markdown_string

    return page_content


def get_page_ids_by_date(start_date, end_date):
    """
    주어진 시작 날짜와 종료 날짜 사이의 페이지 ID를 가져옵니다.

    Args:
        start_date (str): 조회할 시작 날짜 (YYYY-MM-DD 형식).
        end_date (str): 조회할 종료 날짜 (YYYY-MM-DD 형식).

    Returns:
        list: 주어진 기간 내의 페이지 ID 리스트.
    """

    # ✅ Notion DB에서 해당 기간 내 페이지 가져오기
    pages = query_notion_database(start_date, end_date, DATABASE_ID, headers)

    # ✅ 결과 출력
    print(f"🔍 {start_date} ~ {end_date} 기간 내 페이지 개수: {len(pages)}")
    return pages


def get_total_page_content_md(pages):
    """
    주어진 페이지 목록에서 각 페이지의 콘텐츠를 가져와 하나의 문자열로 결합합니다.
    Args:
        pages (list): 각 페이지의 정보를 담고 있는 딕셔너리들의 리스트.
                      각 딕셔너리는 'id' 키를 포함해야 합니다.
    Returns:
        str: 모든 페이지의 콘텐츠를 결합한 문자열.
    """

    total_content = ""

    for page in pages:
        print(f"- 페이지 ID: {page['id']}")
        page_id = page["id"]
        page_content = make_page_content_md(page_id)
        total_content += page_content + "\n\n"

    return total_content


def upload_notion_weekly_retrospect():
    today = get_current_time()
    START_DATE = (today - timedelta(days=6)).strftime("%Y-%m-%d")
    END_DATE = today.strftime("%Y-%m-%d")

    searched_pages_ids = get_page_ids_by_date(START_DATE, END_DATE)
    total_page_content = get_total_page_content_md(searched_pages_ids)

    # 중간 결과 파일 저장하는 폴더 만들기
    output_path = "intermediate_output"
    os.makedirs(output_path, exist_ok=True)

    # total_page_content txt 파일로 저장
    with open(os.path.join(output_path, "total_page_content.txt"), "w") as f:
        f.write(total_page_content)

    gpt_retrospect = make_weekly_retrospect_by_gpt(total_page_content)

    # gpt_response txt 파일로 저장
    with open(os.path.join(output_path, "gpt_response.txt"), "w") as f:
        f.write(gpt_retrospect)

    retrospect_title = make_title_of_retrospect_by_gpt(gpt_retrospect)

    # retrospect_title txt 파일로 저장
    with open(os.path.join(output_path, "retrospect_title.txt"), "w") as f:
        f.write(retrospect_title)

    create_daily_page(retrospect_title, gpt_retrospect)


if __name__ == "__main__":

    logger.info(f"{get_current_time()} - upload_notion_weekly_retrospect 시작")

    # 최근 6일 간의 개발 일지를 참고하여 주간회고를 작성한 후, 노션에 업로드합니다.
    upload_notion_weekly_retrospect()

    logger.info(f"{get_current_time()} - upload_notion_weekly_retrospect 끝")
