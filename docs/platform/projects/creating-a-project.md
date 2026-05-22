# Creating a project

New projects are created through a three-step wizard. The wizard is the same whether you start it from the dashboard's **+ New** button or from the projects list.

## Open the wizard

Two ways:

1. **From the dashboard**: the left column **Projects** card has a blue **+ New** button at the top. Click it.
2. **From the projects list**: click **+ Create new** at the top-left, then choose **New Project** from the dropdown.

![The Create new dropdown showing New Project, New Folder, and New Library](images/create-new-dropdown.png)

(The dropdown also has **New Folder** for organizing projects and **New Library** for reusable code, both covered in later sections.)

## Step 1. Project info

![Step 1: name, folder, description](images/new-project-step1.png)

| Field | Required | Notes |
|---|---|---|
| **Project name** | Yes | Any text. Used as the project identifier and as the URL slug. Two projects in the same workspace can't share a name. |
| **Select folder** | No | Leave as **Root (/)** to put the project at the top level. Otherwise pick one of your existing folders. Folders are visible in the left sidebar of the projects list and help group related projects. |
| **Description** | No | Free text. Shown on the project card in the projects list and in feed activity items. You can edit it later. |

Click **Next** to continue.

## Step 2. Configuration

![Step 2: language and cycle time](images/new-project-step2.png)

| Field | Required | Notes |
|---|---|---|
| **Select language** | Yes | The default programming language for new POUs. Pick one of **Structured Text (ST)**, **Ladder Diagram (LD)**, **Function Block Diagram (FBD)**, **Instruction List (IL)**, or **Sequential Function Chart (SFC)**. You can mix languages inside a project later, this just sets the language the editor opens with. |
| **Cycle time** | Yes | How often the PLC runtime executes the main program. Default is `T#20ms`. Click the field to open a time picker with separate day / hour / minute / second / millisecond / microsecond inputs. |

![The cycle time picker with separate day, hour, min, sec, ms, us inputs](images/new-project-cycle-time.png)

A few tips for cycle time:

- Most discrete control logic is fine at 10–50 ms.
- Tight motion control may need 1–5 ms. Be aware that very short cycles increase CPU load on the vPLC.
- Slow data-collection programs can use 100 ms or longer.

You can change cycle time later through the editor (it's stored in `project.json`).

Click **Back** to revisit step 1, **Cancel** to dismiss the wizard, or **Next** to continue.

## Step 3. Visibility

The last step asks whether the project is **public** or **private**.

- **Public**: anyone can read, star, and fork it. You decide who can write.
- **Private**: only people you invite can see it.

The Community plan can only create public projects. If your personal plan or organization plan supports private projects, you'll see both options here. See **[Visibility and sharing](visibility-and-sharing)** for the deeper picture and **[Plan limits](../../plans-and-billing/plan-limits)** for which plans allow private projects.

Click **Create** to finish. The wizard closes, the project is created, and you land on its **Code** tab.

## What just happened in the background

The platform did the following on the server side:

1. Created an empty git repository for your project.
2. Made an **initial commit** authored by `Autonomy Edge` containing the project skeleton: `programs/`, `functions/`, `function-blocks/`, `devices/`, and `project.json` with the language and cycle time you chose.
3. Set the visibility flag.
4. Added the project to your dashboard feed (so other people see "{you} created a public project" if it's public).

If you go to the **Code** tab now you'll see the file tree pre-populated and a single commit named *Initial commit* in the commit summary bar. You're ready to open the project in the editor and start writing logic.

## Next steps

- **Open in editor and write code** → click **Open in editor** at the top right of the project page. See the **[OpenPLC Editor docs](../../openplc-editor/overview)**.
- **End-to-end first program** → **[Quick Start Guide](../../getting-started/quick-start)**.
- **Find your project later** → **[Projects list](projects-list)**.
