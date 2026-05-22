# Search

A single **Search projects or users** field lives in the header on the dashboard and feed pages. It's the fastest way to find a project you remember by name or a user you've interacted with.

## What it searches

The header search is scoped to two entity types:

- **Projects** — public projects across the platform plus your accessible private projects (your own and any in organizations you belong to).
- **Users** — display names and usernames.

It does **not** search:

- Forum content. Use the forum's own search (on the forum home or any board).
- Commit messages.
- File contents inside projects.
- Organization names. (Use the **[organizations list](organizations/overview)** for that.)

## Results

As you type, results appear inline below the search box:

- A section for **Projects** with up to 5 matches, each shown as a card (cover image, name, description, owner, public/private badge).
- A section for **Users** with up to 5 matches, each shown as a row (avatar, name, username).

Click a result to navigate. Hit Escape or click the **×** to clear.

For more results than the inline preview shows, click **See all results** to land on a full results page.

## Tips for better matches

- **Project IDs** — pasting a short ID (like `cmj4dy45y...`) finds the exact project.
- **Owner-prefixed names** — typing `thiagoralves/edf-demo` narrows to projects under that owner.
- **Username with @** — typing `@thiagoralves` jumps straight to user results.

## Per-section search

Some sections have their own search box that's better-scoped than the header search:

- **Projects list** — search the current workspace's projects only.
- **Forum** — search topics across categories.
- **Forum board** — search topics in one category.
- **Org Members tab** — search members in the org.
- **Messaging** — search conversation participants and message text.

Use those when you know which surface to look on.

## Limitations

- **No advanced operators** (no `is:public`, `owner:`, language filters, etc.) today. Power-user filters are a planned addition.
- **Private results** are limited to things you have access to. Other people's private projects won't appear in your results.
- **Search history** is not surfaced. Use bookmarks or the URL bar's autocomplete for recurring lookups.

## Where to next

- **Find a project by browsing instead** → **[Projects list](projects/projects-list)**.
- **Find a person to message** → **[Members directory](forum/members)**.
- **Look up keyboard shortcuts** → **[Reference → Keyboard shortcuts](../reference/keyboard-shortcuts)**.
