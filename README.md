# Neat Pulse API Tool

A Python command-line tool for interacting with the Neat Pulse API. This tool allows you to manage regions, locations, and rooms in your Neat Pulse tenant with an easy-to-use interactive menu.

## Features

- **List Regions**: Retrieve and display all regions in your Neat Pulse organization
- **Create Region**: Create a new region by entering a region name
- **List Locations**: Retrieve and display all locations in your Neat Pulse organization
- **Create Location**: Create a new location by entering a region ID and location name
- **Create Rooms from CSV**: Bulk create rooms from a CSV file and automatically update the CSV with DEC values returned by the API

## Prerequisites

- Python 3.7 or higher
- A Neat Pulse account with API access
- Organization ID and AKI Key with Read and Write permissions from Neat Pulse

## Installation

1. **Clone or download this repository** to your local machine

2. **Create a virtual environment** (recommended):

   **On macOS/Linux**:
   ```bash
   python3 -m venv venv
   ```

   **On Windows**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   **On macOS/Linux**:
   ```bash
   source venv/bin/activate
   ```

   **On Windows (Command Prompt)**:
   ```bash
   venv\Scripts\activate.bat
   ```

   **On Windows (PowerShell)**:
   ```bash
   venv\Scripts\Activate.ps1
   ```

   You should see `(venv)` appear at the beginning of your command prompt.

4. **Install required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure your credentials**:
   - Copy `.env.template` to `.env`:
     ```bash
     cp .env.template .env
     ```
   - Edit `.env` and add your credentials:
     ```
     NEAT_ORG_ID=your_actual_organization_id
     NEAT_BEARER_TOKEN=your_actual_bearer_token
     ```

## Usage

### Running the Tool

Make sure your virtual environment is activated (you should see `(venv)` in your prompt), then start the tool:

```bash
python neat_pulse_tool.py
```

**Note**: If your virtual environment is not activated, run the activation command from the Installation section first.

You'll see an interactive menu with the following options:

```
NEAT PULSE API TOOL
================================================================================

Options:
  1. List regions
  2. Create region
  3. List locations
  4. Create location
  5. Create rooms from CSV
  6. Exit
```

### Option 1: List Regions

This option retrieves all regions in your Neat Pulse organization and displays them in a formatted table.

**Example output**:
```
+------------+-------------------+
| ID         | Name              |
+============+===================+
| 11         | North America     |
| 12         | Europe            |
+------------+-------------------+

Total regions: 2
```

### Option 2: Create Region

This option allows you to create a new region.

**Steps**:
1. Select option 2 from the menu
2. Enter the region name when prompted
3. The tool will create the region and display the generated Region ID

**Example**:
```
CREATE REGION
================================================================================

Enter region name: Asia Pacific

Creating region 'Asia Pacific'...

✓ Success! Region created:
  - Region ID: 13
  - Name: Asia Pacific
```

### Option 3: List Locations

This option retrieves all locations in your Neat Pulse organization and displays them in a formatted table, including the region each location belongs to.

**Example output**:
```
+------------+-------------------+-------------------+
| ID         | Name              | Region            |
+============+===================+===================+
| 123        | Main Office       | North America     |
| 456        | Branch Office     | Europe            |
+------------+-------------------+-------------------+

Total locations: 2
```

### Option 4: Create Location

This option allows you to create a new location within a specific region.

**Steps**:
1. Select option 4 from the menu
2. Enter the region ID when prompted
3. Enter the location name when prompted
4. The tool will create the location and display the generated Location ID

**Example**:
```
CREATE LOCATION
================================================================================

Enter region ID: 11
Enter location name: San Francisco Office

Creating location 'San Francisco Office' in region '11'...

✓ Success! Location created:
  - Location ID: 789
  - Name: San Francisco Office
  - Region ID: 11
```

**Tip**: Use option 1 (List Regions) first to get the Region IDs you need.

### Option 5: Create Rooms from CSV

This option allows you to bulk create rooms from a CSV file.

**Steps**:
1. Select option 2 from the menu
2. Choose a CSV file from the list of available files, or enter a custom filename
3. The tool will create each room and display progress
4. The CSV file will be automatically updated with DEC values

**Progress output**:
```
Found 3 rooms to create.
Creating rooms...

[1/3] Creating room: Conference Room A (Location: 123) ✓ Success (DEC: ABC123)
[2/3] Creating room: Conference Room B (Location: 123) ✓ Success (DEC: DEF456)
[3/3] Creating room: Meeting Room 1 (Location: 456) ✓ Success (DEC: GHI789)

================================================================================
SUMMARY
================================================================================
Successfully created: 3
Failed: 0
Total: 3

CSV file 'example_rooms.csv' has been updated with DEC values.
```

## CSV File Format

### Input Format

Your CSV file must contain the following columns:

- **locationId**: The numeric ID of the location where the room will be created (required, must be a number)
- **name**: The name of the room (required)

