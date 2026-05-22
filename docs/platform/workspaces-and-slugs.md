# Workspaces and slugs

Every URL on Autonomy Edge starts with a **slug**. The slug tells the platform whose workspace you're looking at. If you understand this one detail, the rest of the URL structure makes sense immediately.

## The two kinds of workspaces

- **Personal workspace** — created automatically when you sign up. Its slug is your username. URLs look like `edge.autonomylogic.com/{your-username}/...`. Anything you create that isn't tied to an organization lives here.
- **Organization workspace** — created when you (or someone else) creates an organization. Its slug is the organization's slug, e.g. `autonomy-mine`. URLs look like `edge.autonomylogic.com/{org-slug}/...`. Organization members share everything in this workspace.

Both kinds of workspace use the same routes. `/{slug}/dashboard`, `/{slug}/projects`, `/{slug}/orchestrators` are all valid for *any* slug you have access to. The page layout is identical; only the content (projects, orchestrators, activity feed) changes.

## Routes that follow the slug

These all live under a workspace slug:

| Route | What it shows |
|---|---|
| `/{slug}/dashboard` | The home view for that workspace |
| `/{slug}/projects` | Project list (Recent / Pinned / Trash views via `?view=`) |
| `/{slug}/projects/{projectId}` | A specific project |
| `/{slug}/orchestrators` | Orchestrator cards for that workspace |
| `/{slug}/orchestrators/{orchestratorId}` | A specific orchestrator |
| `/{slug}/devices/{deviceId}?orchestratorId={oid}` | A specific vPLC device |
| `/{slug}/changelog` | Platform changelog (same content for every slug) |
| `/{slug}/settings` | Redirects: to `/profile` if it's your slug, to `/organizations/{orgId}` if it's an org you belong to |

When you're on the dashboard, the URL is `/{slug}/dashboard`. Click the **AUTONOMY Edge** logo in the header and it takes you back to *your personal* dashboard, not the workspace dashboard you were just on.

## Routes that don't use a slug

These are personal or global; they don't depend on which workspace you're viewing:

| Route | What it shows |
|---|---|
| `/profile` | Your own profile |
| `/profile/{userId}` | Another user's profile |
| `/profile/settings` | Your account settings (with `?tab=` to pick a section) |
| `/organizations` | List of every organization you belong to |
| `/organizations/{orgId}` | Org management for that organization (profile, members, billing) |
| `/notifications` | Your in-app notifications |
| `/forum` and everything under `/forum/...` | The forum and direct messages |
| `/pricing` | Public pricing page |
| `/changelog` | Platform changelog |

## Switching workspaces

There are a few ways to move between workspaces:

- **From the dashboard right column.** The **Organizations** card lists every organization you belong to. Clicking an organization's name jumps to that organization's dashboard.
- **By typing the URL.** If you know the slug, just replace it in the address bar. The platform recognizes the slug and loads that workspace's content.
- **From the user menu.** Clicking your avatar shows you the user menu, but it does **not** include a workspace switcher today. To go to an org, use one of the other two methods.

## How the slug interacts with permissions

The slug determines which projects and orchestrators show up, but it doesn't override your permissions:

- In your own slug you can see everything you own.
- In an org slug you see everything in that org *and* you can do what your role allows (Owner > Admin > Member). If you try to edit something you don't have permission for, the platform shows an error rather than silently failing.

## How the slug interacts with plans

Plans are scoped per workspace:

- Your **personal plan** (Community by default) governs what you can create in your own slug.
- An **organization plan** (None, Education, Teams, Enterprise) governs what you can create in that organization's slug.

If you upgrade your personal plan to Pro, you can suddenly create more projects and orchestrators in `/{your-username}/...`, but it does not unlock anything in `/{some-org}/...`. The organization needs its own plan for that.

See **[Plan limits](../plans-and-billing/plan-limits)** for the per-plan quotas.

## A worked example

You sign up as `mariah`. You create an organization called *FactoryFloor* (slug: `factoryfloor`).

- `edge.autonomylogic.com/mariah/dashboard` → your personal dashboard
- `edge.autonomylogic.com/mariah/projects` → your personal projects
- `edge.autonomylogic.com/factoryfloor/dashboard` → the org dashboard
- `edge.autonomylogic.com/factoryfloor/projects` → the org's projects
- `edge.autonomylogic.com/organizations/{factoryfloor-id}` → manage members, billing, and settings for FactoryFloor
- `edge.autonomylogic.com/profile` → your settings, regardless of which workspace you were just looking at
- `edge.autonomylogic.com/forum` → the global forum, regardless of workspace

The slug is not a permission or a plan, it's just the URL prefix for "whose stuff are we looking at?". Internalize that and the rest of the platform falls into place.
