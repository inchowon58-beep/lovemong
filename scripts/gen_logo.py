"""Original Love Mong mark. Reads GEMINI_API_KEY from the environment."""
import base64
import json
import os
import pathlib
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(r"f:\보호소신규러브몽")
DEST = ROOT / "site" / "assets" / "logo"
MODEL = "gemini-3.1-flash-image"
PROMPT = (
    "A finished square logo icon for a pet shelter, flat vector, professional, original. "
    "A warm cream circle. Inside it, a caramel dog on the left and a white cat on the right, "
    "both with closed eyes, gently touching noses. A small solid persimmon heart floats above them. "
    "Bold even outlines, simple shapes, no fur detail, no shading, no 3D. "
    "Colors only: ink brown #241c16, persimmon #e15a32, ivory #fffdf9, cream #f4efe6. "
    "The area outside the circle is the same flat cream #f4efe6. "
    "Centered, with comfortable margin, still clear at a small header size. "
    "No house, no roof, no leaves, no green, no text, no letters, no numbers, no watermark."
)


def post(body: dict, api_key: str) -> dict:
    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.load(response)


def save_image(payload: dict, dest: pathlib.Path) -> None:
    parts = payload["candidates"][0]["content"]["parts"]
    for part in parts:
        inline = part.get("inlineData") or part.get("inline_data")
        if not inline:
            continue
        mime = inline.get("mimeType") or inline.get("mime_type") or "image/png"
        ext = ".jpg" if "jpeg" in mime or "jpg" in mime else ".png"
        target = dest.with_suffix(ext)
        target.write_bytes(base64.b64decode(inline["data"]))
        print(f"image {target.name} {target.stat().st_size}", flush=True)
        return
    texts = [part.get("text", "") for part in parts]
    raise ValueError("no image " + " ".join(texts)[:240])


def main() -> None:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("GEMINI_API_KEY is missing")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    last_error = None
    for attempt in range(3):
        try:
            payload = post(
                {
                    "contents": [{"role": "user", "parts": [{"text": PROMPT}]}],
                    "generationConfig": {
                        "responseModalities": ["TEXT", "IMAGE"],
                        "imageConfig": {"aspectRatio": "1:1"},
                    },
                },
                api_key,
            )
            save_image(payload, DEST)
            last_error = None
            break
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500] if isinstance(exc, urllib.error.HTTPError) else str(exc)
            last_error = detail
            print(f"retry {attempt + 1} {detail}", flush=True)
            time.sleep(2 + attempt)
    if last_error:
        raise SystemExit(last_error)
    print("done", flush=True)


if __name__ == "__main__":
    main()
