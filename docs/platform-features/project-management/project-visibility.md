# Project Visibility and Sharing

Autonomy Edge provides flexible visibility controls to manage who can access your projects. Understanding these settings is crucial for protecting proprietary work while enabling collaboration and community engagement.

## Visibility Levels

The platform offers two visibility levels for projects:

### Public Projects

Public projects are accessible to anyone on the platform and appear in community features.

**Characteristics:**
- Visible to all users in search results and activity feeds
- Can be viewed and opened by anyone with an Autonomy Edge account
- Ideal for open-source projects, educational content, and community contributions
- Promote collaboration and knowledge sharing within the community
- Cannot be converted to private if they have been forked or shared extensively

**Use Cases:**
- Educational demonstrations and tutorials
- Open-source automation libraries
- Community-contributed function blocks
- Reference implementations and examples
- Projects intended for public deployment

### Private Projects

Private projects are restricted to the project owner and explicitly invited collaborators.

**Characteristics:**
- Only visible to the project owner and invited users
- Do not appear in public search results or activity feeds
- Protected by Row Level Security (RLS) at the database level
- Can be converted to public at any time
- Suitable for proprietary and confidential work

**Use Cases:**
- Proprietary industrial automation systems
- Work-in-progress projects
- Client-specific implementations
- Confidential or sensitive applications
- Projects under development before public release

## Setting Project Visibility

### During Project Creation

You can set the initial visibility when creating a new project in Step 3 of the creation wizard:

![Project Visibility Settings](images/create-project-step3.png)

1. In the "Visibility & Cover" step, select your preferred visibility option
2. Choose "Public" for community-accessible projects
3. Choose "Private" for restricted access projects
4. Complete the project creation process

The default setting is **Public**, so be sure to change it to Private if needed.

### Changing Visibility After Creation

You can modify a project's visibility at any time through the project settings:

1. Open your project
2. Navigate to project settings (gear icon or settings menu)
3. Locate the "Visibility" section
4. Select the new visibility level
5. Confirm the change

**Important:** Converting a public project to private will immediately remove it from public search results and activity feeds, but users who previously accessed it may have local copies.

## Access Control and Security

### Row Level Security (RLS)

Autonomy Edge implements Row Level Security at the database level to enforce access controls:

- **Database-level protection**: Access restrictions are enforced by the database, not just the application layer
- **User-based filtering**: Queries automatically filter results based on the authenticated user
- **Secure by default**: Users can only access projects they own or have been explicitly granted access to
- **Policy-based access**: Access policies are defined and enforced consistently across all platform features

### Authentication Requirements

All project access requires authentication:

- Users must be logged in to view any projects (public or private)
- Anonymous access is not permitted
- Session management ensures secure access throughout the platform
- API access requires valid authentication tokens

## Sharing Private Projects

While the current platform version focuses on individual ownership, future updates will include collaboration features:

### Planned Collaboration Features

- **Invite collaborators**: Add team members to private projects
- **Role-based permissions**: Assign different access levels (viewer, editor, admin)
- **Organization projects**: Share projects within your organization
- **Team workspaces**: Collaborative spaces for project development

### Current Workarounds

For now, if you need to share a private project:

1. **Convert to public**: Change visibility to public temporarily
2. **Export and share**: Export the project XML and share it directly
3. **Screen sharing**: Use external tools for collaborative development sessions

## Best Practices

### Choosing the Right Visibility

- **Start private**: Begin with private visibility for new projects until they're ready for public release
- **Review before publishing**: Ensure no confidential information is included before making a project public
- **Document public projects**: Add clear descriptions and documentation for public projects to help the community
- **Use consistent naming**: Follow naming conventions that indicate project purpose and visibility

### Security Considerations

- **Protect credentials**: Never include passwords, API keys, or credentials in project code
- **Review dependencies**: Check that imported libraries and function blocks don't contain sensitive information
- **Audit access**: Regularly review who has access to your private projects
- **Backup important work**: Maintain local backups of critical private projects

### Community Engagement

For public projects:

- **Provide clear descriptions**: Help others understand your project's purpose
- **Include documentation**: Add comments and documentation within your code
- **Use meaningful names**: Choose project names that clearly indicate functionality
- **Respond to feedback**: Engage with community members who use your projects
- **Version appropriately**: Use clear versioning for public projects that others may depend on

## Privacy and Data Protection

### What Information is Shared

For public projects, the following information is visible:

- Project name and description
- Owner's username and profile information
- Project cover image
- Programming language and configuration
- Last modified date
- Project content (PLC code, configurations, etc.)

For private projects, this information is only visible to:

- The project owner
- Explicitly invited collaborators (when collaboration features are available)

### What Information Remains Private

Regardless of project visibility:

- User email addresses
- Account credentials
- Billing information
- Private messages and notifications
- Personal profile settings

## Troubleshooting

### Common Issues

**Q: I can't find my project in search results**
- Check if the project is set to Private visibility
- Private projects don't appear in public search results
- Use the "All Projects" view in your Projects page to see all your projects

**Q: Someone else can see my private project**
- Verify the project visibility setting in project settings
- Check if you accidentally set it to Public
- Contact support if you believe there's a security issue

**Q: I want to collaborate but can't invite users**
- Collaboration features are planned for future releases
- Consider using the export/import workflow as a temporary solution
- Monitor platform updates for new collaboration features

**Q: Can I make a public project private again?**
- Yes, you can change visibility at any time through project settings
- Note that users may have already accessed or copied the public version
- Consider creating a new private project if security is critical
