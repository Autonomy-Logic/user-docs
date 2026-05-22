# Plan limit reached

You'll hit this modal whenever a creation action would exceed your plan's quota.

![Plan limit reached — Orchestrator limit reached (1/1) on plan Community](images/plan-limit-modal.png)

The modal text follows this pattern:

> **You've reached your plan limit.** {Resource} limit reached ({used} / {total}) on plan {Plan}. Upgrade to add more.

Buttons: **Cancel** and **Upgrade plan**.

## What's hitting the limit

| Modal | Cause |
|---|---|
| *Orchestrator limit reached* | Trying to add an orchestrator beyond your plan cap. Community allows 1. |
| *Device limit reached* | Trying to add a vPLC beyond the cap (across all your orchestrators). Community allows 2. |
| *Private project limit reached* | Trying to create a private project on a plan with 0 private projects allowed (Community). |
| *ACU exhausted* | Triggering an AI Engineer job with insufficient credits. |
| *Seat limit reached* | Trying to invite a new org member beyond seats purchased. |

## The two paths forward

### 1. Free up an existing item

This is the right move if your current usage is bigger than your actual needs.

- **Orchestrators**: delete an orchestrator you don't use. **[Managing orchestrators](../platform/orchestrators/managing-orchestrators)**.
- **Devices**: delete vPLCs you're not running. 3-dot menu on the device card → **Delete**.
- **Private projects**: convert a private project to public, or delete projects you no longer need.
- **Seats**: remove org members you no longer need. **[Members and roles](../platform/organizations/members-and-roles)**.

After freeing up the resource, retry the action that triggered the limit.

### 2. Upgrade

Click **Upgrade plan** in the modal. You'll land on **[Pricing](../plans-and-billing/pricing)**.

For personal slug limits: upgrade your **personal** plan in **[Settings → Billing](../account/settings/billing)** or pick from pricing.

For org slug limits: upgrade the **organization's** plan in **[Org billing](../platform/organizations/billing)**.

For ACU exhaustion specifically: you can buy a one-time ACU top-up without upgrading the plan. See **[AI Credit Units](../plans-and-billing/ai-credit-units)**.

## Confirming your current usage

Always good to verify before deciding what to do. **[Settings → Usage](../account/settings/usage)** shows:

- ACUs (this month vs extras).
- Orchestrators used / allowed.
- Devices used / allowed.
- Private projects used / allowed.

A red bar means you've hit or passed the limit.

## Grandfathered items

If your plan recently decreased (downgrade or trial expiration), you might be *over* your new plan's limit on items you already had. Those items keep working. The plan only blocks **new** creations that would push you further over.

To clean up:

1. Decide which items to keep.
2. Delete the rest.
3. Once you're under the limit, you can resume creating new things.

## Where to next

- **Decide what to delete vs upgrade** → **[Plan limits](../plans-and-billing/plan-limits)**.
- **Compare plans** → **[Pricing](../plans-and-billing/pricing)**.
- **Buy ACU credits one-off** → **[Settings → Usage](../account/settings/usage)** → **Buy more ACUs**.
