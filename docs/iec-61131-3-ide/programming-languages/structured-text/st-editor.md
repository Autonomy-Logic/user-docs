# ST Editor Features

The Autonomy Edge IDE provides a powerful Monaco-based code editor for writing Structured Text programs. This editor includes modern development features like syntax highlighting, IntelliSense code completion, and real-time error detection to help you write correct and efficient ST code.

## Editor Overview

The ST editor is part of the dual-structure workspace for Structured Text programming:

1. **Variables Table** (top section): Define variables with their names, types, and classes
2. **Code Editor** (bottom section): Write ST code using the Monaco editor

This separation ensures that all variables are properly declared before use, following IEC 61131-3 conventions.

## Syntax Highlighting

The editor automatically highlights different elements of your ST code using distinct colors, making it easier to read and understand program structure.

### Highlighted Elements

**Keywords**: Control flow and declaration keywords appear in blue
- `IF`, `THEN`, `ELSE`, `ELSIF`, `END_IF`
- `CASE`, `OF`, `END_CASE`
- `FOR`, `TO`, `BY`, `DO`, `END_FOR`
- `WHILE`, `END_WHILE`
- `REPEAT`, `UNTIL`, `END_REPEAT`
- `VAR`, `END_VAR`, `PROGRAM`, `FUNCTION`, `FUNCTION_BLOCK`

**Operators**: Arithmetic and logical operators are clearly visible
- Assignment: `:=`
- Arithmetic: `+`, `-`, `*`, `/`, `**`, `MOD`
- Comparison: `=`, `<>`, `<`, `>`, `<=`, `>=`
- Logical: `AND`, `OR`, `XOR`, `NOT`

**Variables**: Variable names appear in distinct colors based on their scope and usage

**Literals**: Numeric values, strings, and time literals are highlighted
- Numbers: `25.5`, `100`, `-42`
- Strings: `'Hello, World!'`
- Time: `T#5s`, `T#100ms`
- Boolean: `TRUE`, `FALSE`

**Comments**: Comments appear in green for easy identification
- Single-line: `// This is a comment`
- Multi-line: `(* This is a multi-line comment *)`

![Syntax Highlighting Example](images/st-syntax-highlighting.png)
*ST code with syntax highlighting showing keywords (blue), variables, operators, and comments (green)*

### Benefits of Syntax Highlighting

1. **Improved Readability**: Different colors help distinguish code elements at a glance
2. **Error Detection**: Misspelled keywords remain unhighlighted, indicating potential errors
3. **Structure Visualization**: Nested control structures are easier to follow
4. **Comment Identification**: Comments stand out clearly from executable code

## IntelliSense and Code Completion

IntelliSense provides intelligent code completion suggestions as you type, helping you write code faster and with fewer errors.

### Triggering IntelliSense

IntelliSense activates automatically in several situations:
- When you start typing a variable name
- After typing a dot (`.`) to access structure or function block members
- When typing keywords
- When you press `Ctrl+Space` manually

### What IntelliSense Suggests

**Variable Names**: All variables defined in your Variables Table
```
sensor_temp
setpoint
enable
heater_on
cooler_on
alarm
temp_error
timer
```

**Function Block Members**: When you type a function block instance name followed by a dot, IntelliSense shows its internal members.

![IntelliSense for Function Block Members](images/st-intellisense.png)
*IntelliSense showing TON timer members: IN (BOOL input), PT (preset time), ET (elapsed time), Q (output)*

In this example, typing `timer.` displays the TON function block's members:
- **IN**: Boolean input to start the timer
- **PT**: Preset time (how long to wait)
- **ET**: Elapsed time (current timer value)
- **Q**: Output (TRUE when timer completes)

The autocomplete also shows the data type for each member (e.g., "BOOL (input)" for IN), helping you understand what values are expected.

**Keywords**: ST language keywords for control structures
```
IF
THEN
ELSE
ELSIF
END_IF
CASE
FOR
WHILE
REPEAT
```

**Built-in Functions**: Standard IEC 61131-3 functions
```
ABS       // Absolute value
SQRT      // Square root
SIN, COS  // Trigonometric functions
MAX, MIN  // Maximum/minimum
CONCAT    // String concatenation
LEN       // String length
```

**Function Blocks**: Available function block types from libraries
```
TON       // Timer On-Delay
TOF       // Timer Off-Delay
TP        // Timer Pulse
CTU       // Counter Up
CTD       // Counter Down
RS        // Reset-Set bistable
SR        // Set-Reset bistable
```

**Data Types**: Available data types for declarations
```
BOOL
INT, DINT, REAL
STRING
TIME, DATE
ARRAY
```

### Using IntelliSense Effectively

1. **Start Typing**: Begin typing a variable or keyword name
2. **Review Suggestions**: The dropdown shows matching items
3. **Navigate**: Use arrow keys to move through suggestions
4. **Select**: Press `Enter` or `Tab` to insert the selected item
5. **Continue**: Keep typing to filter suggestions further
6. **Manual Trigger**: Press `Ctrl+Space` to show suggestions at any time

### IntelliSense for Structures

When working with structured data types, IntelliSense helps you navigate nested members:

```
motor_data.speed      // Access speed field
motor_data.current    // Access current field
motor_data.running    // Access running field
```

After typing `motor_data.`, IntelliSense displays all available fields in the structure.

