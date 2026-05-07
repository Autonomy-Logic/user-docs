# Keyboard Shortcuts

All keyboard shortcuts available in the Autonomy Edge web IDE. The shortcuts below show the **Ctrl** variant. Substitute **Cmd** on macOS.

> **Tip:** The IDE auto-detects your platform and adjusts modifier keys accordingly.

## File Operations

| Shortcut | Action |
|----------|--------|
| `Ctrl + N` | Create a new project |
| `Ctrl + O` | Open a project |
| `Ctrl + S` | Save the current file |
| `Ctrl + Shift + S` | Save the entire project |
| `Ctrl + W` | Close the current tab |
| `Ctrl + Shift + W` | Close the project |
| `Ctrl + Q` | Quit / close the application |

## Edit Operations

| Shortcut | Action |
|----------|--------|
| `Ctrl + Z` | Undo the last action |
| `Ctrl + Shift + Z` | Redo (reverse an undo) |
| `Ctrl + Y` | Redo (alternative shortcut) |
| `Ctrl + X` | Cut selection |
| `Ctrl + C` | Copy selection |
| `Ctrl + V` | Paste from clipboard |
| `Ctrl + Shift + F` | Search across the entire project |
| `Ctrl + Backspace` | Delete selected element |

## Code Editor (Structured Text)

These shortcuts are available when the Structured Text code editor (Monaco) has focus.

| Shortcut | Action |
|----------|--------|
| `Ctrl + S` | Save the current file |
| `Ctrl + Shift + S` | Save the entire project |
| `Ctrl + Space` | Trigger autocomplete suggestions |
| `Ctrl + Z` | Undo |
| `Ctrl + Shift + Z` | Redo |

The code editor also supports standard text editing shortcuts: `Ctrl + A` (select all), `Ctrl + D` (select next occurrence), arrow keys with Shift (extend selection), and more. Consistent with standard code editor behavior.

## Graphical Editors (Ladder Diagram / Function Block Diagram)

| Shortcut | Action |
|----------|--------|
| `Ctrl + C` | Copy selected elements |
| `Ctrl + X` | Cut selected elements |
| `Ctrl + V` | Paste elements from clipboard |
| `Delete` or `Backspace` | Remove selected elements |

In the graphical editors, you can also drag and drop elements from the toolbox onto the canvas, and use click-and-drag to select multiple elements.

## Display and Navigation

| Shortcut | Action |
|----------|--------|
| `Ctrl + R` | Refresh the page |
| `F11` | Toggle fullscreen mode |
| `F12` | Toggle panel collapse / switch perspective |

## Project Search

The project-wide search feature (`Ctrl + Shift + F`) provides:

- **Scope selection**: Search the whole project or limit to specific POU types (data types, functions, function blocks, programs, configurations)
- **Case sensitivity**: Toggle case-sensitive matching
- **Regular expressions**: Use regex patterns for advanced searches
- **Results navigation**: Click a result to jump directly to that location in the editor

## Variable Table Shortcuts

When working in the Variables Table editor:

| Shortcut | Action |
|----------|--------|
| `Enter` | Confirm and blur the current input field |
| `Tab` | Move to the next field |

The Variables Table supports both table view and code view editing modes, toggled via the view selector in the toolbar.

## Tips

### Editor Focus

Some shortcuts behave differently depending on which panel has focus:
- **Undo/Redo** (`Ctrl + Z` / `Ctrl + Shift + Z`): When the code editor has focus, these operate on the code editor's history. When the graphical editor has focus, these operate on the diagram history.
- **Save** (`Ctrl + S`): Works regardless of which panel has focus.

### Graphical Editor Selection

In Ladder Diagram and Function Block Diagram editors:
- **Click** an element to select it
- **Click and drag** on the canvas to create a selection box
- **Hold Shift + Click** to add/remove elements from the selection
- Selected elements can be copied, cut, or deleted using the keyboard shortcuts above

## What's Next?

- [ST Language Basics](../openplc-editor/programming-languages/structured-text/st-basics): Structured Text syntax and features
- [FAQ](faq): Common questions about Autonomy Edge
- [Glossary](glossary): Key terms and definitions
