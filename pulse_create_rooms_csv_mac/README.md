# Pulse Create Rooms - CSV - Mac Executable Distribution

This is a standalone executable version of Pulse Create Rooms - CSV for macOS. It does **not** require Python, virtual environments, or any dependencies to be installed on the user's machine.

## What's Included

- `pulse_create_rooms_csv` - The standalone executable for macOS (ARM64/Apple Silicon)
- `.env.template` - Template for configuration file
- `example_rooms.csv` - Example CSV file for creating rooms

## Quick Start

### 1. Download the Files

Download the following files to a folder on your Mac:
- `pulse_create_rooms_csv` (the executable)
- `.env.template`
- `example_rooms.csv` (optional, for reference)

### 2. Set Up Configuration

1. Copy `.env.template` to `.env`:
   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file with your credentials:
   ```
   NEAT_ORG_ID=your_organization_id_here
   NEAT_BEARER_TOKEN=your_bearer_token_here
   ```

### 3. Run the Tool

Simply double-click the `pulse_create_rooms_csv` file in Finder, or run it from Terminal:

```bash
./pulse_create_rooms_csv
```

**Note:** On first run, macOS may block the app because it's from an "unidentified developer." To allow it:

1. Right-click (or Control-click) the `pulse_create_rooms_csv` file
2. Select "Open" from the menu
3. Click "Open" in the security dialog
4. Alternatively, go to System Settings → Privacy & Security and click "Open Anyway"

After the first run, you can double-click normally.

## Features

The tool provides the following options:

1. **List regions** - View all regions in your Pulse tenant
2. **Create region** - Create a new region
3. **List locations** - View all locations in your Pulse tenant
4. **Create location** - Create a new location
5. **Create rooms from CSV** - Bulk create rooms from a CSV file
6. **Exit** - Close the application

## CSV Format for Room Creation

Your CSV file should have the following columns:

```csv
locationId,name
123,Conference Room A
123,Conference Room B
456,Meeting Room 1
```

- `locationId` - The numeric ID of the location (use option 3 to view location IDs)
- `name` - The name of the room

After creating rooms, the tool will automatically add a `DEC` column with the Device Enrollment Code for each room.

## Rate Limiting

The tool automatically handles API rate limiting:
- Limits requests to 10 per second (safely below the API limit of 15/second)
- Automatically retries if rate limits are exceeded
- Shows progress indicators for bulk operations

## System Requirements

- macOS 11.0 (Big Sur) or later
- Apple Silicon (M1/M2/M3) or Intel Mac
- No Python installation required
- No dependencies required

## Troubleshooting

### "Cannot be opened because the developer cannot be verified"

This is a standard macOS security feature. Follow the steps in the "Run the Tool" section above.

### "Permission denied" error

Make the file executable:
```bash
chmod +x pulse_create_rooms_csv
```

### ".env file not found" error

Make sure you've created a `.env` file (not `.env.template`) in the same directory as the executable.

### "Unauthorized" or "Organization not found" errors

Double-check your credentials in the `.env` file.

## Support

For issues or questions, please contact your Neat representative or visit the Neat Community forums.

## Building from Source

If you need to rebuild the executable:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Install PyInstaller: `pip install pyinstaller`
4. Build: `pyinstaller --clean neat_pulse_tool.spec`
5. Find the executable in `dist/pulse_create_rooms_csv`
