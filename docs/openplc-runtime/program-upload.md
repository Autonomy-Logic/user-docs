# Program Upload

This page explains how programs are uploaded to OpenPLC Runtime v4.

## Overview

OpenPLC Runtime v4 uses a ZIP-based program upload mechanism through its REST API. Programs are compiled in OpenPLC Editor and uploaded as a ZIP archive containing all necessary files.

## Upload Process

### From OpenPLC Editor

The easiest way to upload programs is through OpenPLC Editor:

1. Open your project in OpenPLC Editor
2. Connect to the runtime (see [Connecting to Runtimes](../openplc-editor/connecting-to-runtimes.md))
3. Click the **Compile and Download** button
4. The editor compiles your program and uploads it automatically

### ZIP Archive Structure

When uploaded, the program ZIP contains:

```
program.zip
├── program.st          # Compiled IEC code
├── lib/                # Library files
│   └── ...
├── config/             # Configuration files
│   ├── modbus_slave.json    # Modbus server config (if configured)
│   ├── modbus_master.json   # Modbus client config (if configured)
│   └── ...
└── ...
```

## REST API Upload

For advanced users, programs can be uploaded directly via the REST API:

### Endpoint

```
POST /api/program
Content-Type: multipart/form-data
Authorization: Bearer <jwt_token>
```

### Request

- Upload the ZIP file as form data
- Include JWT token in Authorization header

### Response

```json
{
  "success": true,
  "message": "Program uploaded successfully"
}
```

## Program Lifecycle

### Upload

When a program is uploaded:

1. The runtime stops any running program
2. The ZIP is extracted to the program directory
3. Configuration files are processed
4. Plugins are loaded based on configuration

### Start

To start the program:

1. Use the runtime controls in OpenPLC Editor, or
2. Call the REST API: `POST /api/program/start`

### Stop

To stop the program:

1. Use the runtime controls in OpenPLC Editor, or
2. Call the REST API: `POST /api/program/stop`

## Configuration Files

Protocol configurations are included in the ZIP as JSON files:

### Modbus Slave Configuration

```json
{
  "plugin_modbus_slave": {
    "type": "PLUGIN_TYPE_PYTHON",
    "path": "core/src/drivers/modbus_slave.py",
    "enabled": true
  },
  "network_configuration": {
    "host": "0.0.0.0",
    "port": 502
  },
  "buffer_mapping": {
    "max_coils": 8000,
    "max_discrete_inputs": 8000,
    "max_holding_registers": 1000,
    "max_input_registers": 1000
  }
}
```

### Modbus Master Configuration

```json
[
  {
    "name": "Remote Sensor",
    "protocol": "MODBUS",
    "config": {
      "type": "SLAVE",
      "host": "192.168.1.50",
      "port": 502,
      "timeout_ms": 1000,
      "io_points": [
        {
          "fc": 4,
          "offset": "0x0000",
          "iec_location": "%IW100",
          "len": 4,
          "cycle_time_ms": 500
        }
      ]
    }
  }
]
```

## Troubleshooting

### Upload Fails

1. Verify you're authenticated (valid JWT token)
2. Check the program compiles without errors
3. Ensure the runtime is running and accessible

### Program Won't Start

1. Check the runtime logs for errors
2. Verify all required plugins are available
3. Check configuration file syntax
