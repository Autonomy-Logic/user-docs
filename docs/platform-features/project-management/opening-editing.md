# Opening and Editing Projects

Once you've created a project, the next step is to open it in the browser-based IDE. The Autonomy Edge IDE. This guide covers every way to open a project, the IDE layout, and how to edit project settings.

---

## Ways to Open a Project

Several entry points all lead to the same destination: the IDE loaded with your project.

### From the Dashboard

The **Projects** card in the left sidebar lists your most recent projects (up to 5). Click any project to open it in the IDE.

### From the Projects Page

Navigate to the Projects page to see all your projects. Projects can be displayed in **Card view** or **List view**, toggled with buttons in the top-right corner.

**In Card view:** Click anywhere on the project card, or click the **Open in editor** button in the action bar.

**In List view:** Click the project name, or use the three-dot menu (⋯) and select **Open editor**.

### From the Activity Feed

The dashboard's activity feed shows public projects from across the community. Click a project card to open it in the IDE. For projects you don't own, you can view the code but not save changes (fork it first to make your own copy).

### After Importing

After successfully importing a project (see [Importing and Exporting](importing-exporting)), a success modal appears with a **View in project** button that opens the project in the IDE.

---

## The IDE Layout

When the IDE loads your project, you see the full development environment:

- **Activity Bar** (left edge): Icons for Search, Toolbox toggle, Compile, Start/Stop PLC, and Debugger.
- **Project Explorer** (left sidebar): A tree view of your project structure:
  - **Functions**: Reusable POUs that return a value.
  - **Function Blocks**: Reusable POUs with internal state.
  - **Programs**: The main executable POUs.
  - **Data Types**: Custom arrays, enumerations, and structures.
  - **Resource**: Task configuration and program-to-task mapping.
  - **Device**: Orchestrator and device connection management.
  - **Servers**: Communication server configurations (Modbus slave, OPC-UA, S7Comm).
- **Code Editor** (center): Text editor with syntax highlighting for ST/IL, or visual drag-and-drop editor for LD/FBD.
- **Variables Table** (below editor): Define variables for the current POU: name, type, location, initial value, and documentation.
- **Bottom Panel**: Console (compilation output) and PLC Logs (runtime messages from connected devices).

> **Tip:** For a complete walkthrough of writing, compiling, and running a program, see the [Quick Start Tutorial](../../getting-started/quick-start).

---

## Project Detail View

There's also a project detail route within the platform (separate from the IDE) at `/projects/<projectId>`. This shows project metadata without launching the full IDE:

- Project name and ID
- Project type
- POU counts (Programs, Functions, Function Blocks)
- Program previews with source code

This is useful for quickly inspecting a project's structure.

---

## Editing Project Settings

You can modify certain project properties without opening the IDE.

### Renaming a Project

1. Find the project on the Projects page.
2. Open the **options menu** (three-dot menu ⋯):
   - **Card view:** Hover to reveal the menu in the top-right corner.
   - **List view:** Click the menu at the end of the row.
3. Select **Rename**.
4. Enter the new name (1–100 characters) and click **Save changes**.

### Other Options Menu Actions

| Action | Description | More Info |
|---|---|---|
| **Open editor** | Opens the project in the IDE (list view) | This page |
| **Download** | Downloads the project as a `.zip` file (list view) | [Importing and Exporting](importing-exporting) |
| **Rename** | Changes the project name | This page |
| **Move to...** | Moves the project to a different folder | [Organizing Projects](organizing-projects) |
| **Fork** | Creates a copy of the project | [Managing Projects](managing-projects) |
| **Pin / Unpin** | Toggles pinned status | [Managing Projects](managing-projects) |
| **Move to trash** | Soft-deletes the project | [Managing Projects](managing-projects) |

---

## What's Next?

Learn how to organize your projects into folders:

➡️ [Organizing Projects](organizing-projects)
