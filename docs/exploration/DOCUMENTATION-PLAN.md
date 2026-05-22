# Autonomy Edge — User Manual Rewrite Plan

Compiled from live exploration of `edge-staging.autonomylogic.com` on 2026-05-21 plus cross-reference with `autonomy-edge`, `orchestrator-agent`, `openplc-web`, and `openplc-runtime` source. The current docs (in `docs/`) are AI-generated from source-only context and frequently describe code paths, flags, or flows that users never see. **Keep**: the OpenPLC Editor section (good content for reuse) and the Quick Start *guide itself* (`docs/getting-started/quick-start.md`). **Discard / rewrite from scratch**: everything else, including the rest of `getting-started/`.

The new structure below is organized around what a user actually sees and does in the product — not around backend modules.

---

## What I observed (so the structure below makes sense)

Autonomy Edge is a cloud platform with five intertwined surfaces. A new user manual has to introduce all of them because they interlink in the UI:

1. **Workspaces** — every URL is under a *slug*: either a username (`/thiagoralves/...`) or an org slug (`/autonomy-mine/...`). Switching workspaces is implicit, by navigating to URLs under that slug. The user menu always shows your own slug; the dashboard's left sidebar shows your projects and orchestrators *for the slug you are on*.

2. **Projects** — GitHub-style repos. Each has Code / Pull Requests / Settings tabs, a branch selector, commits, a file tree (`programs/`, `functions/`, `function-blocks/`, `devices/`, `project.json`), and an "Open in editor" button. Created via a 3-step wizard: Project Info → Configuration (language + cycle time) → Visibility.

3. **Orchestrators + vPLCs (Devices)** — an Orchestrator is the cloud-side representation of an `orchestrator-agent` daemon on a Linux edge device, installed via `curl https://getedge.me | bash`. Each orchestrator can host multiple vPLCs (OpenPLC runtime containers). Orchestrators have an Inactive/Active state, CPU/Memory/Uptime stats, and a Devices tab listing vPLCs. Each vPLC has its own detail page with network info, NICs, etc.

4. **Community surface** — Forum (Discourse-like categories, threads, member listing, direct messages), Feed on dashboard (project activity, community joins), Trending Topics widget. Forum exists in two states: public (anyone can read) and logged-in (can post, message, star).

5. **Organizations** — collaborative workspaces with their own slug, dashboard, Org Profile, Members, Invitations, Invite Links, Teams, Billing, History. Most member features require a paid plan; the free Community plan can create an org but cannot invite members.

Plan limits are enforced at the UI: free Community plan = 1 orchestrator, 2 devices, 0 private projects (existing private projects are grandfathered). Plans: **Community** (free), **Education** ($7.50/seat/mo annual), **Pro** ($40.83/mo annual, recommended), **Teams** ($82.50/seat/mo annual), **Enterprise** (custom).

Other cross-cutting elements: a **Sparkle button** in the bottom-right of every protected page opens **Autonomy AI** (an in-app assistant chat); a bell icon in the top-right opens **Notifications**; the user's avatar opens a menu with Profile / Pricing / Settings / Forum / Documentation / Feedback / What's new / Light mode / Sign out.

---

## Proposed structure for the new docs

