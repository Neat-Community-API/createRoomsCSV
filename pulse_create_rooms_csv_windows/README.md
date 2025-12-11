# Pulse Create Rooms - CSV - Windows Executable Distribution

This is a standalone executable version of Pulse Create Rooms - CSV for Windows. It does **not** require Python, virtual environments, or any dependencies to be installed on the user's machine.

## What's Included

- `pulse_create_rooms_csv.exe` - The standalone executable for Windows
- `.env.template` - Template for configuration file
- `example_rooms.csv` - Example CSV file for creating rooms

## Quick Start

### 1. Download the Files

Download all files to a folder on your Windows PC.

### 2. Set Up Configuration

1. Copy `.env.template` to `.env`
2. Edit the `.env` file with your credentials:
   ```
   NEAT_ORG_ID=your_organization_id_here
   NEAT_BEARER_TOKEN=your_bearer_token_here
   ```

### 3. Run the Tool

Double-click `pulse_create_rooms_csv.exe` or run from Command Prompt:

```cmd
pulse_create_rooms_csv.exe
```

**Note:** Windows Defender SmartScreen may show a warning on first run. Click "More info" then "Run anyway" to proceed.

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

- Windows 10 or later
- No Python installation required
- No dependencies required

## Troubleshooting

### ".env file not found" error

Make sure you've created a `.env` file (not `.env.template`) in the same directory as the executable.

### "Unauthorized" or "Organization not found" errors

Double-check your credentials in the `.env` file.

### Windows Defender blocks the executable

This is normal for unsigned executables. Click "More info" then "Run anyway".

## Support

For issues or questions, please contact your Neat representative or visit the Neat Community forums.
