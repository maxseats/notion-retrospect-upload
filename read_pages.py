from tqdm import tqdm
import requests


def query_notion_database(
    start_date: str, end_date: str, db_id: str, headers, sort_order: str = "ascending"
) -> list:
    """
    주어진 날짜 범위 내에서 Notion 데이터베이스를 쿼리합니다.
    Args:
        start_date (str): 쿼리할 시작 날짜 (YYYY-MM-DD 형식).
        end_date (str): 쿼리할 종료 날짜 (YYYY-MM-DD 형식).
        sort_order (str, optional): 정렬 순서, "ascending" 또는 "descending". 기본값은 "ascending".
    Returns:
        list: 쿼리 결과를 포함하는 리스트. 오류가 발생한 경우 빈 리스트를 반환합니다.
    """
    url = f"https://api.notion.com/v1/databases/{db_id}/query"

    payload = {
        "filter": {
            "and": [
                {"property": "날짜", "date": {"on_or_after": start_date}},
                {"property": "날짜", "date": {"on_or_before": end_date}},
            ]
        },
        "sorts": [
            {
                "property": "날짜",
                "direction": sort_order,  # "ascending" 또는 "descending"
            }
        ],
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "results" in data:
        return data["results"]
    else:
        print("🚨 오류 발생:", data)
        return []


def get_md_of_a_block(notion, block_id, depth):
    markdown_output = ""  # Markdown 형식으로 저장할 문자열
    try:

        block_info = notion.blocks.retrieve(block_id=block_id)
        block_type = block_info["type"]
        # print(f"{block_id} 해당 블록 info : ", block_info)

        # 블록 타입에 따른 마크다운 형식으로 텍스트 추가
        result = ""
        if block_type == "child_page":
            result = "  " * depth + f"# {block_info['child_page']['title']}\n"
        elif block_type == "heading_2":
            result = (
                "  " * depth
                + "## "
                + " ".join(
                    [
                        text["plain_text"]
                        for text in block_info["heading_2"]["rich_text"]
                    ]
                )
                + "\n"
            )
        elif block_type == "heading_3":
            result = (
                "  " * depth
                + "### "
                + " ".join(
                    [
                        text["plain_text"]
                        for text in block_info["heading_3"]["rich_text"]
                    ]
                )
                + "\n"
            )
        elif block_type == "bulleted_list_item":
            result = (
                "  " * depth
                + "- "
                + " ".join(
                    [
                        text["plain_text"]
                        for text in block_info["bulleted_list_item"]["rich_text"]
                    ]
                )
                + "\n"
            )
        elif block_type == "numbered_list_item":
            result = (
                "  " * depth
                + "1. "
                + " ".join(
                    [
                        text["plain_text"]
                        for text in block_info["numbered_list_item"]["rich_text"]
                    ]
                )
                + "\n"
            )
        elif block_type == "paragraph":
            result = (
                "  " * depth
                + " ".join(
                    [
                        text["plain_text"]
                        for text in block_info["paragraph"]["rich_text"]
                    ]
                )
                + "\n"
            )
        elif block_type == "code":
            code_text = " ".join(
                [text["plain_text"] for text in block_info["code"]["rich_text"]]
            )
            result = "  " * depth + f"```\n{code_text}\n```\n"
        elif block_type == "toggle":
            toggle_text = " ".join(
                [text["plain_text"] for text in block_info["toggle"]["rich_text"]]
            )
            result = "  " * depth + f"> {toggle_text}\n"
        else:
            # print("해당 블록은 처리하지 않음 : ", block_type)
            # print("해당 블록은 처리하지 않음(세부) : ", block_info)
            pass

        # Add the result to markdown_output
        markdown_output += result

        # Remove unwanted characters
        markdown_output = markdown_output.replace("\\xa0", "")
    except Exception as e:
        print(f"❌ 블록 {block_id}을 가져오는 중 오류 발생: {e}")

    return markdown_output


def convert_block_to_markdown(notion, block_id, depth=0):
    """Notion Page를 재귀적으로 탐색하며 블록 별로 Markdown으로 반환"""

    markdown_output = ""  # Markdown 형식으로 저장할 문자열

    while True:
        # 동기화된 블록이면 원본 블록을 대신 가져오기
        block_info = notion.blocks.retrieve(block_id=block_id)
        block_type = block_info["type"]

        if block_type == "synced_block" and block_info["synced_block"]["synced_from"]:
            original_block_id = block_info["synced_block"]["synced_from"]["block_id"]
            block_id = original_block_id
        else:
            break

    # 하위 블록 가져오기
    blocks = notion.blocks.children.list(block_id=block_id).get("results", [])

    for block in tqdm(blocks, desc=f"Processing blocks(depth: {depth})", unit="block"):
        # print("  " * depth + f"- {block['type']} : {block.get('id')}")

        # 하위 블록이 있으면 재귀 호출하여 추가
        if block.get("has_children", True):
            # print('자식이 있는 블록 : ', block['type'])

            markdown_output += get_md_of_a_block(notion, block["id"], depth)
            markdown_output += convert_block_to_markdown(notion, block["id"], depth + 1)
        else:
            # print('자식이 없는 블록 : ', block["id"])
            markdown_output += get_md_of_a_block(notion, block["id"], depth)

    return markdown_output  # 최종 마크다운 문자열 반환
