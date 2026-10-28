"""Read-only audit of provided lab trace archives; no model calls."""
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def spans(node):
    yield node
    for child in node.get("children", []):
        yield from spans(child)

rows = []
for p in sorted((root / "traces").rglob("CONV-002-run*-turn3.json")):
    d = json.loads(p.read_text())
    tree = d["trace"]
    s = next(x for x in spans(tree) if x["name"] == "agent.summarize")
    text = s["attributes"]["summary.text"]
    rows.append({"profile": tree["attributes"]["run.profile"],
        "session": tree["attributes"]["session.id"],
        "turn": d["turn"], "request":tree["request_id"],
        "amount_held": bool(re.search(r"(?<![0-9])240(?:[.,]00)?(?![0-9])", text)),
        "reason_held": "goods_not_received" in text,
        "wrong_reason": "service_not_rendered" in text})
print(json.dumps(rows, ensure_ascii=False, indent=2))
clean = [r for r in rows if r["profile"] == "clean"]
lesson = [r for r in rows if r["profile"] == "lesson-05"]
assert len(clean)==1 and len(lesson)==5
assert all(r["amount_held"] and r["reason_held"] for r in clean)
assert all(not r["amount_held"] and not r["reason_held"] for r in lesson)
assert len({r["session"] for r in lesson})==5
print("PASS: clean summary retains both entities; all five lesson summaries lose exact values")
