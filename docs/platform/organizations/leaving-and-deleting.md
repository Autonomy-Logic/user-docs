# Leaving and deleting an organization

Two different actions:

- **Leaving**: you, personally, exit an organization. The org keeps existing for everyone else.
- **Deleting**: the entire organization is removed. Affects every member.

## Leaving an organization

If you're a Member or Admin, you can leave at any time.

1. Open the organization's management page (click your avatar in the top-right → **Organizations** → select the organization) and switch to the **Members** tab.
2. Find yourself in the list.
3. Click **Leave organization**.
4. Confirm the dialog.

What happens:

- You lose access to all org projects, orchestrators, and devices immediately.
- Your past commits and forum posts stay attributed to you.
- The dashboard's right-column **Organizations** card no longer shows this org.
- The org's member list shows you as "Removed" in the audit log.

You can rejoin later if an admin invites you again.

### If you're the only Owner

You can't leave as the only Owner, that would leave the org without anyone with permission to manage it.

The fix: from the **Members** tab, promote another member to Owner first, then leave. If there's no one else in the org, you have to **delete** the organization instead of leaving it.

## Deleting an organization

Deletion is permanent. It removes the organization and all of its content.

1. Go to **Org Profile** tab.
2. Scroll to the bottom **Danger zone** section.
3. Click **Delete organization**.
4. Type the organization's name to confirm.
5. Click **Delete permanently**.

What's removed:

- All org projects (public and private).
- All org orchestrators (the cloud entries; the agents on the devices keep running with stale credentials until you uninstall them locally).
- All org vPLC devices.
- All membership records.
- Past invitations and invite links.
- The org's profile, billing history, and audit log.

What's *not* removed:

- Forks of your org's public projects that other people made into their own workspaces. Those are theirs now.
- Forum posts. Past posts stay visible, but the org-affiliation badge on them goes away.

### Active subscriptions

If the org has an active paid subscription, deletion does not refund you. Cancel the subscription first (set it to end at the next billing date), and then delete the org after the cycle ends, or accept that the prorated time is lost.

### Required role

Only **Owners** can delete an org. Admins and Members cannot.

## Transferring ownership

There's no formal "transfer ownership" action because ownership isn't singular, there can be multiple Owners. To hand off:

1. Promote the new person to **Owner**.
2. Once you confirm they're set up and have access, demote yourself to **Member** or **Admin**, or leave the org entirely.

## Where to next

- **Membership management overall** → **[Members and roles](members-and-roles)**.
- **Cancel a subscription first** → **[Org billing](billing)**.
- **Audit who did what** → **[Org history](history)** (when ready).
