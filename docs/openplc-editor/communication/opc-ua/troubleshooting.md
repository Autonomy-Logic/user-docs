# OPC-UA Troubleshooting

This page lists common issues you may see while configuring or connecting to an Autonomy Edge OPC-UA server, and the action to take in each case. Most of the messages in this page are quoted directly from the editor or from a typical OPC-UA client.

## Editor Validation Messages

The configuration tabs reject invalid input before you can save. The exact messages and their causes:

### Security Profiles Tab

| Message | Cause | Action |
|---------|-------|--------|
| *"Profile name is required"* | The Profile Name field is empty. | Type a unique name (max 64 characters). |
| *"Profile name must be 64 characters or less"* | Profile Name exceeds 64 characters. | Shorten the name. |
| *"A profile with this name already exists"* | Another profile uses the same name (case-insensitive). | Rename one of the profiles. |
| *"Security Mode must be 'None' when Security Policy is 'None'"* | Mismatched policy and mode. | The Mode dropdown auto-corrects when you change the Policy. If you see this error, reopen the dropdown and pick `None`. |
| *"Security Mode cannot be 'None' when using a security policy"* | Policy is non-None but Mode was left at None. | Switch Mode to `Sign Only` or `Sign and Encrypt`. |
| *"Anonymous authentication is only available with Security Policy 'None'"* | Anonymous was enabled when policy is non-None. | Uncheck Anonymous and use Username / Password or Certificate. |
| *"At least one authentication method is required"* | All three authentication checkboxes are unchecked. | Enable at least one. |
| *"Warning: At least one security profile must be enabled for clients to connect."* | Every profile is disabled. | Enable at least one profile. |

### Users Tab

| Message | Cause | Action |
|---------|-------|--------|
| *"Username is required"* | Empty Username on a Password user. | Type a username. |
| *"Username must be 64 characters or less"* | Username too long. | Shorten the username. |
| *"A user with this username already exists"* | Duplicate username (case-insensitive). | Pick a different username. |
| *"Password is required"* | Password field empty for a new user. | Type a password of 4 or more characters. |
| *"Password must be at least 4 characters"* | Password too short. | Use a longer password. |
| *"Passwords do not match"* | Password and Confirm Password differ. | Retype Confirm Password to match. |
| *"Please select a certificate"* | Certificate user has no certificate selected. | Pick a certificate from the **Client Certificate** dropdown. |
| *"No trusted certificates available. Add certificates in the Certificates tab first."* | Tried to create a Certificate user with no trusted certificates. | Add the certificate on the [Certificates](certificates) tab first. |
| *"Warning: Username authentication is enabled but no password users exist. Add at least one user for clients to authenticate."* | A profile accepts Username / Password but no Password users exist. | Add at least one Password user. |

### Certificates Tab

| Message | Cause | Action |
|---------|-------|--------|
| *"Certificate ID is required"* | Empty Certificate ID. | Type an ID (letters, numbers, hyphens, underscores). |
| *"Certificate ID must be 64 characters or less"* | ID too long. | Shorten the ID. |
| *"Certificate ID can only contain letters, numbers, hyphens, and underscores"* | Invalid characters in the ID. | Replace spaces or symbols with `_` or `-`. |
| *"A certificate with this ID already exists"* | Duplicate ID. | Pick a different ID. |
| *"Certificate PEM content is required"* | Empty PEM area. | Paste or browse for the PEM content. |
| *"Certificate must start with '-----BEGIN CERTIFICATE-----'"* | The text does not begin with the PEM header. | Paste the entire PEM block including the markers. |
| *"Certificate must end with '-----END CERTIFICATE-----'"* | Missing PEM footer. | Make sure the file ends with the closing marker. |
| *"Certificate content appears to be too short"* | Body shorter than ~100 characters of base64. | Verify you pasted the certificate body, not just the headers. |
| *"Certificate contains invalid base64 content"* | Body cannot be base64-decoded. | Re-export the certificate; the file is corrupt or has been edited. |

### Address Space Tab

| Message | Cause | Action |
|---------|-------|--------|
| *"Node ID is required"* | Empty Node ID in the Configure OPC-UA Node modal. | Type a unique Node ID. |
| *"Node ID must be 128 characters or less"* | Node ID too long. | Shorten the Node ID. |
| *"A node with this ID already exists"* | Two exposed variables have the same Node ID. | Choose a different Node ID. The auto-generated `PLC.<POU>.<path>` is unique by construction. |
| *"Browse name is required"* / *"Display name is required"* | One of the names is empty. | Fill in the missing field. |
| *"Browse name must be 64 characters or less"* / *"Display name must be 128 characters or less"* | The respective field is too long. | Shorten the name. |

### General Settings Tab

