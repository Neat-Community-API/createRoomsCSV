# Pulse Create Rooms - CSV - Python Distribution

This is the Python source code version of Pulse Create Rooms - CSV. It requires Python 3.8 or later to be installed on your system.

## What's Included

- `neat_pulse_tool.py` - The main Python script
- `requirements.txt` - Python dependencies
- `.env.template` - Template for configuration file
- `example_rooms.csv` - Example CSV file for creating rooms

## Quick Start

### 1. Prerequisites

- Python 3.8 or later
- pip (Python package installer)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install requests python-dotenv tabulate
```

### 3. Set Up Configuration

1. Copy `.env.template` to `.env`:
   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file with your credentials:
   ```
   NEAT_ORG_ID=your_organization_id_here
   NEAT_BEARER_TOKEN=your_bearer_token_here
   ```

### 4. Run the Tool

```bash
python neat_pulse_tool.py
```

Or make it executable (Mac/Linux):
```bash
chmod +x neat_pulse_tool.py
./neat_pulse_tool.py
```

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

- Python 3.8 or later
- pip package installer
- Internet connection for API access

## Troubleshooting

### "ModuleNotFoundError" errors

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### ".env file not found" error

Make sure you've created a `.env` file (not `.env.template`) in the same directory as the script.

### "Unauthorized" or "Organization not found" errors

Double-check your credentials in the `.env` file.

## Support

For issues or questions, please contact your Neat representative or visit the Neat Community forums.
