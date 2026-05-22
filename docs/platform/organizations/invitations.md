# Invitations

Invitations are one-shot, email-addressed invites to join an organization. They're the simplest way to bring in a known person.

> **Locked on Community.** Requires Teams or Education plan. See **[Org billing](billing)**.

URL: `edge.autonomylogic.com/organizations/{orgId}` → click **Invitations** in the side-nav.

## What an invitation does

When you invite someone:

1. The platform sends an email to the address you provided with a join link.
2. The invitation appears in the org's Invitations list, status **Pending**.
3. When the recipient clicks the link and signs in, they're added to the org with the role you chose, and the invitation moves to **Accepted**.

Invitations expire after a configurable period (typically 7 days). Expired invitations can be re-sent.

## Sending an invitation

Click **Invite member** at the top of the page. The dialog asks for:

| Field | Required | Notes |
|---|---|---|
| **Email** | Yes | The recipient's email address. They don't need an Autonomy Edge account yet, the link will prompt them to sign up if needed. |
| **Role** | Yes | The role they'll have on acceptance. Pick from **Owner**, **Admin**, or **Member**. You can change it later from **[Members](members-and-roles)**. |
| **Message** *(optional)* | No | A note that goes into the invitation email along with the join button. |

For .edu accounts on the **Education** plan, the platform validates that the recipient's email domain matches yours. This is a feature of the Education plan, not a hard rule of invitations in general.

Click **Send invitation**. The recipient gets the email; you see the new row in the list.

## The invitations list

Each row shows:

- Email address.
- Role they'll receive.
- Invited by (you, or another admin).
- Status: **Pending**, **Accepted**, **Expired**, **Revoked**.
- Sent date.
- **3-dot menu** with actions.

## Per-invitation actions (3-dot menu)

- **Resend**: sends the same invitation email again. Useful if it got buried.
- **Copy link**: copies the join link to your clipboard, in case you want to deliver it through a different channel.
- **Revoke**: cancels the invitation. The link stops working immediately.

## Common scenarios

- **You sent the wrong role.** Revoke and re-send with the correct role. Once accepted, change role from **[Members](members-and-roles)**.
- **The invitation expired.** Resend it: the platform issues a new link with a fresh expiration.
- **The recipient already has an Autonomy Edge account but with a different email.** They have two options: accept on the invited email (they'll have two accounts), or ask you to revoke and re-invite to their primary email.

## Where to next

- **Once they're in, manage their role** → **[Members and roles](members-and-roles)**.
- **Prefer a shareable URL** → **[Invite links](invite-links)**.
- **Organize people into sub-groups** → **[Teams](teams)**.