The Port and Cycle Time fields silently revert to the previous valid value if you enter something out of range. If you type a Port outside `1`–`65535` or a Cycle Time outside `10`–`10000` ms, the editor restores the prior value when the field loses focus. Look at the inline hints (`Default: 4840`, `Update frequency for OPC-UA variables (10-10000ms)`) for the accepted range.

## Connection Problems Reported by Clients

The next group of issues appears in the OPC-UA client (UAExpert and similar tools), not in the editor.

### Connection Refused on Port 4840

A `connection refused` or `BadConnectionRejected` error means the TCP connection itself failed. Check, in order:

1. **Is the runtime running?** OPC-UA only listens while the PLC program is loaded. Open the editor's console and confirm the program is in run mode.
2. **Is the server enabled?** On the [General Settings](general-settings) tab, confirm **Enable Server** is on. The helper text under the toggle should read *"Server will start when PLC runs."*
3. **Is the port reachable?** Verify with `telnet <host> 4840` or `nc -zv <host> 4840`. If it fails, an industrial firewall, host firewall, or network ACL is blocking the port.
4. **Is another service using the port?** If you changed the port to a value below 1024 the runtime may not have permission to bind. Use a port above 1024 (for example, `14840`) and update the client URL to match.

### Endpoint Path Mismatch

OPC-UA clients consider the endpoint URL a single string. If your **Endpoint Path** is `/openplc/opcua` but the client connects to `opc.tcp://host:4840` (no path), the server will refuse the session.

| Client URL | Editor Endpoint Path | Connects? |
|------------|----------------------|-----------|
| `opc.tcp://host:4840/openplc/opcua` | `/openplc/opcua` | Yes |
| `opc.tcp://host:4840` | `/openplc/opcua` | No |
| `opc.tcp://host:4840/wrong` | `/openplc/opcua` | No |

Match the client URL exactly, or empty the **Endpoint Path** field on the General Settings tab.

### Server Certificate Rejected

The first time a client connects to a server with an auto-generated self-signed certificate, the client warns that the server is untrusted. This is expected. Accept the certificate in the client (UAExpert calls this "Trust Server Certificate") and the warning will not return on subsequent connections.

If the certificate is rejected on every connection, the client did not save it to its trust store. Check the client's documentation for how to permanently trust a server certificate.

For production deployments, switch to a custom certificate signed by a CA your clients already trust. See [Certificates](certificates).

### BadIdentityTokenInvalid / BadIdentityTokenRejected

The client connected but the credentials were refused.

For Username / Password connections:

- Confirm the user exists on the [Users](users) tab and is of type Password.
- Confirm the password matches what was set in the editor (passwords are case-sensitive).
- Confirm the security profile the client is using has **Username / Password** checked under Authentication Methods.

For Certificate connections:

- Confirm the certificate is in the Trusted Client Certificates list with the same fingerprint.
- Confirm a user on the Users tab is of type Certificate and is bound to that Certificate ID.
- Confirm the security profile has **Certificate** checked under Authentication Methods.

### BadSecurityChecksFailed / BadSecurityModeRejected

The client and server disagree on policy or mode. Check that the **Security Policy** and **Security Mode** the client is configured with match a profile that is enabled on the server. For example, if your server only enables `Basic256Sha256 / Sign and Encrypt`, the client cannot connect with `Basic256 / Sign Only`.

### Stale or Unchanging Values

A subscription returns the same value forever or refreshes very slowly. Check:

1. **Cycle Time**. On the General Settings tab the Cycle Time may be too long. The accepted range is 10–10000 ms; the inline hint reads *"Update frequency for OPC-UA variables (10-10000ms)."* Lower values mean fresher data.
2. **PLC scan cycle**. The variable on the PLC side must actually change. If the program is paused or in error, OPC-UA will report the last value forever.
3. **Sampling interval at the client**. Even with a fast cycle time on the server, the client's subscription has its own sampling interval. Lower it in the client.

### Permission Denied on Read or Write

A client connects successfully but read or write on a particular node is rejected.

1. Open the [Address Space](address-space) tab and find the node in the **Selected for OPC-UA** list.
2. Click **Edit** to reopen the **Configure OPC-UA Node** modal.
3. Check the **Access Permissions** for the role assigned to the connecting user.
   - Viewer with `Read Only` cannot write. Change to `Read/Write`.
   - Operator with `Read Only` cannot write either.
   - Engineer typically has `Read/Write`; if not, adjust accordingly.
4. For structured types, check the per-field row in the **Field Permissions** table. A parent permission of `Read/Write` does not propagate automatically. Use **Apply Parent Permissions to All** to copy the parent's settings to every field.

## What's Next?

- **[Worked Example](example)**: re-run the end-to-end walkthrough to verify a known-good configuration.
- **[Security Profiles](security-profiles)**: review allowed policies and modes.
- **[Address Space](address-space)**: adjust per-variable read / write permissions.
