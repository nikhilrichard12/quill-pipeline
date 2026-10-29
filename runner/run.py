#!/usr/bin/env python3
"""Quill runner: executes the five stage prompts against any OpenAI-compatible chat API.

    python runner/run.py <slug>            # full pipeline for briefs/<slug>.md
    python runner/run.py <slug> --from 3   # resume at stage 3
    python runner/run.py --all             # every brief in briefs/ (skips EXAMPLE-brief.md)

Stdlib only. Config in runner/config.json; the API key comes from the env var it names.
"""
import argparse, glob, json, os, re, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "runner", "config.json")))
PRODUCT = CFG["product"]

STAGES = [
    ("1-orchestrator", "outline"),
    ("2-writer",       "draft"),
    ("3-reviewer",     "review"),
    ("4-factchecker",  "factcheck"),
    ("5-grader",       "grade"),
]

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def bible():
    return "\n\n".join(read(p) for p in sorted(glob.glob(os.path.join(ROOT, "bible", "*.md"))))

def prompt(name):
    return read(os.path.join(ROOT, "prompts", name + ".md")).replace("{{PRODUCT}}", PRODUCT)

def chat(system, user, model=None, retries=4):
    key = os.environ.get(CFG["api_key_env"])
    if not key:
        sys.exit(f"set {CFG['api_key_env']}")
    body = json.dumps({
        "model": model or CFG["model"],
        "temperature": CFG.get("temperature", 0.4),
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
    }).encode()
    req = urllib.request.Request(
        CFG["base_url"].rstrip("/") + "/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.load(r)["choices"][0]["message"]["content"]
        except Exception as e:  # rate limits, transient 5xx
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt * 5)

def verdict(text, pattern):
    m = re.findall(pattern, text, flags=re.I)
    return m[-1].upper() if m else "UNKNOWN"

def run_stage(slug, stage, extra=""):
    name, out = stage
    out_dir = os.path.join(ROOT, "output", slug)
    gating = read(os.path.join(ROOT, "prompts", "GATING-POLICY.md"))
    system = prompt(name) + "\n\n=== GATING POLICY ===\n" + gating + "\n\n=== BIBLE ===\n" + bible()
    ctx = [f"slug: {slug}", "=== BRIEF ===", read(os.path.join(ROOT, "briefs", slug + ".md"))]
    if name == "2-writer":
        ctx += ["=== OUTLINE ===", read(os.path.join(out_dir, "outline.md"))]
    elif name in ("3-reviewer", "4-factchecker", "5-grader"):
        ctx += ["=== DRAFT ===", read(os.path.join(out_dir, "draft.md"))]
    if extra:
        ctx += [extra]
    ctx += [f"Write the {out} now. Output only the file contents, no preamble."]
    model = CFG.get("grader_model") if name == "5-grader" else None
    text = chat(system, "\n\n".join(ctx), model=model)
    write(os.path.join(out_dir, out + ".md"), text)
    print(f"[{slug}] {name} -> output/{slug}/{out}.md")
    return text

def rewrite(slug, feedback_label, feedback):
    """Re-run the writer with the reviewer's or fact-checker's findings appended."""
    out_dir = os.path.join(ROOT, "output", slug)
    extra = (f"=== PREVIOUS DRAFT ===\n{read(os.path.join(out_dir, 'draft.md'))}\n\n"
             f"=== {feedback_label} (resolve every item) ===\n{feedback}")
    return run_stage(slug, STAGES[1], extra=extra)

def pipeline(slug, start=1):
    if start <= 1: run_stage(slug, STAGES[0])
    if start <= 2: run_stage(slug, STAGES[1])
    if start <= 3:
        review = run_stage(slug, STAGES[2])
        if verdict(review, r"\b(PASS|REVISE)\b") == "REVISE":
            rewrite(slug, "REVIEW", review)
    if start <= 4:
        for i in range(CFG.get("max_rewrites", 2) + 1):
            fc = run_stage(slug, STAGES[3])
            if verdict(fc, r"\b(PASS|FAIL)\b") == "PASS":
                break
            if i == CFG.get("max_rewrites", 2):
                print(f"[{slug}] factcheck still FAIL after {i} rewrites; stopping before grade")
                return
            rewrite(slug, "FACTCHECK", fc)
    if start <= 5:
        grade = run_stage(slug, STAGES[4])
        g = verdict(grade, r"\b([A-F])\b(?=\s*(?:\(|$|\n))")
        print(f"[{slug}] grade: {g}")
        if g in ("A", "B"):
            write(os.path.join(ROOT, "output", slug, "final.md"),
                  read(os.path.join(ROOT, "output", slug, "draft.md")))
            print(f"[{slug}] promoted to output/{slug}/final.md")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--from", dest="start", type=int, default=1)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.all:
        slugs = [os.path.basename(p)[:-3] for p in sorted(glob.glob(os.path.join(ROOT, "briefs", "*.md")))
                 if not os.path.basename(p).startswith("EXAMPLE")]
    elif a.slug:
        slugs = [a.slug]
    else:
        ap.error("give a slug or --all")
    for s in slugs:
        pipeline(s, a.start)
