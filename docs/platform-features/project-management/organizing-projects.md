# Organizing Projects with Folders

As your project portfolio grows, organizing projects into folders becomes essential for maintaining an efficient workflow. Autonomy Edge provides a flexible folder system that helps you categorize and manage projects based on application, client, development stage, or any other criteria that suits your needs.

## Understanding the Folder System

The folder system in Autonomy Edge works similarly to file systems on your computer:

- **Hierarchical structure**: Folders can contain projects but currently do not support nested subfolders
- **Root folder (/)**: The default location for projects without a specific folder assignment
- **Folder visibility**: Folders are visible in the sidebar navigation for quick access
- **Project organization**: Each project can belong to one folder at a time

## Viewing Folders

Folders are displayed in the left sidebar of the Projects page:

![Projects Page with Folders](images/projects-page.png)

The sidebar shows:
- **Root folder (/)**: Indicated by a folder icon with a slash
- **Named folders**: Listed below the root folder with folder icons
- **Project count**: Visual indication of projects within each folder
- **Expandable view**: Click on a folder to view its contents

## Creating Folders

You can create folders in two ways:

### Method 1: During Project Creation

The most convenient way to create a folder is while creating a new project:

1. Start the project creation wizard
2. In Step 1 (Project Information), locate the "Folder" dropdown
3. Click the "+" button next to the dropdown
4. Enter a descriptive folder name in the modal
5. Click "Create" to save the folder
6. The new folder will be automatically selected for your project
7. Complete the project creation process

This method ensures your new project is immediately organized into the appropriate folder.

### Method 2: From the Projects Page

You can also create folders directly from the Projects page:

1. Navigate to the Projects page
2. Click the "+" button in the folder section of the sidebar
3. Enter a folder name in the dialog
4. Click "Create" to save the folder
5. The new folder will appear in the sidebar

## Moving Projects Between Folders

To organize existing projects into folders:

1. Navigate to the Projects page
2. Locate the project you want to move
3. Click the three-dot menu (⋯) on the project row
4. Select "Move to folder" from the menu
5. Choose the destination folder from the list
6. Confirm the move

The project will immediately appear in the selected folder.

## Folder Naming Best Practices

Choose folder names that make your organization system clear and maintainable:

### Recommended Naming Conventions

**By Application Type:**
- "Water Treatment"
- "HVAC Systems"
- "Manufacturing Lines"
- "Building Automation"

**By Client or Project:**
- "Client - ABC Manufacturing"
- "Project - Smart Factory 2025"
- "Demo Projects"
- "Training Materials"

**By Development Stage:**
- "Production"
- "Development"
- "Testing"
- "Archive"

**By Technology or System:**
- "Conveyor Systems"
- "Temperature Control"
- "Motor Control"
- "Safety Systems"

### Naming Guidelines

- **Be descriptive**: Use clear, meaningful names that indicate the folder's purpose
- **Keep it concise**: Aim for 2-4 words maximum
- **Use consistent formatting**: Decide on a naming convention and stick to it
- **Avoid special characters**: Stick to letters, numbers, spaces, and hyphens
- **Consider sorting**: Folders are typically sorted alphabetically, so consider prefixes if order matters

## Managing Folders

### Renaming Folders

To rename an existing folder:

1. Navigate to the Projects page
2. Locate the folder in the sidebar
3. Click the folder options menu (if available)
4. Select "Rename"
5. Enter the new folder name
6. Confirm the change

All projects within the folder will remain in place with the updated folder name.

### Deleting Folders

To delete a folder:

1. Ensure the folder is empty (move all projects to other folders first)
2. Navigate to the Projects page
3. Locate the folder in the sidebar
4. Click the folder options menu
5. Select "Delete"
6. Confirm the deletion

**Important:** You cannot delete folders that contain projects. Move all projects out of the folder before attempting to delete it.

## Working with the Root Folder

The root folder (/) serves as the default location for projects:

