# Invite links

Invite links are reusable URLs that let anyone with the link join your organization. They're best for known cohorts, a class of students, a team you've already onboarded elsewhere, where you don't want to type 30 emails.

> **Locked on Community.** Requires Teams or Education plan.

URL: `edge.autonomylogic.com/organizations/{orgId}` → click **Invite Links** in the side-nav.

## How an invite link works

- You create a link with a chosen role.
- Anyone with the URL can visit it; they're prompted to sign in (or sign up if they don't have an account yet).
- On sign-in, they're added to the org with the link's role.
- The platform records *which link* added them, so you can revoke their access later by removing them or by deactivating the link.

Invite links can have:

- **A maximum number of uses**: once exhausted, the link stops working.
- **An expiration date**: after that date, the link stops working.
- **Both, neither, or one of the above**: your call when you create it.

## Creating a link

Click **Create invite link** at the top of the page. The dialog asks for:

| Field | Required | Notes |
|---|---|---|
| **Name** | Yes | A label for the link, visible only to org admins. e.g. *Fall 2026 class*, *Q3 contractors*. |
| **Role** | Yes | Role for anyone joining through this link. **Member** is the safe default; use **Admin** sparingly. |
| **Max uses** | No | Number of times the link can be used. Leave blank for unlimited. |
| **Expires** | No | A date after which the link no longer works. Leave blank for no expiration. |

Click **Create**. The dialog shows the link; copy it with one click. You can also see the link in the list afterwards and copy it from the 3-dot menu.

## The list

Each row shows:

- Link name.
- Role.
- Uses (consumed / total).
- Expiration date or "Never expires".
- Status: **Active**, **Expired**, **Exhausted**, **Revoked**.
- Created by and date.
- **3-dot menu** with actions.

## Per-link actions (3-dot menu)

- **Copy link**: copies the URL to clipboard.
- **View members who joined via this link**: opens a sub-view showing every member who used this link to join.
- **Edit**: change role, max uses, or expiration.
- **Revoke**: deactivates the link immediately. People who already joined keep their membership; the link itself stops accepting new joins.

## Removing members who joined through a link

Use the **Remove invite-link member** action. The dialog lets you select members from the list who joined via this specific link and remove them in bulk. Their access ends immediately; their commits and posts stay attributed to them.

## Security tips

- **Don't post invite links publicly** unless you've set a low max-uses and an expiration.
- **Use named links** to track campaigns. Knowing that 40 people came in via "Fall 2026 class" is much more useful than 40 anonymous joins.
- **Audit periodically.** Revoke links you no longer want active. Members keep their seats; future joins stop.

## Where to next

- **One-off invite by email** → **[Invitations](invitations)**.
- **Manage existing members** → **[Members and roles](members-and-roles)**.
- **Group new members into a team** → **[Teams](teams)**.
