# AI Engineer

The AI Engineer is the editor's built-in coding assistant. It has two surfaces:

- **Inline completion** — ghost-text suggestions in textual editors as you type.
- **Chat** — a side panel for conversational help.

Both run on Anthropic models; you pick between **haiku** (faster, cheaper) and **sonnet** (slower, better at hard problems). Usage is metered in **ACUs** (AI Credit Units). See the platform-level **[AI Credit Units](../../plans-and-billing/ai-credit-units)** page for plan limits and billing.

## First-time consent

The first time you click the **AI** icon (the `[AI]` button in the activity bar), the editor opens a consent modal. It explains:

- Your prompts and the surrounding file context are sent to Anthropic's API.
- Anthropic doesn't train on your data (per Anthropic's policy at the time of writing).
- You can revoke consent later from your account settings.

Accept to continue. Without consent, the AI features stay disabled.

## Inline completion

When AI is enabled and your active editor is one of the supported languages, the editor offers ghost-text completions as you type. Accept with **Tab**, dismiss with **Esc**, or just keep typing and the suggestion updates.

**Supported languages:** Structured Text (`st`), Instruction List (`il`), Python (`py`), C++ (`cpp`).

Inline completion is **off** for Ladder Diagram and FBD bodies (they're graphical, so there's nothing for a ghost text suggestion to attach to). Chat works for LD and FBD.

## Chat panel

Click **AI** to open the right-side chat panel. The chat:

- Sees the currently active file as context (the editor sends the file content alongside your message).
- Sees your project's data types and global variables (so it can answer questions about them).
- **Does not** automatically see other files — paste excerpts in if you need to.

Use the chat for:

- Explaining unfamiliar IEC syntax.
- Drafting an ST function and pasting the result back.
- Debugging a tricky FBD — describe the symptom, ask for likely causes.
- Translating between languages (Python block → equivalent C++, say).

## Models

Switch between **haiku** and **sonnet** from the model selector at the top of the chat panel. Sonnet is the default; haiku is faster and cheaper for short, simple questions.

## ACUs and plan limits

Every chat message and every accepted inline completion consumes ACUs from your monthly allowance. The chat panel shows your remaining balance in the header. When you exhaust the monthly allowance:

- A modal appears explaining the situation.
- You can either wait for the next billing cycle or buy extra credits (extra credits never expire).

See **[AI Credit Units](../../plans-and-billing/ai-credit-units)** for details.

## Telemetry

The editor logs anonymised events for completion lifecycle (`requested`, `shown`, `accepted`, `dismissed`, `error`, `timeout`), chat usage, and ACU consumption. These shape future tuning of the assistant. No prompt content is logged.

## Privacy and security

- Your prompts and file content are transmitted to Anthropic's API.
- The editor does **not** send credentials, secrets, or environment variables it might detect in code.
- If you paste credentials into a chat, **assume they've left the system** — rotate them.

For high-security environments, leave AI disabled. Editor functionality (compile, deploy, debug) works without it.

## What's next

- **[AI Credit Units](../../plans-and-billing/ai-credit-units)** — plan limits, extra credits, billing.
- **[Workspace Layout](workspace-layout)** — where the AI icon sits in the activity bar.
