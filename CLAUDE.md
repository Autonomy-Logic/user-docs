# User Docs repository guidance

## Process entry point

For tracked documentation work, investigations, screenshots, validation, and pull requests, start with
`/autonomy:mister`. Mister verifies the Jira task and current documentation, reconciles process drift,
checks the applicable gates, and routes the work to the right skill. If the plugin or its connected
services are unavailable, report the missing dependency before proceeding; do not invent Jira,
Confluence, approval, or branch state.

This file owns only the conventions of this repository. The current Mister plugin and Confluence
templates are the source of truth for company process. Do not reuse assumptions from an earlier
conversation. Use the approved implementation plan as the primary context and consult the Requirements
Gathering or risk assessment only for a cited constraint or an ambiguity.

Use the branch convention provided by Mister for the current task and branch from `development`.

## Purpose and structure

This repository contains end-user documentation for Autonomy products. Published content lives under
`docs/`; `docs/_config.json` defines the navigation exposed by the product. Keep author-only research and
inventories under `docs/exploration/` and do not present them as published product behaviour. A page may
remain outside the navigation only when it is an authoring aid, exploration material, or reachable by an
intentional internal link from a page that is present in the navigation.

Documentation must describe behaviour verified in the current product. Treat existing prose and old
screenshots as claims to check, not proof. The implementation plan identifies the product repositories
and branches that supply the behaviour being documented.

## Use the integrated application environment

When accurate UI behaviour or new screenshots are required, use
`Autonomy-Logic/local-dev-toolkit` to run the relevant product branches together. If it is not available
locally, leave the User Docs repository and clone it into a sibling workspace directory with
`gh repo clone Autonomy-Logic/local-dev-toolkit ../local-dev-toolkit`. Read its current `CLAUDE.md` and
`README.md`, select the branches named by the implementation plan through its branch command, and run
its status and smoke checks. Do not replace its orchestration with hand-built service commands.

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

Capture screenshots from the branch combination named by the implementation plan. Crop only irrelevant
browser or desktop chrome; do not edit a screenshot in a way that changes product meaning. Review every
image for secrets and personal data before committing it. Record the tested environment, repository
branches, and captured flow in the pull request description.

## Validation

There is no standalone documentation build in this repository. Before opening a pull request:

1. verify the documented flow against the running product when behaviour or UI is involved;
2. resolve every changed internal link relative to its containing file and confirm the destination exists;
3. confirm every changed image reference resolves to an existing file;
4. run `python3 -m json.tool docs/_config.json >/dev/null`;
5. walk each changed navigation entry recursively, concatenate its ancestor and current `path` values,
   and confirm each leaf resolves beneath `docs/` to either `<path>.md` or `<path>/README.md`;
6. inspect the rendered documentation in the product when the change uses product-specific rendering;
7. confirm screenshots match the recorded branches and current terminology.
