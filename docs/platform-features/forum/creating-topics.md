# Creating a Topic

A **topic** is a new discussion thread on the forum. Your question, your project announcement, your hardware troubleshooting, whatever you want the community to engage with. This guide walks you through every field in the composer.

> You need to be **signed in** to create a topic. If you're not, you'll see a sign-in / sign-up card instead of the composer.

---

## Opening the Composer

You can start a new topic from several places:

- **Forum home toolbar**: Click the **New Topic** button in the top right.
- **Any category board**: The **New Topic** button is also available at the top of every category page.
- **Direct URL**: `edge.autonomylogic.com/forum/new-topic`.

All of them take you to the same form.

---

## The Composer Layout

The composer is split in two on desktop:

- **Left column (main area)**: Category selection, title, content editor.
- **Right column (sidebar, desktop only)**: Writing hints that appear as you fill in each field. Hidden on mobile to save space.

The bottom of the page shows a **Discard** button (throws away everything you've typed and returns you to the forum) and a **Publish Topic** button (posts the topic).

---

## Step 1: Pick a Category

You **must** pick a category before you can publish. The prompt reads **"Select a category"** with all available categories shown as clickable pills.

- Click a category pill to select it. It moves up to the top of the section with an `✕` to deselect.
- If the category has sub-categories, a second row appears: **"Narrow it down (optional)"** with sub-category pills.
- Picking a sub-category is optional. If you leave it empty, your topic lives directly under the parent category.

The **Publish Topic** button stays disabled until you've selected at least a category.

> **Tip:** Check whether a sub-category exists that better fits your topic. It helps the right people find your question faster.

---

## Step 2: Write the Title

A large single-line input where you type your topic title. No hard character limit is enforced in the UI, but **aim for 10–80 characters**: long enough to be clear, short enough to fit in activity previews.

Focusing on this field makes the sidebar's **"Writing a good title"** hint appear.

### What makes a good title

- **Be specific.** "PID tuning not settling" is better than "Help".
- **Mention your platform** when relevant ("Raspberry Pi 4", "Arduino Uno", "Windows 11").
- **If it's a bug, include the error message**: even just a keyword from it helps others find their way to you.

Bad: `help please`
Better: `Modbus RTU slave timeout on Raspberry Pi 4 after firmware upgrade`

---

## Step 3: Write the Content

The main body is a **rich text editor** with two tabs:

- **Write**: The active editor, where you type.
- **Preview**: What your post will look like once published. If there's no content yet, it shows "Nothing to preview".

The editor supports a lot more than plain text. Use the toolbar above the editing area to format as you go.

### Formatting toolbar

| Button | What it does |
|---|---|
| **Heading (H)** | Turns the current line into a section heading. |
| **Bold (B)** | **Bold** the selected text. |
| **Italic (I)** | *Italic* the selected text. |
| **Underline (U)** | <u>Underline</u> the selected text. |
| **Strikethrough (S)** | ~~Strike through~~ the selected text. |
| **Code block** | Inserts a multi-line code block with syntax highlighting. Paste logs, code, or error messages here. |
| **Link** | Opens a prompt asking for the URL; wraps your selection with a link. |
| **Bullet list** | An unordered `• • •` list. |
| **Ordered list** | A numbered `1. 2. 3.` list. |
| **Quote** | A blockquote, indented with a left border. |

> **Tip:** Use **code blocks** for any code, log output, or error message. They use a monospace font and keep indentation, which makes debugging help much faster. Avoid pasting raw logs as regular text.

### Adding images

Three ways to add an image:

1. Click the **image icon** in the footer to open your computer's file picker.
2. **Drag and drop** an image file into the editor.
3. **Paste** an image from your clipboard (screenshots work).

Images upload automatically and appear inline. While uploading, the Publish button temporarily shows **"Uploading images..."**: wait for it to finish before publishing.

### Attaching files

Click the **paperclip icon** in the footer to attach non-image files (PDFs, `.zip`, project files, etc.).

- **Max size: 10 MB per file.**
- Any file type is accepted.
- Attachments appear as clickable download links inside your post.

The footer reminds you: *"Paste, drop, or click to add files"*.

### Tagging other users

Type `@` anywhere in the content and an autocomplete popup will suggest people to tag. Click a name to insert a tag like `@username`. Tagged users receive a notification and (if they have it on) an email.

See [@Mentions and Attachments](mentions-and-attachments) for more on tagging etiquette.

---

## Writing Hints (Desktop Sidebar)

On desktop, a hints panel appears on the right side when you focus on the title or content area. It's a quick cheat sheet. No interactive elements, just a reminder of what makes a good post.

The **"Writing great content"** panel suggests:

- Use **code blocks** for logs, errors, and snippets.
- Add **screenshots** when visuals help.
- Include your **OS**, **runtime version**, and **hardware** if the topic is about a technical problem.
- Describe the **steps to reproduce** the issue.

---

## Publishing

When you're happy with your title, category, and content, click **Publish Topic** at the bottom right of the page.

- If anything is missing (title or category), the button stays disabled.
- If images are still uploading, the button reads "Uploading images..." and is disabled until they finish.
- On success, you're redirected to your newly created topic and can see it live.

If you change your mind before publishing, click **Discard** to throw the draft away and go back to the forum home.

> **Heads up:** There's no auto-save draft feature at the moment. If you navigate away, your content is lost. For long posts, write in a separate app and paste into the composer when ready.

---

## What Happens After You Publish

- Your topic appears on the home page in Latest (and may appear in Trending as it accumulates activity).
- It's visible to everyone, even people without an account.
- People can upvote, downvote, reply, or report.
- If you tagged anyone with `@username`, they get an in-app notification and (if they opted in) an email.
- **You become the "author"** of this topic. Which means you'll get an email every time someone replies, unless you turn that off in your Privacy settings.

---

## Quick Reference

| Field | Required | Notes |
|---|---|---|
| Category | Yes | Pill selection at the top |
| Sub-category | No | Only offered if the parent category has subs |
| Title | Yes | Plain text, one line |
| Content | Yes | Rich text, images, code, attachments |
| Attachments | No | 10 MB per file, any type |

---

## What's Next?

Ready to see what happens when someone replies? Next up:

➡️ [Viewing and Replying to Topics](viewing-and-replying)
