import json
import pathlib
from collections import Counter
pets = json.loads(pathlib.Path(r"f:\보호소신규러브몽\data\pets.json").read_text(encoding="utf-8"))
c = Counter(p.get("species") or "없음" for p in pets)
lines = [f"{n}\t{name}" for name, n in c.most_common()]
pathlib.Path(r"f:\보호소신규러브몽\data\species.txt").write_text("\n".join(lines), encoding="utf-8")
print(len(c))
