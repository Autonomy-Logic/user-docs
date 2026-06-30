# LD Visual Editor

The Autonomy Edge IDE provides a dedicated visual editor for Ladder Diagram programming. You build logic by placing contacts, coils, and function blocks on rungs, then wiring them together on a graphical canvas. This page covers everything you need to know about working with the LD editor.

## Editor Layout

When you open a Ladder Diagram POU, the workspace splits into two sections:

1. **Variables Table** (top): Define the Boolean and other variables your program uses.
2. **Graphical Editor** (bottom): The visual canvas where you build the ladder logic.

The graphical editor displays rungs vertically. Each rung is a self-contained horizontal circuit numbered in order.

## Working with Rungs

### Creating a Rung

Click the **Create Rung** button at the bottom of the rung list. A new rung appears with:

- A left power rail on the far left
- A right power rail on the far right
- Empty space between them where you place elements

Each new rung starts with placeholder nodes where you can add your first elements.

### Rung Structure

A rung consists of these element types connected left to right:

- **Left Power Rail**: The starting point (power source)
- **Contacts**: Input conditions (normally open, normally closed, edge-detect)
- **Function Blocks**: Timer, counter, and other blocks with multiple I/O pins
- **Coils**: Output elements (regular, negated, set, reset, edge-detect)
- **Right Power Rail**: The endpoint (power return)
- **Parallel branches**: Vertical connections that create OR logic paths

### Reordering Rungs

You can reorder rungs by dragging. Click and hold the rung header (the numbered area on the left), then drag the rung to a new position. The IDE shows visual feedback to indicate valid drop positions.

Rung order determines execution order. The runtime evaluates rungs from top to bottom.

### Deleting a Rung

Right-click on a rung to access context menu options including delete. You can also select elements within a rung and press **Delete** to remove them.

## Placing Elements

### Adding Contacts

To add a contact to a rung:

1. Click on a placeholder node (the small circular targets between elements).
2. A contact element appears at that position.
3. Type the variable name in the text field above the contact. The IDE shows autocomplete suggestions from your Variables Table.
4. Only `BOOL` type variables are valid for contacts. Assigning a non-BOOL variable or an undefined name highlights the contact in red.

Contacts go on the left portion of the rung (between the left power rail and the coils).

### Adding Coils

To add a coil:

1. Click on the placeholder near the right power rail.
2. A coil element appears.
3. Type the variable name above the coil. Autocomplete helps you pick valid variables.
4. Only `BOOL` type variables are valid for coils.

Coils go on the right portion of the rung, before the right power rail.

### Adding Function Blocks

To add a function block:

1. Click a placeholder position on the rung.
2. Select the block type from the system library (TON, TOF, CTU, etc.) or from user-defined function blocks.
3. Connect input and output variables using the variable fields on each pin.

Function blocks appear as rectangular boxes with named input pins on the left and output pins on the right. See [Function Blocks in LD](function-blocks-ld) for details.

### Creating Parallel Branches

Parallel branches create OR logic. To add a parallel path:

1. Click the placeholder node at the bottom of an existing element.
2. A new parallel branch opens below the current path.
3. Place contacts or other elements on the parallel branch.
4. Both the original path and the parallel path connect to the same output side.

Parallel branches appear as vertical connections splitting from and merging back into the main rung path.

## Editing Elements

### Changing Contact/Coil Types

To change a contact or coil variant (e.g., from normally open to normally closed):

1. Double-click the contact or coil element.
2. A dialog opens with available variants.
3. For contacts: **Default** (NO), **Negated** (NC), **Rising Edge** (P), **Falling Edge** (N).
4. For coils: **Default**, **Negated**, **Set**, **Reset**, **Rising Edge**, **Falling Edge**.
5. Select the desired type and confirm.

### Renaming Variables

Click on the variable name text above any contact or coil. The text becomes editable:

- Type a new variable name.
- Autocomplete shows matching variables from the Variables Table.
- Press **Enter** to confirm, or **Escape** to cancel.
- If the variable name doesn't match a BOOL variable in the table, the element turns red.

### Moving Elements

You can reposition elements within a rung by dragging them. The IDE maintains proper wiring connections as you rearrange elements.

### Deleting Elements

Select an element and press **Delete**, or right-click for context menu options. Deleting an element removes it from the rung and reconnects the surrounding wires automatically.

## Variable Autocomplete

The LD editor provides context-aware autocomplete when editing variable names on contacts, coils, and function block pins:

- As you type, a dropdown appears showing matching variables from the Variables Table.
- Use **Arrow Down** / **Arrow Up** to navigate suggestions.
- Press **Tab** or **Enter** to accept a suggestion.
- The autocomplete filters by compatible data types (e.g., only BOOL variables for contacts and coils).

## Visual Feedback

The LD editor provides several visual cues to help you work:

- **Blue outline**: The currently selected element
- **Red text / red element**: A variable name that is undefined or has an incompatible type
- **Drag opacity**: Elements being dragged become semi-transparent
- **Hover outline**: A blue highlight appears when hovering over an element

## Undo and Redo

Every edit in the LD editor is tracked in the undo history:

- **Ctrl+Z** (Cmd+Z on macOS) to undo
- **Ctrl+Y** (Cmd+Shift+Z on macOS) to redo

This includes element placement, deletion, variable assignment, rung creation, rung reordering, and type changes.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Delete** | Remove selected element |
| **Ctrl+Z** | Undo |
| **Ctrl+Y** | Redo |
| **Ctrl+S** | Save current file |
| **Ctrl+Shift+S** | Save entire project |
| **Enter** | Confirm variable name entry |
| **Escape** | Cancel variable name entry |
| **Arrow keys** | Navigate autocomplete suggestions |

## Tips for Effective LD Programming

1. **Define variables first**: Fill out the Variables Table before building rungs. This ensures autocomplete works and prevents red-highlighted errors.
2. **One logical function per rung**: Keep rungs focused on a single operation for readability.
3. **Use meaningful variable names**: `start_button` is much clearer than `I0_0` when reading the diagram.
4. **Comment your rungs**: Use rung comments to describe the purpose of each circuit.
5. **Test incrementally**: Build one or two rungs, compile and test, then add more.
6. **Leverage parallel branches**: Don't create separate rungs for simple OR logic; use parallel branches on a single rung instead.

---

## What's Next?

Dive deeper into the specific elements: [Contact Elements](contact-elements) and [Coil Elements](coil-elements).
