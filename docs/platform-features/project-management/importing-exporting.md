# Importing and Exporting Projects

Autonomy Edge supports importing projects from ZIP archives and exporting (downloading) your projects as ZIP files. This enables backups, sharing outside the platform, migrating between accounts, and importing projects created with the desktop OpenPLC Editor.

---

## Importing a Project

You can import a project by uploading a `.zip` archive that contains a valid project structure.

### Opening the Import Modal

Click the **Import Project** button (cloud upload icon) on the Projects page toolbar, next to the search bar. It's always visible regardless of which view you're on.

### The Import Form

#### Project Archive (.zip) — Required

Click the upload area (or drag and drop) to select a `.zip` file. **Only `.zip` files are accepted.**

After selecting a file, you'll see the file name, size, and an **×** button to remove it.

> **Tip:** To create a ZIP archive:
> - **Windows:** Right-click the project folder → "Send to" → "Compressed (zipped) folder"
> - **macOS:** Right-click the project folder → "Compress"
> - **Linux:** `zip -r project.zip project_folder/`

#### Project Name — Optional

Enter a custom name for the imported project. If you leave this empty, the name is taken from the `project.json` file inside the archive.

#### Visibility — Required

- **Private** (default) — Only you can access it.
- **Public** — Anyone on the platform can view it.

#### Destination Folder — Required

Choose where to place the project in your folder hierarchy. **No Folder (Root)** places it at the top level.

### Submitting the Import

Click **Import Project**. A loading spinner shows while the upload is processed.

**On success:** A toast notification appears, and an **Import complete!** modal gives you three options:
- **Import another file** — Reopen the import modal.
- **View in project** — Open the imported project in the IDE.
- **Close** — Dismiss the modal.

**On failure:** An error toast appears with a specific message (invalid ZIP, name conflict, file too large, etc.).

### ZIP File Requirements

Your ZIP archive must meet these requirements:

- **Must contain `project.json`** at the root level (or inside a single top-level folder). This file must have a `meta.name` field.
- **Allowed file types:** `.st`, `.ld`, `.fbd`, `.il`, `.json`, `.py`, `.c`, `.cpp`. Other files are silently skipped.
- **Size limits:** Max 50 MB per file, 100 MB total extracted, 1,000 files, 10 folder levels.
- **Unique name:** The project name must be unique for your account. If it conflicts, you'll get a 409 error.

### Language Detection

The platform automatically detects the programming language based on the most common file extension in the archive (e.g., mostly `.st` files → Structured Text).

---

## Exporting (Downloading) a Project

Exporting downloads your project as a `.zip` archive containing all project files. You can later re-import it as a new project.

### How to Download

**Card view:** Click the **download icon** (↓) in the card's action bar.

**List view:** Open the three-dot menu (⋯) and select **Download**.

### What Gets Downloaded

The ZIP includes:
- `project.json` — Project metadata.
- POU source files in their directory structure.
- Any additional configuration or source files.

The file is named after your project (sanitized, lowercase, hyphens for spaces). For example, `My First Project` becomes `my-first-project.zip`.

### Permissions

- You can download any project you own, regardless of visibility.
- For other users' projects, you can only download **public** projects.

---

## Common Workflows

### Backup and Restore

1. **Export** your project by downloading it as a ZIP.
2. Store the ZIP safely (cloud drive, USB, etc.).
3. To restore, use **Import Project** to upload the ZIP. Choose a new name if the original still exists, or delete the original first.

### Migrating from Desktop OpenPLC Editor

1. Find the project folder on your computer (it should contain a `project.json` file).
2. Compress the folder into a `.zip` archive.
3. Use **Import Project** on Autonomy Edge to upload it.
4. The platform reads the `project.json`, extracts the POUs, and creates the project.

Make sure the folder contains a valid `project.json` with a `meta.name` field, and that source files use supported extensions (`.st`, `.ld`, `.fbd`, `.il`, `.json`, `.py`, `.c`, `.cpp`).

---

## What's Next?

You've covered the full project management lifecycle — creating, organizing, sharing, managing, and importing/exporting.

To continue exploring:

- [Quick Start Tutorial](../../getting-started/quick-start) — Hands-on walkthrough of writing and running a PLC program.
- [Understanding Orchestrators](../orchestrator-management/understanding-orchestrators) — Deploy your programs to virtual PLC devices.
- [IDE Overview](../../openplc-editor/overview) — In-depth look at the browser-based editor.
