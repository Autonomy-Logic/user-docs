# Source Control

Every project in the OpenPLC Editor lives in a **git repository**. The editor's **Source Control** panel is the GUI on top of that repository. You stage changes, commit, browse history, switch branches, and resolve dirty-tree warnings without leaving the editor.

Open it by clicking the **git-branch** icon in the activity bar (second from the top). A small badge on the icon shows how many files have pending edits.

## Changes view

The default tab. It lists every file in the working tree that differs from the last commit.

For each file:

- **Click** to open an inline diff (Monaco's DiffEditor) in the central editor area, the left pane is the committed version, the right pane is the current working copy.
- **Discard** (per-file): reverts the file to the last committed state. A confirmation modal warns you that unstaged work in this file will be lost.
- **Restore** (per-file): used when you've discarded changes but still want them back; the editor keeps the diff state so this is non-destructive.

At the bottom of the changes view:

- **Commit message**: free text. Required.
- **Commit**: stages all listed files and creates the commit.

The editor does **not** offer per-file staging in this build. A commit ships everything in the changes list.

## History view

Switch tabs to see the commit log. Each entry shows the SHA, author, message, and timestamp. Click an entry to open a **commit details** panel showing:

- The full commit message.
- The list of files in that commit.
- Per-file diffs (click a file to open it in the central editor).

History is read-only, you don't rewrite commits from here.

## Branches

The current branch is shown in the status bar at the very bottom of the editor (e.g. `main`). Click it to open the **branch switcher** popover:

- **Switch** to an existing branch by clicking its name.
- **Create new branch**: opens a small form for the branch name. Names are sanitised automatically (no leading slashes, no spaces).
- **Delete**: opens a confirmation; a branch can't be deleted if it's the active one or has uncommitted changes that aren't merged.

If the working tree has uncommitted changes when you try to switch, the editor opens an **Unsaved Changes** modal asking whether to commit first, stash, or discard.

## Pulling and pushing

The version-control port supports `pull` and `push`, but the editor surfaces them from the **commit details** panel (right-click menu on a commit), not as standalone buttons. For shared workflows, push and pull happen at the platform level, the editor's git is local to the runtime, and the platform synchronises with GitHub / GitLab / Gitea on its own schedule.

## Diff view

The inline diff is a Monaco DiffEditor: side-by-side panes with syntax highlighting, navigable hunks (use the small chevrons at the right edge to jump between hunks), and inline annotations.

For graphical bodies (LD, FBD), the diff shows the underlying JSON representation, not a visual diff. Reading a JSON diff for a graphical body is more involved than reading code; expect to lean on the body editor for visual context.

## Troubleshooting

**My commit hangs.** The pre-commit hook may be running. Check the console, the runtime publishes hook output there.

**I can't switch branches.** The working tree has uncommitted changes that conflict with the destination branch. Commit them first, or stash them.

**A file shows in the changes view but I haven't edited it.** Some auto-save flows (graphical bodies, project metadata) update files behind the scenes. Open the diff to see what changed. If it's noise, discard it.

**The branch switcher is empty except for `main`.** No other branches exist yet. Create one with the **Create new branch** action.

## What's next

- **[Workspace Layout](workspace-layout)**: where the source-control icon sits in the activity bar.
- **[Pull requests](../../platform/projects/pull-requests)** in the platform docs: the cross-developer review flow that sits on top of branches.
