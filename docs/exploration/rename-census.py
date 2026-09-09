#!/usr/bin/env python3
"""
EDGE-642 / EDGE-633 terminology rename: occurrence census for user-docs.

Emits one row per occurrence of "orchestrator" or "device" across the markdown
under docs/, with a decision code and the id of the rule that assigned it.

The point is FR17 and FR20: every occurrence of both words carries a recorded
decision, including the ones that stay unchanged. The reason for a decision is
written once per code in RENAME-DECISION-RECORD.md; a row carries the code, so
the record does not repeat a sentence 1200 times.

Run from docs/:      python3 exploration/rename-census.py
Outputs:             exploration/rename-census.csv
Verification (Phase 10):
    python3 exploration/rename-census.py --verify
which re-runs the census on the current tree and fails if any occurrence still
carries a code from the CHANGES set.
"""

import csv
import os
import re
import sys

WORD = re.compile(r"orchestrator|device", re.I)
CTX = 70

# This demand's own artefacts. They are full of both words by construction, and
# counting them would make the census measure itself instead of the documentation.
SELF = {
    "exploration/RENAME-DECISION-RECORD.md",
    "exploration/RENAME-IMAGE-MAP.md",
}

# ---------------------------------------------------------------- legend ----
# decision: "changes" rows must not survive the rewrite; "stays" rows must.
LEGEND = {
    # ---- changes -----------------------------------------------------------
    "O-ENTITY":     ("changes", "orchestrator = the parent product entity -> Device (BR01)"),
    "O-AGENT":      ("changes", "the orchestrator agent, the daemon -> Device Agent (BR04)"),
    "O-EDGEDEV":    ("changes", "the platform entity named inside the Editor docs -> Edge Device / "
                                "Edge Devices, because the Editor already uses Device for the PLC "
                                "target (BR05, FR10)"),
    "O-PATH":       ("changes", "path, link target or image filename carrying the old vocabulary -> "
                                "rewritten by the section move (FR18)"),
    "D-VPLC":       ("changes", "device = the child entity, the virtual PLC -> vPLC (BR02, sense 1)"),
    "D-PATH":       ("changes", "path, link target or image filename where device means the child "
                                "entity -> renamed to vplc (FR18)"),
    # ---- stays -------------------------------------------------------------
    "O-LITERAL":    ("stays",  "a literal the software still emits or resolves: container name, "
                               "image reference, repository URL, or a log line quoted verbatim. "
                               "Changing it would print an instruction that does not work (BR09, BR13)"),
    "O-SE":         ("stays",  "the ordinary software-engineering sense of orchestrator, not the "
                               "product entity (BR07)"),
    "D-HOST":       ("stays",  "device = the machine the agent runs on, written as 'your edge "
                               "device'. This is the sense the new vocabulary promotes, so it gets a "
                               "consistency pass rather than a rename (sense 2)"),
    "D-EDITORNODE": ("stays",  "device = the Editor's Device node and its Device Configuration "
                               "screens, the PLC target being programmed. A different concept "
                               "(BR06, FR09, sense 3)"),
    "D-TARGET":     ("stays",  "device = the PLC or runtime the editor is connected to. SEVENTH "
                               "SENSE, absent from the original framework: the target can be a vPLC "
                               "or physical hardware, so calling it a vPLC would make these pages "
                               "wrong for anyone running a real PLC"),
    "D-REMOTE":     ("stays",  "remote device: a Modbus master or an EtherCAT bus or slave device. "
                               "A different concept (sense 4)"),
    "D-PLAIN":      ("stays",  "the plain networking or hardware sense, ordinary English, including "
                               "'every device' meaning the reader's own browser session (sense 5)"),
    "D-LICENSE":    ("stays",  "licensed device: the VPP licensing unit, a physical hardware unit "
                               "identified by a serial anchor. Neither entity (BR12, sense 6)"),
    "D-LITERAL":    ("stays",  "a string quoted verbatim from a product interface or message, a CLI "
                               "subcommand, or the on-disk devices/ project directory. Quoting it "
                               "differently would misreport what the screen says or print a command "
                               "that does not work (BR09)"),
    "X-HIST":       ("stays",  "a dated historical record: the internal planning documents under "
                               "docs/exploration/, and the changelog entries. These say what was "
                               "true, or what a release actually said, at a past date, so renaming "
                               "them would falsify a record"),
}
CHANGES = {k for k, v in LEGEND.items() if v[0] == "changes"}

# --------------------------------------------------------------- helpers ----
def code_blocks(text):
    """Line numbers (1-based) that sit inside a fenced code block."""
    inside, fenced = False, set()
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            inside = not inside
            fenced.add(n)
            continue
        if inside:
            fenced.add(n)
    return fenced


