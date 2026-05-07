# Project Visibility

Every project on Autonomy Edge has a visibility setting that controls who can see and interact with it. This guide explains the two visibility levels, how they affect discoverability, and how forking works.

---

## Visibility Levels

You choose visibility in Step 3 of the project creation wizard.

### Public

A public project is visible to **everyone on the platform**:

- It appears in the **activity feed** on the dashboard.
- Other users can **view** your code, **fork** the project, and **download** it.
- The project's **star count** is visible, showing community interest.
- Shown with a **globe icon** (🌐).

Public visibility is ideal for open-source PLC programs, learning examples, tutorials, and showcasing your work.

### Private

A private project is visible **only to you**:

- It does **not** appear in the activity feed.
- Other users **cannot** find, view, fork, or download it.
- Shown with a **lock icon** (🔒).

Private visibility is appropriate for work-in-progress projects, proprietary automation logic, and personal experiments.

---

## Identifying Visibility

You can tell a project's visibility at a glance:

- **Card view**: Globe icon (public) or lock icon (private) in the action bar.
- **List view**: The **Access** column shows a globe or lock icon with a label.

---

## The Activity Feed

The dashboard's central area shows an **activity feed**: a scrollable list of public projects from across the Autonomy Edge community. This is the main way users discover each other's work.

Each card in the feed shows the creator's avatar and name, the project description, star count, and a timestamp. Click a card to open the project in the IDE for viewing.

The feed has a search bar and sorting options (currently **Recents**, with **Recommended** and **Popular** coming soon).

---

## Stars

Every project has a **star count** reflecting community interest. Stars appear on project cards, in the table view, and in the activity feed.

---

## Forking a Public Project

Forking creates a personal copy of someone else's public project. The fork is independent. Changes to your fork don't affect the original, and vice versa.

### How to Fork

1. Find the project you want to fork.
2. Open the **options menu** (three-dot menu ⋯).
3. Select **Fork**.
4. In the **Fork Project** modal, click the destination folder.

The fork is created immediately.

### What Happens

- The forked project is named `<Original Name> (Fork)`. If that name exists, a number is appended (up to 100).
- The fork is always **Private**, regardless of the original's visibility.
- All project files are copied to your fork.
- The original's fork count is incremented.
- The fork's description is set to *"Cloned from \<Original Name\>"*.

### Restrictions

- You can only fork **public** projects (or your own projects).
- You can't fork into an archived folder.

---

## Changing Visibility After Creation

Currently, visibility is set during project creation and can't be changed afterward from the UI. This capability will be added in a future update.

---

## Summary

| Aspect | Public | Private |
|---|---|---|
| Visible in activity feed | Yes | No |
| Other users can view code | Yes | No |
| Other users can fork | Yes | No |
| Other users can download | Yes | No |
| Icon | 🌐 Globe | 🔒 Lock |
| Default when creating | No (Private is default) | Yes |

---

## What's Next?

Learn about pinning, downloading, trash management, and more:

➡️ [Managing Projects](managing-projects)