```
docs/
├── index.md                                # Landing
├── getting-started/                        # KEEP quick-start.md, rewrite the rest
│   ├── what-is-autonomy-edge.md            # NEW – replaces introduction.md
│   ├── account-and-signup.md               # NEW – replaces account-setup.md
│   ├── dashboard-tour.md                   # NEW – the one screen orientation
│   ├── quick-start.md                      # KEEP (already good)
│   └── images/
├── platform/                               # NEW top-level – all UI features
│   ├── workspaces-and-slugs.md             # Personal vs org workspaces, URL model
│   ├── projects/
│   │   ├── overview.md                     # Repo model, what a project is
│   │   ├── creating-a-project.md           # 3-step wizard
│   │   ├── projects-list.md                # Recent / Pinned / Trash, folders, list vs grid
│   │   ├── project-page.md                 # Code tab, file tree, branches
│   │   ├── commits-and-history.md          # Commit log, author, hashes
│   │   ├── pull-requests.md                # PR list, filters, new PR
│   │   ├── importing-and-forking.md        # Import Project button, public project forks
│   │   ├── pinning-and-stars.md            # Pin to top, star public projects
│   │   ├── visibility-and-sharing.md       # Public/Private, README, share link
│   │   └── images/
│   ├── editor/                             # KEEP existing openplc-editor/ content; relink
│   ├── orchestrators/
│   │   ├── overview.md                     # What an orchestrator is, why
│   │   ├── installing-the-agent.md         # curl|bash + ID flow
│   │   ├── orchestrators-list.md           # List card view, CPU/MEM/UPTIME
│   │   ├── orchestrator-detail.md          # Devices tab + Orchestrator tab (charts)
│   │   ├── managing-orchestrators.md       # Rename, delete, three-dot menu
│   │   └── images/
│   ├── vplcs/
│   │   ├── overview.md                     # vPLC = OpenPLC runtime container
│   │   ├── creating-a-vplc.md              # Add Device wizard: name, runtime version, NICs
│   │   ├── vplc-detail.md                  # Uptime, restarts, IP, NICs, status
│   │   ├── network-modes.md                # DHCP vs Static, MACVLAN explanation
│   │   ├── connecting-from-editor.md       # Existing flow; link to editor docs
│   │   └── images/
│   ├── organizations/
│   │   ├── overview.md                     # Personal vs org slugs
│   │   ├── creating-an-org.md              # New Organization modal
│   │   ├── org-dashboard.md                # /{slug}/dashboard for orgs
│   │   ├── org-profile.md                  # Editing org info, logo, links
│   │   ├── members-and-roles.md            # admin/member, role-select
│   │   ├── invitations.md                  # Direct email invites
│   │   ├── invite-links.md                 # Shareable join links
│   │   ├── teams.md                        # Sub-groups within an org
│   │   ├── billing.md                      # Org-level subscription
│   │   ├── history.md                      # Audit log (coming soon)
│   │   ├── leaving-and-deleting.md         # Leave / Delete Organization
│   │   └── images/
│   ├── community/
│   │   ├── feed.md                         # Dashboard center column
│   │   ├── trending-topics.md              # Right sidebar widget
│   │   ├── following-users-and-projects.md # Follow, star, watch
│   │   └── images/
│   ├── forum/
│   │   ├── overview.md                     # Categories, hero, layout
│   │   ├── reading-and-searching.md        # Topics list, sort by Latest/Trending/etc, search
│   │   ├── posting-a-topic.md              # Editor, categories, attachments
│   │   ├── replying-and-reactions.md       # Up/downvotes, flagging, author badge
│   │   ├── messaging.md                    # Direct messages UI
│   │   ├── members.md                      # Top Posters / Most Reputed / New / All
│   │   ├── moderation.md                   # Pinned, Locked topics, reporting
│   │   └── images/
│   ├── notifications.md                    # Bell icon + /notifications
│   ├── autonomy-ai-assistant.md            # Sparkle button, ⌘J shortcut
│   └── search.md                           # Search projects/users (header)
├── account/                                # NEW – everything under user menu
│   ├── user-profile.md                     # Overview / Projects / Stars tabs, contributions
│   ├── editing-your-profile.md             # Name, username, bio, location, timezone
│   ├── settings/
│   │   ├── profile.md                      # Avatar, profile info
│   │   ├── security-email.md               # Email change (7-day cooldown)
│   │   ├── security-password.md            # Password change (sign-out everywhere)
│   │   ├── privacy.md                      # Group chat invites, weekly digest, @mentions
│   │   ├── usage.md                        # ACU credits, orchestrator/device/project quotas
│   │   ├── billing.md                      # Current plan, billing history
│   │   └── account.md                      # Danger zone – delete account
│   └── images/
├── plans-and-billing/                      # NEW
│   ├── pricing.md                          # The 5 plans (Community/Education/Pro/Teams/Enterprise)
│   ├── plan-limits.md                      # Orchestrators/devices/projects per plan
│   ├── ai-credit-units.md                  # ACU model, monthly vs extra credits
│   ├── upgrading-and-downgrading.md
│   └── images/
├── reference/                              # KEEP, but trim to what users actually see
│   ├── glossary.md                         # Reorient: project, orchestrator, vPLC, slug, ACU, board
│   ├── keyboard-shortcuts.md               # ⌘J for AI panel, etc
│   ├── url-cheatsheet.md                   # NEW – the SPA routes that work as direct URLs
│   ├── faq.md
│   └── (drop hardware-boards/iec-keywords/data-types/function-blocks — they belong under editor/)
├── troubleshooting/                        # Trim hallucinated entries
│   ├── orchestrator-not-connecting.md
│   ├── vplc-stuck-stopped.md
│   ├── plan-limit-reached.md
│   ├── email-not-arriving.md
│   └── images/
└── changelog-link.md                       # Just point to /changelog in-app
```

