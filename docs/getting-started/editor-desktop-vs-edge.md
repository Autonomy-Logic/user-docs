# Editor Desktop vs Autonomy Edge

## Two Products, Two Different Workflows

Autonomy offers **two separate products** for working with PLCs. They serve different purposes and work in different ways. Understanding the difference will help you choose the right tool for your needs.

| Feature | Editor Desktop | Autonomy Edge |
|---------|---------------|---------------|
| **Type** | Local desktop application | Cloud platform (web browser) |
| **Runtime** | Runtime v4. User installs manually | Managed automatically by Orchestrator |
| **Works without internet?** | Yes | No (cloud-based) |
| **Device management** | Local configuration files | Platform web UI |
| **Target user** | Developer doing local PLC programming | Team managing multiple devices remotely |

---

## Editor Desktop + Runtime v4

**Editor Desktop** (also known as OpenPLC Editor) is a **local desktop application** that you install on your computer (Windows, macOS, or Linux).

### How It Works

- You download and install the Editor Desktop application on your computer.
- You download **Runtime v4** from GitHub and install it manually on the machine that will run your PLC program.
- You write your PLC program in the Editor, then deploy it to the Runtime.
- Everything runs **locally on your machine**: no internet connection required.

### Key Points

- Editor Desktop is a **standalone application**. It runs entirely on your computer.
- Runtime v4 is downloaded from the [OpenPLC Runtime GitHub repository](https://github.com/Autonomy-Logic/openplc-runtime) and installed by the user.
- Runtime v4 works **only** with the Editor Desktop application.
- Editor Desktop and Runtime v4 have **no connection to Autonomy Edge**. They are completely separate products.

> **Important:** The Runtime v4 GitHub repository is for Editor Desktop users only. If you are using Autonomy Edge, you do **not** need to download or install Runtime v4.

---

## Autonomy Edge + Orchestrator

**Autonomy Edge** is a **cloud platform** that you access through your web browser at any time, from anywhere.

### How It Works

- You log in to Autonomy Edge from your web browser.
- You install the **Orchestrator** on a Linux machine with a single command (`curl https://getedge.me | bash`).
- The Orchestrator connects your Linux machine to the cloud platform.
- You create and manage **Devices (virtual PLCs)** entirely through the web interface.
- The Runtime is managed **automatically**: you never install, update, or configure it yourself.

### Key Points

- Autonomy Edge is a **cloud platform**. You access it from your browser. No desktop application to install.
- The Orchestrator is installed with **one command** and handles all communication between the cloud and your local machine.
- The Runtime is managed **automatically** by the Orchestrator. You never need to download or install it.
- All device management happens through the **platform web UI**: no terminal commands, no config files.

> **Important:** The Runtime v4 GitHub repository has **no connection** to Autonomy Edge. Autonomy Edge manages its own runtime automatically through the Orchestrator.

---

## Which One Should I Use?

Use this quick guide to decide:

| If you want to... | Use |
|-------------------|-----|
| Program a PLC locally on your own computer | **Editor Desktop** |
| Manage devices remotely through a web platform | **Autonomy Edge** |
| Work offline without internet | **Editor Desktop** |
| Manage multiple devices across different machines | **Autonomy Edge** |
| Use the OpenPLC Editor desktop application | **Editor Desktop** |
| Collaborate with a team on device management | **Autonomy Edge** |

### Still Not Sure?

- **"I want to program a PLC locally"** → Use **Editor Desktop**
- **"I want to manage devices remotely through a web platform"** → Use **Autonomy Edge**
- **"I am using OpenPLC Editor"** → You are using **Editor Desktop**
- **"I installed something with `curl https://getedge.me | bash`"** → You are using **Autonomy Edge**
- **"I downloaded Runtime v4 from GitHub"** → You are using **Editor Desktop**

---

## Can I Use Both?

Yes. The two products are independent but compatible. A vPLC Device created through Autonomy Edge runs the same OpenPLC Runtime, and you can connect to it using the Editor Desktop application from any computer on the same local network. However, the two products are managed separately. Editor Desktop does not sync with the Autonomy Edge cloud platform.
