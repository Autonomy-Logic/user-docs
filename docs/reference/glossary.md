# Glossary

A quick reference for the vocabulary the platform uses. This is what the words on screen actually mean.

## Account

Your Autonomy Edge identity, including credentials, profile, and settings. One account per email.

## ACU (AI Credit Unit)

The credit consumed by AI Engineer jobs. Two pools: monthly allowance and extra credits (never expire). See **[AI Credit Units](../plans-and-billing/ai-credit-units)**.

## Agent (Orchestrator Agent)

The Python+Docker daemon that runs on your edge device. Pairs with the cloud via mTLS WebSocket, manages vPLC containers locally. Installed via `curl https://getedge.me | bash`.

## Audit log

A historical record of changes to an organization (membership, settings, billing). Visible on the org's History tab once the feature ships. See **[Org history](../platform/organizations/history)**.

## Board

A forum category. URL: `/forum/board/{boardSlug}`. Contains topics. See **[Forum overview](../platform/forum/overview)**.

## Branch

A git branch within a project. Defaults to `main`. Used to develop changes in isolation before merging via a pull request.

## Commit

A versioned snapshot of project files with a message, author, and timestamp. See **[Commits and history](../platform/projects/commits-and-history)**.

## Community plan

The free tier. Limits: 1 orchestrator, 2 devices, 0 private projects. AI Chat included, AI Engineer not included. See **[Pricing](../plans-and-billing/pricing)**.

## Cycle time

How often the vPLC runtime executes the main program. Set at project creation. Default `T#20ms`. See **[Creating a project](../platform/projects/creating-a-project)**.

## Device (vPLC device)

A virtual PLC container running on an orchestrator. Has a name, runtime version, NICs. See **[vPLC overview](../platform/vplcs/overview)**.

## DHCP mode

NIC mode where the vPLC gets its IP from your network's DHCP server. Easy, no configuration. Counter-balance: IP can change. See **[Network modes](../platform/vplcs/network-modes)**.

## Education plan

Paid plan for academic institutions. Per-seat pricing, allows same-domain (.edu) invites. See **[Pricing](../plans-and-billing/pricing)**.

## Enterprise plan

Custom-contract plan with unlimited orchestrators/devices and special terms. Contact sales.

## Fork

A copy of a public project, made into a workspace you control. Edit freely, send PRs back. See **[Importing and forking](../platform/projects/importing-and-forking)**.

## IEC 61131-3

The international standard that defines five PLC programming languages: ST, LD, FBD, IL, SFC. The OpenPLC Editor supports all five.

## Invite link

A reusable URL that adds anyone who clicks it as an organization member. See **[Invite links](../platform/organizations/invite-links)**.

## MACVLAN

Docker networking driver that gives a container its own MAC and IP on the physical LAN. The mechanism behind vPLC networking — vPLCs appear as native devices to the rest of the network.

## Notification

A platform-generated alert about an event (PR review request, @mention, plan limit). Both in-app (bell icon, /notifications) and optionally via email. See **[Notifications](../platform/notifications)**.

## OpenPLC

The open-source PLC runtime project that Autonomy Edge is built around. Runs inside each vPLC.

## Orchestrator

The cloud-side entity representing an edge device. Hosts vPLCs. See **[Orchestrator overview](../platform/orchestrators/overview)**.

## Organization

A shared workspace for teams. Has its own slug, dashboard, projects, orchestrators, and billing. See **[Organizations overview](../platform/organizations/overview)**.

## Pinned project

A project you've marked as a personal favorite. Visible only to you, in the **Pinned** view of your projects list. See **[Pinning and stars](../platform/projects/pinning-and-stars)**.

## POU (Program Organization Unit)

An IEC 61131-3 unit of code: a Program, a Function, or a Function Block. Lives in the editor.

## Private project

A project visible only to invited people. Requires a paid plan to create. See **[Visibility and sharing](../platform/projects/visibility-and-sharing)**.

## Project

A git-versioned IEC 61131-3 codebase. The fundamental unit of work. See **[Projects overview](../platform/projects/overview)**.

## Pro plan

Paid personal plan. 20 orchestrators, 100 devices, private projects, full AI Engineer. Recommended for solo professionals. See **[Pricing](../plans-and-billing/pricing)**.

## Public project

A project visible to anyone, including non-account-holders. Stars, forks, and PRs from any account.

## Pull request (PR)

A proposed merge of one branch into another. Reviewable, commentable, mergeable. See **[Pull requests](../platform/projects/pull-requests)**.

## Role (org)

A member's level of access in an organization: Owner, Admin, or Member. See **[Members and roles](../platform/organizations/members-and-roles)**.

## Runtime user

A user account local to a single vPLC. Separate from your Autonomy Edge account. Created on first connect from the editor. See **[Connecting from the editor](../platform/vplcs/connecting-from-editor)**.

## Slug

The username or organization handle in a URL. `/{slug}/dashboard`, `/{slug}/projects`. See **[Workspaces and slugs](../platform/workspaces-and-slugs)**.

## Star

A public "like" on a public project. Counted publicly. See **[Pinning and stars](../platform/projects/pinning-and-stars)**.

## Static mode

NIC mode where you assign a fixed IP, mask, gateway, DNS. Predictable. Use for production. See **[Network modes](../platform/vplcs/network-modes)**.

## Team

A sub-group within an organization. Teams scope project access and notifications. Teams plan and above. See **[Teams](../platform/organizations/teams)**.

## Teams plan

Paid collaborative plan. Adds Organizations with members, invitations, invite links, teams. Seat-priced.

## Topic (forum)

A single conversation thread. Contains an original post and replies. Lives under a board.

## Trash

A holding area for deleted projects. Items can be restored or permanently deleted. See **[Projects list → Trash](../platform/projects/projects-list)**.

## vPLC

Virtual PLC. A Docker container running the OpenPLC runtime on an orchestrator. Behaves on the network like a standalone PLC. See **[vPLC overview](../platform/vplcs/overview)**.

## Workspace

The unit of scoping for projects and orchestrators. Each user has a personal workspace; each organization is a workspace. URL prefix is the slug. See **[Workspaces and slugs](../platform/workspaces-and-slugs)**.

## Where to next

- **Look up keyboard shortcuts** → **[Keyboard shortcuts](keyboard-shortcuts)**.
- **Bookmarkable URLs** → **[URL cheat sheet](url-cheatsheet)**.
- **Frequently asked questions** → **[FAQ](faq)**.