---

## Section-by-section content brief

### `getting-started/`

**`what-is-autonomy-edge.md`** — One page positioning, no architecture diagrams pretending the agent is documented. Cover: browser-first PLC dev, IEC 61131-3 in the cloud, vPLC vs traditional PLC, Linux edge device requirement for running vPLCs, and "you can read/post on the forum and edit public projects without an account." Screenshot: `screenshots/dashboard/01-dashboard-full.png` cropped to top half.

**`account-and-signup.md`** — Sign up flow, email verification (mention the code flow at `/verify-email-code`), forgot-password, password requirements (8+ chars, uppercase, lowercase, number — from `settings/03-settings-security-password.png`), the "rememberMe" checkbox. Note SSO: source imports `AppleIcon, GoogleIcon, WindowsIcon` in `signin.tsx` — so Apple/Google/Microsoft SSO is supported. **Need new screenshots** (logged-out signin, signup, forgot-password forms).

**`dashboard-tour.md`** — The one screen that orients a user. Walk through the three columns (Projects sidebar, Feed center, Organizations + Trending Topics sidebar), the header (logo, search, notifications bell, avatar menu), and the bottom-right Sparkle (Autonomy AI). Screenshots: `dashboard/01-dashboard-full.png`, `overview/01-user-menu-open.png`, `feed/01-feed-filter-dropdown.png`, `misc/03-autonomy-ai-chat-panel.png`.

**`quick-start.md`** — **KEEP AS-IS** for now. It's the only good page in `getting-started/`. Update the image paths once new docs land.

---

### `platform/workspaces-and-slugs.md`

**Critical concept the old docs miss entirely.** Explain that every page lives under a *slug* in the URL:
- `/thiagoralves/dashboard` = your personal workspace
- `/autonomy-mine/dashboard` = the Autonomy-Mine org's workspace
- `/{slug}/projects`, `/{slug}/orchestrators`, etc. — same routes, scoped to the slug
- `/{slug}/settings` redirects to `/profile` (your settings) if slug = your username, or to `/organizations/{id}` (org management) if slug is an org you belong to

Show the user menu badge ("Community Plan") — that's your *personal* plan, distinct from any org plan.

Screenshot needed: one with `/thiagoralves/dashboard` and one with `/autonomy-mine/dashboard` side-by-side, plus `organizations/02-org-dashboard.png`.

---

### `platform/projects/`

The **most important conceptual shift**: projects are *git repos*. Each project has commits, branches, PRs, a file tree with `programs/`, `functions/`, `function-blocks/`, `devices/`, and a `project.json`. The "Open in editor" button launches the OpenPLC Editor on that repo.

- **`overview.md`** — "A project is a versioned IEC 61131-3 codebase backed by git." Cover visibility (Public/Private, lock icon), the four standard folders, README.md. Screenshot: `projects/08-project-detail-code-tab.png`.

