import json
import pathlib

data = json.loads(pathlib.Path(r"f:\보호소신규러브몽\data\vod.json").read_text(encoding="utf-8"))
lines = []
for item in data["videos"]["list"]:
    lines.append(
        f"{item.get('encodingOption', {}).get('name')} {item.get('size')} {item.get('duration')} {(item.get('source') or '')[:180]}"
    )
pathlib.Path(r"f:\보호소신규러브몽\data\vod-list.txt").write_text("\n".join(lines), encoding="utf-8")
