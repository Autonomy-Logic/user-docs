# XML Export

You can export your PLC project as a standard IEC 61131-3 XML file. This is the industry-standard interchange format, making your work portable across compliant tools and platforms.

## What Gets Exported

The exported XML file is a complete snapshot of your project, including:

- **All POUs**: Every Program, Function, and Function Block with their variable declarations and logic.
- **Data Types**: All user-defined arrays, enumerations, and structures.
- **Configuration**: Task definitions, program instance assignments, and global variables.
- **Project metadata**: Project name, creation date, and version information.

The export preserves the full fidelity of your PLC logic regardless of language. Structured Text, Ladder Diagram, Function Block Diagram, Instruction List, and Python/C++ blocks are all included.

## How to Export

1. Open your project in the IDE.
2. Select the **Export XML** option from the project actions menu.
3. The IDE generates the XML file from your current project state.
4. The file downloads automatically to your browser's default download location.

> **Tip:** The export uses your current in-memory project state, so any unsaved changes in the editor are included.

### Requirements

- Your project must have at least one **program-type POU** designated as the main program.
- All POUs must have valid logic. Empty or malformed implementations may cause the export to fail.

## Use Cases

### Project Backup

Export regularly to keep offline backups. The XML file is plain text, so it works well with version control systems like Git. You can track changes over time by committing exports at different stages.

### Sharing Projects

Share your PLC project with colleagues, clients, or the community by distributing the XML file. Recipients can import it into their own Autonomy Edge workspace or any other IEC 61131-3 compliant IDE.

This is useful for:

- **Team collaboration**: Share snapshots with team members who may not have access to the same workspace.
- **Code review**: Provide a complete project representation without requiring platform access.
- **Education**: Distribute example projects or assignments in a standard format.

### Interoperability

The IEC 61131-3 XML standard is supported by many development environments. Exporting to XML lets you:

- Migrate projects to or from other PLC programming tools.
- Archive projects in a vendor-neutral format.
- Compare implementations across different platforms.

### Importing XML Projects

Autonomy Edge also supports **importing** XML project files. You can:

- Restore a project from a backup.
- Import projects created in other IEC 61131-3 environments.
- Load shared projects from colleagues.

When importing, the IDE parses the XML and reconstructs the full project structure.

## Export vs. Compilation

These are separate operations:

- **XML Export** saves your project as a portable file for backup, sharing, or interoperability.
- **Compilation** builds your project into a deployable program and uploads it to a device.

You can export at any time without compiling, and vice versa.

---

## What's Next?

- [Project Compilation](project-compilation): Learn how to compile and deploy your project.
- [Deployment](deployment-vplc): Deploy your compiled program to a device.
- [Connecting to Runtimes](../connecting-to-runtimes): Connect the IDE to your devices.
