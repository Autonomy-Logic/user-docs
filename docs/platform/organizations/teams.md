# Teams

A **team** is a sub-group within an organization. Teams let you scope access and notifications without giving everyone in the org access to everything.

> **Available on Teams and Enterprise plans only.** Not available on Education or Community.

URL: `edge.autonomylogic.com/organizations/{orgId}` → click **Teams** in the side-nav.

## What teams are useful for

- **Per-project access control.** Add Team A to Project X, and Team B to Project Y. People outside the relevant team can't see the project (or can see read-only).
- **Notification routing.** Tag a team in a PR description (`@team-name`) and everyone in that team gets notified.
- **Internal hierarchy.** Mirror your real org chart: *Controls*, *Mechanical*, *Software*, *External Contractors*.

Teams are not required. Many orgs run flat with everyone in the same pool. Use teams when you start tripping over each other.

## The teams page

The page has a master/detail layout:

- **Left**: list of teams in the org, each with a member count.
- **Right**: the selected team's detail view.

## Detail view tabs

Each team's detail view has tabs:

- **General**: name, description, color/icon.
- **Members**: who's in the team. Add or remove from the org's pool.
- **Projects**: which org projects this team has access to, and with what permission level (Read / Write / Admin).
- **Settings**: delete, rename, change visibility (some teams may be hidden from non-members).

The exact tab list may evolve as the feature matures.

## Creating a team

Click **+ New team** at the top of the team list. The dialog asks for:

| Field | Required | Notes |
|---|---|---|
| **Name** | Yes | e.g. *Controls*, *Backend*, *DevOps*. |
| **Description** | No | Optional one-liner. |
| **Visibility** | No | Public (visible to all org members) or Private (visible only to its members). |

Click **Create team**. The team appears in the list. You can now add members and projects.

## Adding members

In the team's **Members** tab, click **Add members**. Pick from the org's existing members. Use search to narrow down for large orgs.

A member can belong to multiple teams. Permissions are union, if Team A grants Read on Project X and Team B grants Write on Project X, the member gets Write.

## Adding projects

In the team's **Projects** tab, click **Add project**. Pick from the org's projects and choose a permission level:

- **Read**: view files, history, PRs.
- **Write**: push commits, open and merge PRs.
- **Admin**: write plus manage project-level settings (when those land).

The same project can be granted to multiple teams at different permission levels.

## Removing a team

From the team's **Settings** tab click **Delete team**. Confirm. Members of the team don't leave the org, only the team grouping goes away. Projects scoped to the team revert to org-wide visibility unless they were *only* visible via this team, in which case they become invisible to former team members.

## Where to next

- **Manage individual people** → **[Members and roles](members-and-roles)**.
- **Send notifications via @team in a PR** → **[Pull requests](../projects/pull-requests)**.
- **Plan eligibility** → **[Pricing](../../plans-and-billing/pricing)**.
