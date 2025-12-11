#!/bin/bash
# Create distribution packages for all platforms

echo "📦 Creating distribution packages for all platforms..."
echo ""

# ============================================================================
# MAC DISTRIBUTION
# ============================================================================
echo "🍎 Creating Mac distribution..."
MAC_DIR="pulse_create_rooms_csv_mac"
rm -rf "$MAC_DIR"
mkdir -p "$MAC_DIR"

cp dist/pulse_create_rooms_csv "$MAC_DIR/" 2>/dev/null || echo "  ⚠️  Mac executable not found (run: pyinstaller --clean neat_pulse_tool.spec)"
cp env.template "$MAC_DIR/.env.template"
cp example_rooms.csv "$MAC_DIR/"
cp DISTRIBUTION_README.md "$MAC_DIR/README.md"

if [ -f "$MAC_DIR/pulse_create_rooms_csv" ]; then
    chmod +x "$MAC_DIR/pulse_create_rooms_csv"
    MAC_ZIP="pulse_create_rooms_csv_mac_$(date +%Y%m%d).zip"
    zip -q -r "$MAC_ZIP" "$MAC_DIR"
    echo "  ✅ Created: $MAC_ZIP"
else
    echo "  ⚠️  Skipped Mac package (executable not found)"
fi

# ============================================================================
# WINDOWS DISTRIBUTION
# ============================================================================
echo ""
echo "🪟 Creating Windows distribution..."
WIN_DIR="pulse_create_rooms_csv_windows"
rm -rf "$WIN_DIR"
mkdir -p "$WIN_DIR"

# Check for Windows executable (old or new name)
if [ -f "pulse_create_rooms_csv.exe" ]; then
    cp pulse_create_rooms_csv.exe "$WIN_DIR/"
    WIN_EXE_FOUND=true
elif [ -f "neat_pulse_tool.exe" ]; then
    cp neat_pulse_tool.exe "$WIN_DIR/pulse_create_rooms_csv.exe"
    echo "  ℹ️  Renamed neat_pulse_tool.exe to pulse_create_rooms_csv.exe"
    WIN_EXE_FOUND=true
else
    echo "  ⚠️  Windows executable not found"
    WIN_EXE_FOUND=false
fi

cp env.template "$WIN_DIR/.env.template"
cp example_rooms.csv "$WIN_DIR/"

# Create Windows-specific README
cat > "$WIN_DIR/README.md" << 'EOF'
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
EOF

if [ "$WIN_EXE_FOUND" = true ]; then
    WIN_ZIP="pulse_create_rooms_csv_windows_$(date +%Y%m%d).zip"
    zip -q -r "$WIN_ZIP" "$WIN_DIR"
    echo "  ✅ Created: $WIN_ZIP"
else
    echo "  ⚠️  Skipped Windows package (executable not found)"
fi

# ============================================================================
# PYTHON DISTRIBUTION
# ============================================================================
echo ""
echo "🐍 Creating Python distribution..."
PYTHON_DIR="pulse_create_rooms_csv_python"
rm -rf "$PYTHON_DIR"
mkdir -p "$PYTHON_DIR"

cp neat_pulse_tool.py "$PYTHON_DIR/"
cp requirements.txt "$PYTHON_DIR/"
cp env.template "$PYTHON_DIR/.env.template"
cp example_rooms.csv "$PYTHON_DIR/"

# Create Python-specific README
cat > "$PYTHON_DIR/README.md" << 'EOF'
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
EOF

PYTHON_ZIP="pulse_create_rooms_csv_python_$(date +%Y%m%d).zip"
zip -q -r "$PYTHON_ZIP" "$PYTHON_DIR"
echo "  ✅ Created: $PYTHON_ZIP"

# ============================================================================
# SUMMARY
# ============================================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 DISTRIBUTION PACKAGES CREATED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
ls -lh pulse_create_rooms_csv_*_$(date +%Y%m%d).zip 2>/dev/null || echo "No packages created"
echo ""
echo "Distribution folders:"
ls -d pulse_create_rooms_csv_*/ 2>/dev/null || echo "No folders created"
echo ""
echo "✅ Done! Share the appropriate ZIP file with your users."
