from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")


def main():
    csv_files = list(RAW_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found in data/raw.")
        return

    for file in csv_files:
        print("\n" + "=" * 80)
        print(f"FILE: {file.name}")
        print("=" * 80)

        try:
            df = pd.read_csv(file, nrows=5)
            print(f"Columns ({len(df.columns)}):")
            for col in df.columns:
                print(f"  - {col}")

            print("\nPreview:")
            print(df.head())

        except Exception as e:
            print(f"Could not read {file.name}: {e}")


if __name__ == "__main__":
    main()