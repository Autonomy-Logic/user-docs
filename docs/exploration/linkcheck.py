#!/usr/bin/env python3
"""Link checker for user-docs. Run: python3 linkcheck.py <docs-dir>

Checks:
  - every markdown link target that is not external resolves to a file on disk
  - every image reference resolves to a file on disk
  - every _config.json leaf path resolves to a markdown file

Handles the site-root form /docs/... that the docs use, and the extensionless
page-link form the docs use for markdown pages.

TWO WARNINGS, both of which have already cost somebody a wrong verdict on this
demand. Phase 10 depends on both.

1. THIS SCRIPT ALWAYS EXITS 0, even with broken links. Judge it by the
   "TOTAL BROKEN" line, never by its exit code, and never by `&&`. It also
   needs the docs directory as argv[1] and raises IndexError without it, so a
   silent-looking run may have checked nothing at all. Before trusting a
   verdict, run a negative control: append one broken link and one broken
   image to any page, confirm the total moves and names them, then remove them.
   The pre-existing baseline in this repository is 6.

2. Its sibling, rename-census.py, OVERWRITES exploration/rename-census.csv
   when run from the working tree. That CSV is the base-commit record of what
   was decided. Generate it from a checkout of the base commit; against the
   working tree use --verify, which classifies and writes nothing.

Undoing a control experiment with `git checkout <file>` will also discard any
uncommitted edits to that file. Copy the file aside and copy it back instead.
"""
import json
import re
import sys
from pathlib import Path

LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^\s*(```|~~~)")

EXTERNAL = ("http://", "https://", "mailto:", "tel:", "#")


def strip_fences(text):
    """Yield (lineno, line) for lines outside fenced code blocks."""
    inside = False
    for n, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            inside = not inside
            continue
        if not inside:
            yield n, line


def resolve(docs: Path, md: Path, target: str):
    """Return list of candidate paths that would satisfy the target."""
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    if target.startswith("/docs/"):
        base = docs / target[len("/docs/") :]
    elif target.startswith("/"):
        base = docs / target.lstrip("/")
    else:
        base = md.parent / target
    cands = [base]
    if not base.suffix:
        cands += [base.with_suffix(".md"), base / "index.md", base / "README.md"]
    return cands


def main():
    docs = Path(sys.argv[1]).resolve()
    broken = []

    for md in sorted(docs.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for lineno, line in strip_fences(text):
            for m in LINK.finditer(line):
                raw = m.group(1)
                if raw.startswith(EXTERNAL):
                    continue
                cands = resolve(docs, md, raw)
                if cands is None:
                    continue
                if not any(c.exists() for c in cands):
                    kind = "image" if m.group(0).startswith("!") else "link"
                    broken.append(
                        (kind, str(md.relative_to(docs)), lineno, raw)
                    )

    cfg = docs / "_config.json"
    if cfg.exists():
        conf = json.loads(cfg.read_text(encoding="utf-8"))

        def walk(node, prefix):
            """Accumulate path segments; only leaves (no items) are pages."""
            if isinstance(node, list):
                for v in node:
                    walk(v, prefix)
                return
            if not isinstance(node, dict):
                return
            path = node.get("path")
            here = prefix + [path] if path else prefix
            if "items" in node:
                walk(node["items"], here)
                return
            if not path:
                return
            target = "/".join(here)
            cands = resolve(docs, cfg, target)
            if cands and not any(c.exists() for c in cands):
                broken.append(("config", "_config.json", 0, target))

        walk(conf.get("navigation", []), [])

    for b in broken:
        print(f"{b[0]:6} {b[1]}:{b[2]} -> {b[3]}")
    print(f"\nTOTAL BROKEN: {len(broken)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
