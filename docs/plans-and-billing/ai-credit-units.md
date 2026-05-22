# AI Credit Units

**AI Credit Units (ACUs)** are the credits that power the **AI Engineer** features, multi-step automation jobs, deeper code generation, longer context windows. They are *not* required for the free **AI Chat** assistant in the Sparkle panel.

![Usage tab showing ACU pools](images/usage-acus.png)

## The two pools

There are two separate ACU balances:

### Monthly allowance

Refills with your billing cycle. Each plan includes a different amount:

| Plan | ACUs/month |
|---|---|
| Community | 0 |
| Education | 1,125 |
| Pro | 6,125 |
| Teams | 12,375 / seat |
| Enterprise | Custom |

The monthly pool **does not roll over.** Unused ACUs at the end of the cycle are lost.

### Extra credits

Top-ups you've bought. These **never expire**.

Use them when:

- You're approaching the end of the cycle and don't want to risk running out.
- You have a heavy month and need a one-time bump.
- You want to spread the cost of AI Engineer work across multiple cycles instead of upgrading a plan permanently.

## Consumption order

When an AI Engineer job runs:

1. **Monthly allowance is drained first.**
2. **Extra credits kick in only when the monthly pool is empty.**

This means casual usage never touches your extras. You can stockpile them safely.

If both pools combined still can't cover the job's estimate, the job is blocked and you'll see a "Plan limit reached" message.

## Buying more ACUs

From **[Settings → Usage](../account/settings/usage)**, click **+ Buy more ACUs**. A dialog opens with packs (typical sizes: 1,000 / 5,000 / 10,000 / 50,000 ACUs).

Pick a pack, confirm payment, and the extra credits land in the Extra Credits pool immediately.

## What ACUs are spent on

Concrete examples:

- **A short code generation request** in AI Engineer (e.g. "write a TON timer with a 2-second blink"), single-digit ACUs.
- **A guided refactor** of a function block: tens of ACUs.
- **A multi-step debug session** with long context: hundreds of ACUs.
- **A full project scaffold**: possibly thousands of ACUs.

Each job shows an estimate before it runs so you can decide whether to proceed.

## Checking your balance

**[Settings → Usage](../account/settings/usage)** is the canonical view. It shows:

- **This month**: used vs allowance, reset date.
- **Extra credits**: total available.
- Per-job log (when available): what each ACU was spent on.

## ACUs and organizations

Organizations on Teams or Enterprise plans have their **own** ACU pools that any member can draw from. Your personal ACUs are separate from any org's.

When you trigger an AI Engineer job, the platform infers which pool to charge:

- Job operating on resources in your personal slug → personal ACUs.
- Job operating on resources in an org slug → that org's ACUs.

You can see org-level ACU consumption on the org's billing tab (when available).

## What ACUs do **not** affect

- The **AI Chat** assistant (the sparkle panel). It's free on every plan, doesn't consume ACUs.
- Editor autocomplete, syntax checking, type checking. These are free and unmetered.
- Forum mentions of `@autonomy-ai` or any future bot interactions in the forum (governed separately).

## Where to next

- **See your current balance** → **[Settings → Usage](../account/settings/usage)**.
- **Upgrade your plan for a bigger monthly allowance** → **[Pricing](pricing)**.
- **Free assistant** → **[Autonomy AI assistant](../platform/autonomy-ai-assistant)**.
