# Search in Project

The activity-bar **magnifying-glass** icon opens project-wide text search. It finds matches across POU names, variable names, comments, and body contents.

Open the panel, type a query, hit Enter.

## Where it looks

By default, search covers everything:

- **POU names**: every `function`, `function-block`, and `program` in the tree.
- **Variable names**: all classes (`Local`, `Input`, `Output`, `InOut`, `External`, `Temp`, `Global`).
- **Comments**: line and block comments in textual languages; rung and node comments in graphical ones.
- **Body content**: Structured Text source, IL opcodes, LD contact/coil/block names, FBD block instance names and labels.
- **Data Type fields**: names and types inside structures, enum values, array dimensions.

## What results look like

Results render as a tree that mirrors the project structure. Each branch you'd see in the project tree appears here if any matches fell under it.

Within each leaf, the matched range is highlighted. Click a result to jump to it, the editor opens the corresponding POU body, scrolls to the line, and selects the matched range.

## Case sensitivity and whole-word matching

The query box behaves as a plain substring match. There's no toggle for case-sensitive or whole-word search; everything is case-insensitive substring.

If you need precision (e.g. find every reference to a specific variable), use the **Variables editor** → click the variable → **Rename Impact** dialog, which lists every body that references it.

## Performance

Search runs in-memory on the loaded project. Even projects with thousands of POUs respond near-instantly. The first search after opening a project may take a few hundred ms while the index warms.

## What's next

- **[Variables editor](../working-with-variables/variables-editor)**: when you need to find every reference to a single variable, the Rename Impact dialog is more precise than text search.
- **[Workspace Layout](workspace-layout)**: where Search sits in the activity bar.
