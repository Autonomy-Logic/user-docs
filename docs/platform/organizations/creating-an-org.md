# Creating an organization

You can create an organization on any plan, including Community. The Community plan limits what you can do *inside* an org (no member management), but creating one and using it as a sandbox is free.

## Open the create dialog

Two entry points:

1. **From the dashboard.** The right column's **Organizations** card has a **+ Create new** button. Click it.
2. **From the organizations list.** Go to `edge.autonomylogic.com/organizations` and click **+ New** in the toolbar.

The Create Organization dialog opens.

![Create Organization modal with name, description, and website fields](images/create-organization-modal.png)

## Fields

| Field | Required | Notes |
|---|---|---|
| **Organization name** | Yes | Free text. Used as the display name. The slug is derived from this, *Autonomy Mine* becomes `autonomy-mine`. |
| **Description** *(optional)* | No | A one-liner shown on the org's profile. You can edit it later. |
| **Website** *(optional)* | No | URL. Renders as a link on the org's profile. |

Click **Create Organization**.

## What happens next

- The org is created and you're added as the **Owner**.
- Its slug is reserved. From now on, `edge.autonomylogic.com/{org-slug}/dashboard` shows the org's dashboard, `/{org-slug}/projects` shows its projects, etc.
- The dashboard right column adds a new card for this org with your role badge (**Owner**).
- The activity feed records "{you} created the organization."

## Slug collisions

If the platform-derived slug is already taken (because someone else has a similarly named user or org), creation will fail with a message asking you to change the name. Pick a different name; the slug is derived automatically.

## Next steps after creation

1. **Pick a plan if you need to collaborate.** Click **View plans** on the org dashboard's banner (or go to org → Billing tab) to pick **Teams** or **Education**. Until then, member management is locked.
2. **Customize the profile.** Upload a logo, fill in the description, add social/contact links. See **[Org profile](org-profile)**.
3. **Move or create projects.** Go to `/{org-slug}/projects` and click **+ Create new**, or fork an existing project into the org. (Cross-workspace moves require a project export/import; see **[Importing and forking](../projects/importing-and-forking)**.)
4. **Install an orchestrator for the org.** Same flow as personal, but performed under the org's slug. See **[Installing the agent](../orchestrators/installing-the-agent)**.

## Where to next

- **Configure the org** → **[Org profile](org-profile)**.
- **Invite teammates** → **[Invitations](invitations)** or **[Invite links](invite-links)** (paid plans).
- **Set up billing** → **[Org billing](billing)**.