## Code Editor Features

### Line Numbers

Line numbers appear on the left side of the editor, making it easy to:
- Reference specific lines when discussing code
- Navigate to particular locations
- Identify error locations from compiler messages

### Indentation

The editor automatically indents code within control structures:
- Code inside `IF...END_IF` blocks is indented
- Nested structures receive additional indentation
- Pressing `Enter` maintains the current indentation level

**Example:**
```
IF enable THEN
    temp_error := setpoint - sensor_temp;
    
    IF timer.Q THEN
        heater_on := TRUE;
    END_IF;
END_IF;
```

### Bracket Matching

When you click on or move the cursor near a bracket or parenthesis, the editor highlights the matching pair, helping you:
- Verify that all brackets are properly closed
- Understand the scope of expressions
- Navigate complex nested structures

### Selection and Editing

**Multi-line Selection**: Click and drag to select multiple lines

**Copy/Paste**: Standard keyboard shortcuts work:
- `Ctrl+C`: Copy
- `Ctrl+X`: Cut
- `Ctrl+V`: Paste

**Undo/Redo**:
- `Ctrl+Z`: Undo last change
- `Ctrl+Y` or `Ctrl+Shift+Z`: Redo

**Find and Replace**:
- `Ctrl+F`: Open find dialog
- `Ctrl+H`: Open find and replace dialog

### Code Folding

The editor supports code folding for control structures, allowing you to collapse sections of code to focus on specific areas. Look for fold indicators next to line numbers for:
- IF/END_IF blocks
- CASE/END_CASE blocks
- FOR/END_FOR loops
- WHILE/END_WHILE loops
- REPEAT/END_REPEAT loops

## Working with Variables

### Variables Table Integration

The Variables Table and Code Editor work together seamlessly:

1. **Define First**: Add variables in the Variables Table before using them in code
2. **Automatic Recognition**: Variables appear in IntelliSense immediately after definition
3. **Type Checking**: The editor knows each variable's data type
4. **Scope Awareness**: Only variables in scope are suggested

For more information on the variables table, see [Working With Variables in the IDE](../../iec-concepts/variables-datatypes#working-with-variables-in-the-ide)

### Drag and Drop

You can drag functions and function blocks from the library directly into the code editor, automatically inserting the variable name at the cursor position.

## Best Practices for Using the Editor

### Leverage IntelliSense

1. **Use Ctrl+Space frequently**: Don't hesitate to trigger IntelliSense manually
2. **Let it guide you**: IntelliSense shows what's available and valid
3. **Check member types**: Pay attention to data types shown in suggestions
4. **Explore function blocks**: Use dot notation to discover function block capabilities

### Write Readable Code

1. **Use consistent indentation**: Let the editor auto-indent your code
2. **Add blank lines**: Separate logical sections with empty lines
3. **Write comments**: Document complex logic and non-obvious operations
4. **Use meaningful names**: Choose descriptive variable names that IntelliSense can help complete

### Organize Your Code

1. **Group related operations**: Keep related logic together
2. **One statement per line**: Avoid cramming multiple statements on one line
3. **Align assignments**: Use consistent spacing around `:=` operators
4. **Break long expressions**: Split complex calculations across multiple lines

### Error Prevention

1. **Watch syntax highlighting**: Unhighlighted keywords indicate typos
2. **Use IntelliSense**: Reduces spelling errors in variable names
3. **Check bracket matching**: Ensure all brackets are properly paired
4. **Test incrementally**: Write and test small sections of code at a time

## Editor Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Space` | Trigger IntelliSense manually |
| `Ctrl+F` | Find in current file |
| `Ctrl+H` | Find and replace |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+C` | Copy selection |
| `Ctrl+X` | Cut selection |
| `Ctrl+V` | Paste |
| `Ctrl+A` | Select all |
| `Home` | Move to beginning of line |
| `End` | Move to end of line |
| `Ctrl+Home` | Move to beginning of file |
| `Ctrl+End` | Move to end of file |
| `Tab` | Indent selection |
| `Shift+Tab` | Unindent selection |

## Monaco Editor Foundation

The Autonomy Edge ST editor is built on the Monaco Editor, the same technology that powers Visual Studio Code. This provides:

- **Professional-grade editing**: Industry-standard code editing experience
- **Performance**: Handles large programs efficiently
- **Extensibility**: Supports custom language features and extensions
- **Cross-platform**: Works consistently across different browsers and operating systems

## Tips for Efficient Coding

1. **Define variables first**: Complete your Variables Table before writing code
2. **Use descriptive names**: Longer, clear names are better than cryptic abbreviations
3. **Leverage autocomplete**: Let IntelliSense type long variable names for you
4. **Add comments as you go**: Document your logic while it's fresh in your mind
5. **Test frequently**: Compile and test code regularly rather than writing everything at once
6. **Use the console**: Check compiler messages for errors and warnings
7. **Learn shortcuts**: Keyboard shortcuts speed up editing significantly

## Next Steps

- [ST Language Basics](st-basics) - Review ST syntax, operators, and control structures
- [ST Programming Examples](st-examples) - Study practical ST programming patterns
- [Variables and Data Types](../../iec-concepts/variables-datatypes) - Learn about variable management
- [Building and Deploying](../../building-deploying/compilation) - Compile and deploy your ST programs
