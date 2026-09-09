# Terminology rename: decision record for user-docs

Internal working document. Not part of the published documentation and not in `_config.json`.

Demand [EDGE-633](https://autonomylogic.atlassian.net/browse/EDGE-633), subtask
[EDGE-642](https://autonomylogic.atlassian.net/browse/EDGE-642). Specification in section 8.5 of the
Requirements Gathering, FR17 to FR22. Risk assessment: Cybersecurity Risk Assessment - Ecosystem
terminology rename - User Docs.

This record satisfies **FR17** and **FR20**: every occurrence of "orchestrator" and "device" in this
repository carries a recorded decision, including the ones that stay unchanged. It is the evidence
for **AC05**.

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

## How a decision gets recorded without 1237 sentences

`exploration/rename-census.csv` holds **one row per occurrence**: file, line, column, the word, the
decision code, the id of the rule that assigned it, whether the decision is *changes* or *stays*, and
140 characters of context.

The **reason** is written once per code, in the legend below. A row carries the code. That is the
whole trick: the reason for keeping "remote device" is one sentence, not 184 copies of one sentence.

The census is reproducible: `python3 exploration/rename-census.py` from `docs/`, which classifies
the tree it is run against. The CSV committed here is the run against the base commit; see
`D-PATH-NEW` below for the one classifier change made after it, and why the CSV was left alone.

## The legend

Fourteen codes cover all 1237 occurrences. Two further codes are defined and legitimately empty.
A seventeenth, `D-PATH-NEW`, was added once the section had moved; it is described after the
tables, and its count at the base commit is 0.

### Codes whose occurrences must not survive the rewrite

| Code | n | Sense | Decision and reason |
|---|---|---|---|
| `O-ENTITY` | 272 | orchestrator = the parent product entity | **-> Device.** The rename itself (BR01) |
| `D-VPLC` | 93 | device = the child entity, the virtual PLC | **-> vPLC.** The rename itself (BR02, sense 1) |
| `O-EDGEDEV` | 68 | the platform entity named inside the Editor docs, including both halves of the Editor's screen label "Device Orchestrators" | **-> Edge Device / Edge Devices.** The Editor already uses "Device" for the PLC target, so the platform entity needs the qualifier to stay distinguishable (BR05, FR10) |
| `O-PATH` | 66 | a path, link target or image filename carrying "orchestrator" | **Rewritten by the section move** (FR18) |
| `O-AGENT` | 11 | the orchestrator agent, the daemon on the customer machine | **-> Device Agent** (BR04) |
| `D-PATH` | 10 | a path, link target or image filename where "device" means the child entity | **Renamed to vplc** (FR18) |
| | **520** | | |

### Codes whose occurrences must survive the rewrite unchanged

| Code | n | Sense | Decision and reason |
|---|---|---|---|
| `D-REMOTE` | 184 | remote device: a Modbus master, or an EtherCAT bus or slave device | **Stays.** A different concept, and the word is the industry's, not ours (sense 4) |
| `D-EDITORNODE` | 145 | the Editor's `Device` node and its Device Configuration screens: board selection, pin mapping, communication settings | **Stays.** It means the PLC target being programmed, not the platform entity. This is also why the on-disk `devices/` directory is not renamed (BR06, FR09, sense 3) |
| `X-HIST` | 125 | a dated historical record: the three internal planning documents under `exploration/`, and the changelog entries in `changelog-link.md` | **Stays.** These say what was true, or what a release actually said, at a past date. Renaming them would falsify a record. The planning documents are outside the navigation and already name sections that no longer exist |
| `D-TARGET` | 101 | device = the PLC or runtime the editor is connected to | **Stays. SEVENTH SENSE, absent from the original framework.** The target can be a vPLC or physical hardware, so calling it a vPLC would make these pages wrong for anyone running a real PLC. 99 of the 101 sit in `openplc-editor/building-deploying/` |
| `D-HOST` | 90 | device = the machine the agent runs on, written today as "your edge device" | **Stays as a word.** This is the sense the new vocabulary promotes, so it gets a consistency pass rather than a rename (sense 2) |
| `D-LITERAL` | 33 | a string quoted verbatim from a product interface or message, a CLI subcommand, or the on-disk `devices/` project directory | **Stays byte-identical.** Quoting it differently would misreport what the screen says or print a command that does not work (BR09) |
| `D-PLAIN` | 29 | the plain networking or hardware sense, ordinary English, including "every device" meaning the reader's own browser session | **Stays** (sense 5) |
| `O-LITERAL` | 10 | a literal the software still emits or resolves: the container name, the image reference, the repository URL, and the log line `Unknown orchestrator` | **Stays byte-identical.** These name components that keep their names. Changing them would print an instruction that does not work (BR09, BR13) |
| | **717** | | |

### Defined and legitimately empty

| Code | n | Why it is empty |
|---|---|---|
| `O-SE` | 0 | The ordinary software-engineering sense of "orchestrator" (BR07). It exists in the code of other repositories, `library-build-orchestrator.ts` among them, which is what RSK01 is about. **It does not occur in this repository at all**, so BR07 has nothing to protect here |
| `D-LICENSE` | 0 | The VPP licensed device, a physical hardware unit with a serial anchor (BR12, sense 6). **user-docs does not document VPP licensing**, so this sense never appears |

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
measure `origin/development` at `79c4faa` and still sum to 1237. `rename-census.csv` was **not**
regenerated, so re-running the generator over the base tree no longer reproduces its 10 `D-PATH`
rows: the classifier tracks the tree as it is now, and the CSV is the record of what was decided
then. The census and the 84 overrides are re-derived against the final tree in the verification
phase, where the gate is that no *changes*-coded occurrence survives.

## Where the occurrences are

| Area | O-ENTITY | D-REMOTE | D-EDITORNODE | X-HIST | D-TARGET | D-VPLC | D-HOST | O-EDGEDEV | O-PATH | D-LITERAL | D-PLAIN | O-AGENT | D-PATH | O-LITERAL | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `openplc-editor` | - | 164 | 136 | - | 101 | - | 28 | 67 | 7 | 26 | 3 | 1 | - | - | 533 |
| `platform` | 158 | 2 | 7 | - | - | 52 | 25 | - | 36 | 6 | 14 | 3 | 7 | 3 | 313 |
| `exploration` | - | - | - | 124 | - | - | - | - | - | - | - | - | - | - | 124 |
| `getting-started` | 51 | 18 | 2 | - | - | 13 | 19 | 1 | 9 | - | 4 | 5 | 2 | - | 124 |
| `troubleshooting` | 30 | - | - | - | - | 6 | 13 | - | 8 | 1 | 4 | - | - | 7 | 69 |
| `reference` | 13 | - | - | - | - | 6 | 4 | - | 3 | - | 2 | 2 | - | - | 30 |
| `plans-and-billing` | 12 | - | - | - | - | 11 | - | - | 1 | - | - | - | 1 | - | 25 |
| `account` | 6 | - | - | - | - | 4 | - | - | - | - | 2 | - | - | - | 12 |
| docs root | 2 | - | - | 1 | - | 1 | 1 | - | 2 | - | - | - | - | - | 7 |
| **total** | **272** | **184** | **145** | **125** | **101** | **93** | **90** | **68** | **66** | **33** | **29** | **11** | **10** | **10** | **1237** |

Read the `openplc-editor` row as the reason the rename is smaller than the raw count suggests: 533 of
the 1237 occurrences live there, and only 75 of those change.

**57 of the 182 files** contain at least one occurrence that changes. 99 files contain at least one
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

- 1153 rows were assigned by 17 ordered rules, keyed on the file, the position of the match and the
  text touching it.
- **84 rows were read individually and pinned** in `exploration/rename-census-overrides.csv`, which
  wins over the rules. 67 of those were rows no rule could classify; the other 17 were rows a rule
  classified wrongly, found by auditing.
- The audit is what earned its keep. Two rules were wrong in a way that mattered and were fixed:
  - The agent rule matched the word "agent" anywhere in the 140-character window, which turned 21
    occurrences of the entity into the daemon. It now fires only when "agent" touches the match.
  - The path rule renamed every link and image path containing "device", which would have renamed
    **14 remote-device and device-config paths** that must not move.
  A third fix added a rule for the Editor's `Device Orchestrators` label, whose two words are one
  label and move together; 7 occurrences of its "Device" half had been filed under senses that stay.

A fourth fix closed a hole rather than a misclassification: an unclassified row sitting inside a
fenced code block used to acquire a literal code from the fallback instead of being reported. One row
had been masked that way. Unclassified rows now survive the fallback and are reported, so the census
cannot quietly claim to be complete.

The census also excludes this demand's own two artefacts, which are full of both words by
construction; without that it would measure itself and report 1306.

**What is exact:** the *changes* or *stays* decision on all 1237 rows, and the completeness of the
census. An independent count of raw matches returns 1237, equal to the number of rows, and
`--verify` currently fails with 520 changes-rows outstanding, which is what proves the Phase 10 gate
actually fires.

**What is approximate:** among the *stays* codes, a small number of rows sit on the boundary between
two senses that both stay, most often `D-EDITORNODE` against `D-REMOTE` where a page discusses the
Editor's Device node and remote devices in one sentence. The decision on those rows is right and the
sense is arguable. No row's *decision* depends on resolving one.

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
| `rename-census.csv` | The census: 1237 rows, one per occurrence |
| `rename-census-overrides.csv` | The 84 hand-pinned rows, which win over the rules |
| `rename-census.py` | Generates the census, and re-verifies it with `--verify` |
| `RENAME-DECISION-RECORD.md` | This document |

The image map required by FR21 is produced separately, in its own phase, and lands as
`RENAME-IMAGE-MAP.md`.
