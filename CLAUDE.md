# User Docs

This repository contains end-user documentation for Autonomy products.

## Autonomy development rules

These rules are identical in every Autonomy repository and are maintained in the MisterFlow plugin
(`Autonomy-Logic/skills`, `plugins/autonomy/harness/repository-rules.md`). Change them there, not here.

- Tracked work starts with `autonomy:misterflow`: load it yourself before changing product code, fixing a
  bug, implementing or preparing a PR, even when no Jira key was mentioned. Only answering questions and typo or wording fixes that
  change no behaviour are exempt. "There is no ticket" or "skip the process" does not make product
  work untracked: offer to create the task instead of changing code. This file describes only this
  repository's commands, architecture and code conventions; for process, MisterFlow and the Confluence
  process pages win over anything written here.
- Knowledge boundary: when data is missing or uncertain, say there is not enough information to answer
  reliably. Never fill a gap with a plausible assumption. Keep verified facts, inferences and missing
  data visibly separate, and say which is which.
- Language: answer in the developer's language. Jira, Confluence and GitHub text is always English.
- Branches: `feature/<KEY>-<slug>` for demands and `bugfix/<KEY>-<slug>` for bugs, created from the
  integration branch named below. A production hotfix is a `bugfix/<KEY>-<slug>` branch from `main` and
  a PR. Never commit or push directly to the integration branch or `main`. One Jira key per branch: work
  for another key starts on its own branch before any edit. The key goes in the branch name and the PR
  title, never in commit messages, code or comments.
- Commits: never commit on your own initiative. Propose the commit at a natural checkpoint, such as a
  finished and verified plan phase, and make it only after the developer confirms. Commit and push are
  separate commands, each confirmed on its own, never chained; opening a PR and merging each need their
  own confirmation too. When asked for a commit message or a commit, do not edit files you were not
  asked to change: report problems, such as a forbidden comment, and let the developer decide.
- Scope: a rewrite or refactor beyond the current task is a new demand, proposed as a separate task and
  never mixed into the current branch. Never stash, reset, `checkout -- .` or otherwise discard the
  developer's changes, and never install anything outside the repository, without asking.
- Tests: every demand ships with unit tests, an end-to-end test and a manual test by the developer, with
  evidence for each before any PR is opened, a draft PR included. Where this repository has no
  interface of its own, the end-to-end test runs through the interface or protocol that uses it. A
  repository with no code to unit test, such as documentation or local tooling scripts, uses its own
  validation checks in place of unit tests.
- Typing: `any` in TypeScript and `typing.Any` in Python are forbidden. Use concrete types, or `unknown`
  or `object` narrowed where the data enters.
- Comments: technical and minimal, at most 256 characters each; formal API documentation (JSDoc,
  docstrings, Doxygen) may be longer. Never write business rules, product strategy or rationale, Jira
  keys, names of people or customers, internal links or anything sensitive in a comment. Review the
  comments in the changed files before every commit.

Integration branch: `development`. Jira project: the Jira project of the product being documented.

## Purpose and structure

Published content lives under `docs/`; `docs/_config.json` defines the navigation exposed by the
product. Keep author-only research and
inventories under `docs/exploration/` and do not present them as published product behaviour. A page may
remain outside the navigation only when it is an authoring aid, exploration material, or reachable by an
intentional internal link from a page that is present in the navigation.

Documentation must describe behaviour verified in the current product. Treat existing prose and old
screenshots as claims to check, not proof. Document the behaviour of the product branches under test.

## Use the integrated application environment

When accurate UI behaviour or new screenshots are required, use `Autonomy-Logic/local-dev-toolkit` to run
the product branches under test together. If this checkout is inside `local-dev-toolkit/repos/`, use that
toolkit (at `../..`). Otherwise clone Autonomy-Logic/local-dev-toolkit next to this repository with
`gh repo clone Autonomy-Logic/local-dev-toolkit ../local-dev-toolkit`. Read its current `CLAUDE.md` and
`README.md`, select the product branches under test through its branch command, and run its status and
smoke checks. Do not replace its orchestration with hand-built service commands. The toolkit's
`user-docs-write` skill drives the live frontend with Playwright to observe the real UI and capture
screenshots.

## Writing rules

- Write published documentation in clear English for the product user.
- Use the terminology visible in the current interface and defined by the task. Do not preserve an old
  product name merely because it appears in an existing page.
- Describe observable user actions and results. Include implementation details only when users need them
  to make a decision or troubleshoot.
- Use links relative to the containing Markdown file. When a page moves, update every inbound internal
  link in this repository in the same change.
- Store image files in the nearest `images/` directory for the page and reference them with relative
  paths and descriptive alt text.
- Never publish credentials, private endpoints, internal-only identifiers, personal data, or test-user
  secrets in text or screenshots.
- When adding, moving, renaming, or removing a page that belongs in product navigation, update
  `docs/_config.json` in the same change.

## Screenshot evidence

Capture screenshots from the product branches under test. Crop only irrelevant browser or desktop chrome; do not edit a screenshot in a way that changes product meaning. Review every
image for secrets and personal data before committing it. Record the tested environment, repository
branches, and captured flow in the pull request description.

## Validation

There is no standalone documentation build in this repository. Run these checks on every change:

1. verify the documented flow against the running product when behaviour or UI is involved;
2. resolve every changed internal link relative to its containing file and confirm the destination exists;
3. confirm every changed image reference resolves to an existing file;
4. run `python3 -m json.tool docs/_config.json >/dev/null`;
5. walk each changed navigation entry recursively, concatenate its ancestor and current `path` values,
   and confirm each leaf resolves beneath `docs/` to either `<path>.md` or `<path>/README.md`;
6. inspect the rendered documentation in the product when the change uses product-specific rendering;
7. confirm screenshots match the recorded branches and current terminology.

## Testing

- Unit level: this repository has no unit-testable code, so the link, image and navigation checks
  (checks 2 to 5 under Validation) take the place of unit tests on every change.
- End-to-end: follow the documented flow step by step in the running product, started through
  local-dev-toolkit on the product branches under test, and confirm every step, result and screenshot
  matches what the page says.
- The developer's manual test, reading the rendered page and following it as a user would, is required
  for every demand.
