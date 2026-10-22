# Accessing the editor

The OpenPLC Editor is part of Autonomy Edge. There's nothing to install. Open a project, click **Open in editor**, and you're in.

1. Open a modern browser (Chrome, Edge, Firefox, or Safari).
2. Go to [edge.autonomylogic.com](https://edge.autonomylogic.com) and log in.
3. Open a project, then click **Open in editor**.

The editor loads in the same tab.

## System requirements

- A modern browser with JavaScript enabled.
- A stable internet connection.
- An Autonomy Edge account.

Graphical editors (Ladder, FBD) are easiest with a mouse or trackpad. The editor works on tablets but isn't tuned for touch input.

## Desktop editor (separate product)

The OpenPLC project also publishes a standalone desktop editor for Windows, macOS, and Linux. It shares the same project format and most of the same features. A handful of surfaces (the board selector, VPP vendor screens, USB upload, local-disk project paths) live only on the desktop side, so if you need them, install the desktop editor and use it alongside the web one.

For most Autonomy Edge users, the web editor is enough, including the in-browser Simulator for quick tests without setting up hardware.

### Updating the desktop editor

The web editor is always up to date. The desktop editor tells you when a newer version is out and lets you decide when to install it.

About a minute after you open the desktop editor, it checks for a newer release. When there is one, a blue bar appears at the top of the window: **A new version of OpenPLC Editor is available**.

1. Click **Update**. The editor downloads the installer for your computer and checks that the file matches the published release.
    - **Windows** and **macOS**: the file goes to your Downloads folder.
    - **Linux**: you choose where to save the new AppImage.
2. The editor opens what it downloaded: the installer on Windows, the disk image on macOS, the folder with the new AppImage on Linux.
3. Save your project and click **Quit Now**, or **Later** to keep working. While the bar shows **Open Installer**, it opens the same file again without downloading it.
4. Install the new version as you did the first time. On Linux, run the new AppImage.

On Windows, the installer asks you to close the editor if it is still open. It never closes the editor for you, so unsaved work is never lost.

Click **X** on the bar to hide it until you open the editor again.

To check at any time, use **File > Check for Updates**. To stop the automatic check, untick **File > Check for Updates Automatically**; the change applies from the next start.

## What's next

Take the **[Workspace Layout](workspace-overview/workspace-layout)** tour.
