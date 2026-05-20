from pathlib import Path

import pandas as pd


# Folder where the raw NBA playoff dashboard CSV files are stored.
RAW_DIR = Path("data/raw")


def main():
    """Print column names and a small preview for each raw CSV file."""

    # Collect all CSV files in the raw data folder.
    csv_files = list(RAW_DIR.glob("*.csv"))

    # Stop the script early if no raw CSV files are available.
    if not csv_files:
        print("No CSV files found in data/raw.")
        return

    # Loop through each CSV file and inspect its structure.
    for file in csv_files:
        print("\n" + "=" * 80)
        print(f"FILE: {file.name}")
        print("=" * 80)

        try:
            # Read only the first five rows to quickly inspect the file
            # without loading the full dataset into memory.
            df = pd.read_csv(file, nrows=5)

            # Print the number of columns and each column name.
            print(f"Columns ({len(df.columns)}):")
            for col in df.columns:
                print(f"  - {col}")

            # Print a small preview of the dataset.
            print("\nPreview:")
            print(df.head())

        except Exception as e:
            # Continue checking other files even if one file cannot be read.
            print(f"Could not read {file.name}: {e}")


# Run main() only when this script is executed directly.
if __name__ == "__main__":
    main()
