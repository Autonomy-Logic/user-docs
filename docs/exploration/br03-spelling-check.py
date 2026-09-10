#!/usr/bin/env python3
"""BR03 spelling gate for user-docs. Run: python3 br03-spelling-check.py <docs-dir>

BR03, from the EDGE-633 Requirements Gathering: "The spelling is vPLC, lowercase
v and uppercase PLC, plural vPLCs. The forms VPLC, Vplc and vPlc are not
accepted."

THE ONE THING THAT MAKES THIS GATE HONEST: it checks PROSE, so it masks

  - fenced code blocks,
  - inline `code` spans,
  - link and image TARGETS, i.e. the part inside ](...)

before it looks, and it skips exploration/ entirely.

MEASURED, because a smaller figure was carried into Phase 10 and did not
reproduce. The Phase 7 record predicted 13 violations unmasked. Against the
finished tree it is:

    no masking at all ................ 145
    code spans masked only ...........  77
    link targets masked only .........  70
    both masked ......................   2
    both masked, exploration/ skipped    0

So the inherited 13 is wrong by an order of magnitude, while the reason behind
it is right and then some: all 145 are lowercase paths such as
../platform/vplcs/overview, image filenames such as vplc-stopped.png, or
quoted literals. Those are URLs. BR03 governs the word the reader reads, not
the slug, and the section was deliberately published at platform/vplcs/ in
lowercase. A gate that reports them is a gate somebody learns to ignore.

exploration/ is skipped for the same reason the census codes it X-HIST: those
are dated internal planning records, not text a customer reads, so BR03 does
not reach them. Both hits that survive masking are in there and both are
substring false positives rather than prose: "D-VPLC" is the name of a census
decision code, and "Renamed to vplc" in the legend table names a path segment.
Anchoring would not have helped, since a hyphen is a word boundary; scope did.

The accepted set is exactly {vPLC, vPLCs}, which is stricter than BR03's letter.
BR03 names VPLC, Vplc and vPlc as rejected; matching case-insensitively also
catches a bare lowercase "vplc" left in running prose, and once the paths are
masked that is the only place such a match can come from.

Exits 1 when it finds a violation, 0 when clean, and prints the total either
way. Before trusting a clean verdict, run the negative control: write "VPLC" and
"vPlc" into any page as prose, confirm both are named, then take them out. This
script has no way to tell "checked 179 files and found nothing" apart from
"resolved no files at all", so it prints the file count it actually read.
"""
import re
import sys
from pathlib import Path

ACCEPTED = {"vPLC", "vPLCs"}
CANDIDATE = re.compile(r"v\s?plcs?", re.I)
FENCE = re.compile(r"^\s*(```|~~~)")
CODE_SPAN = re.compile(r"`[^`]*`")
LINK_TARGET = re.compile(r"(!?\[[^\]]*\]\()([^)]*)(\))")


def mask(line):
    """Blank out inline code spans and link/image targets, preserving columns.

    Link TEXT is deliberately left visible: it is prose the reader reads, and a
    "VPLC" typed inside [ ] is a real violation.
    """
    line = CODE_SPAN.sub(lambda m: " " * len(m.group(0)), line)
    line = LINK_TARGET.sub(
        lambda m: m.group(1) + " " * len(m.group(2)) + m.group(3), line
    )
    return line


def main():
    docs = Path(sys.argv[1]).resolve()
    violations = []
    files = 0

    for md in sorted(docs.rglob("*.md")):
        rel = md.relative_to(docs)
        if rel.parts and rel.parts[0] == "exploration":
            continue
        files += 1
        inside = False
        for lineno, raw in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE.match(raw):
                inside = not inside
                continue
            if inside:
                continue
            for m in CANDIDATE.finditer(mask(raw)):
                if m.group(0) not in ACCEPTED:
                    violations.append(
                        (str(md.relative_to(docs)), lineno, m.start() + 1,
                         m.group(0), raw.strip()[:100])
                    )

    for f, ln, col, word, ctx in violations:
        print(f"{f}:{ln}:{col}  {word!r}  {ctx}")
    print(f"\nfiles read: {files}")
    print(f"BR03 VIOLATIONS: {len(violations)}")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
