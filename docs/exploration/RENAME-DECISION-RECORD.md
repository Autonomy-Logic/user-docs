# Terminology rename: decision record for user-docs

Internal working document. Not part of the published documentation and not in `_config.json`.

Demand [EDGE-633](https://autonomylogic.atlassian.net/browse/EDGE-633), subtask
[EDGE-642](https://autonomylogic.atlassian.net/browse/EDGE-642). Specification in section 8.5 of the
Requirements Gathering, FR17 to FR22. Risk assessment: Cybersecurity Risk Assessment - Ecosystem
terminology rename - User Docs.

This record satisfies **FR17** and **FR20**: every occurrence of "orchestrator" and "device" in this
repository carries a recorded decision, including the ones that stay unchanged. It is the evidence
for **AC05**.

The census pattern is `orchestrator|orchestration|device`. "orchestration" is in it because the
ordinary software-engineering sense of the word is reader-facing copy here, on the first page a new
reader opens, and a pattern of the two nouns alone cannot see it. See `O-SE`.

Measured against `origin/development` at `79c4faa`.

## What the rename is

| Before | After |
|---|---|
| Orchestrator, the parent entity | **Device** |
| Device, the child entity | **vPLC** (plural **vPLCs**, lowercase v, uppercase PLC) |
| Orchestrator Agent | **Device Agent** |
| The platform entity, named inside the OpenPLC Editor docs | **Edge Device** / **Edge Devices** |

The Editor's own `Device` node keeps its name, because it means the PLC target being programmed,
which is a different concept (BR06, FR09).

## How a decision gets recorded without 1238 sentences

`exploration/rename-census.csv` holds **one row per occurrence**: file, line, column, the word, the
decision code, the id of the rule that assigned it, whether the decision is *changes* or *stays*, and
140 characters of context. **1238 rows.**

The **reason** is written once per code, in the legend below. A row carries the code. That is the
whole trick: the reason for keeping "remote device" is one sentence, not 184 copies of one sentence.

The census is reproducible: `python3 exploration/rename-census.py` from `docs/`, which classifies
the tree it is run against. The CSV committed here is the run against the base commit; see
`D-PATH-NEW` below for the one classifier change made after it, and why the CSV was left alone.

## The legend

Sixteen codes cover all 1238 occurrences. One further code is defined and legitimately empty.
`D-PATH-NEW` was added once the section had moved; it is described after the tables, and its count at
the base commit is 0.

### Codes whose occurrences must not survive the rewrite

| Code | n | Sense | Decision and reason |
|---|---|---|---|
| `O-ENTITY` | 267 | orchestrator = the parent product entity | **-> Device.** The rename itself (BR01) |
| `D-VPLC` | 110 | device = the child entity, the virtual PLC | **-> vPLC.** The rename itself (BR02, sense 1) |
| `O-PATH` | 67 | a path, link target or image filename carrying the old vocabulary | **Rewritten by the section move** (FR18) |
| `O-EDGEDEV` | 64 | the platform entity named inside the Editor docs, including both halves of the Editor's screen label "Device Orchestrators" | **-> Edge Device / Edge Devices.** The Editor already uses "Device" for the PLC target, so the platform entity needs the qualifier to stay distinguishable (BR05, FR10) |
| `O-AGENT` | 12 | the orchestrator agent, the daemon on the customer machine | **-> Device Agent** (BR04) |
| `D-PATH` | 10 | a path, link target or image filename where "device" means the child entity | **Renamed to vplc** (FR18) |
| `O-REWRITE` | 7 | the parent entity in a sentence that defines it in terms of the daemon or of the machine | **The sentence is rewritten, not word-substituted.** Listed row by row below (BR01, BR04) |
| | **537** | | |

### Codes whose occurrences must survive the rewrite unchanged

| Code | n | Sense | Decision and reason |
|---|---|---|---|
| `D-REMOTE` | 192 | remote device: a Modbus master, or an EtherCAT bus or slave device | **Stays.** A different concept, and the word is the industry's, not ours (sense 4) |
| `D-EDITORNODE` | 129 | the Editor's `Device` node and its Device Configuration screens: board selection, pin mapping, communication settings | **Stays.** It means the PLC target being programmed, not the platform entity. This is also why the on-disk `devices/` directory is not renamed (BR06, FR09, sense 3) |
| `X-HIST` | 125 | a dated historical record: the three internal planning documents under `exploration/`, and the changelog entries in `changelog-link.md` | **Stays.** These say what was true, or what a release actually said, at a past date. Renaming them would falsify a record. The planning documents are outside the navigation and already name sections that no longer exist |
| `D-TARGET` | 98 | device = the PLC or runtime the editor is connected to | **Stays. SEVENTH SENSE, absent from the original framework.** The target can be a vPLC or physical hardware, so calling it a vPLC would make these pages wrong for anyone running a real PLC. 96 of the 98 sit in `openplc-editor/building-deploying/` |
| `D-HOST` | 84 | device = the machine the agent runs on, written today as "your edge device" | **Stays as a word.** This is the sense the new vocabulary promotes, so it gets a consistency pass rather than a rename (sense 2) |
| `D-LITERAL` | 33 | a string quoted verbatim from a product interface or message, a CLI subcommand, or the on-disk `devices/` project directory | **Stays byte-identical.** Quoting it differently would misreport what the screen says or print a command that does not work (BR09) |
| `D-PLAIN` | 29 | the plain networking or hardware sense, ordinary English, including "every device" meaning the reader's own browser session | **Stays** (sense 5) |
| `O-LITERAL` | 10 | a literal the software still emits or resolves: the container name, the image reference, the repository URL, and the log line `Unknown orchestrator` | **Stays byte-identical.** These name components that keep their names. Changing them would print an instruction that does not work (BR09, BR13) |
| `O-SE` | 1 | the ordinary software-engineering sense of "orchestrator" | **Stays** (BR07). The single occurrence is named below |
| | **701** | | |

### Defined and legitimately empty

| Code | n | Why it is empty |
|---|---|---|
| `D-LICENSE` | 0 | The VPP licensed device, a physical hardware unit with a serial anchor (BR12, sense 6). **user-docs does not document VPP licensing**, so this sense never appears |

### `O-SE`: the ordinary software-engineering sense DOES occur here

This entry previously sat in the table above, stating flatly that the sense does not occur in this
repository and that BR07 has nothing to protect here. **That was an artefact of the word list, not a
property of the repository.** `getting-started/quick-start.md:26` ends:

> ... It maintains a secure connection to the cloud and handles container **orchestration**,
> networking, and system monitoring.

That is the ordinary software-engineering sense, in published reader-facing copy, on the terminology
block of the first page a new reader opens. A pattern of `orchestrator|device` cannot match
"orchestration", so the census could not see it and the emptiness of the code was self-inflicted.

The pattern now includes `orchestration`. There is **exactly one** such occurrence in the repository:
`getting-started/quick-start.md:26:221`, pinned to `O-SE` by hand override **H11**. It **stays**: the
word is being used correctly. Rule **R06** routes any other inflection of "orchestrate" to `REVIEW`
rather than guessing, so a future one is reported instead of silently coded.

Phase 5 rewrites that exact line, because the sentence around it is one of the seven `O-REWRITE`
rows: the word "orchestration" survives while "Orchestrator" at column 3 does not.

### `O-REWRITE`: the seven sentences that cannot be word-substituted

The rename has three targets, not one: the **Device** is the customer machine, the **Device Agent** is
the daemon that runs on it, and the **vPLC** is the container the agent starts. Rule R03 assigns
`O-AGENT` only when the literal word "agent" touches the match, which is right, but it means the
daemon sense expressed any other way fell through to `O-ENTITY` and would have been word-substituted
to "Device". A sentence that defines one of the three in terms of another cannot survive a word
substitution; it has to be rewritten. These seven rows are flagged so the phase that rewrites the page
cannot treat them as a find-and-replace, and the intended reading is recorded here.

| Row | Today | What a substitution would produce | The intended reading |
|---|---|---|---|
| `getting-started/quick-start.md:26:3` | "**Orchestrator**: An agent that runs on an edge device ... and manages your vPLC instances" | "**Device**: An agent that runs on an edge device", which the demand's own glossary contradicts | The **Device** is the machine. The terminology block names the machine and the daemon separately: the Device is the edge machine, the Device Agent is what runs on it and manages the vPLCs |
| `getting-started/quick-start.md:66:4` | "An orchestrator is an edge agent that manages your vPLC devices. It runs on your physical hardware" | "A Device is an edge agent ... It runs on your physical hardware" | Same split. The Device Agent manages the vPLCs; the Device is the hardware |
| `index.md:19:6` | "**[Orchestrators]**: The cloud-managed agent that runs on your edge device" | "**Devices**: The cloud-managed agent that runs on your edge device" | The Device is the edge machine, managed from the cloud through the Device Agent |
| `platform/projects/overview.md:43:10` | "The **orchestrator**, the agent on your edge device" | "The **Device**, the agent on your edge device" | The Device is the edge machine; the agent on it is the Device Agent |
| `platform/orchestrators/overview.md:3:6` | "An **orchestrator** is the cloud-side representation of a small piece of software (the *orchestrator agent*) that you run on your edge hardware" | a Device defined as the representation of a piece of software | A Device is the cloud-side representation of the **machine**; the Device Agent is the software on it |
| `openplc-editor/communication/README.md:108:87` | "a serial port available on the machine where the Orchestrator is installed" | "the machine where the Edge Device is installed", self-contradictory | The Edge Device **is** that machine: "a serial port available on the Edge Device" |
| `openplc-editor/communication/modbus/client.md:158:65` | "From a shell on the orchestrator host" | "the Edge Device host", redundant | "From a shell on the Edge Device" |

One neighbouring row is the same class but resolves to a clean substitution rather than a rewrite, so
it is `O-AGENT` and not `O-REWRITE`: `openplc-editor/communication/ethercat/prerequisites.md:21:84`,
"a second NIC ... for the orchestrator connection". The connection belongs to the daemon, so it reads
"for the **Device Agent** connection". Hand override **H16**.

`reference/glossary.md` carries the same problem and is deliberately **not** flagged: FR19 already
mandates that its `Orchestrator` entry be redefined as the customer machine running the Device Agent,
so the rewrite is instructed there by the requirement rather than by this record.

### `D-PROSE-NEW`, added at Phase 5

The prose analogue of `D-PATH-NEW`, and it exists for the same reason one layer up. `D-PATH-NEW`
was needed because after the section moved, a link target containing "device" was usually right.
`D-PROSE-NEW` is needed because after a page is rewritten, a **sentence** containing "Device" is
usually right, and R18 cannot tell: "Device" with a "vPLC" nearby is exactly what the child sense
used to look like. Left alone, R18 codes 35 correct new sentences on the rewritten pages as `D-VPLC`,
a *changes* code, and the Phase 10 gate fails forever on prose that is already finished.

**Capitalisation is what makes it decidable.** The platform entity is written `Device` / `Devices`;
the machine stays lowercase "edge device", the Editor's node and plain hardware English stay
lowercase, and the child entity is spelled `vPLC` and so cannot match at all. That is why the
capitalised-in-prose convention is recorded as a decision rather than left as a preference: the gate
depends on it.

Rule **R20** assigns it, and the rule is scoped to an **enumerated set of finished files**,
`D_PROSE_DONE`, not applied tree-wide. A bare capitalisation rule would be unsafe, because before a
page is rewritten its capitalised "Device" is usually the *child* ("Add Device wizard", "vPLC
Device", "## Step 2: Create a vPLC Device"), so the rule would mark outstanding work as done. That is
the invisible direction and the gate cannot catch it. A file joins the set in the commit that
rewrites it.

Measured when it was added, over the six pages the rename had finished: 117 rows, of which 65 would
otherwise have been `REVIEW` (base-commit overrides no longer line up once the prose moves), 35 would
have been `D-VPLC` and therefore *changes*, and 17 would have been `D-HOST` or `D-PLAIN`, both
*stays*. Outstanding *changes* rows on those six pages went to **0**.

### `D-PATH-NEW`, added at Phase 3

A seventeenth code, and the only one added after the census was written: **a path, link target or image
filename that correctly names the new entity**. A *stays* code, no action required.

It exists because `D-PATH` carried a hidden assumption. At the base commit no parent-entity path
contained the word "device", so rule R11 could treat any link target containing it as the child
entity, to be renamed to `vplc`. Once the section moved to `platform/devices/`, that stopped being
true: 57 link and image targets now contain "device" **because they are right**, and a *changes* code
on them would make the Phase 10 gate fail forever on correct paths.

Rule **R11c** assigns it. It is the inverse of the old rule: a path occurrence is `D-PATH-NEW` unless
it appears in `D_PATH_PENDING`, the enumerated set of captures whose child-sense name is still
outstanding. Measured after the navigation landed: `D-PATH-NEW` 57, `D-PATH` 2, the two being
`getting-started/images/add-device-modal.png` and `getting-started/images/devices-list-with-vplc.png`,
whose renames sit in the phase that rewrites `quick-start.md`. When that phase lands the set is empty
and `D-PATH` is 0.

The base-commit count for this code is 0, which is why it is absent from the tables above: they
measure `origin/development` at `79c4faa` and sum to 1238. `rename-census.csv` **is** the record of
what was decided then, so re-running the generator over the base tree reproduces it byte for byte
**except for exactly those 8 path rows**, which the generator now codes `D-PATH-NEW` because the
tree it classifies has moved on. Nothing else differs; the difference was measured, not assumed.
The census and the 115 overrides are re-derived against the final tree in the verification phase,
where the gate is that no *changes*-coded occurrence survives.

## Where the occurrences are

| Area | O-ENTITY | D-REMOTE | D-EDITORNODE | X-HIST | D-VPLC | D-TARGET | D-HOST | O-PATH | O-EDGEDEV | D-LITERAL | D-PLAIN | O-AGENT | D-PATH | O-LITERAL | O-REWRITE | O-SE | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `openplc-editor` | - | 174 | 120 | - | 9 | 98 | 28 | 8 | 63 | 26 | 3 | 2 | - | - | 2 | - | 533 |
| `platform` | 156 | - | 7 | - | 57 | - | 22 | 36 | - | 6 | 14 | 3 | 7 | 3 | 2 | - | 313 |
| `getting-started` | 49 | 18 | 2 | - | 14 | - | 18 | 9 | 1 | - | 4 | 5 | 2 | - | 2 | 1 | 125 |
| `exploration` | - | - | - | 124 | - | - | - | - | - | - | - | - | - | - | - | - | 124 |
| `troubleshooting` | 30 | - | - | - | 8 | - | 11 | 8 | - | 1 | 4 | - | - | 7 | - | - | 69 |
| `reference` | 13 | - | - | - | 6 | - | 4 | 3 | - | - | 2 | 2 | - | - | - | - | 30 |
| `plans-and-billing` | 12 | - | - | - | 11 | - | - | 1 | - | - | - | - | 1 | - | - | - | 25 |
| `account` | 6 | - | - | - | 4 | - | - | - | - | - | 2 | - | - | - | - | - | 12 |
| docs root | 1 | - | - | 1 | 1 | - | 1 | 2 | - | - | - | - | - | - | 1 | - | 7 |
| **total** | **267** | **192** | **129** | **125** | **110** | **98** | **84** | **67** | **64** | **33** | **29** | **12** | **10** | **10** | **7** | **1** | **1238** |

Read the `openplc-editor` row as the reason the rename is smaller than the raw count suggests: 533 of
the 1238 occurrences live there, and only 84 of those change.

**59 of the 182 files** contain at least one occurrence that changes. 99 files contain at least one
occurrence of either word; 83 files contain neither.

## The nine literals that must survive byte-identical

Everything else in this repository is prose. These are not, and rewriting one of them would hand a
customer an instruction that fails.

| Where | Literal |
|---|---|
| `platform/orchestrators/managing-orchestrators.md:49,50` | `docker stop orchestrator-agent`, `docker start orchestrator-agent` |
| `platform/orchestrators/overview.md:36` | `https://github.com/Autonomy-Logic/orchestrator-agent` |
| `troubleshooting/orchestrator-not-connecting.md:22` | `ghcr.io/autonomy-logic/orchestrator-agent` |
| `troubleshooting/orchestrator-not-connecting.md:53,59,65,85` | `docker ps \| grep`, `docker start`, `docker logs --tail 100`, `docker restart`, each on `orchestrator-agent` |
| `troubleshooting/orchestrator-not-connecting.md:106` | `docker logs orchestrator-agent` |

The tenth `O-LITERAL` row is `orchestrator-not-connecting.md:76`, the agent log line quoted as
`"Unauthorized" or "Unknown orchestrator"`. It stays for the same reason: the agent still emits it.
Per BR13 only installer and uninstaller feedback text moves; ordinary runtime log strings do not.

## Method, and what it is worth

The classification is **rule-based and then audited**, not pattern-replaced.

- 1123 rows were assigned by 19 ordered rules, keyed on the file, the position of the match and the
  text touching it.
- **115 rows were read individually and pinned** in `exploration/rename-census-overrides.csv`, which
  wins over the rules. 68 of those are rows no rule could classify, 46 are rows a rule classified
  wrongly, and 1 is a row that was read by hand before R09 existed and that R09 now reaches on its
  own (`getting-started/quick-start.md:262:43`, override H06, kept because it records that somebody
  read it).
- The audit is what earned its keep. Rules were wrong in ways that mattered and were fixed:
  - The agent rule matched the word "agent" anywhere in the 140-character window, which turned **22**
    occurrences of the entity into the daemon. It now fires only when "agent" touches the match. (The
    record said 21. Measured on the basis the audit itself used, the committed classifier and its 84
    overrides, the window rule flips 22 rows.)
  - The path rule renamed every link and image path containing "device", which would have renamed
    **17 occurrences across 12 distinct link targets** that must not move: 4 occurrences of
    `device-config-overview` and 13 across 10 `*remote-device*` and `*device-from-repository*` image
    names. (The record said "14 paths", which is neither the occurrence count nor the target count.)
  - A rule was added for the Editor's `Device Orchestrators` label, whose two words are one label and
    move together. It codes exactly **7** occurrences of the "Device" half. Before it existed **6** of
    those sat under senses that stay, `D-EDITORNODE` and `D-TARGET`, and the **7th** sat under
    `D-PATH`, a *changes* code, because it is inside an image filename. (The record said all 7 sat
    under senses that stay.)
  - The remote-equipment rule matched the short industrial abbreviations as unanchored substrings, so
    **`pdo` matched inside "dropdown" and `esi` inside "beside"**. Seven occurrences were coded as
    remote equipment on the strength of an ordinary English word. Two of them are the platform's own
    vPLC creation wizard and were *changes* rows filed as *stays*. The alternation is now anchored on
    word boundaries. Same defect class as the agent-window bug: a substring test on a 140-character
    window.

### The root cause behind three of those, named so it is not rediscovered

The agent-window bug, the `pdo`-in-"dropdown" bug and the `on the device`-in-"on the device card" bug
are **one defect, found three times**:

> **An alternation matching a phrase fragment against a wide window silently absorbs rows that belong
> to another sense.** The window is 140 characters, so any short or unanchored alternative will
> eventually be satisfied by text that has nothing to do with the sense the rule is testing for, and
> the row lands on a plausible-looking code with nothing to report it.

It bites hardest in the invisible direction, because the senses these rules assign are mostly *stays*
codes, so an absorbed *changes* row disappears from the gate. The three instances:

| Rule | Alternative | What it absorbed |
|---|---|---|
| R03, the daemon | `agent` anywhere in the window | 22 rows where the entity, not the daemon, was meant |
| R13, remote equipment | `pdo`, `esi` as bare substrings | 7 rows on the strength of "dropdown" and "beside", 2 of them *changes* rows |
| R15, the machine | `on the device` as a phrase fragment | 6 rows reading "on the device **row**" and "on the device **card**", all of them *changes* rows |

The defence used here is the same in all three: **judge positionally, on the text touching the match,
or anchor the alternative on word boundaries.** A rule that must look at the window should be treated
as a hypothesis to audit, not an answer. When a new sense pattern is added to this script, the
question to ask is not "does this phrase appear nearby" but "does this phrase govern *this*
occurrence".

Two fixes closed holes rather than misclassifications.

**The fenced-block fallback no longer converts a decision, in either direction.** A fenced block is
normally a literal, and the fallback refines a *stays* code into the literal code. Both ways it could
convert a decision are now shut: an unclassified row survives it and is reported, and **a row the
rules coded *changes* keeps that code and is reported** instead of becoming `O-LITERAL` or
`D-LITERAL` with nobody prompted. Only the first half had been closed. Proved in both directions
against a probe file: with the old classifier, a fenced "Delete the orchestrator you no longer need"
became `O-LITERAL`/stays and a fenced "the stale vPLC device entry" became `D-LITERAL`/stays; with the
current one they stay `O-ENTITY`/changes and `D-VPLC`/changes and are listed under a `??` heading.
No row in this repository currently takes that path.

**An abandoned rule was deleted.** `EDITOR_SCREEN` was defined and never called. Its
`device orchestrators` alternative is R09's job, and R09 does it positionally; its
`expand \*\*device\*\*` alternative would have coded the Editor's project-tree `Device` node as the
platform entity, which is the one reading that must **not** become Edge Device (BR06, FR09). An
unused rule that reads as intentional is worse than no rule, so it is gone rather than wired up.

The census also excludes this demand's own two artefacts, which are full of both words by
construction; without that it would measure itself, and counting them too returns 1304 against the
current tree's 1230. That number moves whenever this document is edited, which is the reason for the
exclusion.

**What is exact:** the *changes* or *stays* decision on all 1238 rows, and the completeness of the
census. Four independent counts agree at 1238: the CSV rows, a fresh walk of the tree with a fresh
pattern and no classifier, the sum of the per-code counts, and the sum of the per-area counts, all
over the same 182 resolved files that `find` reports in the base tree, of which 99 carry at least one
occurrence. The CSV as committed splits **537 changes / 701 stays**; re-running the generator over the
base tree reports 529 / 709, the difference being exactly the 8 path rows described under
`D-PATH-NEW` and nothing else. `--verify` fails with **461** changes-rows outstanding against the tree
as it stands after Phase 3, which is what proves the Phase 10 gate actually fires rather than passing
vacuously on a tree it never looked at.

**A note on casing, and a divergence from autonomy-node that is deliberate.** The platform entity is
written capitalised in prose here: "at least one Device", "the Device card", "between Devices". This
departs from how this repository cased the old word, where 87 of 92 mid-sentence "orchestrator"
occurrences were lowercase. It also **diverges from autonomy-node**, whose implementer derived the
opposite rule from that repository's own shipped copy: `Device Agent` capitalised as a proper name,
`device` lowercase in running prose.

Both rules are locally right, for a reason that is worth writing down rather than harmonising away.
Node's interface carries one sense of the word. These pages carry five in the same paragraphs: the
platform entity, the machine the agent runs on, the Editor's `Device` node, the connected PLC target
and plain hardware English, and four of the five stay lowercase. Capitalising the entity is the only
thing that keeps them apart, and it is the same reasoning that produced "Edge Device" inside the
editors under BR05. It is also what makes rule R20 decidable at all.

**We chose disambiguation over cross-repository symmetry.** A reader moving between user-docs and
autonomy-node will see different casing for the same thing. That is known and accepted; nobody should
"fix" one to match the other without re-opening this decision.

**What is approximate:** among the *stays* codes, a small number of rows sit on the boundary between
two senses that both stay, most often `D-EDITORNODE` against `D-REMOTE` where a page discusses the
Editor's Device node and remote devices in one sentence. The decision on those rows is right and the
sense is arguable. No row's *decision* depends on resolving one.

## Review pass: the 52 rows that moved and why

This census was reviewed after it was first landed, page by page rather than by re-reading the
classifier, and the review returned changes required. **52 rows moved and 1 was added.** The direction
matters more than the count: `--verify` only fails on a surviving *changes* row, so a row coded
*changes* that should stay produces a wrong edit the gate catches, while a row coded *stays* that
should change produces a wrong edit **the gate can never catch**. Every decision the review overturned
was in that second, invisible direction.

### 17 rows flipped from *stays* to *changes*

Each one would have left an "orchestrator" or a child-sense "device" standing in a published page with
nothing to report it. All 17 are the child entity, the vPLC, and all 17 are now `D-VPLC`.

| Row | Was | Why it was wrong |
|---|---|---|
| `platform/vplcs/creating-a-vplc.md:19:29` | `D-REMOTE`/R13 | The platform's own vPLC creation wizard, "New Device wizard step 1, **Device Details**". Coded as remote equipment because `pdo` matched inside "dropdown" later on the line. Column 7 of the same line was correctly `D-VPLC`, so the rewrite would have half-renamed one alt text and the gate would still have passed |
| `platform/vplcs/creating-a-vplc.md:19:45` | `D-REMOTE`/R13 | Same line, the "**Device Name** field". Same cause |
| `openplc-editor/README.md:50:56` | `D-EDITORNODE`/R17 | "At least one orchestrator registered with an active device", the device being a vPLC. As coded, the rewrite produced "At least one Edge Device registered with an active device." |
| `openplc-editor/README.md:50:78` | `D-EDITORNODE`/R17 | Link text "Managing **Device** Status", target `../platform/vplcs/vplc-detail` |
| `openplc-editor/communication/README.md:113:22` | `D-EDITORNODE`/R17 | "When creating a vPLC **Device**", the child entity named with both its old and its new word |
| `openplc-editor/communication/README.md:115:186` | `D-EDITORNODE`/R17 | "a serial line cannot be shared between multiple **devices**. If a port is already assigned to another vPLC" |
| `openplc-editor/communication/README.md:117:20` | `D-EDITORNODE`/R17 | Link text "Creating vPLC **Devices**", target `../../platform/vplcs/creating-a-vplc` |
| `openplc-editor/communication/README.md:117:80` | `D-EDITORNODE`/R17 | "the full **Device** creation walkthrough", the same vPLC wizard |
| `openplc-editor/communication/s7comm/example.md:53:44` | `D-EDITORNODE`/R17 | "transfer it to a vPLC **device**" |
| `openplc-editor/communication/ethercat/troubleshooting.md:11:101` | `D-REMOTE`/R13 | "The vPLC's EtherCAT NIC was not marked as a Dedicated Interface when the **device** was created". The NIC is dedicated in the vPLC wizard; the row was coded as remote equipment because the sentence says EtherCAT |
| `openplc-editor/communication/ethercat/troubleshooting.md:13:221` | `D-EDITORNODE`/R17 | "Once the new **device** boots", the vPLC the linked wizard just created |
| `platform/vplcs/connecting-from-editor.md:10:45` | `D-HOST`/R15 | "Select the target vPLC. Click on the **device** row." The sibling occurrence 84 characters later was already `D-VPLC` by hand |
| `platform/vplcs/vplc-detail.md:40:109` | `D-HOST`/R15 | "the 3-dot menu on the **device** card", the vPLC card |
| `platform/vplcs/vplc-detail.md:40:143` | `D-HOST`/R15 | "in the orchestrator's **Devices** tab", the tab that lists vPLCs |
| `troubleshooting/plan-limit-reached.md:30:5` | `D-HOST`/R15 | "**Devices**: delete vPLCs you're not running" |
| `troubleshooting/plan-limit-reached.md:30:67` | `D-HOST`/R15 | "3-dot menu on the **device** card", same line |
| `getting-started/quick-start.md:66:57` | `D-HOST`/R15 | "manages your vPLC **devices**" |

Two defect classes produced all 17. Seven came from the two blanket path rules, R17 ("anything under
`openplc-editor/` is the Editor's `Device` node") and R13 reading an EtherCAT sentence as being about
EtherCAT hardware. **A link target pointing into `platform/vplcs/` is strong evidence the surrounding
prose means the child**, and three of the seven sit on such a line. Six came from `HOST`'s loose
`on the device` alternative, which captures "on the device row" and "on the device card". The blanket
rules are kept, because they are right about the other several hundred rows; the exceptions are pinned
by hand as **H12** and **H13**.

An independent check on the same suspicion: every one of the 21 occurrences of the literal phrase
"vPLC device(s)" in the repository is the child entity. Sixteen were already `D-VPLC`; the five that
were not are in this table.

### 9 rows moved between *changes* codes

The decision does not move, but the target word does, and a phase reading only the code would have
written the wrong word.

- **7 rows to `O-REWRITE`**, listed with their intended readings in the `O-REWRITE` section above.
- `openplc-editor/communication/ethercat/prerequisites.md:21:84` -> `O-AGENT` (H16).
- `openplc-editor/hardware-configuration/device-config-overview.md:19:84` -> `O-PATH` via the new
  rule **R11d**. It is the "device" half of the image filename `device-orchestrators-expanded.png`
  and it was carrying a prose code, `O-EDGEDEV`, while the "orchestrator" half of the same filename
  was correctly a path code. R09 ran before the link-target rule; the two now run the other way
  round, so a path occurrence gets a path code. R11d is judged positionally, exactly as R09 is, and
  deliberately does **not** fire on a target of the shape `orchestrator-detail-devices.png`, where the
  second half is the child entity and becomes `vplcs`.

### 26 rows moved between *stays* codes

No edit changes. The codes are corrected anyway, because the record is evidence.

- **7 rows `D-TARGET` -> `D-EDITORNODE`** (H15): `simulator.md:13:34`, `persistent-storage.md:32:42`
  and `:34:29`, `runtime-status.md:5:22` and `:9:219`, `user-management.md:5:68` and `:7:29`. Every one
  is the project tree's `Device` branch or the desktop editor's `Device Configuration` screen, not the
  connected target. R16 is a blanket path rule over `openplc-editor/building-deploying/`, and the
  identical sentence in `connecting-to-runtimes.md:11` was correctly `D-EDITORNODE`. The eighth
  candidate raised in review, `user-management.md:5:175`, "it configures the **connected device**
  rather than the project", is genuinely the connected target and **stays** `D-TARGET`.
- **15 rows `D-EDITORNODE` -> `D-REMOTE`**: the EtherCAT **Scanned Devices** and **Configured
  Devices** panels, across `bus-scan.md` (8), `bus-repository.md`, `diagnostics.md`, `example.md`,
  `slave-info.md`, `troubleshooting.md`. Anchoring the remote-equipment alternation on word boundaries
  would have dropped these to the R17 blanket, so `scanned device` and `configured device` were added
  to the rule, which also caught 15 rows that were already wrong.
- **4 rows `D-REMOTE` -> `D-TARGET`**: `headless-cli.md:112:135`, `retrieve-project.md:54:163`,
  `runtime-status.md:64:110`, `user-management.md:98:130`. These are four of the five harmless
  `pdo`-in-"dropdown" and `esi`-in-"beside" hits; with the alternation anchored they fall to R16,
  which is their real sense. The fifth, `bus-scan.md:7:111`, stays `D-REMOTE` on the strength of
  "Scanned Devices" in the same line, which is correct.

`getting-started/quick-start.md:214`, named in review as a sixth harmless instance, is **not** one:
its context is "Enter a device name (e.g., \"**Modbus**Coils\")" and the rule matches the whole word
"modbus", not a fragment. It is a Modbus remote-device walkthrough and `D-REMOTE` is right, before and
after the fix. So there were 5 harmless instances of that bug, not 6, plus the 2 that mattered.

### One row added

`getting-started/quick-start.md:26:221`, the `O-SE` occurrence the old pattern could not see. Total
1237 -> **1238**.

### One review finding whose diagnosis does not hold

The review said the fenced-block hole "is exactly why `vplc-stuck-stopped.md:27` needed hand override
H10 to escape". Measured: with H10 removed, that row falls to `REVIEW` under both the old and the
current classifier, because it is `docker ps -a | grep <device-name>` and no rule reaches it. H10
codes an unclassified row; it was not escaping the changes-to-literal flip. **The hole itself is
real** and is now closed, as described above and proved against a probe file; only the causal story
is wrong.

## Every census total, with the commit and the script it belongs to

These numbers were being quoted without provenance, and two of them looked like a contradiction that
would have made the Phase 10 gate read a correct tree as a loss. They are all true; they measure
different trees with different classifiers. **Measured, each at its own commit, with that commit's
own script.**

| Commit | Phase | Committed CSV | That commit's script over that commit's tree | Reproduces its own CSV? |
|---|---|---|---|---|
| `c86992f` | 1 | **1237** | **1237** | **yes, byte-identical** |
| `21230b3` | 2 | 1237 | **1229** | no, and deliberately: the CSV was not regenerated |
| `d08ae9c` | 3 | 1237 | **1229** | no, same reason |
| `073ad86` | census review | **1238** | **1230** | against the BASE tree, yes but for 8 path rows |
| this commit | 4 and 5 | 1238 | **1205** | as above |

Reading the table:

- **1237** is the base at `c86992f`, and it is the only figure that is both a committed CSV and a
  live measurement of the same tree.
- **1238** is that same base corrected: widening the pattern to see `orchestration` added the one
  `O-SE` row the old pattern could not match. It is a base-commit figure, not a live one.
- **1229** and **1230** are the same *live* tree after Phase 3, measured with the old and the
  corrected classifier respectively. The +1 is that same `O-SE` row.
- The live total falls as the rename lands, legitimately: renaming
  `orchestrator-detail-devices.png` to `device-detail-vplcs.png` removes an occurrence, and
  rewriting "vPLC devices" to "vPLCs" removes another. **1205** is where it stands now.

The reproducibility claim, stated exactly: the current generator run **against the base tree**
reproduces the committed CSV byte for byte except for 8 rows, the `D-PATH` / `D-PATH-NEW` rows
described above. Run against a *later* tree it differs in hundreds of rows, which is not a failure
but the documented consequence of the CSV being a historical record while the classifier tracks the
tree in front of it.

**What Phase 10 should assert is the code check, not a count.** No occurrence carrying a *changes*
code survives, and every survivor carries a *stays* code that is in this legend. A target total is
not a useful gate, because it moves with every phase for correct reasons.

## Corrections to the demand's documents

Found while measuring, and carried into the change records at pass 2:

1. The Requirements Gathering says **182 documentation pages**. That is a file count. Only **167** are
   reachable from `_config.json`. The other 15 are the 3 internal planning documents, 7 section
   `README.md` files, `index.md`, and the 4 pages of `openplc-editor/hardware-configuration/`.
2. It says **59 files mention "orchestrator" and 82 mention "device"**. Measured: **60 and 84**, or 57
   and 81 excluding `exploration/`.
3. The Cybersecurity Risk Assessment names "the Node network isolation model" as security-relevant
   guidance carried by this repository. **There are zero mentions of Autonomy Node in user-docs**;
   every match for "node" is an OPC-UA node or a project-tree node. The security-relevant set is
   `platform/vplcs/network-modes.md`, `platform/vplcs/overview.md`,
   `platform/orchestrators/installing-the-agent.md`,
   `troubleshooting/orchestrator-not-connecting.md` and `troubleshooting/vplc-stuck-stopped.md`.

## Defects found that predate this demand

Reported, not fixed here, so they can be tracked separately.

1. **`openplc-editor/hardware-configuration/` is orphaned from the navigation.** Four pages,
   `board-selection`, `communication-settings`, `device-config-overview` and `pin-mapping`, are absent
   from `_config.json` and unreachable from it.
2. **Six broken links**, which is the baseline the rename must not extend:
   - `openplc-editor/programming-languages/ladder-diagram/function-blocks-ld.md` points at
     `../images/block-properties-ton.png` and `../images/block-properties-ton-eneno.png`; the files
     are two levels up, in `openplc-editor/images/`
   - `openplc-editor/communication/modbus/addressing.md` -> `../../device-config-overview`
   - `openplc-editor/task-configuration/instance-management.md` ->
     `../working-with-variables/global-variables-editor`
   - `changelog-link` from `platform/autonomy-ai-assistant.md` and `platform/notifications.md`
3. **`docs/platform-features/` is a dead directory**: 7 images, no markdown, and no page references
   any of them. It is the leftover of a `platform-features/orchestrator-management/` section that the
   planning document still describes.
4. **39 images are referenced by no page.** Handled in the phase that deletes them.
5. **Two Editor UI generations coexist in the screenshots.** Older captures show the project tree as
   `Device > Configuration`; newer ones show `Devices > Orchestrators`. The documentation is already
   visually inconsistent, independently of this demand. Filed separately.

## Files

| File | What it is |
|---|---|
| `rename-census.csv` | The census: 1238 rows, one per occurrence |
| `rename-census-overrides.csv` | The 115 hand-pinned rows, which win over the rules |
| `rename-census.py` | Generates the census, and re-verifies it with `--verify` |
| `RENAME-DECISION-RECORD.md` | This document |

The image map required by FR21 is produced separately, in its own phase, and lands as
`RENAME-IMAGE-MAP.md`.
