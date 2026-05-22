# Upgrading and downgrading

## Where to upgrade

Three entry points, all go to the same place:

- **Settings → Billing → Change plan.** From your account settings.
- **Pricing page** at `edge.autonomylogic.com/pricing`. From the user menu's *Pricing* link, or directly.
- **Plan-limit modal.** Click **Upgrade plan** when you hit a limit.

For organization plans, use the org's own Billing tab at `edge.autonomylogic.com/organizations/{orgId}` → **Billing**.

## Upgrading

1. Pick the target plan on the pricing page.
2. Choose **Monthly** or **Annual** billing.
3. Enter (or confirm) payment details.
4. Confirm.

The new plan activates **immediately**. You're charged a prorated amount for the rest of the current cycle if you had a prior paid plan, or the full first cycle if you were on the free plan.

Once active:

- Higher limits unlock.
- ACU allowance jumps to the new plan's amount, prorated to the rest of the cycle.
- You can immediately create things you couldn't before.

## Starting a trial

Pro and Teams plans offer **14-day trials**. To start a trial:

1. Pick the plan on the pricing page.
2. Click **Start trial**.
3. Enter payment details (the platform asks but doesn't charge yet).
4. The trial activates.

During the trial:

- Every plan feature is available.
- Your billing card is not charged.
- You'll get reminder emails about the trial end.
- At the end of the trial, the platform either auto-charges your payment method (if added) or drops you back to Community (if no payment method).

You can cancel the trial at any time before it ends without being charged.

## Downgrading

1. Click **Change plan** in **Settings → Billing**.
2. Pick a smaller plan.
3. Confirm.

The downgrade is scheduled for the **next billing cycle**, not immediate. You keep the higher plan's features until the cycle ends.

When the downgrade lands:

- Limits drop to the new plan's quotas.
- Items over the new limit are **grandfathered**: they keep working but you can't add new ones over the limit. See **[Plan limits → Grandfathering](plan-limits)**.
- ACU monthly allowance drops to the new plan's amount.

## Canceling

1. **Settings → Billing → Cancel subscription**.
2. Confirm.

Your subscription continues until the end of the current cycle, then drops to **Community**.

While the cancellation is pending:

- You keep the higher plan's features.
- No further charges occur.
- You can reactivate (or upgrade to something else) at any time before the cycle ends.

## Switching billing cycle (Monthly ↔ Annual)

1. **Change plan** → pick the same plan with a different cycle.
2. Confirm.

Annual cycles save ~20%. The platform pro-rates the difference.

## Plan changes and ACUs

- **Upgrade**: your monthly ACU allowance increases. The unused portion of your current allowance carries forward into the new larger allowance for the rest of the cycle.
- **Downgrade**: your monthly ACU allowance decreases at the next cycle. Extra credits are unaffected.
- **Cancel + reactivate later**: you get a fresh monthly allowance from the new activation date. Extra credits persist throughout.

## Org plan changes

Org plan changes follow the same rules but live on the org's Billing tab.

- Adding seats is immediate, pro-rated.
- Removing seats takes effect at the next cycle.
- Downgrading from Teams to Community on an org effectively disables member management; existing members keep access until removed manually.

## What's not yet supported

- **Custom invoice billing.** Today most plans charge a card. Enterprise contracts can use invoice billing; smaller plans cannot yet.
- **Multi-year commitments.** Plans are monthly or annual.
- **Currency selection.** Charges are in USD.

## Where to next

- **See the plans side by side** → **[Pricing](pricing)**.
- **What you can do per plan** → **[Plan limits](plan-limits)**.
- **AI credit accounting** → **[AI Credit Units](ai-credit-units)**.
- **Org-level plan management** → **[Org billing](../platform/organizations/billing)**.