- **`creating-a-project.md`** — The 3-step wizard. Step 1: name + folder + description. Step 2: language (ST/LD/FBD/IL/SFC) + cycle time (T#20ms default, picker with day/hour/min/sec/ms/us — `projects/07-new-project-cycle-time-picker.png`). Step 3: visibility (Public/Private — free plan can't go private). Screenshots: `projects/04-create-new-dropdown.png`, `05-new-project-step1-info.png`, `06-new-project-step2-config.png`.

- **`projects-list.md`** — `/{slug}/projects` with sidebar Recent / Pinned / Trash, folder tree, grid vs list view toggle, search bar, Import Project button. Each card shows: open-in-editor icon, public/private lock, star count, link icon (copy URL?), pin, download icon. Screenshots: `projects/01-projects-recent-grid.png`, `02-projects-pinned-empty.png`, `03-projects-trash-empty.png`.

- **`project-page.md`** — Three tabs: Code (default), Pull Requests, Settings (Settings says "coming soon"). Branch selector, "1 branch" link, search files, the file tree, README placement, commit summary bar. Screenshots: `projects/08`, `09`, `10`.

- **`commits-and-history.md`** — `/{slug}/projects/{id}?...` commits view, group-by-date, copy hash, code icon next to each commit. Screenshot: `projects/11-project-commits-history.png`. **Note**: clicking the commit hash currently 404s on staging — *do not document a diff view that doesn't work yet*.

- **`pull-requests.md`** — Filters: All / Open / Closed / Merged / Created by me / Awaiting my review. "New pull request" button. Empty state copy: "No pull requests yet — open one to start a review." Screenshot: `projects/09-project-detail-pull-requests.png`. **Need new screenshot** of an actual PR (none exist on staging).

- **`importing-and-forking.md`** — Import Project button (top of projects list). Public projects show "Star" button on the dashboard feed and project card. Public projects in the feed have a fork-like flow when you open them. Source check: `(Fork)` shows up in project names in screenshots (`Autonomy Factory (Fork)`).

- **`pinning-and-stars.md`** — Pin = personal shortcut in sidebar; Star = like for a public project.

- **`visibility-and-sharing.md`** — Public projects show on user feeds; Private requires paid plan; "Add README" prompts on empty projects.

---

### `platform/orchestrators/` and `platform/vplcs/`

Already partially documented in current `platform-features/orchestrator-management/`, but the existing copy describes flags and Docker internals users never touch. The new pages should be UI-only.

- **`orchestrators/overview.md`** — One orchestrator = one Linux edge device running the `orchestrator-agent` daemon (a Python+Docker container). It maintains a persistent mTLS WebSocket to the cloud and hosts vPLC containers. Screenshot: `orchestrators/01-orchestrators-list.png`.

- **`installing-the-agent.md`** — From the New Orchestrator wizard: enter name → run `curl https://getedge.me | bash` on a Linux machine → paste the generated Orchestrator ID back into the wizard (expires in 5 min). Quote `orchestrator-agent/README.md` for what the agent does. *Don't* document the agent's CLI internals — they're not user-facing.

- **`orchestrators-list.md`** — Card layout: name, status badge (Inactive/Active), three-dot menu, CPU/MEMORY/UPTIME row, expandable "N devices" section. "+ New Orchestrator" tile. Screenshots: `orchestrators/01`, `02-orchestrators-devices-expanded.png`, `05-orchestrator-plan-limit.png` (the plan limit modal).

- **`orchestrator-detail.md`** — Two tabs: **Devices** (default — grid of vPLC cards with status, uptime, project) and **Orchestrator** (OS, CPU cores, memory, disk, network, version stats; CPU Usage and Memory Usage charts with 1h selector). Screenshots: `orchestrators/03-orchestrator-detail-devices.png`, `04-orchestrator-info-tab.png`.

- **`vplcs/creating-a-vplc.md`** — From source (`devices/create.tsx`): name (required), runtime version (selectable from list — `useRuntimeVersions`), at least one virtual NIC (name, physical port, network mode DHCP/static, optional IP/subnet/gateway/DNS, mac auto/manual). Serial ports are configurable too (`useSerialDevices`, `AvailableSerialDevice`). **Need new screenshots** of the Add Device wizard — couldn't open it on staging (2/2 plan limit reached, screenshot: `vplcs/02-new-device-plan-limit.png`). Tell the user to delete a device first if at limit.

- **`vplcs/vplc-detail.md`** — `/{slug}/devices/{id}?orchestratorId={oid}`. Shows UPTIME, RESTARTS, INTERNAL IP, NETWORK MODE, GATEWAY, DNS, SUBNET MASK, CREATED, plus Network Interfaces section. Screenshot: `vplcs/01-device-detail-stopped.png`.

- **`vplcs/network-modes.md`** — DHCP (default, gets IP from your router) vs Static. Explain MACVLAN briefly: the vPLC container appears on your physical LAN as if it were a standalone PLC with its own IP and MAC. This is from `orchestrator-agent/README.md` and is the differentiator from regular Docker networking.

- **`vplcs/connecting-from-editor.md`** — Cross-link to existing `openplc-editor/connecting-to-runtimes.md`.

---

### `platform/organizations/`

This is the biggest documentation gap — old docs barely mention organizations.

- **`overview.md`** — An org is a separate workspace with its own slug, dashboard, and projects. Members have roles (admin/member from `role-select.tsx`). Free Community plan can create one org but member management is locked. Screenshots: `organizations/01-organizations-list.png`, `02-org-dashboard.png`.

- **`creating-an-org.md`** — "+ New" button on `/organizations`. Modal: name (required), description (optional), website (optional). Screenshot: `organizations/06-create-organization-modal.png`.

- **`org-dashboard.md`** — `/{org-slug}/dashboard` mirrors the user dashboard layout but scoped to the org. Banner if no plan: "Autonomy-Mine doesn't have an active plan yet → View plans." Screenshot: `organizations/02-org-dashboard.png`.

- **`org-profile.md`** — `/organizations/{orgId}` → Org Profile tab. Avatar upload (400×400 JPG/PNG/GIF, 2MB max), name (100 chars), description (500 chars), Contact & Social links (below the fold). Screenshot: `organizations/03-org-management-profile.png`. **Need new screenshot** of the full form scrolled.

- **`members-and-roles.md`** — Lock-gated on free plan. From source (`member-list.tsx`, `role-select.tsx`): admin can change roles, remove members. Use existing source to describe roles. **Need new screenshots** of unlocked Members tab — needs paid plan.

- **`invitations.md`** — Direct email invites (`invite-member-modal.tsx`, `invitation-list.tsx`). Locked on free plan.

- **`invite-links.md`** — Shareable URLs that anyone with the link can use to join (`invite-link-list.tsx`, `create-invite-link-modal.tsx`). Locked on free plan. There's also a `remove-invite-link-member-modal.tsx` so admins can revoke individual members who joined via a link.

- **`teams.md`** — Sub-groups within an org (`teams/TeamsPage`, `TeamCreateView`, `TeamDetailView`, with `general` tab). Locked on free plan.

- **`billing.md`** — Org-level subscription separate from personal plan. "Choose a plan" → Teams/Education. Screenshot: `organizations/04-org-billing-no-subscription.png`.

- **`history.md`** — "Coming soon" — invoices and lifecycle events. Screenshot: `organizations/05-org-history.png`.

- **`leaving-and-deleting.md`** — `leave-organization-modal.tsx` and `delete-organization-modal.tsx`.

---

### `platform/community/`

- **`feed.md`** — Dashboard center column. Activity types observed: user created public project, user joined community ("Welcome to the community!"), org updated settings. Filter dropdown: Recommended (Coming soon), **Recents** (default), Popular (Coming soon), Organization Feeds (per-org filter). Screenshots: `dashboard/01-dashboard-full.png`, `feed/01-feed-filter-dropdown.png`.

- **`trending-topics.md`** — Right sidebar showing forum hot topics with category, author, comments, views. "View Forum" CTA.

- **`following-users-and-projects.md`** — Star on projects, follower count on profiles ("1 follower / 0 following" in `user-profile/01-profile-overview.png`).

---

### `platform/forum/`

The forum is a fully-featured community surface. Categories observed on staging:
- News & Announcements (87 topics)
- OpenPLC - General Discussion (with sub-tags: OpenPLC on Raspberry Pi / UniPi / Arduino / PC; 997 topics)
- OpenPLC Hardware (Modbus TCP can not c... topic shown at fold)
- OpenPLC Editor
- Sample PLC Programs
- OpenPLC Projects
- Custom Function Blocks
- OpenPLC em Português (PT-BR localized)
- Bug Reports
- Patreons Only (gated)

Total stats from staging: 4.4K Topics, 27K Posts.

- **`overview.md`** — Hero, stats, categories, topic table. Mark All Read / Members / + New Topic toolbar. Screenshot: `forum/01-forum-home.png`.

- **`reading-and-searching.md`** — Sort: Latest / Trending / Most Replied / Most Viewed. Search topics bar. Topic table columns: TOPIC / USERS / REPLIES / LIKES / VIEWS / ACTIVITY. Screenshot: `forum/03-forum-board-category.png`.

- **`posting-a-topic.md`** — `/forum/new-topic` (no slug needed). Category picker chips, Topic title, rich-text editor (Write/Preview tabs, H/B/I/U/S, code, link, lists, quote toolbar), drag-drop file attachments, Discard / Publish Topic. Screenshot: `forum/05-forum-new-topic.png`.

- **`replying-and-reactions.md`** — Author badge (post owner) vs Member badge. Up/downvote counts. Flag icon for reporting. Screenshot: `forum/04-forum-thread-detail.png` (shows Pinned + Locked badges, a thread with 2 posts).

- **`messaging.md`** — `/forum/messages` direct messages. Two-pane Discord/Slack-style UI: conversation list + chat. Search conversations, filter, "+" new conversation, group chat icon. Same rich text toolbar. Screenshot: `forum/07-forum-messages.png`.

- **`members.md`** — `/forum/members` with tabs Top Posters (default) / Most Reputed / New Members / All Members. Period filter (This Month / This Year / etc.). Screenshot: `forum/06-forum-members.png`.

- **`moderation.md`** — Topic states: Pinned (📌), Locked (🔒). Reporting via flag icon. Admin/staff features from `app/(protected)/_layout/admin/forum-*` routes (forum-moderation, forum-bans, forum-ban-user, forum-categories) — link to a future admin guide rather than expanding here.

---

### `platform/notifications.md`

`/notifications` page and the bell icon in the header. Empty state: "No notifications yet. We'll let you know when something happens." Screenshot: `misc/01-notifications-empty.png`. **Need new screenshot** with at least one populated notification.

### `platform/autonomy-ai-assistant.md`

The Sparkle button in the bottom-right of every protected page (added in v1.3.0, March 18 2026 per changelog). Shortcut: ⌘J to toggle, Esc to close. Opens a chat panel: "I'm grounded on the full Autonomy Edge documentation — ask me anything about the platform, and I'll guide you through how things work." Screenshot: `misc/03-autonomy-ai-chat-panel.png`. **Note**: AI Engineer credits (ACUs) are tracked separately on Usage tab — clarify that the AI assistant chat itself is free on all plans but full "AI Engineer access" requires Education+.

### `platform/search.md`

Header search bar: "Search projects or users". Returns project cards + user cards. (No screenshot of populated results captured — **need new screenshot**.)

---

### `account/` (everything under the user-avatar menu)

User menu items: Profile / Pricing / Settings / Forum / Documentation / Feedback / What's new (= `/changelog`) / Light mode (theme toggle) / Sign out. Screenshot: `overview/01-user-menu-open.png`.

- **`user-profile.md`** — `/profile/{userId}` for others, `/profile` for yourself. GitHub-style: avatar, name, @username, follower/following count, email (own only), Edit Profile button (own only), README.md placeholder, contribution heatmap by year (Jan–Dec, weekday rows), Current streak / Longest streak / Best day / Most active stats. Tabs: Overview / Projects / Stars. Screenshot: `user-profile/01-profile-overview.png`.

- **`editing-your-profile.md`** — `/profile/settings?tab=profile`. Avatar upload, Name, Username, Bio, Location, Time zone. Screenshot: `settings/01-profile-settings.png`. **Need new screenshot** of avatar uploader.

- **`settings/security-email.md`** — Change email with 7-day cooldown, signs out everywhere after. Screenshot: `settings/02-settings-security-email.png`.

- **`settings/security-password.md`** — Current + new + confirm, signs out of all sessions. 8 chars / uppercase / lowercase / number rule. Screenshot: `settings/03-settings-security-password.png`.

- **`settings/privacy.md`** — Toggles for: Group chat invitations, Weekly forum digest, Forum @mention emails, Replies to topics you started (and more below the fold — **need full scrolled screenshot**). Screenshot: `settings/04-settings-privacy.png`.

- **`settings/usage.md`** — Tracks AI Credit Units (ACUs) and plan quotas. "THIS MONTH" pool (refills with billing cycle) vs "EXTRA CREDITS" (never expire). How-it-works explainer. Below: Usage bars for Orchestrators / Devices / Private projects (color goes red at limit). Screenshot: `settings/05-settings-usage.png`. Cross-link to `plans-and-billing/ai-credit-units.md`.

- **`settings/billing.md`** — Personal subscription: plan, cycle, next billing date, billing history table. Screenshot: `settings/06-settings-billing.png`.

- **`settings/account.md`** — Danger zone: Delete my account. "Forum posts, topics and direct messages remain visible, credited to [deleted]. If you own organizations, you must transfer them or delete them first." Screenshot: `settings/07-settings-account-danger-zone.png`.

---

### `plans-and-billing/`

- **`pricing.md`** — Monthly vs Annual toggle. Five plans with exact numbers from staging (snapshot 2026-05-21):
  | Plan | Annual price | ACUs/mo | Limits | Key features |
  |---|---|---|---|---|
  | Community | Free | — | 1 orch · 2 devices · 0 private projects | IEC 61131-3 editor, PLC simulator, version control, AI Chat (free), public projects |
  | Education | $7.50/seat/mo | 1,125 | 1 orch · 10 devices/seat | Private projects, .edu invites, Full AI Engineer |
  | Pro (recommended) | $40.83/mo | 6,125 | 20 orch · 100 devices | Private projects, Full AI Engineer, 14-day trial |
  | Teams | $82.50/seat/mo | 12,375 | 5 orch · 20 devices/seat | Private + Orgs + invites + Full AI + 14-day trial |
  | Enterprise | Custom | Custom | Unlimited | Orgs + invites, Full AI Engineer, custom contract |

  Screenshots: `billing/01-pricing-annual.png`, `02-pricing-monthly.png`.

- **`plan-limits.md`** — What happens at the limit (the "You've reached your plan limit" modal with Upgrade plan / Cancel buttons). Show both orchestrator and device limit modals. Screenshots: `orchestrators/05-orchestrator-plan-limit.png`, `vplcs/02-new-device-plan-limit.png`.

- **`ai-credit-units.md`** — How ACUs work: monthly allowance refills with billing cycle, extras never expire, monthly drains first. "Buy more ACUs" button. **Need new screenshot** of the buy-more modal.

- **`upgrading-and-downgrading.md`** — From `/profile/settings?tab=billing` or from any limit modal. Personal vs org plan are separate. Trial mechanics for Pro/Teams.

---

### `reference/`

Trim hard. The current reference files (`data-types.md`, `function-blocks.md`, `iec-keywords.md`, `hardware-boards.md`) belong under the editor section, not under a "platform reference" — they're language docs, not UI docs. Move them to `platform/editor/reference/` or leave them where they are under `openplc-editor/`.

- **`glossary.md`** — Reframe around UI vocabulary: *workspace, slug, project, branch, commit, orchestrator, agent, vPLC, device, NIC, MACVLAN, ACU, organization, board, thread*. Drop IEC-specific terms (they live with the editor).

- **`keyboard-shortcuts.md`** — Observed: ⌘J toggles Autonomy AI panel, Esc closes it. Cmd/Ctrl+S to save in editor (mentioned in quick-start). **Audit needed** — likely more shortcuts in the editor.

- **`url-cheatsheet.md`** — NEW. Direct URLs that work (so users can bookmark):
  - `/{slug}/dashboard`
  - `/{slug}/projects` (with `?view=recent|pinned|trash`)
  - `/{slug}/projects/{id}`
  - `/{slug}/orchestrators`
  - `/{slug}/orchestrators/{orchestratorId}`
  - `/{slug}/devices/{deviceId}?orchestratorId={oid}`
  - `/organizations`, `/organizations/{orgId}`
  - `/profile`, `/profile/{userId}`, `/profile/settings?tab=...`
  - `/forum`, `/forum/board/{slug}`, `/forum/thread/{slug}`, `/forum/new-topic`, `/forum/messages`, `/forum/members`
  - `/notifications`, `/changelog`, `/pricing`

- **`faq.md`** — Trim hallucinated entries. Add the ones we actually observed: "Why can't I create a private project?" "Why can't I add members to my org?" "Why is the Members tab grayed out?" "How do I reset my orchestrator ID?" "What happens if I delete my account but own an org?"

---

### `troubleshooting/`

Trim hallucinated entries. Reorganize around real symptoms observed:

- **`orchestrator-not-connecting.md`** — Inactive status, expired install ID (5 min), agent logs to check.

- **`vplc-stuck-stopped.md`** — Status "Stopped", "Container unknown". Check orchestrator connectivity first, then runtime logs.

- **`plan-limit-reached.md`** — Modal copy and what to do. Different limits per plan.

- **`email-not-arriving.md`** — Verify email, resend verification, change email cooldown. Mention v1.2.2 fix for verification token bug.

---

## What still needs to be captured

Items I couldn't capture during this session, in priority order:

1. **Logged-out pages** — landing page (`/`), `/signin`, `/signup`, `/forgot-password`, `/reset-password`, `/verify-email-code`, public forum view, public profile, public project view, `/terms-of-use`. These need either a second incognito session or a logout + re-login round trip.
2. **Add Device wizard** — blocked by 2/2 plan limit. Delete a device first, or do this on a paid test account.
3. **Active orchestrator views** — the staging orchestrator is Inactive; need a screenshot of CPU/memory charts with actual data and a connected vPLC showing IP.
4. **Org Members / Invitations / Invite Links / Teams** — locked by free plan; do on a paid test account.
5. **Populated notifications panel** — empty on staging.
6. **Search results** — header search with a populated query.
7. **Buy more ACUs modal** — didn't open it.
8. **Avatar upload modal** — didn't open it.
9. **Three-dot menus** on orchestrator card and vPLC card — show rename/delete options.
10. **Project import flow** — didn't run Import Project.
11. **Visibility step 3** of New Project wizard — didn't reach it (the modal seems to auto-submit when you click certain areas).
12. **Light mode** — captured everything in dark mode.

---

## What to discard from the old docs

Be ruthless. Specifically:

- `getting-started/account-setup.md`, `dashboard-overview.md`, `desktop-vs-edge.md`, `editor-desktop-vs-edge.md`, `introduction.md`, `user-profile.md` — all to be rewritten; new structure handles all of this.
- `getting-started/images/*` — keep only the editor-related ones referenced by `quick-start.md`. Delete the others — they will mismatch the new screenshots.
- `platform-features/README.md` and all sub-READMEs — replaced by per-feature structure under `platform/`.
- `advanced-topics/integration-apis/` — verify it describes real endpoints before keeping; the source has a clear API surface (we saw `/organizations`, `/devices`, etc.) but the existing docs may hallucinate endpoint shapes.
- `reference/hardware-boards.md`, `iec-keywords.md`, `data-types.md`, `function-blocks.md` — these are *editor* reference content, not platform reference. Either move under `platform/editor/reference/` or leave under `openplc-editor/`.
- Any references to flags, env vars, or commands that aren't `curl https://getedge.me | bash` or `Cmd+S`. Users don't see those.

---

## What to keep

- `docs/openplc-editor/**` — the whole tree. There may be small inaccuracies but the content shape is right.
- `docs/getting-started/quick-start.md` — keep. Update internal image paths after the rewrite settles.
- `docs/diagrams/` — keep if the diagrams still reflect the architecture; otherwise redo with current observations.
- `docs/_config.json` — keep, update the nav tree to match new structure.

---

## Suggested first slice (if you want to ship something in days, not weeks)

If you don't want to rewrite everything at once, this is the order I'd ship in:

1. **`platform/workspaces-and-slugs.md`** — unblocks every other page that uses URLs.
2. **`getting-started/dashboard-tour.md`** — the entry point for new users.
3. **`platform/projects/{overview, creating-a-project, project-page}.md`** — most-used surface.
4. **`platform/orchestrators/{overview, installing-the-agent, orchestrators-list}.md` + `platform/vplcs/overview.md`** — bridges to the existing quick-start.
5. **`plans-and-billing/pricing.md` + `account/settings/usage.md`** — answers the inevitable "why is X locked?" question.
6. **`platform/forum/{overview, posting-a-topic}.md`** — community onboarding.
7. **`platform/organizations/{overview, creating-an-org}.md`** — collaboration onboarding.

Everything else is incremental fill-in.
