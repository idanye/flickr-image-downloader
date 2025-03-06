import csv
import os


def read_csv(csv_filepath):
    if not os.path.exists(csv_filepath):
        print(f"Error: CSV file '{csv_filepath}' not found.")
        return []

    with open(csv_filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        keywords = [row[0].strip() for row in reader if row and row[0].strip()]

    return keywords if keywords else print("Warning: CSV file is empty.") or []
