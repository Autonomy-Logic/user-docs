# Terminology rename: image map

Internal working document, the **FR21** deliverable. Not part of the published documentation and not
in `_config.json`.

Demand [EDGE-633](https://autonomylogic.atlassian.net/browse/EDGE-633), subtask
[EDGE-642](https://autonomylogic.atlassian.net/browse/EDGE-642).

**The deliverable is this map, not the images.** Regenerating them is FR22 and out of scope here.
What this document owes the recapture session is a list it can work from and a reason per image.

## How this was measured, and what is inherited

Everything in the counts below was **measured against the tree as it stands**, not carried over.
Several inherited figures did not reproduce, and they are called out where they differ.

Two mechanical instruments, both reproducible:

1. **Reference sweep.** For each image, a boundary-correct match of its basename
   (`(?<![\w.-])basename`) against the 179 published pages. Plain substring matching is wrong here
   and was caught doing damage: `orchestrators-expanded.png` matches inside
   `device-orchestrators-expanded.png`, which made a one-page image look like a two-page image.
2. **Full-window detection.** PNG `IHDR` dimensions. A capture at least 1500x850 is a full editor or
   platform window; anything smaller is a crop. The threshold is **sample-validated**, not assumed:
   `bus-tab.png` 3840x2160 and `device-selected-connect.png` 1550x1035 are full windows showing the
   project tree, while `variables-table.png` 2802x370, `project-tree.png` 699x686 and
   `menu-edit.png` 640x664 are crops. An earlier threshold of 1500 on the width alone excluded the
   whole 1550x1035 family and had to be corrected.

**What is inherited and NOT re-verified image by image:** the per-image visual judgement from the
Phase 1 sweep. Reading all 276 again was not affordable, so instead the classification below is
re-derived from mechanical triggers and **sample-validated on four images**. Where the two methods
disagree, both numbers are given.

## Totals

| | Count |
|---|---|
| Images in the repository | **276** (275 PNG + 1 SVG) |
| Referenced by at least one published page | **191** named, **187** actually displayed |
| Not referenced by any published page | **85** |
| ... of which internal capture scratch under `exploration/screenshots/` | **46** |
| ... of which in published areas, i.e. true orphans | **39** |
| Referenced by nothing at all, published or internal | **41** |

**The 191/187 split, added at Phase 10.** The reference sweep above matches an image's
*basename*, so it answers "is this filename named on a published page". Resolving each
reference's path instead answers "does a published page actually display this file", and that
gives **187**. Both are correct answers to different questions, and the sweep's own method
reproduces its 191 exactly, so nothing here is a miscount. But the recapture session cares about
the second question, and **four images differ**:

| Image | Why it is named but not displayed |
|---|---|
| `getting-started/images/profile-overview.png` | `account/user-profile.md:7` displays a **different file of the same name**, `account/images/profile-overview.png`. Different bytes, different screenshot. This copy is an orphan. |
| `openplc-editor/images/block-properties-ton.png` | `programming-languages/ladder-diagram/function-blocks-ld.md:57` points at `../images/...`, which resolves to `programming-languages/images/`. **That directory does not exist.** Two of the six pre-existing link-check failures are exactly this. |
| `openplc-editor/images/block-properties-ton-eneno.png` | Same broken reference, line 61. |
| `openplc-editor/images/server-create-dialog.png` | The page displays `communication/modbus/images/server-create-dialog.png`. Same-basename duplicate; this copy is an orphan. |

All four predate this branch and none was touched by it, so fixing them is not this demand's
call. They matter to **FR22** in one specific way: two of them sit in **tier A**, so a recapture
session working the tier A list would recapture the two TON dialogs for a page that cannot
display them either way. **Fix the path before recapturing those two**, or the new capture is as
invisible as the old one.

Consequently, under path resolution the tiers are **A+B+C = 145 live of the 148 listed** and
**tier D = 42**, against 148 and 43 under the basename sweep. The tier lists themselves are
unchanged: no image moved tier, and the three non-displayed entries are named above rather than
quietly dropped.

Two inherited figures do not reproduce, and the smaller ones are right:

- The plan draft said **43** published-area orphans and **89** orphans in total. Measured: **39**
  and **85**. The decision record's own figure of 39 was correct; the plan draft's 43 was not.
- The 46 files under `exploration/screenshots/` are referenced by the internal planning documents,
  so they are "unpublished" rather than "unreferenced". Only **2** of them are referenced by nothing
  at all. Calling all 46 orphans conflated two different questions.

## The headline finding, confirmed

**The driver is background chrome, not subject matter.** An Editor screenshot needs recapture because
the project tree sits in its left panel reading `Device > Orchestrators`, regardless of what the
screenshot is *about*. Confirmed directly on `openplc-editor/communication/ethercat/images/bus-tab.png`:
its subject is an EtherCAT bus, and its tree plainly shows `Device > Orchestrators`. Nobody would
predict that from the page text, which is exactly why this map is a deliverable.

**But it applies only to full-window captures.** `variables-table.png` is a tight crop of the
variables table with no tree and no tab strip, and needs nothing. The inherited claim that "roughly
45 Editor screenshots about EtherCAT, Modbus, OPC-UA, variables and data types carry the old
vocabulary" is true for the full-window ones and false for the crops. Measured: **68 live Editor
images are full-window captures.**

Also confirmed while sampling: **two Editor UI generations coexist in the captures.**
`bus-tab.png` shows the tree parent as singular `Device`; `device-selected-connect.png` shows it as
plural `Devices`. The documentation is already visually inconsistent, independently of this demand.

## Recapture classification

Three triggers, each mechanical. A live image is certain to need recapture if any of A or B holds.

| Tier | Trigger | Count |
|---|---|---|
| **A** | Its own alt text changed in this branch, or its filename was renamed here. The words around the picture now describe something the picture does not show. | **47** |
| **B** | A full-window **Editor** capture. The tree in it reads `Device > Orchestrators`. | **53** |
| **C** | A full-window capture outside the Editor docs. May or may not show the old vocabulary depending on the screen. **Needs a look, not a decision.** | **48** |
| **D** | A crop with no window chrome, and nothing else triggered. Likely fine. | **43** named, **42** displayed |

**Certain recapture, A + B: 100 live images.** By area:
- `getting-started`: 9
- `openplc-editor`: 73
- `plans-and-billing`: 2
- `platform`: 14
- `troubleshooting`: 2

The inherited figure was **82 both live and needing recapture**. This method gives **100**
certain plus **48** to inspect. The two are consistent: 82 sits inside the band, and the
difference is that a visual sweep judged each non-Editor full window individually where this method
defers them to tier C rather than guessing.

## The SVG is not recapture work

`getting-started/images/platform-architecture.svg` is **hand-authored SVG text, not a capture**. Its
`<text>`, `<title>` and `<desc>` elements were edited in Phase 2 and already read "Device Agent". It
needs nothing from FR22, and it is the one image in the repository that could be fixed by editing
rather than recapturing.

## Tier A, certain: the words no longer match the picture

- `getting-started/images/add-device-step1.png` (1550x1035)
- `getting-started/images/add-device-step2.png` (1550x1035)
- `getting-started/images/add-device-step3.png` (1550x1035)
- `getting-started/images/add-remote-device.png` (1669x968)
- `getting-started/images/add-vplc-modal.png` (1550x1035)
- `getting-started/images/configure-remote-device.png` (1669x968)
- `getting-started/images/devices-list.png` (1550x1035)
- `getting-started/images/platform-architecture.svg` (0x0)
- `getting-started/images/vplcs-list-with-vplc.png` (1550x1035)
- `openplc-editor/communication/ethercat/images/add-device-from-repository-expanded.png` (3840x2160)
- `openplc-editor/communication/ethercat/images/add-device-from-repository.png` (3840x2160)
- `openplc-editor/communication/ethercat/images/add-remote-device-protocol-dropdown.png` (3840x2160)
- `openplc-editor/communication/ethercat/images/add-remote-device.png` (3840x2160)
- `openplc-editor/communication/ethercat/images/bus-tab.png` (3840x2160)
- `openplc-editor/communication/ethercat/images/repository-tab.png` (3840x2160)
- `openplc-editor/communication/modbus/images/remote-device-config.png` (1550x1035)
- `openplc-editor/communication/modbus/images/remote-device-create.png` (376x452)
- `openplc-editor/communication/modbus/images/remote-device-empty.png` (3840x1750)
- `openplc-editor/communication/modbus/images/remote-device-io-group-expanded.png` (3840x1750)
- `openplc-editor/communication/modbus/images/remote-device-io-group-with-alias.png` (3840x1750)
- `openplc-editor/images/block-properties-ton-eneno.png` (1250x1478)
- `openplc-editor/images/block-properties-ton.png` (1250x1478)
- `openplc-editor/images/create-element-popover.png` (376x452)
- `openplc-editor/images/edge-devices-expanded-full.png` (1550x1035)
- `openplc-editor/images/edge-devices-expanded.png` (2802x942)
- `openplc-editor/images/edge-devices-screen.png` (2908x942)
- `openplc-editor/images/edge-devices-vplc-selected.png` (2802x942)
- `openplc-editor/images/project-tree.png` (699x686)
- `openplc-editor/images/vplc-connected.png` (1550x1035)
- `plans-and-billing/images/device-plan-limit.png` (1000x400)
- `plans-and-billing/images/vplc-plan-limit.png` (1000x400)
- `platform/devices/images/device-3dot-menu.png` (1400x460)
- `platform/devices/images/device-detail-vplcs.png` (3840x2000)
- `platform/devices/images/device-info.png` (3840x2000)
- `platform/devices/images/devices-list.png` (3840x2000)
- `platform/devices/images/devices-vplcs-expanded.png` (3840x2000)
- `platform/devices/images/new-device-step1.png` (3840x1926)
- `platform/devices/images/new-device-step2.png` (3840x1926)
- `platform/devices/images/new-device-step3.png` (3840x1926)
- `platform/organizations/images/org-dashboard.png` (3840x1814)
- `platform/vplcs/images/new-vplc-runtime-dropdown.png` (3840x2000)
- `platform/vplcs/images/new-vplc-step1.png` (3840x2000)
- `platform/vplcs/images/new-vplc-step2-network.png` (3840x2000)
- `platform/vplcs/images/new-vplc-step2-nic-expanded.png` (3840x2000)
- `platform/vplcs/images/new-vplc-step3-serial.png` (3840x2000)
- `troubleshooting/images/device-inactive.png` (3840x1814)
- `troubleshooting/images/plan-limit-modal.png` (1000x400)

## Tier B, certain: full-window Editor captures carrying the tree

- `openplc-editor/communication/ethercat/images/bus-advanced.png` (3840x2160)
- `openplc-editor/communication/ethercat/images/repository-tab-expanded.png` (3840x2160)
- `openplc-editor/communication/ethercat/images/slave-channel-mappings-with-alias.png` (3840x2160)
- `openplc-editor/communication/ethercat/images/slave-channel-mappings.png` (3840x2160)
- `openplc-editor/communication/ethercat/images/slave-configuration.png` (3840x2160)
- `openplc-editor/communication/ethercat/images/slave-info.png` (3840x2160)
- `openplc-editor/communication/ethercat/images/slave-startup-params.png` (3840x2160)
- `openplc-editor/communication/modbus/images/modbus-server-buffer-mapping.png` (2795x1912)
- `openplc-editor/communication/modbus/images/modbus-server-overview.png` (3840x1750)
- `openplc-editor/communication/opc-ua/images/opcua-address-space.png` (3840x1750)
- `openplc-editor/communication/opc-ua/images/opcua-certificates.png` (3840x1750)
- `openplc-editor/communication/opc-ua/images/opcua-general-settings.png` (2795x1846)
- `openplc-editor/communication/opc-ua/images/opcua-security-profiles.png` (3840x1750)
- `openplc-editor/communication/opc-ua/images/opcua-users.png` (3840x1750)
- `openplc-editor/communication/s7comm/images/s7-server-full.png` (2795x2092)
- `openplc-editor/custom-data-types/images/array-editor.png` (3840x1750)
- `openplc-editor/custom-data-types/images/enum-editor.png` (3840x1750)
- `openplc-editor/custom-data-types/images/struct-editor.png` (3840x1750)
- `openplc-editor/iec-concepts/images/array-editor-intbuffer.png` (1550x1035)
- `openplc-editor/iec-concepts/images/create-datatype-form.png` (1550x1035)
- `openplc-editor/iec-concepts/images/create-pou-function-form.png` (1550x1035)
- `openplc-editor/iec-concepts/images/datatype-derivation-dropdown.png` (1550x1035)
- `openplc-editor/iec-concepts/images/enum-editor-color.png` (1550x1035)
- `openplc-editor/iec-concepts/images/pou-language-dropdown.png` (1550x1035)
- `openplc-editor/iec-concepts/images/structure-editor-view.png` (1550x1035)
- `openplc-editor/iec-concepts/images/tasks-instances.png` (1550x1035)
- `openplc-editor/iec-concepts/images/variables-table-graphical.png` (1550x1035)
- `openplc-editor/iec-concepts/images/variables-text-mode.png` (1550x1035)
- `openplc-editor/images/create-first-user-dialog.png` (1550x1035)
- `openplc-editor/images/editor-with-program.png` (1550x1035)
- `openplc-editor/images/runtime-status-mainscreen.png` (1897x856)
- `openplc-editor/images/simulator-debugger.png` (3840x1750)
- `openplc-editor/images/simulator-running.png` (3840x1750)
- `openplc-editor/images/source-control-panel.png` (3840x1750)
- `openplc-editor/images/workspace-overview.png` (3840x1750)
- `openplc-editor/library-manager/images/add-library-menu.png` (3136x1482)
- `openplc-editor/library-manager/images/browse-public-libraries.png` (3136x1482)
- `openplc-editor/library-manager/images/library-build-complete.png` (1920x960)
- `openplc-editor/library-manager/images/library-editor-manifest.png` (3136x1482)
- `openplc-editor/library-manager/images/library-function-block.png` (3136x1482)
- `openplc-editor/library-manager/images/library-function.png` (3136x1482)
- `openplc-editor/library-manager/images/library-installed.png` (3136x1482)
- `openplc-editor/library-manager/images/library-manager-system.png` (3136x1482)
- `openplc-editor/library-manager/images/library-project-files.png` (2880x1800)
- `openplc-editor/library-manager/images/missing-libraries.png` (3136x1482)
- `openplc-editor/library-manager/images/new-library-wizard.png` (2880x1800)
- `openplc-editor/library-manager/images/project-libraries.png` (3136x1482)
- `openplc-editor/library-manager/images/publications-tab.png` (2880x1800)
- `openplc-editor/library-manager/images/publish-dialog.png` (2880x1800)
- `openplc-editor/programming-languages/structured-text/images/st-intellisense.png` (1550x1035)
- `openplc-editor/programming-languages/structured-text/images/st-syntax-highlighting.png` (1550x1035)
- `openplc-editor/programming-languages/structured-text/images/st-variables-table.png` (1550x1035)
- `openplc-editor/working-with-variables/images/variables-code-mode.png` (3840x1814)

## Tier C, inspect before deciding

- `account/images/profile-overview.png` (3840x1814)
- `account/settings/images/account-danger-zone.png` (3840x1814)
- `account/settings/images/billing.png` (3840x1926)
- `account/settings/images/privacy.png` (3840x1814)
- `account/settings/images/profile-settings.png` (3840x1814)
- `account/settings/images/security-email.png` (3840x1814)
- `account/settings/images/security-password.png` (3840x1814)
- `account/settings/images/usage.png` (3840x1926)
- `getting-started/images/add-io-group.png` (1669x968)
- `getting-started/images/blank-editor.png` (1669x968)
- `getting-started/images/dashboard-full.png` (3840x1814)
- `getting-started/images/expand-io-group.png` (1669x968)
- `getting-started/images/first-connect-runtime.png` (1669x968)
- `getting-started/images/first-login-runtime.png` (1669x968)
- `getting-started/images/profile-overview.png` (1550x1035)
- `getting-started/images/program.png` (1669x968)
- `getting-started/images/runtime-running.png` (1669x968)
- `plans-and-billing/images/pricing-annual.png` (3840x1814)
- `plans-and-billing/images/pricing-monthly.png` (3840x1814)
- `plans-and-billing/images/usage-acus.png` (3840x1814)
- `platform/community/images/dashboard-feed.png` (3840x1814)
- `platform/forum/images/forum-board.png` (3840x1814)
- `platform/forum/images/forum-home.png` (3840x1814)
- `platform/forum/images/forum-members.png` (3840x1814)
- `platform/forum/images/forum-messages.png` (3840x1814)
- `platform/forum/images/forum-new-topic.png` (3840x1814)
- `platform/forum/images/forum-thread.png` (3840x1814)
- `platform/images/notifications-empty.png` (3840x1814)
- `platform/organizations/images/org-billing.png` (3840x1926)
- `platform/organizations/images/org-history.png` (3840x1926)
- `platform/organizations/images/org-invitations.png` (3840x1926)
- `platform/organizations/images/org-invite-links.png` (3840x1926)
- `platform/organizations/images/org-members.png` (3840x1926)
- `platform/organizations/images/org-new-team.png` (3840x1926)
- `platform/organizations/images/org-profile.png` (3840x1926)
- `platform/organizations/images/org-teams.png` (3840x1926)
- `platform/organizations/images/org-usage.png` (3840x1926)
- `platform/organizations/images/organizations-list.png` (3840x1814)
- `platform/projects/images/project-code-tab.png` (3840x1814)
- `platform/projects/images/project-commits.png` (3840x1814)
- `platform/projects/images/project-import.png` (3840x1926)
- `platform/projects/images/project-pull-requests.png` (3840x1814)
- `platform/projects/images/project-settings.png` (3840x1814)
- `platform/projects/images/projects-pinned-empty.png` (3840x1814)
- `platform/projects/images/projects-recent-grid.png` (3840x1814)
- `platform/projects/images/projects-trash-empty.png` (3840x1814)
- `platform/vplcs/images/vplc-detail.png` (3840x2000)
- `troubleshooting/images/vplc-stopped.png` (3840x1814)

## Deleted in Phase 9 rather than recaptured

An image no page references is dead weight, and recapturing one would be work for nobody.

**19 Editor orphans that would otherwise need recapture:**

- `openplc-editor/communication/modbus/images/add-element-menu.png` (1550x1035)
- `openplc-editor/communication/modbus/images/add-remote-device-dialog.png` (1550x1035)
- `openplc-editor/communication/modbus/images/add-server-dialog.png` (1550x1035)
- `openplc-editor/communication/modbus/images/io-group-expanded.png` (1550x1035)
- `openplc-editor/communication/modbus/images/io-group-with-iec-location.png` (1550x1035)
- `openplc-editor/communication/modbus/images/modbus-server-full.png` (2795x1620)
- `openplc-editor/communication/modbus/images/new-io-group-dialog.png` (1550x1035)
- `openplc-editor/communication/modbus/images/remote-device-protocol-dropdown.png` (1550x1035)
- `openplc-editor/communication/modbus/images/server-protocol-dropdown.png` (1550x1035)
- `openplc-editor/communication/s7comm/images/s7-server-overview.png` (2795x1292)
- `openplc-editor/images/build-process-started.png` (1550x1035)
- `openplc-editor/images/device-orchestrators-connect.png` (1550x1035)
- `openplc-editor/images/device-orchestrators-list.png` (1550x1035)
- `openplc-editor/images/device-selected-connect.png` (1550x1035)
- `openplc-editor/images/program-running.png` (1550x1035)
- `openplc-editor/images/simulator-chart-plotting.png` (3840x1750)
- `openplc-editor/images/workspace-overview-raw.png` (1920x875)
- `openplc-editor/workspace-overview/images/project-explorer-clean.png` (1550x1035)
- `openplc-editor/workspace-overview/images/workspace-layout-full.png` (1550x1035)

**7 images in `docs/platform-features/`, a directory with no markdown at all:**

- `platform-features/project-management/images/create-project-step1.png` (1550x1035)
- `platform-features/project-management/images/create-project-step2.png` (1550x1035)
- `platform-features/project-management/images/create-project-step3.png` (1550x1035)
- `platform-features/project-management/images/dashboard-overview.png` (1550x1035)
- `platform-features/project-management/images/pinned-section.png` (1550x1035)
- `platform-features/project-management/images/projects-page.png` (1550x1035)
- `platform-features/project-management/images/trash-section.png` (1550x1035)

Note the two files Phase 7 deliberately left behind, `device-orchestrators-connect.png` and
`device-orchestrators-list.png`, are **inside** that 19 rather than additional to it. The total
deleted is **26**, not 28.

## Orphans deliberately kept

13 images are referenced by no published page but show no old vocabulary and are not
full-window Editor captures, so deleting them is not this demand's call:

- `getting-started/images/dashboard-main.png` (1550x1035)
- `getting-started/images/forgot-password-page.png` (1550x1035)
- `getting-started/images/login-page.png` (1550x1035)
- `getting-started/images/profile-edit.png` (1550x1035)
- `getting-started/images/signup-page.png` (1550x1035)
- `openplc-editor/images/activity-bar-raw.png` (112x1702)
- `openplc-editor/images/ld-body-blink.png` (1870x284)
- `openplc-editor/images/menu-display.png` (640x116)
- `openplc-editor/images/menu-edit.png` (640x664)
- `openplc-editor/images/menu-file.png` (640x600)
- `openplc-editor/images/menu-help.png` (640x116)
- `openplc-editor/working-with-variables/images/variables-class-dropdown.png` (260x280)
- `platform/images/changelog.png` (3840x1814)

## Internal capture scratch, out of scope

The 46 files under `exploration/screenshots/` are the raw captures behind the internal
planning documents. They are not published, they are referenced only by those documents, and they
are historical by nature, the same reasoning as the `X-HIST` census code. **13 of them show the old
vocabulary** by the inherited sweep; none is customer-facing, so none is recapture work.

## What FR22 has to plan for

- **100 certain**, plus up to **48** more after inspection.
- The Editor share is the bulk of it, and it cannot be reduced by choosing subjects carefully: any
  capture of the current Editor window carries the tree.
- Two UI generations are already mixed in the existing captures, so a recapture pass is also a
  consistency pass whether or not that is intended. Worth a separate ticket.
