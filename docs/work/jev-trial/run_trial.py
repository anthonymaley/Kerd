#!/usr/bin/env python3
"""Ask Jev to grade Kerd's front-page claims and compare with recorded verdicts.

Three conditions, one request per item:
  A  claim alone   -> is this checkable at all?          (truth: label != UNPROVABLE)
  B  claim+evidence -> proved / not yet run / wrong / not checkable
  C  sentence+evidence -> does the sentence claim more than the evidence? (Noul)

Reads JEV_API_KEY (or TYPESAFE_API_KEY) from the environment or the repo's .env;
never prints it. --dry-run builds every request and sends nothing.
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
URL = "https://api.typesafe.ai/v1/systemone"

VERDICTS = {
    "PROVED": "The evidence shows the claim is true as written.",
    "UNRUN": "The claim could be checked by a concrete run or observation, but the evidence shows no such check has been done.",
    "KNOWN-WRONG": "The evidence shows the claim is false or claims more than is true.",
    "UNPROVABLE": "As written, the claim is a value judgment, instruction, intention or undefined term that no observation could settle.",
}


def api_key():
    for name in ("JEV_API_KEY", "TYPESAFE_API_KEY"):
        if os.environ.get(name):
            return os.environ[name]
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            k, _, v = line.partition("=")
            if k.strip() in ("JEV_API_KEY", "TYPESAFE_API_KEY") and v.strip():
                return v.strip().strip('"').strip("'")
    sys.exit("no JEV_API_KEY in the environment or .env")


def clean(claim):
    return re.sub(r"\s*\(L[\d\u2013\-, L]+\)", "", claim).strip()


def requests(data):
    for c in data["claims"]:
        yield ("A", c["id"], c["label"] != "UNPROVABLE", {
            "state": f"A sentence from a software project's README:\n\n{clean(c['claim'])}",
            "questions": {"checkable": {
                "type": "noul",
                "instructions": "Some concrete observation, run or document check could show this sentence true or false as written.",
            }},
        })
    for c in data["claims"]:
        if c.get("exclude_from_evidence_condition"):
            continue
        yield ("B", c["id"], c["label"], {
            "state": f"Claim from a software project's README:\n{clean(c['claim'])}\n\nWhat a reviewer found when checking it against the repository:\n{c['evidence']}",
            "questions": {"verdict": {
                "type": "choice",
                "instructions": "Given what the reviewer found, which verdict does the claim deserve?",
                "criteria": VERDICTS,
            }},
        })
    for o in data["overstatements"]:
        yield ("C", o["id"], o["overclaims"], {
            "state": f"Evidence:\n{o['evidence']}\n\nSentence written about it:\n{o['sentence']}",
            "questions": {"overclaims": {
                "type": "noul",
                "instructions": "The sentence claims more than the evidence shows, or states something the evidence contradicts.",
            }},
        })


def ask(key, body, tries=4):
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST", headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for n in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and n < tries - 1:
                time.sleep(2 ** n)
                continue
            return {"error": e.code, "detail": e.read().decode(errors="replace")[:500]}
        except (urllib.error.URLError, TimeoutError) as e:
            if n < tries - 1:
                time.sleep(2 ** n)
                continue
            return {"error": "connection", "detail": str(e)[:500]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--limit", type=int, help="send only the first N requests")
    p.add_argument("--out", default=str(HERE / "results.json"))
    a = p.parse_args()
    data = json.loads((HERE / "dataset.json").read_text())
    items = list(requests(data))[: a.limit]
    if a.dry_run:
        print(f"{len(items)} requests:", {c: sum(i[0] == c for i in items) for c in "ABC"})
        print(json.dumps(items[0][3], indent=1)[:800])
        return
    key = api_key()
    out = []
    for cond, iid, truth, body in items:
        body = {"model": "jev-latest", **body}
        t0 = time.monotonic()
        resp = ask(key, body)
        out.append({"condition": cond, "id": iid, "truth": truth, "ms": round((time.monotonic() - t0) * 1000), "response": resp})
        print(cond, iid, "error" if "error" in resp else "ok", flush=True)
    Path(a.out).write_text(json.dumps(out, indent=1))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
