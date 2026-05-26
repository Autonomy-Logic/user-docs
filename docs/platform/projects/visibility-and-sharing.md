# Visibility and sharing

Every project is either **public** or **private**. The setting controls who can read it and what they can do with it.

## Public projects

A public project is visible to anyone, including people who don't have an Autonomy Edge account.

What other people can do with your public project:

- **Read everything**: the file tree, every branch, every commit, the README.
- **Star** it. The count is visible to everyone.
- **Fork** it into their own workspace. The fork becomes their project; changes there don't affect yours.
- **Open pull requests** from their fork into your project. You decide whether to merge.

What other people *cannot* do:

- Push commits directly to your project unless you've added them as a collaborator.
- See or change project settings.
- Run vPLC deployments using your orchestrators.

Public projects also appear in **community feeds** and may surface in **trending** widgets and **recommendations**.

## Private projects

A private project is invisible to anyone except the people you've explicitly invited.

What members of a private project can do depends on their role (covered when collaborator management ships, see the **Settings** tab placeholder on the project page). At minimum, an invited collaborator can read; higher roles can push and merge.

Private projects do **not** appear in:

- Public feed activity.
- Forum trending.
- Search results for users without access.
- Your own public profile's project list.

## Setting visibility

- **At creation time**: step 3 of the **[New Project wizard](creating-a-project)**.
- **Later**: from the project's **Settings** tab. This tab is currently a placeholder; visibility changes will be exposed here as the feature ships. Until then, plan to make the right choice at creation time.

## When you cannot create a private project

The Community (free) plan can't create private projects. If you try, the wizard hides the **Private** option and only Public is selectable. On the **Pro**, **Teams**, **Education**, or **Enterprise** plans, private projects are allowed.

If you previously had a paid plan with private projects and have since downgraded, your existing private projects stay private (they're grandfathered). You just can't create new ones above the new plan's limit. Confirm what you have via **[Settings → Usage](../../account/settings/usage)**.

## Sharing a project URL

Public or private, every project has a stable URL:

```
edge.autonomylogic.com/{slug}/projects/{projectId}
```

You can copy this URL with the **link icon** on the project card or the project page header. People who follow the link:

- For public projects, they land on the project page and can read everything.
- For private projects, they're prompted to sign in. If they're signed in but don't have access, they see a "You don't have permission to view this project" message instead of the project page.

For temporary, time-limited share links (anonymous viewing of private projects with an expiring token), watch for that feature in the project Settings tab; it isn't yet shipped.

## What if I want a *gist*-style "anyone with the link" share?

The current model is binary: anyone or invitees only. If you want a guarded share without paying for a private project, the simplest workaround is:

1. Make the project **public**.
2. Use a name that doesn't surface it (don't name it `bug-report-for-acme`; name it `experiment-42`).
3. Share the URL out-of-band.

This isn't a security feature, public is public, but the platform doesn't go out of its way to advertise an unloved project, so casual discovery is unlikely.

## Where to next

- **Set visibility on a new project** → **[Creating a project](creating-a-project)**.
- **Plan limits on private projects** → **[Plan limits](../../plans-and-billing/plan-limits)**.
- **Import an existing project** → **[Importing and forking](importing-and-forking)**.
