# Verification email not arriving

When you sign up, change your email, or trigger a password reset, the platform sends a verification email. If you can't find it, work through the checks below.

## 1. Spam / junk folder

The most common reason. Look for an email from a sender like `noreply@autonomylogic.com` or `accounts@autonomylogic.com` in:

- Spam.
- Junk.
- Promotions tab (Gmail).
- "Other" / "Focused" tabs (Outlook).

If you find it there, mark it as **Not spam** so future platform emails arrive in your inbox.

## 2. Wait 60 seconds

Email delivery occasionally lags. Wait a minute and refresh your inbox before assuming it's lost.

## 3. Confirm the email address

Typos happen. On the sign-in screen the platform shows which email it sent the verification to. Confirm it matches the one you actually own:

- Look for transpositions (`thaigoralves` vs `thiagoralves`).
- Confirm the domain (`gmail.com` vs `gnail.com`).

If the email you used has a typo:

- For signup: you'll need to re-sign-up with the correct email.
- For email change: the change has not taken effect. Repeat the email change with the correct destination.

## 4. Request a fresh email

Most flows have a **Resend verification email** action on the page after the initial send. Click it; you'll get a new email.

For sign-up verification specifically, go back to `edge.autonomylogic.com/verify-email-code` and click **Resend code**.

## 5. Domain blocklist

Some corporate or institutional mail servers block automated emails from new senders by default. To test:

- Try a personal address (Gmail, Outlook, etc.) for the same flow.
- If the personal email works, the issue is on the corporate mail server: ask your IT to whitelist `noreply@autonomylogic.com` or `*.autonomylogic.com`.

## 6. Aliases and plus-addressing

If you signed up with a plus-addressed alias like `you+autonomy@gmail.com` or a forwarding alias, double-check the underlying inbox actually receives it. Some forwards drop emails silently.

## 7. The historical fix in v1.2.2

Until **v1.2.2** (February 24, 2026), the platform had a known issue where verification tokens weren't sent reliably on sign-up. This was fixed in v1.2.2 (see the **[Changelog](../platform/notifications)**). If you signed up before that and were affected, the resend flow now reliably issues a new token.

## 8. Still nothing?

- Contact platform support via the **Feedback** action in the user menu. Include the email address you signed up with and the timestamp of the resend attempt.
- For sign-up specifically, you can usually delete the half-created account by waiting for the soft expiration and trying again with the same email.

## Email change cooldown

Note: if you're trying to **change** your email rather than verify a new one, you may be hitting the 7-day cooldown. See **[Settings → Security → Email](../account/settings/security-email)**.

## Where to next

- **Sign up flow** → **[Account and signup](../getting-started/account-and-signup)**.
- **Email change** → **[Settings → Security → Email](../account/settings/security-email)**.
- **Forgot password** → enter your email at `edge.autonomylogic.com/forgot-password` and watch for the reset email (same delivery rules apply).
