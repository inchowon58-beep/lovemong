import json
import pathlib

stories = json.loads(pathlib.Path(r"f:\보호소신규러브몽\data\stories.json").read_text(encoding="utf-8"))
lines = []
for story in stories:
    lines.append(f"## {story['id']} {story['title']}")
    for block in story["blocks"]:
        if block["type"] == "text":
            lines.append("\n".join(block["lines"]))
            lines.append("---")
    lines.append("")
pathlib.Path(r"f:\보호소신규러브몽\data\story-text.txt").write_text("\n".join(lines), encoding="utf-8")