# Literals the software still emits or resolves. Never rewritten.
# Judged POSITIONALLY, on the text touching the match, never on the 140-char
# window: a window rule marks "the orchestrator goes Inactive" as a literal
# just because a docker command sits earlier on the same line.
def is_o_literal(line, start, end):
    after = line[end:end + 8].lower()
    before = line[max(0, start - 24):start].lower()
    if after.startswith("-agent"):          # orchestrator-agent, the container/image/repo
        return True
    if "/var/" in before:                   # /var/orchestrator, written on the machine
        return True
    if before.endswith("unknown ") or before.endswith('"unknown '):
        return True                         # log line the agent emits
    return False


def is_agent(line, start, end):
    """True only when the match is part of the phrase 'orchestrator agent'."""
    return re.match(r"[-*_ ]{0,3}agent", line[end:end + 12], re.I) is not None


def in_code_span(line, col):
    """True when the match sits inside a `...` inline code span."""
    return line.count("`", 0, col - 1) % 2 == 1

# A link target or an image filename, i.e. ](...orchestrator...) or ](...device...)
def in_link_target(line, col):
    """True when the match sits inside a markdown link/image target."""
    open_paren = line.rfind("](", 0, col)
    if open_paren == -1:
        return False
    close = line.find(")", open_paren)
    return close == -1 or close > col


REMOTE = re.compile(
    r"remote device|remote-device|modbus|ethercat|slave|bus master|coe |sdo|pdo|esi"
    r"|io group|remote equipment",
    re.I,
)

EDITOR_SCREEN = re.compile(
    r"orchestrators screen|orchestrators editor|orchestrators panel|orchestrators card"
    r"|orchestrators tab|device orchestrators|click \*\*orchestrators\*\*"
    r"|expand \*\*device\*\*|orchestrators\*\*",
    re.I,
)

# Quoted product strings that must stay byte-identical.
D_LITERAL = re.compile(
    r"no coe object dictionary|coe object dictionary available|no configurable sdo"
    r"|the ethercat device could not be found|no channels available for this device"
    r"|`devices/|devices/servers|devices/remote|select this device for"
    r"|choose a device to retrieve",
    re.I,
)

# The child entity, the vPLC, in platform / billing / account contexts.
VPLC_CTX = re.compile(
    r"vplc|virtual plc|new device|add device|add new device|create device|device name"
    r"|device limit|devices tab|device entries|devices\*\* tab|device detail"
    r"|containerized|container",
    re.I,
)

HOST = re.compile(
    r"edge device|linux device|linux-based device|your device|target linux|on the device"
    r"|edge hardware|edge computer|physical hardware|industrial pc|raspberry pi",
    re.I,
)

PLAIN = re.compile(
    r"every device|all your devices|physical i/o|sensors|actuators|native devices"
    r"|external devices|expensive hardware|physical devices|device integration"
    r"|remote i/o|hmi",
    re.I,
)


def classify(path, line, col, word, ctx):
    """Return (code, rule_id). Ordered rules; the first that matches wins."""
    w = word.lower()
    top = path.split("/")[0]

    # R00 - the internal planning documents, both words.
    if top == "exploration":
        return "X-HIST", "R00"

    if w == "orchestrator":
        # R01 - literals the software emits or resolves, judged positionally.
        if is_o_literal(line, col - 1, col - 1 + len(word)) or in_code_span(line, col):
            return "O-LITERAL", "R01"
        # R02 - link targets and image filenames.
        if in_link_target(line, col):
            return "O-PATH", "R02"
        # R03 - the daemon, only when the word "agent" touches the match.
        if is_agent(line, col - 1, col - 1 + len(word)):
            return "O-AGENT", "R03"
        # R04 - inside the Editor docs the entity reads Edge Device.
        if top == "openplc-editor":
            return "O-EDGEDEV", "R04"
        # R05 - everywhere else it is the parent entity.
        return "O-ENTITY", "R05"

    # w == "device"
    # R09 - the "Device" half of the Editor's screen label "Device Orchestrators",
    # which becomes "Edge Devices" as one label. Both words move together, so the
    # half that reads "Device" is not one of the senses that stay.
    if re.match(r"[s]?[ -]orchestrator", line[col - 1 + len(word):col + 20], re.I):
        return "O-EDGEDEV", "R09"
    # R10 - quoted product strings and the on-disk project directory.
    if D_LITERAL.search(ctx) or in_code_span(line, col):
        return "D-LITERAL", "R10"
    # R11 - link targets and image filenames. A path is only renamed when the
    # "device" in it means the child entity; the remote-device captures and the
    # Editor's device-config page keep their names, so they are excluded first.
    if in_link_target(line, col):
        target = line[line.rfind("](", 0, col) + 2:]
        target = target[:target.find(")")] if ")" in target else target
        if re.search(r"remote-device|device-from-repository|device-config", target, re.I):
            return ("D-REMOTE", "R11a") if "config" not in target.lower() \
                else ("D-EDITORNODE", "R11b")
        return "D-PATH", "R11"
    # R12 - VPP licensing.
    if re.search(r"licensed device|serial anchor|vpp licen", ctx, re.I):
        return "D-LICENSE", "R12"
    # R13 - remote equipment: Modbus, EtherCAT.
    if REMOTE.search(ctx):
        return "D-REMOTE", "R13"
    # R14 - plain networking or hardware English.
    if PLAIN.search(ctx):
        return "D-PLAIN", "R14"
    # R15 - the machine the agent runs on.
    if HOST.search(ctx):
        return "D-HOST", "R15"
    # R16 - the connected PLC or runtime, the seventh sense.
    if path.startswith("openplc-editor/building-deploying/"):
        return "D-TARGET", "R16"
    # R17 - the Editor's Device node and its configuration screens.
    if path.startswith("openplc-editor/"):
        return "D-EDITORNODE", "R17"
    # R18 - the child entity, everywhere outside the Editor docs.
    if VPLC_CTX.search(ctx):
        return "D-VPLC", "R18"
    # R19 - residual, reviewed by hand and pinned in OVERRIDES.
    return "REVIEW", "R19"