- **Default location**: Projects created without a folder selection go here
- **Always available**: The root folder cannot be deleted or renamed
- **Quick access**: Useful for temporary projects or those that don't fit other categories
- **No organization**: Projects in the root folder have no additional categorization

### When to Use the Root Folder

- Quick test projects that don't need long-term organization
- Projects that don't fit into existing folder categories
- Temporary projects that will be moved or deleted soon
- Single-project workflows where folders aren't necessary

## Folder Navigation

### Sidebar Navigation

The sidebar provides quick access to your folder structure:

1. **Click a folder** to view all projects within it
2. **Click the root folder (/)** to view all unorganized projects
3. **Use the search bar** to find projects across all folders
4. **View project count** to see how many projects are in each folder

### Filtering by Folder

When viewing a folder:

- The main content area displays only projects from that folder
- The breadcrumb navigation shows your current location
- You can still access other folders through the sidebar
- Search functionality can be scoped to the current folder

## Organizing Strategies

### Strategy 1: By Client or Customer

Organize projects by the client or customer they're developed for:

```
/ (Root)
├── Client - ABC Manufacturing
├── Client - XYZ Industries
├── Client - Demo Projects
└── Internal Projects
```

**Benefits:**
- Easy to find all work for a specific client
- Simplifies billing and project tracking
- Clear separation of client work

### Strategy 2: By Application Domain

Group projects by their industrial application:

```
/ (Root)
├── Water Treatment
├── HVAC Systems
├── Manufacturing
├── Building Automation
└── Energy Management
```

**Benefits:**
- Reuse code and patterns across similar applications
- Build domain expertise
- Easy to find reference implementations

### Strategy 3: By Development Stage

Organize based on project maturity:

```
/ (Root)
├── Production
├── Testing
├── Development
├── Archive
└── Templates
```

**Benefits:**
- Clear project lifecycle management
- Easy to identify active vs. archived projects
- Supports quality assurance processes

### Strategy 4: Hybrid Approach

Combine multiple organizational principles:

```
/ (Root)
├── Production - Client A
├── Production - Client B
├── Development - New Features
├── Testing - QA
├── Templates
└── Archive
```

**Benefits:**
- Flexible organization for complex needs
- Supports multiple workflows
- Scalable as project count grows

## Best Practices

### Organization Tips

- **Create folders proactively**: Set up your folder structure before accumulating many projects
- **Review regularly**: Periodically review and reorganize your folder structure
- **Keep it simple**: Don't create too many folders; aim for 5-15 main categories
- **Use consistent naming**: Maintain a consistent naming convention across all folders
- **Document your system**: Keep notes on your organizational logic for team members

### Maintenance

- **Archive old projects**: Move completed or obsolete projects to an Archive folder
- **Clean up regularly**: Delete test projects and temporary work
- **Consolidate when needed**: Merge similar folders if they become too granular
- **Update folder names**: Rename folders as your organization evolves

### Collaboration Considerations

When working with teams:

- **Agree on conventions**: Establish folder naming and organization standards
- **Document the structure**: Maintain documentation of your folder organization
- **Communicate changes**: Notify team members when reorganizing folders
- **Use descriptive names**: Make folder purposes clear for all team members

## Troubleshooting

### Common Issues

**Q: I can't find a project I created**
- Check if it's in the root folder (/)
- Use the search functionality to locate it across all folders
- Check the "All Projects" view to see all projects regardless of folder

**Q: I want to create nested folders**
- The current version supports single-level folders only
- Use naming conventions to simulate hierarchy (e.g., "Client A - Production", "Client A - Development")
- Monitor platform updates for nested folder support

**Q: How do I move multiple projects at once?**
- Currently, projects must be moved individually
- Plan your folder structure before creating many projects
- Consider using bulk operations if they become available in future updates

**Q: Can I have a project in multiple folders?**
- No, each project can only belong to one folder at a time
- Consider using tags or naming conventions if you need multiple categorizations
- Duplicate the project if it truly needs to exist in multiple contexts
