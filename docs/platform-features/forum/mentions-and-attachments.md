# @Mentions and Attachments

This guide covers two features that work in every rich-text editor on the forum (topic composer, reply composer, DMs): **tagging people with @** and **adding files or images**.

---

## @Mentions

Mentioning someone with `@username` tags them directly in your post. They receive:

- An **in-app notification** (the bell icon shows a new item).
- An **email**, unless they've turned off mention emails in their Privacy settings.

### How to mention someone

1. Anywhere in the editor. Topic body, reply, DM. Type `@`.
2. A small popup appears, listing up to **8 suggested people**:
   - On a topic reply, it's pre-loaded with the **topic author** and **anyone who recently posted** in the thread.
   - Keep typing to **search** across all members by username or display name.
3. Use the arrow keys and Enter to select, or click the person's name.
4. Their handle is inserted as a styled `@username` tag in blue.

The mention stays as a tag. It's not just plain text. It renders as a link in the published post, and mention notifications are triggered when you click **Publish** or **Reply**.

### What mentioned people see

- **In-app notification**: "You were mentioned by [your name] in 'Topic title'".
- **Email** (if they opted in): A formatted email with the topic title, your post excerpt, and a **View the discussion** button. The email has a footer link to unsubscribe from `@mention` emails specifically (see [Email and Privacy Preferences](email-preferences)).

### Etiquette

- **Don't spray mentions.** Tagging 10 people at once is noisy. Tag only the people whose input you genuinely need.
- **Don't mention yourself.** The system won't email you for a self-mention, but it's still weird to see in a post.
- **Don't use mentions as decoration.** Writing `thanks @alice 🎉` in a celebration post is fine; writing `@alice @bob @carol check this out` in every post gets old fast.

> **Heads up:** If someone has turned off mention emails in their Privacy settings, they still get the in-app notification. They just don't get an email copy.

---

## Attachments and Images

All three editors. Topic body, reply, and DMs. Accept file attachments. Images render inline; other file types appear as download links.

### How to add a file or image

Three ways, all equivalent:

1. **Click the icons in the footer.**
   - **📎 Paperclip**: Any file type. Use this for `.pdf`, `.zip`, `.txt`, project files, logs, etc.
   - **🖼️ Image icon**: Filtered to image file types. Use this for screenshots, diagrams, photos.
2. **Drag and drop** the file from your computer directly into the editor.
3. **Paste** an image from your clipboard (works perfectly with screenshot tools on macOS, Windows, and Linux).

The footer gives a subtle hint: *"Paste, drop, or click to add files"*.

### Upload limits

| Rule | Limit |
|---|---|
| Maximum size per file | **10 MB** |
| Accepted file types | **Any**: the paperclip accepts everything |
| Number of files per post | No fixed limit. Keep it reasonable |

If you drop a file larger than 10 MB, the upload is rejected and you'll see an error message. Try compressing the file or hosting it externally and linking to it.

### What happens during upload

- The file uploads in the background while you keep writing.
- The **Publish** / **Reply** / **Send** button changes to **"Uploading images..."** and stays disabled until the upload finishes.
- If an upload fails, you'll see an error. Retry by dropping the file again.

### How files appear in the post

- **Images**: Rendered inline at their natural size (capped to fit the content column). Click an inline image to open it full-size in a new tab.
- **Other files**: Shown as a clickable download link with the filename. Readers click to download.

### Screenshots: the fastest workflow

If you're asking for hardware help, **screenshots are gold**. The fastest flow:

1. Take a screenshot (Cmd+Shift+4 on Mac, Win+Shift+S on Windows, Shift+PrtSc on most Linux distros).
2. Click inside the editor.
3. Paste (Cmd+V / Ctrl+V).
4. The image uploads and appears inline immediately.

No need to save the screenshot to your desktop first.

---

## What Files Are Good for Which Use Case

| You want to share... | Best approach |
|---|---|
| A short code snippet | **Code block** (format `<>` button in the toolbar), not an attachment |
| Log output or error text | **Code block**, pasted as text |
| A screenshot | **Paste** an image directly; or drop a `.png` |
| A long log file or core dump | Attach as `.txt` |
| A sample project or bundle | Attach as `.zip` |
| A datasheet or PDF | Attach the PDF |
| A video | Upload to YouTube / Vimeo and paste the link. The forum doesn't host video |

---

## Quick Reference

| Action | How | Notes |
|---|---|---|
| Mention a user | Type `@` + their username | 8 suggestions max in the popup |
| Attach a file | Paperclip icon / drag / paste | 10 MB max, any type |
| Attach an image | Image icon / drag / paste | Renders inline |
| Paste screenshot | Cmd+V / Ctrl+V in the editor | Uploads automatically |

---

## What's Next?

Curious who's most active in the community? Next:

➡️ [Members Directory](members-directory)