# Rows the rules get wrong or cannot see, pinned by (path, line, col).
# Each entry was read in context before being written here.
OVERRIDES = {}


def load_overrides():
    p = os.path.join("exploration", "rename-census-overrides.csv")
    if not os.path.exists(p):
        return
    for r in csv.DictReader(open(p, encoding="utf-8")):
        OVERRIDES[(r["file"], int(r["line"]), int(r["col"]))] = (r["code"], r["rule"])


def census():
    load_overrides()
    rows = []
    for root, _dirs, files in os.walk("."):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            p = os.path.relpath(os.path.join(root, f), ".")
            if p in SELF:
                continue
            text = open(p, encoding="utf-8").read()
            fenced = code_blocks(text)
            for ln, line in enumerate(text.splitlines(), 1):
                for m in WORD.finditer(line):
                    col = m.start() + 1
                    a, b = max(0, m.start() - CTX), min(len(line), m.end() + CTX)
                    ctx = line[a:b].strip()
                    key = (p, ln, col)
                    if key in OVERRIDES:
                        code, rule = OVERRIDES[key]
                    else:
                        code, rule = classify(p, line, col, m.group(0), ctx)
                        # A fenced block is normally a literal. It must never be a
                        # way for an unclassified row to acquire a code by accident,
                        # so REVIEW is left standing and reported.
                        if (ln in fenced and code != "REVIEW"
                                and code not in ("O-LITERAL", "D-LITERAL", "X-HIST")):
                            code, rule = ("O-LITERAL" if m.group(0).lower() == "orchestrator"
                                          else "D-LITERAL"), rule + "+fenced"
                    rows.append({
                        "file": p, "line": ln, "col": col, "word": m.group(0),
                        "code": code, "rule": rule,
                        "decision": LEGEND[code][0] if code in LEGEND else "REVIEW",
                        "context": ctx,
                    })
    return rows


def main():
    rows = census()
    verify = "--verify" in sys.argv
    if not verify:
        out = os.path.join("exploration", "rename-census.csv")
        with open(out, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["file", "line", "col", "word",
                                               "code", "rule", "decision", "context"])
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {out}: {len(rows)} occurrences")

    from collections import Counter
    by_code = Counter(r["code"] for r in rows)
    print(f"\n{'code':14} {'n':>5}  decision")
    for code, n in sorted(by_code.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{code:14} {n:>5}  {LEGEND.get(code, ('REVIEW',))[0]}")
    print(f"{'TOTAL':14} {len(rows):>5}")

    todo = [r for r in rows if r["code"] == "REVIEW"]
    if todo:
        print(f"\n!! {len(todo)} occurrences unclassified, rule R19 fell through:")
        for r in todo[:60]:
            print(f"   {r['file']}:{r['line']}:{r['col']}  {r['context'][:110]}")

    if verify:
        left = [r for r in rows if r["code"] in CHANGES]
        if left:
            print(f"\nFAIL: {len(left)} occurrences still carry a CHANGES code:")
            for r in left[:80]:
                print(f"   [{r['code']}] {r['file']}:{r['line']}  {r['context'][:100]}")
            return 1
        print("\nPASS: every surviving occurrence carries a 'stays' code.")
    return 1 if todo else 0


if __name__ == "__main__":
    sys.exit(main())
