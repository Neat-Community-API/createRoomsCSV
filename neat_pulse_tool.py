#!/usr/bin/env python3
"""
Neat Pulse API Tool
A command-line tool for interacting with the Neat Pulse API.
"""

import os
import sys
import csv
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from dotenv import load_dotenv
from tabulate import tabulate


BASE_URL = "https://api.pulse.neat.no"


class RateLimiter:
    """
    Rate limiter to prevent exceeding API rate limits.
    
    The Pulse API has a rate limit of 15 requests/second per integration token.
    This class enforces a configurable rate (default: 10 req/s) to stay safely
    below the limit.
    """
    
    def __init__(self, requests_per_second: float = 10.0):
        """
        Initialize the rate limiter.
        
        Args:
            requests_per_second: Maximum number of requests per second (default: 10)
        """
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second  # Minimum seconds between requests
        self.last_request_time = 0.0
    
    def wait_if_needed(self) -> None:
        """
        Wait if necessary to maintain the rate limit.
        This should be called before making each API request.
        """
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_interval:
            sleep_time = self.min_interval - time_since_last_request
            time.sleep(sleep_time)
    
    def record_request(self) -> None:
        """
        Record that a request was made.
        This should be called after making each API request.
        """
        self.last_request_time = time.time()


def load_config() -> Tuple[str, str]:
    """
    Load configuration from .env file.

    Returns:
        Tuple of (org_id, bearer_token)

    Raises:
        SystemExit: If .env file doesn't exist or required variables are missing
    """
    env_path = Path(".env")

    if not env_path.exists():
        print("Error: .env file not found!")
        print("Please copy .env.template to .env and fill in your credentials.")
        sys.exit(1)

    load_dotenv()

    org_id = os.getenv("NEAT_ORG_ID")
    bearer_token = os.getenv("NEAT_BEARER_TOKEN")

    if not org_id or not bearer_token:
        print("Error: Missing required environment variables!")
        print("Please ensure NEAT_ORG_ID and NEAT_BEARER_TOKEN are set in your .env file.")
        sys.exit(1)

    if org_id == "your_organization_id_here" or bearer_token == "your_bearer_token_here":
        print("Error: Please update the .env file with your actual credentials.")
        sys.exit(1)

    return org_id, bearer_token


