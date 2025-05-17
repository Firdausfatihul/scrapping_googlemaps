# file_utils.py

import csv 
import os 
import config

def load_locations_csv(filepath, expected_headers):
    print(
        f"[FileUtil] Attempting to load locations from: {filepath}"
    )

    if not os.path.exists(filepath):
        print(
            f"[FileUtil] File does not exist: {filepath}"
        )
        return []

    locations = []

    try:
        with open(filepath, 'r', newline='') as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print(
                    f"[FileUtil] CSV file is empty: {filepath}"
                )
                return []

            #check apakah ada header yang kosong
            missing_headers = [
                header for header in expected_headers if header not in reader.fieldnames
            ]

            if missing_headers:
                print(
                    f"[FileUtil] Missing headers in CSV file: {missing_headers}"
                )
                print(
                    f"[FileUtil] Actual headers in CSV file: {reader.fieldnames}"
                )
                print(
                    f"[FileUtil] Expected headers in CSV file: {expected_headers}"
                )
                return []
            
            #check each row apakah ada value yang kosong
            for i, row in enumerate(reader):
                location_data = {}
                valid_row = True
                for header_key in expected_headers:
                    cell_value = row.get(header_key)
                    if cell_value is None or cell_value.strip() == "":
                        print(
                            f"[FileUtil] Empty cell in CSV file at row {i+1}, column {header_key}, in filepath {filepath}"
                        )
                        valid_row = False
                        break
                    location_data[header_key] = cell_value

                if valid_row:
                    locations.append(location_data)

        print(
            f"[FileUtil] Successfully loaded {len(locations)} locations from: {filepath}"
        )

        return locations
    except Exception as e:
        print(
            f"[FileUtil] Error loading locations from {filepath}: {e}"
        )
        return []

def save_results_to_csv(data_list_of_dicts, filepath, output_headers):
    print(
        f"[FileUtil] Attempting to save {len(data_list_of_dicts)} results to: {filepath}"
    )

    if not data_list_of_dicts:
        print(
            f"[FileUtil] No data to save to: {filepath}"
        )
        return True 

    try:
        with open(filepath, 'w', newline='') as file:
            writer = csv.DictWriter(
                file,
                fieldnames=output_headers,
                extrasaction='ignore'
            )
            writer.writeheader()
            for data in data_list_of_dicts:
                writer.writerow(data)

        print(
            f"[FileUtil] Successfully saved {len(data_list_of_dicts)} results to: {filepath}"
        )
        return True
    except Exception as e:
        print(
            f"[FileUtil] Error saving results to {filepath}: {e}"
        )
        return False
        