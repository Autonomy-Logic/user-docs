# Installation

This guide covers how to install the OpenPLC Editor desktop application on Windows, macOS, and Linux. The web version of OpenPLC Editor (Autonomy Edge) requires no installation - simply visit [edge.autonomylogic.com](https://edge.autonomylogic.com) and sign up for an account.

## System Requirements

OpenPLC Editor runs on most modern computers. The minimum requirements are:

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+, Debian 11+, or equivalent)
- **Processor**: 64-bit processor (x64 or ARM64)
- **Memory**: 4 GB RAM minimum, 8 GB recommended
- **Storage**: 500 MB available disk space
- **Display**: 1280x720 minimum resolution

## Downloading OpenPLC Editor

Visit [autonomylogic.com/download](https://autonomylogic.com/download) to download the latest version of OpenPLC Editor. The website will automatically detect your operating system and recommend the appropriate download.

### Available Downloads

| Platform | Architecture | Download Type |
|----------|-------------|---------------|
| Windows | x64 | Installer (.exe) |
| Windows | ARM | Installer (.exe) |
| macOS | Apple Silicon (M1/M2/M3/M4) | Application (.dmg) |
| macOS | Intel | Application (.dmg) |
| Linux | x64 | AppImage |
| Linux | ARM | AppImage |

## Windows Installation

1. Download the Windows installer from the download page.
2. Run the downloaded `.exe` file.
3. If Windows SmartScreen appears, click "More info" and then "Run anyway". This warning appears because the application is not yet signed with an Extended Validation certificate.
4. Follow the installation wizard to complete the installation.
5. Launch OpenPLC Editor from the Start menu or desktop shortcut.

## macOS Installation

1. Download the macOS `.dmg` file for your processor type:
   - **Apple Silicon**: For Macs with M1, M2, M3, or M4 chips
   - **Intel**: For older Macs with Intel processors
2. Open the downloaded `.dmg` file.
3. Drag the OpenPLC Editor application to your Applications folder.
4. The first time you open the application, you may see a security warning. To allow the application:
   - Go to **System Preferences** > **Security & Privacy** > **General**
   - Click "Open Anyway" next to the message about OpenPLC Editor
5. Launch OpenPLC Editor from your Applications folder or Launchpad.

### Determining Your Mac's Processor

If you're unsure which version to download:
1. Click the Apple menu in the top-left corner
2. Select "About This Mac"
3. Look for "Chip" (Apple Silicon) or "Processor" (Intel)

## Linux Installation

OpenPLC Editor is distributed as an AppImage for Linux, which runs on most distributions without requiring installation.

### Running the AppImage

1. Download the Linux AppImage for your architecture (x64 or ARM).
2. Make the AppImage executable:
   ```bash
   chmod +x OpenPLC_Editor-*.AppImage
   ```
3. Run the AppImage:
   ```bash
   ./OpenPLC_Editor-*.AppImage
   ```

### Creating a Desktop Entry (Optional)

To add OpenPLC Editor to your application menu:

1. Move the AppImage to a permanent location:
   ```bash
   mkdir -p ~/Applications
   mv OpenPLC_Editor-*.AppImage ~/Applications/
   ```

2. Create a desktop entry file:
   ```bash
   cat > ~/.local/share/applications/openplc-editor.desktop << EOF
   [Desktop Entry]
   Name=OpenPLC Editor
   Exec=$HOME/Applications/OpenPLC_Editor-*.AppImage
   Icon=openplc-editor
   Type=Application
   Categories=Development;IDE;
   EOF
   ```

3. The application should now appear in your application menu.

## Building from Source

For developers who want to build OpenPLC Editor from source or contribute to the project:

### Prerequisites

- Git
- Node.js version 20 or later

### Build Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Autonomy-Logic/openplc-editor.git
   cd openplc-editor
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run start:dev
   ```

4. To build a distributable package:
   ```bash
   npm run package
   ```

For more information about contributing to OpenPLC Editor, visit the [GitHub repository](https://github.com/Autonomy-Logic/openplc-editor).

## Updating OpenPLC Editor

OpenPLC Editor does not currently include automatic updates. To update to a new version:

1. Download the latest version from [autonomylogic.com/download](https://autonomylogic.com/download)
2. Install the new version following the same steps as the initial installation
3. Your projects and settings will be preserved

## Troubleshooting

### Windows: "Windows protected your PC" message

This message appears because the application is not signed with an Extended Validation certificate. Click "More info" and then "Run anyway" to proceed with the installation.

### macOS: "App is damaged and can't be opened"

This can occur if the application was quarantined during download. To fix:
```bash
xattr -cr /Applications/OpenPLC\ Editor.app
```

### Linux: AppImage won't run

Ensure the AppImage has execute permissions:
```bash
chmod +x OpenPLC_Editor-*.AppImage
```

If you see FUSE-related errors, you may need to install FUSE:
```bash
# Ubuntu/Debian
sudo apt install fuse libfuse2

# Fedora
sudo dnf install fuse fuse-libs
```

## Next Steps

After installing OpenPLC Editor, you're ready to:

1. [Connect to an OpenPLC Runtime](connecting-to-runtimes.md) to deploy and test your programs
2. Explore the [Workspace Overview](workspace-overview/workspace-layout.md) to learn the IDE interface
3. Create your first project using the [Programming Languages](programming-languages/) guides
