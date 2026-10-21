"""Ask Gemini for interchangeable paragraph variants. The key stays in the environment."""
import json
import os
import pathlib
import urllib.request

ROOT = pathlib.Path(r"f:\보호소신규러브몽")
DEST = ROOT / "data" / "seo_copy.json"
MODEL = "gemini-3.8-flash"
PROMPT = """
러브몽 보호소 안내문 단락을 JSON으로만 작성하세요. 설명 문장은 쓰지 마세요.
보호소는 전국 전화 상담입니다. 지역마다 지점 주소, 수수료, 즉시 입소, 무료라는 가격은 만들지 마세요.
무료분양 글도 판매나 0원 나눔처럼 쓰지 말고, 입양은 전화 상담 뒤 만나는 절차라고 쓰세요.
자리가 없으면 맡길 수 없다고 쓰세요.

자리표시는 반드시 이 글자만 사용합니다. {지역} {키워드} {동물} {전화}
{키워드}는 한 단락에 한 번만 넣고, 나머지는 자연스러운 한국어로 쓰세요.
각 단락은 2문장입니다.

키는 surrender, shelter, adopt 세 개입니다.
각 키 안에 p1 p2 p3 p4가 있고, 각각 문자열 5개입니다.
p1은 그 검색이 무엇인지 바로 답합니다.
p2는 전화에서 나이와 건강, 사정을 듣고 자리를 확인한다고 씁니다.
p3는 surrender면 파양 뒤 사진과 입양 공고, shelter면 보호와 입양 안내, adopt면 입양 상담과 만남입니다.
p4는 이 페이지의 사진과 이야기가 실제 보호소 기록이며 전화로 이어진다고 씁니다.
서로 다른 번호의 단락을 섞어도 순서가 맞게, 각 단락은 자기 역할만 말합니다.
""".strip()


def main() -> None:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("GEMINI_API_KEY is missing")
    body = {
        "contents": [{"role": "user", "parts": [{"text": PROMPT}]}],
        "generationConfig": {
            "temperature": 0.7,
            "responseMimeType": "application/json",
        },
    }
    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        payload = json.load(response)
    text = payload["candidates"][0]["content"]["parts"][0]["text"]
    data = json.loads(text)
    DEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", DEST.name)


if __name__ == "__main__":
    main()
