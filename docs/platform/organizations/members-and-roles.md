# Members and roles

The **Members** tab lists everyone in the organization and lets owners and admins manage their roles.

> **This tab is locked on the free Community plan.** You need an active **Teams** or **Education** plan to add members beyond yourself. See **[Org billing](billing)** and **[Pricing](../../plans-and-billing/pricing)**.

URL: `edge.autonomylogic.com/organizations/{orgId}` → click **Members** in the side-nav.

## The three roles

| Role | Can read projects | Can write projects | Can manage members | Can manage org settings | Can manage billing | Can delete the org |
|---|---|---|---|---|---|---|
| **Owner** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Admin** | ✓ | ✓ | ✓ | ✓ | – | – |
| **Member** | ✓ | ✓ | – | – | – | – |

There's always at least one Owner. You can have multiple Owners. Owners can promote Admins to Owner, and Members to Admin or Owner.

## What's on the page

For each member, a row shows:

- Avatar and display name.
- Username and email (visible to admins/owners; email is hidden from members).
- **Role** dropdown (when you have permission to change it).
- **Joined** date.
- **3-dot menu** with member-level actions.

A toolbar at the top usually has:

- Search box to filter by name or email.
- **Invite member** button (opens the invite dialog: see **[Invitations](invitations)**).
- Filter by role.

## Changing a member's role

1. Find the member in the list.
2. Click the **Role** dropdown next to their name.
3. Pick **Owner**, **Admin**, or **Member**.

The change is immediate. The affected member gets a notification.

You cannot demote the last Owner. The platform requires at least one Owner at all times, promote someone else first, then demote yourself.

## Removing a member

From the 3-dot menu pick **Remove from organization**. A confirmation dialog appears. After confirming:

- The member loses access to all org projects, orchestrators, and devices.
- Their commits and forum posts stay attributed to them.
- Their pull requests on org projects stay open (you can close them manually).

You can re-invite a removed member later with **Invitations**.

## Self-actions

A member sees a slightly different menu:

- **Leave organization**: voluntarily exit. See **[Leaving and deleting](leaving-and-deleting)**.
- **View profile**: open their own profile.

## Audit trail

Member changes (added, removed, role changed) are recorded in the org's audit log and surface in the **[History](history)** tab once that feature ships.

## Where to next

- **Invite new members by email** → **[Invitations](invitations)**.
- **Invite via a shareable URL** → **[Invite links](invite-links)**.
- **Group members for project access** → **[Teams](teams)**.
