# FAQ

The questions we see most often. If your question isn't here, ask the **[Autonomy AI assistant](../platform/autonomy-ai-assistant)** (⌘J / Ctrl+J) or post in the **[forum](../platform/forum/overview)**.

## Accounts

### Why can't I sign in?

Check that you've verified your email. Until verification, sign-in succeeds but most actions are blocked. If you don't have the verification email, see **[Verification email not arriving](../troubleshooting/email-not-arriving)**.

### Can I change my email?

Yes, from **[Settings → Security → Email](../account/settings/security-email)**. There's a 7-day cooldown between email changes for security.

### Can I change my username?

Yes, from **[Settings → Profile](../account/settings/profile)**. Old direct links to your forum posts and projects keep working because they use IDs internally, but mentions of your old username won't auto-update.

### How do I delete my account?

**[Settings → Account](../account/settings/account)**. Deletion is permanent. If you own organizations, you must transfer or delete them first.

## Projects

### Why can't I create a private project?

The Community plan can only create public projects. Upgrade to Pro, Teams, or Enterprise to create private projects. See **[Plan limits](../plans-and-billing/plan-limits)**.

### What's the difference between pin and star?

A **pin** is private; only you see it in your Pinned view. A **star** is public; the count is visible everywhere. See **[Pinning and stars](../platform/projects/pinning-and-stars)**.

### Can I clone a project with git?

Full git clone access (push from a local checkout) is enabled for paid-plan workspaces. The download icon gives you a zip on all plans. See **[Importing and forking](../platform/projects/importing-and-forking)**.

### How do I move a project between workspaces?

Today: download the project as a zip, then **Import Project** in the destination workspace. Cross-workspace move-in-place isn't supported yet.

### A commit hash link gives me a 404. Why?

Commit detail pages (full file diffs) are still being built. Use the editor for diffs in the meantime — it shows file-level changes between commits.

## Orchestrators and vPLCs

### How do I install the orchestrator agent?

Run `curl https://getedge.me | bash` on a Linux device. See **[Installing the agent](../platform/orchestrators/installing-the-agent)** for the full flow.

### The Orchestrator ID expired before I finished installing. What now?

Run the install command again on the device. The installer detects the existing install and prints a fresh ID.

### Why is my orchestrator stuck "Inactive"?

The agent isn't reporting. See **[Orchestrator not connecting](../troubleshooting/orchestrator-not-connecting)**.

### My vPLC stays "Stopped". What should I check?

See **[vPLC stuck in Stopped](../troubleshooting/vplc-stuck-stopped)**.

### Can I run more than 2 vPLCs on Community?

No. Community is capped at 2 vPLC devices. Upgrade to Pro for 100 or to a per-seat plan for more.

### What is a runtime user, and why do I need to create one?

The runtime user is local to a single vPLC. It's what the editor uses to authenticate to that PLC's runtime. Separate from your Autonomy Edge account. The first connection creates it; subsequent connections sign in with it. See **[Connecting from the editor](../platform/vplcs/connecting-from-editor)**.

### Why does my vPLC have its own IP on the LAN?

MACVLAN. The vPLC's container is attached directly to your physical network with its own MAC, so other devices see it like a standalone PLC. See **[Network modes](../platform/vplcs/network-modes)**.

## Organizations

### Why is the Members tab grayed out in my org?

Member management requires a paid plan (Teams or Education). The Community plan can create an org but can't invite others. See **[Org billing](../platform/organizations/billing)**.

### Why does Pro not let me invite teammates?

Pro is a **personal** plan. Multi-user collaboration is on the **Teams** plan. See **[Pricing](../plans-and-billing/pricing)**.

### What's the difference between Invitations and Invite Links?

**Invitations** target a specific email and are single-use. **Invite links** are URLs that anyone with the link can use (with optional usage caps and expiration). See **[Invitations](../platform/organizations/invitations)** and **[Invite links](../platform/organizations/invite-links)**.

### How do I leave an organization?

From the org's Members tab, find yourself and click **Leave organization**. You can't leave if you're the only Owner — promote someone else first.

### What happens to my account if I delete an org I own?

The org and all its content disappear; you keep your account. If you delete *your account* while owning an org, the platform forces you to deal with the org first.

## Plans and billing

### What plan am I on?

User menu → **Settings** → **[Billing](../account/settings/billing)**. The plan badge is also visible in the user menu next to your name.

### How do trials work?

Pro and Teams have 14-day trials. You're not charged during the trial. If you don't add a payment method by trial end, the plan reverts to Community. See **[Upgrading and downgrading](../plans-and-billing/upgrading-and-downgrading)**.

### Do unused monthly ACUs roll over?

No. Monthly ACUs reset at the start of each billing cycle. Extra credits (purchased one-time) never expire. See **[AI Credit Units](../plans-and-billing/ai-credit-units)**.

### My private project still exists but my plan now disallows private projects. Why?

Grandfathering. Existing items continue to work; only *new* over-the-limit creations are blocked. See **[Plan limits → Grandfathering](../plans-and-billing/plan-limits)**.

## Forum and community

### Why aren't I getting forum notification emails?

Check **[Settings → Privacy](../account/settings/privacy)** — the toggles for @mentions, replies, digests, and DMs are independently switchable. Also verify your email isn't going to spam.

### How do I report a post?

The flag icon at the top right of each post. Choose a reason and submit. See **[Moderation](../platform/forum/moderation)**.

### Can I DM someone who doesn't have an account?

No. DMs are between platform accounts. Invite them to sign up first.

### Why can't I post in a thread?

The thread may be **🔒 Locked** by moderators. Locked threads are read-only.

## AI features

### Is the AI assistant free?

Yes. The **AI Chat** assistant (the sparkle panel) is free on every plan, including Community. The **AI Engineer** features that consume ACUs require Education+, Pro, Teams, or Enterprise. See **[AI Credit Units](../plans-and-billing/ai-credit-units)**.

### What does ⌘J do?

Toggles the AI assistant panel from anywhere. **[Autonomy AI assistant](../platform/autonomy-ai-assistant)**.

## Privacy

### Who can see my profile?

Public. Anyone (with or without an account) can visit it. Email is hidden from non-self viewers.

### Who can DM me?

Anyone with an account, by default. You can disable group-chat invitations specifically in **[Settings → Privacy](../account/settings/privacy)**; 1:1 DMs are always available today.

### Can I block a user?

Not yet. For unwelcome behavior, flag their posts or contact the platform admins via the Feedback action.

## Anything else?

- Open the **AI assistant** (⌘J) and ask.
- Post in the **[OpenPLC forum](../platform/forum/overview)**.
- Use the **Feedback** action in the user menu to report bugs or request features.