**Example** (`example_rooms.csv`):
```csv
locationId,name
123,Conference Room A
123,Conference Room B
456,Meeting Room 1
```

**Important**: Location IDs must be numeric values. Use Option 3 (List Locations) to find the numeric IDs for your locations.

### Output Format

After running the tool, a **DEC** column will be added to your CSV with values returned by the API:

```csv
locationId,name,DEC
123,Conference Room A,ABC123
123,Conference Room B,DEF456
456,Meeting Room 1,GHI789
```

**Note**: The DEC (Device Enrollment Code) is generated by the Neat Pulse API when each room is created and is used for device pairing.

## API Endpoints

This tool uses the following Neat Pulse API endpoints:

- **List Regions**: `GET https://api.pulse.neat.no/v1/orgs/{orgID}/regions`
- **Create Region**: `POST https://api.pulse.neat.no/v1/orgs/{orgID}/regions`
- **List Locations**: `GET https://api.pulse.neat.no/v1/orgs/{orgID}/locations`
- **Create Location**: `POST https://api.pulse.neat.no/v1/orgs/{orgID}/locations`
- **Create Room**: `POST https://api.pulse.neat.no/v1/orgs/{orgID}/rooms`

## Error Handling

The tool includes comprehensive error handling for common issues:

### Configuration Errors
- **Missing .env file**: The tool will prompt you to create one from `.env.template`
- **Invalid credentials**: Check that your Organization ID and Bearer Token are correct
- **Placeholder values**: Ensure you've replaced the template values with actual credentials

### CSV File Errors
- **File not found**: Verify the CSV file exists in the current directory
- **Missing columns**: Ensure your CSV has both `locationId` and `name` columns
- **Empty file**: The CSV must contain at least one data row

### API Errors
- **401 Unauthorized**: Your bearer token is invalid or expired
- **404 Not Found**: Your organization ID is incorrect
- **Network errors**: Check your internet connection
- **Timeout errors**: The API request took too long (30 second timeout)

## Troubleshooting

### Problem: "Error: .env file not found!"
**Solution**: Copy `.env.template` to `.env` and add your credentials

### Problem: "Error: Unauthorized"
**Solution**: Verify your bearer token in the `.env` file is correct and not expired

### Problem: "Error: Organization not found"
**Solution**: Check that your `NEAT_ORG_ID` in the `.env` file is correct

### Problem: CSV file missing required columns
**Solution**: Ensure your CSV has headers `locationId` and `name` (case-sensitive)

### Problem: No CSV files found
**Solution**: Make sure your CSV file is in the same directory as the script

### Problem: "Operation preconditions not met" when creating rooms
**Solution**:
- This usually means the location ID in your CSV doesn't exist
- Use option 3 (List Locations) to verify the location ID exists
- Make sure you're using the correct numeric location ID from your organization
- Ensure the location is properly configured in Neat Pulse

## Example Workflow

### Complete Setup: Region → Location → Rooms

1. **Activate your virtual environment**:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate.bat  # On Windows
   ```

2. **Create a region** (if needed):
   ```bash
   python neat_pulse_tool.py
   # Select option 2 (Create region)
   # Enter region name: "North America"
   # Note down the generated Region ID (e.g., 11)
   ```

3. **List existing regions** (optional):
   ```bash
   python neat_pulse_tool.py
   # Select option 1 (List regions)
   # View all regions and their IDs
   ```

4. **Create a location**:
   ```bash
   python neat_pulse_tool.py
   # Select option 4 (Create location)
   # Enter region ID: 11
   # Enter location name: "New York Office"
   # Note down the generated Location ID (e.g., 456)
   ```

5. **List your locations** (optional):
   ```bash
   python neat_pulse_tool.py
   # Select option 3 (List locations)
   # Verify your location was created
   ```

6. **Create your CSV file**:
   ```csv
   locationId,name
   456,Conference Room A
   456,Conference Room B
   456,Meeting Room 1
   ```

7. **Create the rooms**:
   ```bash
   python neat_pulse_tool.py
   # Select option 5 (Create rooms from CSV)
   # Choose your CSV file
   # Rooms will be created and CSV updated with DEC values
   ```

8. **Verify the results**:
   - Check the console output for success/failure messages
   - Open your updated CSV file to see the DEC values

9. **Deactivate the virtual environment** (when finished):
   ```bash
   deactivate
   ```

## Files Included

- `neat_pulse_tool.py`: Main Python script
- `requirements.txt`: Python package dependencies
- `.env.template`: Template for environment variables
- `example_rooms.csv`: Example CSV file with sample data
- `README.md`: This documentation file

## Security Notes

- Keep your `.env` file secure and never commit it to version control
- Add `.env` and `venv/` to your `.gitignore` file if using Git
- Your bearer token provides full API access - treat it like a password

## Support

For issues with the Neat Pulse API or to obtain your Organization ID and Bearer Token, please contact Neat Pulse support.

## License

This tool is provided as-is for use with the Neat Pulse API.
