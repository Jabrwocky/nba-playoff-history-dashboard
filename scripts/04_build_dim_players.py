from pathlib import Path

import pandas as pd


# Define input and output folders for the dashboard data pipeline.
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

# Create the processed data folder if it does not already exist.
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_column_names(df):
    """
    Convert DataFrame column names to lowercase snake_case.
    """
    df = df.copy()

    # Standardize column names for consistent renaming and selection.
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    return df


def main():
    """Clean the raw players table and save a player dimension table."""

    # Identify the raw players file.
    players_file = RAW_DIR / "Players.csv"

    print("Loading players table...")
    df = pd.read_csv(players_file)

    print(f"Original shape: {df.shape}")

    # Standardize column names before renaming or selecting variables.
    df = clean_column_names(df)

    # Map raw player columns to clearer analysis-friendly names.
    rename_dict = {
        "personid": "player_id",
        "firstname": "first_name",
        "lastname": "last_name",
        "birthdate": "birth_date",
        "heightinches": "height_inches",
        "bodyweightlbs": "weight_lbs",
        "draftyear": "draft_year",
        "draftround": "draft_round",
        "draftnumber": "draft_number",
        "fromyear": "from_year",
        "toyear": "to_year"
    }

    df = df.rename(columns=rename_dict)

    # Combine first and last name fields into one player display name.
    df["player_name"] = (
        df["first_name"].fillna("")
        + " "
        + df["last_name"].fillna("")
    ).str.strip()

    # Convert birth dates to datetime format.
    df["birth_date"] = pd.to_datetime(
        df["birth_date"],
        errors="coerce"
    )

    # Build a compact position label from the guard/forward/center flags.
    df["position"] = ""

    df.loc[df["guard"] == 1, "position"] += "G"
    df.loc[df["forward"] == 1, "position"] += "F"
    df.loc[df["center"] == 1, "position"] += "C"

    # Keep only the fields needed for the player dimension table.
    final_columns = [
        "player_id",
        "player_name",
        "first_name",
        "last_name",
        "birth_date",
        "school",
        "country",
        "height_inches",
        "weight_lbs",
        "position",
        "draft_year",
        "draft_round",
        "draft_number",
        "from_year",
        "to_year"
    ]

    df = df[final_columns]

    # Ensure each player appears only once in the dimension table.
    df = df.drop_duplicates(subset="player_id")

    # Sort players alphabetically for easier inspection.
    df = df.sort_values(by="player_name")

    # Define the cleaned output file path.
    output_file = (
        PROCESSED_DIR /
        "dim_players.csv"
    )

    # Save the cleaned player dimension table for dashboard joins.
    df.to_csv(output_file, index=False)

    print(f"\nSaved player dimension table:")
    print(output_file)

    print("\nFinal preview:")
    print(df.head())


# Run the cleaning script only when this file is executed directly.
if __name__ == "__main__":
    main()
