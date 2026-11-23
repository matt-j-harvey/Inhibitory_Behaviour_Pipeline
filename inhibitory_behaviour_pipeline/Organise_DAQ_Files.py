import os
import re
import shutil


def organise_daq_files_by_day(mouse_directory):

    # Match filenames like:
    # 20260601-103142_daq_1.h5
    pattern = re.compile(r"^(\d{8})-\d{6}_daq_\d+\.h5$")

    for filename in os.listdir(mouse_directory):

        match = pattern.match(filename)

        if match is None:
            continue

        # Extract date string
        date_string = match.group(1)

        # Convert YYYYMMDD -> YYYY_MM_DD
        folder_name = (
            f"{date_string[0:4]}_"
            f"{date_string[4:6]}_"
            f"{date_string[6:8]}"
        )

        # Create destination directory
        destination_directory = os.path.join(
            mouse_directory,
            folder_name
        )

        os.makedirs(destination_directory, exist_ok=True)

        # Move file
        source_file = os.path.join(mouse_directory, filename)
        destination_file = os.path.join(destination_directory, filename)

        shutil.move(source_file, destination_file)

        print(f"Moved {filename} -> {folder_name}")


