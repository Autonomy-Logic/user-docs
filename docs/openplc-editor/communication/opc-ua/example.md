# Worked Example: Exposing a Blink Program over OPC-UA

This walkthrough takes a project that contains a simple blink program and exposes one variable to an OPC-UA client. The end result is a server an operator can connect to with [UAExpert](https://www.unified-automation.com/products/development-tools/uaexpert.html) (or any other OPC-UA client) using a username and password over an encrypted channel.

The starting point is a project with a single `BOOL` variable named `led` mapped to `%QX0.0` on the program `main`. The variable that blinks on and off. You can follow the same steps for any project; the variable names will differ.

## Step 1: Add an OPC-UA Server

1. In the project explorer click the **+** button.
2. Choose **Server**.
3. Type `plant_floor_opcua` as the **Server name** and pick **OPC-UA** from the **Protocol** dropdown.
4. Click **Create**.

The server appears under the **Servers** folder and the configuration view opens.

## Step 2: Configure General Settings

Open the **General Settings** tab.

1. Toggle **Enable Server** on. The helper text changes to *"Server will start when PLC runs."*
2. Set **Server Name** to `Plant Floor PLC`.
3. Leave **Network Interface** at `All Interfaces (0.0.0.0)`.
4. Leave **Port** at `4840`.
5. Set **Endpoint Path** to `/openplc/opcua`.
6. In the **Application Identity** section, set **Application URI** to `urn:plant_floor:opcua:server` and leave **Product URI** at the placeholder.
7. Leave **Cycle Time (ms)** at `100`.
8. Leave **Namespace URI** at `urn:openplc:opcua:namespace`.

The endpoint URL clients will use, once the project runs on a vPLC at `192.168.1.50`, is:

```
opc.tcp://192.168.1.50:4840/openplc/opcua
```

## Step 3: Replace the Default Security Profile

Open the **Security Profiles** tab. The profile named `insecure` is enabled by default; you will replace it with an encrypted one.

1. Click **+ Add Security Profile**.
2. **Profile Name**: `secure_password`.
3. Leave **Enabled** toggled on.
4. **Security Policy**: select **Basic256Sha256 (Recommended)**. Note that **Security Mode** auto-switches to **Sign and Encrypt** and the **Anonymous** checkbox is disabled.
5. In **Authentication Methods**, leave **Username / Password** checked. Uncheck **Anonymous** (already disabled) and **Certificate**.
6. Click **Add Profile**.

Now disable the original profile:

7. In the `insecure` row, click the toggle to turn it off. Because there is now another enabled profile, the toggle is no longer locked.

The list now shows two profiles: `insecure` (disabled) and `secure_password` (enabled, Basic256Sha256 / Sign and Encrypt / Username / Password).

## Step 4: Add an Operator User

Open the **Users** tab.

1. Click **+ Add User**.
2. Leave **Authentication Type** at **Password**.
3. **Username**: `operator1`.
4. **Password**: type a password of at least 4 characters (for example `change-me-now`).
5. **Confirm Password**: type the same password.
6. **Role**: select **Operator**.
7. Click **Add User**.

The user appears in the list with a 👤 icon, an amber Operator badge, and an Edit / Delete pair on the right.

## Step 5: Use the Default Self-Signed Certificate

Open the **Certificates** tab.

The default **Certificate Strategy** is **Auto-generate Self-Signed**. Leave it as is. The helper text reads: *"The runtime will automatically generate a self-signed certificate."* The runtime creates the certificate the first time the server starts on the target.

You do not need to add anything to **Trusted Client Certificates** for this example, because the security profile uses Username / Password authentication rather than Certificate authentication.

## Step 6: Expose the Blink Variable

Open the **Address Space** tab.

1. Confirm **Namespace URI** is `urn:openplc:opcua:namespace`.
2. In the **Available PLC Variables** panel, expand the `main` program node.
3. Click the `led (BOOL)` row.

The **Configure OPC-UA Node** modal opens with these defaults:

- **Node ID**: `PLC.main.led`
- **Browse Name**: `led`
- **Display Name**: `Led`
- **Description**: empty
- **Initial Value**: `false`
- **Access Permissions**: Viewer = Read Only, Operator = Read Only, Engineer = Read/Write

Make two adjustments:

4. Change **Display Name** to `Blink Output`.
5. Change **Operator** in the Access Permissions panel to **Read/Write** so `operator1` can both observe and force the blink output.
6. Click **Add to Address Space**.

The right-hand **Selected for OPC-UA** panel now shows `Blink Output` with the permission summary `V:r O:rw E:rw`. The header reads *"1 variable configured."*

## Step 7: Deploy and Connect

1. Save the project.
2. Transfer the project to a Runtime v4 vPLC and start it.
3. From a workstation that can reach the vPLC, open UAExpert (or your preferred OPC-UA client) and connect using:
   - **Endpoint URL**: `opc.tcp://<vPLC_IP>:4840/openplc/opcua`
   - **Security Policy**: `Basic256Sha256`
   - **Security Mode**: `SignAndEncrypt`
   - **Authentication**: `Username`
   - **Username**: `operator1`
   - **Password**: the password you set in Step 4
4. The first time the client connects it will warn that the server certificate is self-signed. Accept it once and the warning will not appear again.
5. Browse the server's address space until you find `Blink Output` under the `urn:openplc:opcua:namespace` namespace. Subscribe to it. The value alternates between `true` and `false` at the rate dictated by the blink program.
6. Right-click the node and write `true` to it. Because the Operator role has Read/Write permission on this node, the write succeeds and the runtime applies the new value on the next scan cycle.

## Optional: Add a Certificate-Authenticated Engineer

To allow an engineering workstation to connect with a certificate instead of a password:

1. Export the engineer's client certificate from the OPC-UA client.
2. On the **Certificates** tab, click **+ Add Trusted Certificate**, give it a **Certificate ID** of `eng_workstation`, paste the PEM, and click **Add Certificate**.
3. On the **Security Profiles** tab, edit `secure_password` (or add a second profile) and check the **Certificate** authentication box.
4. On the **Users** tab, click **+ Add User**, switch **Authentication Type** to **Certificate**, choose `eng_workstation` from the **Client Certificate** dropdown, set the role to **Engineer**, and click **Add User**.

Re-deploy. The engineering workstation can now connect by presenting its certificate, and it will have read/write access to every exposed node.

## What's Next?

- **[Troubleshooting](troubleshooting)**: common errors and how to fix them.
- **[Address Space](address-space)**: expand the example by exposing more variables, structures, or arrays.
- **[Users](users)**: add Viewer accounts for monitoring-only clients.
