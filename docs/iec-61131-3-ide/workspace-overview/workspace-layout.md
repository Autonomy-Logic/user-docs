# Workspace Layout

The Autonomy Edge IDE provides a comprehensive workspace designed for efficient PLC program development. The interface is organized into several key areas, each serving a specific purpose in your development workflow.

## Overview of the IDE Interface

When you open a project in the IDE, you'll see a well-organized workspace with multiple panels and tools. The layout is designed to maximize productivity while keeping all essential tools within easy reach.

![IDE Workspace Layout](images/workspace-layout-full.png)
*The complete IDE workspace showing all major components*

## Main Components

The IDE workspace consists of the following main areas:

### 1. Menu Bar (Top)

Located at the very top of the IDE, the menu bar provides access to essential commands and features:

- **File**: Project operations like save, export, and close
- **Edit**: Editing commands like undo, redo, cut, copy, and paste
- **Display**: View options and zoom controls
- **Help**: Access to documentation and help resources
- **Recent**: Quick access to recently opened files

### 2. Activity Bar (Left Side)

The activity bar on the left side of the screen contains icon buttons that control the visibility of different panels:

- **Explorer Icon**: Shows/hides the Project Explorer panel
- **Search Icon**: Opens the search functionality to find text across your project
- **Zoom Icon**: Toggles the Explorer panel to maximize editor space
- **Download Icon**: Exports your project to XML format
- **Play Icon**: Compiles and runs your program
- **Debugger Icon**: Opens debugging tools and variable monitoring
- **Exit Icon**: Returns to the dashboard

### 3. Project Explorer Panel (Left)

The Project Explorer displays your project's hierarchical structure, showing all Programs, Function Blocks, Functions, Data Types, Resources, and Device Configuration. This panel can be collapsed to provide more space for the editor.

The Explorer also includes a Library section at the bottom, which provides access to standard function blocks and additional libraries that you can use in your programs.

### 4. Editor Area (Center)

The central editor area is where you write and edit your code. This area includes:

- **Tab Bar**: Shows all open files with tabs for easy switching between them
- **Breadcrumb Navigation**: Displays the current file's location in the project hierarchy
- **Variables Panel**: A table view above the editor showing all variables defined in the current POU
- **Code Editor**: The main editing area with syntax highlighting and code completion
- **Graphical Editor**: For visual programming languages like Ladder Diagram and Function Block Diagram

The editor area adapts based on the type of file you're editing. For text-based languages (ST, IL), you'll see a code editor with syntax highlighting. For graphical languages (LD, FBD, SFC), you'll see a visual canvas with drag-and-drop functionality.

### 5. Console Panel (Bottom)

The console panel at the bottom displays runtime logs, compilation messages, and debugging information. It includes:

- **Console Tab**: Shows system messages, errors, and runtime logs
- **Search Tab**: Displays search results when using the search functionality
- **Clear Console Button**: Removes all messages from the console

The console can be resized by dragging its top edge, or collapsed entirely to maximize the editor space.

## Resizable Panels

All panels in the IDE are resizable, allowing you to customize the workspace to your preferences:

- **Drag Panel Edges**: Click and drag the edges between panels to resize them
- **Collapse Panels**: Use the activity bar icons to show or hide panels
- **Maximize Editor**: Collapse the Explorer and Console panels to focus on your code

## Workspace Customization

The IDE remembers your panel sizes and layout preferences, so your workspace will look the same each time you open a project. This allows you to create a comfortable working environment tailored to your development style.

### Tips for Efficient Workspace Usage

1. **Use Keyboard Shortcuts**: Learn keyboard shortcuts for common actions to speed up your workflow
2. **Collapse Unused Panels**: Hide the Explorer or Console when you need more space for editing
3. **Use Multiple Tabs**: Keep related files open in tabs for quick switching
4. **Resize Strategically**: Adjust panel sizes based on the task at hand (e.g., larger console when debugging)
5. **Use Breadcrumbs**: Navigate quickly through your project using the breadcrumb trail

## Next Steps

Now that you understand the workspace layout, you can explore the Project Explorer to learn how your project is organized, and the Console to understand how to monitor your program's execution.
