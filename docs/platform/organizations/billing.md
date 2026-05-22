# Organization billing

Organization billing is separate from personal billing. Your personal plan governs your own slug; an organization's plan governs the org's slug.

URL: `edge.autonomylogic.com/organizations/{orgId}` → click **Billing** in the side-nav.

![Billing tab — No active subscription state](images/org-billing.png)

## States the page can be in

- **No active subscription.** Fresh org, or after a subscription was canceled. The page shows "No active subscription" with a **Choose a plan** button.
- **Trialing.** A trial is active; you'll see the trial end date and a payment-method warning.
- **Active.** The plan is paid; you see the plan name, billing cycle, next billing date, and a list of seats/usage.
- **Past due.** A payment failed; the platform shows a warning and asks you to update the payment method.

## Picking a plan

From the "No active subscription" state, click **Choose a plan**. You'll be redirected to the pricing page filtered to plans available for organizations (Education and Teams; Enterprise is "Contact sales").

After picking a plan you'll go through a checkout flow with seat count, billing cycle (monthly or annual), and payment details. Once the webhook confirms activation, the billing tab updates to the **Active** state.

## What you'll see on an active subscription

For a typical Teams subscription:

| Field | Description |
|---|---|
| **Plan** | e.g. *Teams · Annual*. Includes seat count and any add-ons. |
| **Next billing date** | When the next charge will hit your payment method. |
| **Seats** | Used / Total. Used = number of members. |
| **AI Credit Units (ACUs)** | Monthly allowance and balance. |
| **Devices and orchestrators** | Limits per plan. |

Changing seats, billing cycle, or payment method happens in this tab.

## Adding seats

If you've hit your seat cap, the **Add seats** action lets you bump the count. The platform pro-rates the charge to the current billing cycle.

## Downgrading

From the **Change plan** action you can switch to a smaller plan. Downgrades take effect at the next billing cycle, not immediately. If the downgrade would put you below current usage (e.g. you have 12 members but the new plan allows 10), the platform either prompts you to remove members or rejects the change.

## Canceling

**Cancel subscription** is available under the plan summary. Cancellation:

- Sets the subscription to end at the next billing date.
- Keeps everything working until that date.
- Drops you to no-subscription state afterwards — member management, private projects, and other paid features stop working.

## Payment methods

The platform supports credit cards via its payment processor. Methods are managed inline in this tab: **Add card**, **Set as default**, **Remove**.

## Invoices

A list of past invoices with **Download PDF** for each. Each invoice has the line items, taxes, totals, and your billing address.

## Who can see billing

- **Owner**: full access.
- **Admin**: full access.
- **Member**: cannot see this tab. The side-nav hides it for them.

## Where to next

- **Plan comparison** → **[Pricing](../../plans-and-billing/pricing)**.
- **Plan limits per feature** → **[Plan limits](../../plans-and-billing/plan-limits)**.
- **Past invoices and audit log** → **[Org history](history)**.
