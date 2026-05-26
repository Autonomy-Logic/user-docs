# What is Autonomy Edge?

Autonomy Edge is a cloud platform for industrial automation. You write IEC 61131-3 PLC programs in a browser-based IDE, store them as git-versioned projects, and deploy them to virtual PLCs running on your own edge hardware. The platform also bundles a public community: project sharing, an OpenPLC forum, direct messaging, and an AI assistant grounded on the platform's own documentation.

Everything happens in your browser. You don't install IDE software locally. You don't move files around manually. The only thing that runs on your hardware is a small **orchestrator agent** that talks to the cloud and starts and stops vPLC containers.

## Who this is for

- **Plant engineers and integrators** who want to program PLCs from anywhere without licensing a desktop IDE per machine.
- **OEMs and machine builders** who need to ship the same program to many devices and keep them in sync over the air.
- **Teaching staff and students** working with open-source PLC tooling in classroom settings.
- **Hobbyists and tinkerers** running OpenPLC on a Raspberry Pi or a Linux PC at home.

If you already use the [OpenPLC desktop editor](https://autonomylogic.com/), Autonomy Edge is the cloud-hosted continuation of that tooling: same IEC 61131-3 support, same five languages, plus version control, remote deployment, organizations, and a community layer that the desktop editor cannot provide on its own.

## What you can build

- **Single-PLC machines.** One project, one vPLC, one device. The Quick Start walks through exactly this case.
- **Multi-PLC machines.** One orchestrator on a beefy edge device, several vPLCs each running an isolated runtime, all coordinated from one browser session.
- **Fleets of identical devices.** Push the same project to many orchestrators across sites. (Multiple orchestrators require a paid plan; see [Pricing](../plans-and-billing/pricing).)
- **Collaborative projects.** Invite teammates to an [organization](../platform/organizations/overview), branch and review changes via [pull requests](../platform/projects/pull-requests), and discuss in the [forum](../platform/forum/overview).

## How the pieces fit together

There are four things in play whenever you ship a program:

1. **The web app** at `edge.autonomylogic.com`. This is what you read, click, and type into. The login, the dashboard, the projects list, the editor, the forum, all of it lives here.
2. **The orchestrator agent.** A small Python daemon that runs on a Linux edge device (PLC, PAC, industrial PC, server, Raspberry Pi). You install it with one curl command. It connects to the cloud over a secure mTLS WebSocket and waits for instructions.
3. **vPLC containers.** When you tell the platform to create a vPLC, the orchestrator starts an OpenPLC v4 runtime in a Docker container on that device. Each vPLC appears on your physical LAN with its own IP and MAC address, so it behaves like a standalone PLC. You can run several side by side on one piece of hardware.
4. **Industrial I/O.** The vPLC talks to your sensors, drives, HMIs, and remote I/O over Modbus TCP/RTU, EtherCAT, EtherNet/IP, OPC-UA, or S7Comm, the same protocols you'd use with any other PLC.

You don't have to deal with any of this manually. The platform handles the cloud-to-agent connection, the agent manages the containers, and the containers manage your runtime. You write code in the browser and click Download. That's the workflow.

## What's free and what's paid

The Community plan is free forever and is enough to:

- Read and post in the forum.
- Create and edit **public** projects.
- Run one orchestrator with two vPLC devices.
- Use the AI Chat assistant.

Private projects, additional orchestrators, more devices, and team features require a paid plan. The five plans are summarized in **[Pricing](../plans-and-billing/pricing)** and the per-plan limits are listed in **[Plan limits](../plans-and-billing/plan-limits)**.

## Where to go next

- **You want to try it out** → **[Account and signup](account-and-signup)**, then **[Quick Start](quick-start)**.
- **You're logged in and looking around** → **[Dashboard tour](dashboard-tour)**.
- **You're not sure what something on screen does** → use the **[URL cheat sheet](../reference/url-cheatsheet)** to find the page and its docs.
- **You want a one-page vocabulary refresher** → **[Glossary](../reference/glossary)**.
