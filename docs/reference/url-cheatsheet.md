# URL cheat sheet

Every screen on Autonomy Edge has a stable URL. Memorize a few of these and you can skip a lot of clicking.

Base: `https://edge.autonomylogic.com`.

Replace `{slug}` with your username or an org's slug (see **[Workspaces and slugs](../platform/workspaces-and-slugs)**).

## Workspace-scoped

| URL | What it opens |
|---|---|
| `/{slug}/dashboard` | Workspace dashboard |
| `/{slug}/projects` | Projects list, default *Recent* view |
| `/{slug}/projects?view=recent` | Recent view |
| `/{slug}/projects?view=pinned` | Pinned view |
| `/{slug}/projects?view=trash` | Trash view |
| `/{slug}/projects/{projectId}` | A project's Code tab |
| `/{slug}/orchestrators` | Orchestrators list |
| `/{slug}/orchestrators/{orchestratorId}` | Orchestrator detail (Devices tab) |
| `/{slug}/devices/{deviceId}?orchestratorId={oid}` | vPLC device detail |
| `/{slug}/changelog` | Platform changelog (also `/changelog`) |
| `/{slug}/settings` | Redirects: to `/profile/settings` if it's you, to `/organizations/{orgId}` if it's an org |

## Personal

| URL | What it opens |
|---|---|
| `/profile` | Your own profile |
| `/profile/{userId}` | Someone else's profile |
| `/profile/settings` | Your settings (Profile tab by default) |
| `/profile/settings?tab=profile` | Settings → Profile |
| `/profile/settings?tab=security-email` | Settings → Security → Email |
| `/profile/settings?tab=security-password` | Settings → Security → Password |
| `/profile/settings?tab=privacy` | Settings → Privacy |
| `/profile/settings?tab=usage` | Settings → Usage |
| `/profile/settings?tab=billing` | Settings → Billing |
| `/profile/settings?tab=account` | Settings → Account |
| `/notifications` | Notifications page |

## Organizations

| URL | What it opens |
|---|---|
| `/organizations` | Your organizations list |
| `/organizations/{orgId}` | Org management (Org Profile tab by default) |

The org's "regular" workspace (projects, dashboard, orchestrators) uses the slug pattern `/{org-slug}/...`.

## Forum and community

| URL | What it opens |
|---|---|
| `/forum` | Forum home |
| `/forum/board/{boardSlug}` | A specific category |
| `/forum/thread/{threadSlug}` | A specific thread |
| `/forum/new-topic` | Compose a new topic |
| `/forum/messages` | Direct messages |
| `/forum/members` | Members directory |

## Public pages (no login required)

| URL | What it opens |
|---|---|
| `/` | Landing page |
| `/pricing` | Public pricing |
| `/forum` and everything under `/forum/...` | Forum is browsable without an account |
| `/profile/{userId}` | Any user's public profile |
| `/{slug}/projects/{projectId}` | Public projects readable without an account |
| `/terms-of-use` | Terms |
| `/unsubscribe` | Unsubscribe page (linked from emails) |

## Auth

| URL | What it opens |
|---|---|
| `/signin` | Sign in |
| `/signup` | Sign up |
| `/forgot-password` | Password reset request |
| `/reset-password` | Set a new password (via email link) |
| `/verify-email-code` | Enter the 6-digit email verification code |
| `/verify-code` | Other code verifications (e.g. 2FA when shipped) |
| `/auth-callback` | OAuth/SSO callback (internal) |

## Invitations and unsubscribes

| URL | What it opens |
|---|---|
| `/invitations/join?...` | Join an org via invite link |
| `/invitations/accept?...` | Accept an org email invitation |
| `/unsubscribe?...` | One-click unsubscribe from emails |

## Where to next

- **Memorize the slug concept** → **[Workspaces and slugs](../platform/workspaces-and-slugs)**.
- **Keyboard navigation** → **[Keyboard shortcuts](keyboard-shortcuts)**.
- **The glossary** → **[Glossary](glossary)**.
