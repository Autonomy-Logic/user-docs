# Project Compilation

This page shows you how to compile your PLC project, what to expect in the Console output, and how to fix common errors.

## How to Compile

1. Open your project in the IDE.
2. Click the **Compile** button in the Activity Bar (left side of the screen).
3. Watch the Console Panel at the bottom. It shows real-time progress for each step of the build.
4. Wait for the final message: `Compilation completed successfully`.

That's it. If you're connected to a device, the compiled program is automatically uploaded and ready to run.

> **Tip:** Clear the Console before compiling (click the trash icon) so you have a clean view of just this build's output.

## What You See in the Console

During compilation, the Console logs each step as it progresses:

```
[INFO]  Build process started
[INFO]  Generating XML...
[INFO]  Step 1: Generating Structured Text...
[INFO]  Step 2: Compiling to program files...
[INFO]  Step 3: Generating debug files...
[INFO]  Step 4: Generating variable bindings...
[INFO]  Step 5: Creating package...
[INFO]  Step 6: Uploading program to runtime...
[INFO]  Step 7: Monitoring runtime compilation...
[INFO]  Compilation completed successfully (exit code: 0).
```

Each line is timestamped and color-coded by severity:

- **Info** (blue): Normal progress
- **Warning** (yellow): Something to be aware of, but not a blocker
- **Error** (red): Something went wrong; the build stops here

## Successful Compilation

When compilation succeeds:

- The Console shows `Compilation completed successfully`.
- Your program has been uploaded to the connected device (if one is connected).
- You can now click the **Start PLC** button to run your program.

If you compiled without a connected device, the IDE validates your code but can't upload it. You'll see this message:

```
You need to connect to a device to be able to upload the PLC program.
```

This is still useful. It tells you your code compiles without errors, so you can connect and deploy later.

## Compiling Without a Device

You don't need a device connected to compile. The IDE will:

- Validate your project structure
- Check your code for syntax errors and type mismatches
- Report any issues in the Console

This is great for catching errors early while you're still developing your logic.

## Common Compilation Errors

### No program POU found

Your project needs at least one program-type POU. Check the Project Explorer. If the **Programs** branch is empty, create a program first.

### Syntax errors

These show up with line numbers and descriptions:

```
[ERROR] Line 15: Unexpected token 'THEN' - expected ';'
```

Go back to your code and fix the issue at the indicated line. Common causes:

- Missing semicolons at the end of statements
- Missing `END_IF`, `END_FOR`, or `END_WHILE` keywords
- Misspelled language keywords

### Undeclared variables

```
[ERROR] Line 23: Undeclared variable 'counter_value'
```

The variable you're using in your code isn't declared. Open the Variables Table at the top of the editor and add the missing variable with the correct name and type.

### Type mismatches

You're trying to assign a value of one type to a variable of a different type. For example, assigning a `REAL` value to an `INT` variable without a conversion function.

### Python or C/C++ validation errors

If your project includes Python or C/C++ function blocks, the IDE validates the custom code before compilation starts. Check the Console for specific validation messages. Make sure your code follows the required structure (see [Python Blocks](../custom-languages/python-blocks/python-basics) and [C/C++ Blocks](../custom-languages/cpp-blocks/cpp-basics)).

### Upload fails

If the code compiles but upload fails:

- Check that your device is still connected (look at the Orchestrators panel).
- Make sure the orchestrator is online.
- Check the Console for specific error messages.

### Compilation timeout

The IDE waits up to 5 minutes for the device to finish processing. If it times out:

- The device may be under heavy load. Try again.
- Check that the device is still running in the platform dashboard.
- Reconnect to the device and recompile.

## Server IP Validation

If your project includes communication servers (Modbus slave, S7Comm, OPC-UA), the IDE checks that the configured bind addresses match the target device's network interfaces before uploading.

If there's a mismatch, a dialog appears with three options:

- **Cancel**: Stop the upload and fix the address.
- **Continue**: Upload anyway (the server may fail to start on the device).
- **Switch to all interfaces**: Temporarily use `0.0.0.0` so the server listens on all available interfaces.

---

## What's Next?

- [Deployment](deployment-vplc): Learn what happens after compilation and how to manage your running program.
- [XML Export](xml-export): Export your project for backup or sharing.
- [Console & Debugging](../workspace-overview/console-debugging): Learn how to read and filter build logs effectively.