def get_headers(token: str) -> Dict[str, str]:
    """
    Generate request headers with authentication.

    Args:
        token: Bearer token for authentication

    Returns:
        Dictionary of HTTP headers
    """
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def list_locations(org_id: str, token: str) -> None:
    """
    List all locations in the Neat Pulse tenant.

    Args:
        org_id: Organization ID
        token: Bearer token for authentication
    """
    url = f"{BASE_URL}/v1/orgs/{org_id}/locations"
    headers = get_headers(token)

    print("\nFetching locations...")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Handle different response structures
        # The API might return locations directly or wrapped in an object
        if isinstance(data, dict):
            # Check if locations are in a 'locations' key
            if 'locations' in data:
                locations = data['locations']
            elif 'data' in data:
                locations = data['data']
            else:
                # Treat the dict itself as a single location
                locations = [data]
        elif isinstance(data, list):
            locations = data
        else:
            print(f"\nError: Unexpected response format. Response type: {type(data)}")
            print(f"Response content: {data}")
            return

        if not locations:
            print("\nNo locations found.")
            return

        # Prepare data for table display
        table_data = []
        for loc in locations:
            if isinstance(loc, dict):
                # Get region information - could be regionId, region.id, or region.name
                region_info = "N/A"
                if "regionId" in loc:
                    region_info = loc.get("regionId", "N/A")
                elif "region" in loc:
                    region = loc.get("region")
                    if isinstance(region, dict):
                        # If region is an object, try to get name first, then id
                        region_info = region.get("name", region.get("id", "N/A"))
                    else:
                        region_info = str(region)

                table_data.append([
                    loc.get("id", "N/A"),
                    loc.get("name", "N/A"),
                    region_info
                ])
            else:
                print(f"\nWarning: Unexpected location format: {loc}")

        if not table_data:
            print("\nNo valid location data found.")
            return

        # Sort by ID (ascending order)
        table_data.sort(key=lambda x: int(x[0]) if str(x[0]).isdigit() else 0)

        # Display as formatted table
        print("\n" + "="*80)
        print("LOCATIONS")
        print("="*80)
        print(tabulate(
            table_data,
            headers=["ID", "Name", "Region"],
            tablefmt="grid"
        ))
        print(f"\nTotal locations: {len(table_data)}")

    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please check your network connection.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Neat Pulse API. Please check your network.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Error: Unauthorized. Please check your bearer token.")
        elif e.response.status_code == 404:
            print("Error: Organization not found. Please check your organization ID.")
        else:
            print(f"Error: HTTP {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("\nDebug information:")
        traceback.print_exc()


def list_regions(org_id: str, token: str) -> None:
    """
    List all regions in the Neat Pulse tenant.

    Args:
        org_id: Organization ID
        token: Bearer token for authentication
    """
    url = f"{BASE_URL}/v1/orgs/{org_id}/regions"
    headers = get_headers(token)

    print("\nFetching regions...")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        # Handle different response structures
        if isinstance(data, dict):
            if 'regions' in data:
                regions = data['regions']
            elif 'data' in data:
                regions = data['data']
            else:
                regions = [data]
        elif isinstance(data, list):
            regions = data
        else:
            print(f"\nError: Unexpected response format. Response type: {type(data)}")
            print(f"Response content: {data}")
            return

        if not regions:
            print("\nNo regions found.")
            return

        # Prepare data for table display
        table_data = []
        for region in regions:
            if isinstance(region, dict):
                table_data.append([
                    region.get("id", "N/A"),
                    region.get("name", "N/A")
                ])
            else:
                print(f"\nWarning: Unexpected region format: {region}")

        if not table_data:
            print("\nNo valid region data found.")
            return

        # Sort by ID (ascending order)
        table_data.sort(key=lambda x: int(x[0]) if str(x[0]).isdigit() else 0)

        # Display as formatted table
        print("\n" + "="*80)
        print("REGIONS")
        print("="*80)
        print(tabulate(
            table_data,
            headers=["ID", "Name"],
            tablefmt="grid"
        ))
        print(f"\nTotal regions: {len(table_data)}")

    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please check your network connection.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Neat Pulse API. Please check your network.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Error: Unauthorized. Please check your bearer token.")
        elif e.response.status_code == 404:
            print("Error: Organization not found. Please check your organization ID.")
        else:
            print(f"Error: HTTP {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("\nDebug information:")
        traceback.print_exc()


def create_region(org_id: str, token: str) -> None:
    """
    Create a new region in the Neat Pulse tenant.

    Args:
        org_id: Organization ID
        token: Bearer token for authentication
    """
    print("\n" + "="*80)
    print("CREATE REGION")
    print("="*80)

    region_name = input("\nEnter region name: ").strip()

    if not region_name:
        print("Error: Region name cannot be empty.")
        return

    url = f"{BASE_URL}/v1/orgs/{org_id}/regions"
    headers = get_headers(token)
    payload = {"name": region_name}

    print(f"\nCreating region '{region_name}'...")

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        region_id = result.get("id", "N/A")

        print(f"\n✓ Success! Region created:")
        print(f"  - Region ID: {region_id}")
        print(f"  - Name: {region_name}")

    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please check your network connection.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Neat Pulse API. Please check your network.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Error: Unauthorized. Please check your bearer token.")
        elif e.response.status_code == 404:
            print("Error: Organization not found. Please check your organization ID.")
        else:
            print(f"Error: HTTP {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")


def create_location(org_id: str, token: str) -> None:
    """
    Create a new location in the Neat Pulse tenant.

    Args:
        org_id: Organization ID
        token: Bearer token for authentication
    """
    print("\n" + "="*80)
    print("CREATE LOCATION")
    print("="*80)

    region_id_input = input("\nEnter region ID: ").strip()

    if not region_id_input:
        print("Error: Region ID cannot be empty.")
        return

    # Validate and convert region ID to integer
    try:
        region_id = int(region_id_input)
    except ValueError:
        print(f"Error: Region ID must be a number. You entered: '{region_id_input}'")
        return

    location_name = input("Enter location name: ").strip()

    if not location_name:
        print("Error: Location name cannot be empty.")
        return

    url = f"{BASE_URL}/v1/orgs/{org_id}/locations"
    headers = get_headers(token)
    payload = {
        "name": location_name,
        "regionId": region_id
    }

    print(f"\nCreating location '{location_name}' in region '{region_id}'...")

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        location_id = result.get("id", "N/A")

        print(f"\n✓ Success! Location created:")
        print(f"  - Location ID: {location_id}")
        print(f"  - Name: {location_name}")
        print(f"  - Region ID: {region_id}")

    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please check your network connection.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Neat Pulse API. Please check your network.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Error: Unauthorized. Please check your bearer token.")
        elif e.response.status_code == 404:
            print("Error: Organization not found. Please check your organization ID.")
        elif e.response.status_code == 400:
            print(f"Error: Bad request - {e.response.text}")
            print("Please verify the region ID is correct.")
        else:
            print(f"Error: HTTP {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")


def read_csv_file(csv_filename: str) -> Optional[List[Dict[str, str]]]:
    """
    Read CSV file and validate required columns.

    Args:
        csv_filename: Name of the CSV file

    Returns:
        List of dictionaries with room data, or None if error
    """
    csv_path = Path(csv_filename)

    if not csv_path.exists():
        print(f"Error: File '{csv_filename}' not found in the current directory.")
        return None

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Validate required columns
            if not reader.fieldnames:
                print("Error: CSV file is empty or malformed.")
                return None

            required_columns = {"locationId", "name"}
            missing_columns = required_columns - set(reader.fieldnames)

            if missing_columns:
                print(f"Error: CSV is missing required columns: {', '.join(missing_columns)}")
                print(f"Required columns: locationId, name")
                return None

            rooms = list(reader)

            if not rooms:
                print("Error: CSV file contains no data rows.")
                return None

            return rooms

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None


def create_room(org_id: str, token: str, location_id: str, name: str) -> Optional[Dict]:
    """
    Create a single room via the Neat Pulse API.

    Args:
        org_id: Organization ID
        token: Bearer token
        location_id: Location ID for the room (will be converted to integer)
        name: Name of the room

    Returns:
        API response dictionary if successful, None otherwise
    """
    url = f"{BASE_URL}/v1/orgs/{org_id}/rooms"
    headers = get_headers(token)

    # Convert location_id to integer as required by the API
    try:
        location_id_int = int(location_id)
    except (ValueError, TypeError):
        print(f"  Failed: Invalid location ID '{location_id}' - must be a number")
        return None

    payload = {
        "locationId": location_id_int,
        "name": name
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        error_msg = f"  Failed: HTTP {e.response.status_code} - {e.response.text}"
        print(error_msg)

        # Provide helpful hints for common errors
        if e.response.status_code == 400:
            try:
                error_data = e.response.json()
                if "preconditions not met" in error_data.get("message", "").lower():
                    print(f"  Hint: Location ID {location_id_int} may not exist. Use option 3 to verify location IDs.")
            except:
                pass

        return None
    except Exception as e:
        print(f"  Failed: {e}")
        return None


def create_room_with_retry(
    org_id: str, 
    token: str, 
    location_id: str, 
    name: str,
    rate_limiter: Optional[RateLimiter] = None,
    max_retries: int = 3
) -> Optional[Dict]:
    """
    Create a room with automatic retry logic for rate limit errors.
    
    This function wraps create_room() and adds:
    - Rate limiting to prevent hitting API limits
    - Automatic retry with exponential backoff for HTTP 429 errors
    - Enhanced error messages
    
    Args:
        org_id: Organization ID
        token: Bearer token
        location_id: Location ID for the room
        name: Name of the room
        rate_limiter: Optional RateLimiter instance to enforce rate limits
        max_retries: Maximum number of retry attempts for rate limit errors (default: 3)
    
    Returns:
        API response dictionary if successful, None otherwise
    """
    retry_count = 0
    base_wait_time = 5  # Start with 5 seconds
    
    while retry_count <= max_retries:
        # Apply rate limiting before making the request
        if rate_limiter:
            rate_limiter.wait_if_needed()
        
        # Attempt to create the room
        url = f"{BASE_URL}/v1/orgs/{org_id}/rooms"
        headers = get_headers(token)
        
        # Convert location_id to integer as required by the API
        try:
            location_id_int = int(location_id)
        except (ValueError, TypeError):
            print(f"  Failed: Invalid location ID '{location_id}' - must be a number")
            return None
        
        payload = {
            "locationId": location_id_int,
            "name": name
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            # Record the request for rate limiting
            if rate_limiter:
                rate_limiter.record_request()
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            # Record the request even if it failed
            if rate_limiter:
                rate_limiter.record_request()
            
            # Handle rate limit errors (HTTP 429) with exponential backoff
            if e.response.status_code == 429:
                if retry_count < max_retries:
                    wait_time = base_wait_time * (2 ** retry_count)  # Exponential backoff: 5s, 10s, 20s, 40s
                    print(f"  Rate limit exceeded (429). Waiting {wait_time}s before retry {retry_count + 1}/{max_retries}...")
                    time.sleep(wait_time)
                    retry_count += 1
                    continue  # Retry the request
                else:
                    print(f"  Failed: Rate limit exceeded after {max_retries} retries")
                    return None
            
            # Handle other HTTP errors
            error_msg = f"  Failed: HTTP {e.response.status_code} - {e.response.text}"
            print(error_msg)
            
            # Provide helpful hints for common errors
            if e.response.status_code == 400:
                try:
                    error_data = e.response.json()
                    if "preconditions not met" in error_data.get("message", "").lower():
                        print(f"  Hint: Location ID {location_id_int} may not exist. Use option 3 to verify location IDs.")
                except:
                    pass
            
            return None
        
        except Exception as e:
            # Record the request even if it failed
            if rate_limiter:
                rate_limiter.record_request()
            
            print(f"  Failed: {e}")
            return None
    
    return None


def create_rooms_from_csv(org_id: str, token: str, csv_filename: str) -> None:
    """
    Create rooms from CSV file and update CSV with DEC values.

    Args:
        org_id: Organization ID
        token: Bearer token
        csv_filename: Name of the CSV file
    """
    # Read CSV file
    rooms_data = read_csv_file(csv_filename)
    if not rooms_data:
        return

    print(f"\nFound {len(rooms_data)} rooms to create.")
    print("Creating rooms with rate limiting (10 requests/second)...\n")

    # Initialize rate limiter (10 requests/second to stay safely below 15 req/s limit)
    rate_limiter = RateLimiter(requests_per_second=10.0)

    results = []
    success_count = 0
    failure_count = 0
    skipped_count = 0
    
    # Track progress timing
    start_time = time.time()

    # Create each room
    for idx, room in enumerate(rooms_data, 1):
        location_id = room.get("locationId", "").strip()
        name = room.get("name", "").strip()
        existing_dec = room.get("DEC", "").strip()

        if not location_id or not name:
            print(f"[{idx}/{len(rooms_data)}] Skipping row with missing data")
            results.append({"success": False, "dec": None})
            failure_count += 1
            continue
        
        # Skip if room already has a DEC value
        if existing_dec:
            print(f"[{idx}/{len(rooms_data)}] Skipping room: {name} (already exists with DEC: {existing_dec})")
            results.append({"success": True, "dec": existing_dec})
            skipped_count += 1
            success_count += 1  # Count as success since room exists
            continue

        print(f"[{idx}/{len(rooms_data)}] Creating room: {name} (Location: {location_id})")

        # Use the new create_room_with_retry function with rate limiting
        response = create_room_with_retry(org_id, token, location_id, name, rate_limiter=rate_limiter)

        if response:
            dec = response.get("dec", "")
            if not dec:
                print(f"  ✓ Success (WARNING: No DEC in response)")
                print(f"  API Response keys: {list(response.keys())}")
            else:
                print(f"  ✓ Success (DEC: {dec})")
            results.append({"success": True, "dec": dec})
            success_count += 1
        else:
            results.append({"success": False, "dec": None})
            failure_count += 1
        
        # Display progress indicators after each room
        elapsed_time = time.time() - start_time
        rooms_processed = idx
        
        # Calculate rate and ETA
        if elapsed_time > 0:
            rate_per_minute = (rooms_processed / elapsed_time) * 60
            remaining_rooms = len(rooms_data) - rooms_processed
            
            if rate_per_minute > 0:
                eta_seconds = (remaining_rooms / rate_per_minute) * 60
                eta_minutes = int(eta_seconds // 60)
                eta_secs = int(eta_seconds % 60)
                
                # Format ETA
                if eta_minutes > 0:
                    eta_str = f"{eta_minutes}m {eta_secs}s"
                else:
                    eta_str = f"{eta_secs}s"
            else:
                eta_str = "calculating..."
        else:
            rate_per_minute = 0
            eta_str = "calculating..."
        
        # Calculate percentage
        percentage = (rooms_processed / len(rooms_data)) * 100
        
        # Display progress line
        print(f"  Progress: {rooms_processed}/{len(rooms_data)} ({percentage:.1f}%) | "
              f"Elapsed: {int(elapsed_time)}s | "
              f"ETA: {eta_str}")


    # Update CSV with DEC values
    if success_count > 0:
        update_csv_with_dec(csv_filename, rooms_data, results)

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    newly_created = success_count - skipped_count
    print(f"Newly created: {newly_created}")
    print(f"Skipped (already existed): {skipped_count}")
    print(f"Failed: {failure_count}")
    print(f"Total: {len(rooms_data)}")

    if success_count > 0:
        print(f"\nCSV file '{csv_filename}' has been updated with DEC values.")


def update_csv_with_dec(csv_filename: str, rooms_data: List[Dict], results: List[Dict]) -> None:
    """
    Update CSV file to add DEC column with values from API responses.

    Args:
        csv_filename: Name of the CSV file
        rooms_data: Original room data from CSV
        results: List of results with DEC values
    """
    csv_path = Path(csv_filename)

    print(f"\nUpdating CSV file '{csv_filename}' with DEC values...")

    try:
        # Read original fieldnames
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames)

        # Add DEC column if not present
        if "DEC" not in fieldnames:
            fieldnames.append("DEC")
            print(f"  Added 'DEC' column to CSV")

        # Prepare updated data
        updated_data = []
        dec_count = 0
        for room, result in zip(rooms_data, results):
            updated_room = room.copy()
            dec_value = result.get("dec", "") if result.get("success") else ""
            updated_room["DEC"] = dec_value
            if dec_value:
                dec_count += 1
            updated_data.append(updated_room)

        print(f"  Prepared {len(updated_data)} rows with {dec_count} DEC values")

        # Write updated CSV
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_data)

        print(f"  Successfully wrote updated CSV to {csv_path.absolute()}")

    except Exception as e:
        print(f"\nWarning: Could not update CSV file: {e}")
        import traceback
        traceback.print_exc()


def list_csv_files() -> List[str]:
    """
    List all CSV files in the current directory.

    Returns:
        List of CSV filenames
    """
    csv_files = [f.name for f in Path(".").glob("*.csv")]
    return sorted(csv_files)


def display_menu() -> str:
    """
    Display interactive menu and get user selection.

    Returns:
        User's menu choice
    """
    print("\n" + "="*80)
    print("NEAT PULSE API TOOL")
    print("="*80)
    print("\nOptions:")
    print("  1. List regions")
    print("  2. Create region")
    print("  3. List locations")
    print("  4. Create location")
    print("  5. Create rooms from CSV")
    print("  6. Exit")
    print()

    while True:
        choice = input("Select an option (1-6): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6"]:
            return choice
        print("Invalid choice. Please enter 1-6.")


def main():
    """Main entry point for the tool."""
    print("="*80)
    print("NEAT PULSE API TOOL")
    print("="*80)

    # Load configuration
    try:
        org_id, token = load_config()
    except SystemExit:
        return

    print(f"Loaded configuration for organization: {org_id}")

    # Main loop
    while True:
        choice = display_menu()

        if choice == "1":
            list_regions(org_id, token)

        elif choice == "2":
            create_region(org_id, token)

        elif choice == "3":
            list_locations(org_id, token)

        elif choice == "4":
            create_location(org_id, token)

        elif choice == "5":
            csv_files = list_csv_files()

            if not csv_files:
                print("\nNo CSV files found in the current directory.")
                continue

            print(f"\nAvailable CSV files:")
            for idx, filename in enumerate(csv_files, 1):
                print(f"  {idx}. {filename}")

            print(f"  {len(csv_files) + 1}. Enter custom filename")
            print(f"  {len(csv_files) + 2}. Cancel")

            while True:
                try:
                    selection = input(f"\nSelect a file (1-{len(csv_files) + 2}): ").strip()
                    selection_num = int(selection)

                    if 1 <= selection_num <= len(csv_files):
                        csv_filename = csv_files[selection_num - 1]
                        break
                    elif selection_num == len(csv_files) + 1:
                        csv_filename = input("Enter CSV filename: ").strip()
                        break
                    elif selection_num == len(csv_files) + 2:
                        csv_filename = None
                        break
                    else:
                        print(f"Invalid selection. Please enter a number between 1 and {len(csv_files) + 2}.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            if csv_filename:
                create_rooms_from_csv(org_id, token, csv_filename)

        elif choice == "6":
            print("\nExiting. Goodbye!")
            break


if __name__ == "__main__":
    main()
