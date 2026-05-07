# Email and Privacy Preferences

Everything the forum sends by email is controlled by **you**, from a single screen: **Profile → Settings → Privacy**. This guide explains every toggle and how email unsubscribe links work.

**Where:** Click your avatar top-right → **Settings** → **Privacy** tab.
**Direct URL:** `edge.autonomylogic.com/profile/settings?tab=privacy`

---

## The Five Toggles

The Privacy tab contains five switches, each with its own card. All five are **on by default**: so if you never visit this page, you'll get every type of notification the forum can send.

### 1. Group chat invitations

**Allow group chat invitations**

> Decide whether others can invite you to group conversations from the forum.

When **on** (default): People can add you to group chats. You'll see the invitation in the Messages sidebar and can accept or decline.

When **off**: You don't appear in search results when other users are picking members for a new group, and no one can invite you.

> **Note:** This only affects **group** chats. Other users can still start a 1:1 DM with you regardless of this setting.

---

### 2. Weekly forum digest

**Receive the weekly digest email**

> Get a Monday morning recap of the 15 most active forum topics from the past week.

When **on** (default): Every Monday around 07:00 (São Paulo time), if you haven't visited the forum for the past 7 days, you get an email summarizing the top 15 topics of the week. It's a gentle nudge to come back and see what you missed.

When **off**: No weekly digest. Ever.

**Anti-spam rule**: The digest only fires if you were inactive on the forum for a week. Active users never get it, regardless of the toggle.

---

### 3. Forum @mention emails

**Receive an email for @mentions**

> Get an email when someone tags you with @username in a forum post.

When **on** (default): Whenever someone types `@your-username` in a forum topic or reply, you get an email with the topic title, who mentioned you, an excerpt of what they wrote, and a button to jump to the discussion.

When **off**: No email. **You still get the in-app notification** (the bell icon will still light up). This toggle only controls the email copy. Never the in-app bell.

---

### 4. Replies to topics you started

**Receive an email for new replies on your topics**

> Get an email when someone replies to a forum topic you created.

When **on** (default): Every time someone replies in a topic **you** started, you receive an email. Great for staying on top of questions you asked.

When **off**: No reply emails, even if it's your own topic.

**Important detail**: Only **topic authors** receive these emails. If you just replied in someone else's topic, you don't receive an email when more replies come in. This keeps email volume sane on busy threads.

---

### 5. Unread messages reminder

**Receive unread-message reminders**

> Get a nudge by email when you have messages you haven't read for 3+ days.

When **on** (default): If you have one or more direct messages that have been unread for more than 3 days, the platform sends a gentle reminder with a preview of up to 3 unread conversations. You won't get more than one reminder email per 3 days, no matter how many unread messages pile up.

When **off**: No reminders. Unread messages stay unread silently.

**Anti-spam rule**: The reminder only fires for messages older than 3 days **and** waits at least 3 days between any two reminder emails.

---

## Toggling a Setting

All five controls are **switch toggles** (like an iOS or Android switch):

- Click the switch → it slides from on to off (or vice versa).
- A toast appears: **"Email preferences updated"** or **"Privacy preferences updated"**.
- The change takes effect immediately. The next email of that type that would have been sent simply isn't sent.

No "save" button is needed. Each toggle saves on click.

---

## Unsubscribe Links in Emails

Every forum email has an **unsubscribe link in the footer** that takes you straight to the Privacy tab with the right setting turned off automatically.

### What happens when you click

1. You're taken to `/profile/settings?tab=privacy&unsubscribe=[target]`.
2. The platform instantly turns **off** the matching toggle.
3. A toast confirms:
   - "You've been unsubscribed from the weekly forum digest."
   - "You've been unsubscribed from unread-message reminders."
   - "You've been unsubscribed from forum reply notifications."
   - "You've been unsubscribed from forum @mention emails."
4. The query string is scrubbed from the URL so a page refresh doesn't re-trigger anything.

### If you've already unsubscribed

If the matching toggle was already off, you see a gentler toast:

- "You've already unsubscribed from [feature]."

Nothing changes. You're already where you want to be.

### Which link unsubscribes from which thing

| Email | Unsubscribe link target | Toggle turned off |
|---|---|---|
| Weekly digest | `?unsubscribe=weekly-digest` | Receive the weekly digest email |
| Unread messages reminder | `?unsubscribe=unread-messages` | Receive unread-message reminders |
| Reply on your topic | `?unsubscribe=forum-reply` | Receive an email for new replies on your topics |
| @mention | `?unsubscribe=forum-mention` | Receive an email for @mentions |

---

## What Still Happens When You Turn Things Off

Turning off an email toggle **only turns off the email**. The equivalent **in-app notification** (the bell icon, the unread badges in Messages, etc.) keeps working.

| If you turn off... | The email stops | The in-app notification still works |
|---|---|---|
| Weekly digest | ✅ |. (digest is email-only) |
| @mention | ✅ | ✅ (bell still rings) |
| Reply on your topic | ✅ | ✅ (bell still rings) |
| Unread messages reminder | ✅ | ✅ (unread counter still works) |
| Group invitations | Not an email toggle. It controls whether you can be invited at all |. |

---

## Quick Reference

| # | Toggle | What it controls | Default |
|---|---|---|---|
| 1 | Group chat invitations | Whether others can invite you to group chats | ON |
| 2 | Weekly digest | Weekly forum recap email (Mondays) | ON |
| 3 | Forum @mention emails | Email when someone tags you | ON |
| 4 | Replies to topics you started | Email when someone replies in your topic | ON |
| 5 | Unread messages reminder | Email if you have DMs unread for 3+ days | ON |

---

## FAQ

**Can I pause all emails at once?**
There's no master switch. Turn each one off individually. Four clicks total for the four email toggles.

**Do these settings apply to admin or legal emails?**
No. Account-critical emails (password reset, security notices, legal/ToS updates) always go through regardless of these toggles. These five toggles only affect community/notification emails.

**I turned something off but still got an email.**
The change takes effect immediately on the **next** attempt to send. If an email was already queued or in-flight when you toggled off, it might still arrive. Any later email definitely won't.

**Can I block a specific user's notifications?**
Not with these toggles. They're per-type, not per-sender. If someone is spamming you with mentions in bad faith, report the post(s) (see [Reporting a Post](reporting-content)) and moderation will step in.

**What if someone creates my account and changes these?**
If you're worried about account security, change your password from the Account tab and review all five toggles afterward.

---

## What's Next?

You've seen everything the forum has to offer. Come back to the top to review any part:

➡️ [Forum Overview](forum-overview)
