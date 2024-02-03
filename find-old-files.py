import os
import time
from prettytable import PrettyTable
from datetime import datetime

def find_old_files(folder_path, years):
    """Find files older than a specified number of years in the given folder."""
    target_time = time.time() - (years * 365 * 24 * 60 * 60)  # Convert years to seconds
    old_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getmtime(file_path) < target_time:
                old_files.append(file_path)

    # Sort files by age, oldest first
    old_files.sort(key=os.path.getmtime)
    return old_files

def delete_file(file_path):
    """Delete a file and handle errors."""
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except OSError as e:
        print(f"Error: {e.strerror} - {file_path}")

def display_old_files(old_files):
    """Display old files in a table format."""
    table = PrettyTable()
    table.field_names = ["Index", "File", "Last Modified"]
    for index, file_path in enumerate(old_files, start=1):
        last_modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        table.add_row([index, file_path, last_modified])
    print(table)

def manage_old_files(old_files):
    """Let the user manage old files after displaying them."""
    for i, file_path in enumerate(old_files, start=1):
        print(f"\nManage File {i}:")
        last_modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        print(f"File: {file_path}\nLast Modified: {last_modified}")
        choice = input("Select action - (D)elete, (S)kip, (E)xit: ").strip().upper()
        if choice == 'D':
            delete_file(file_path)
        elif choice == 'E':
            print("Exiting...")
            break

# Main program flow
folder = input("Enter the path of the folder to check for old files: ")
years = float(input("Enter the number of years to identify old files: "))
old_files = find_old_files(folder, years)

if old_files:
    print(f"Found old files (older than {years} years):")
    display_old_files(old_files)
    manage = input("Do you want to manage these files? (Y/N): ").strip().upper()
    if manage == 'Y':
        manage_old_files(old_files)
    else:
        print("Exiting without managing old files.")
else:
    print("No old files found.")
