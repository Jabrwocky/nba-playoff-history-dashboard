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
    """Clean raw NBA team history data and save a team dimension table."""

    # Identify the raw team histories file.
    teams_file = RAW_DIR / "TeamHistories.csv"

    print("Loading team histories...")
    df = pd.read_csv(teams_file)

    print(f"Original shape: {df.shape}")

    # Standardize column names before renaming or selecting variables.
    df = clean_column_names(df)

    # Map raw team history columns to clearer analysis-friendly names.
    rename_dict = {
        "teamid": "team_id",
        "teamcity": "team_city",
        "teamname": "team_name",
        "teamabbrev": "team_abbrev",
        "seasonfounded": "season_founded",
        "seasonactivetill": "season_active_till"
    }

    df = df.rename(columns=rename_dict)

    # Combine city and team name into one display-friendly team name.
    df["team_full_name"] = (
        df["team_city"].fillna("")
        + " "
        + df["team_name"].fillna("")
    ).str.strip()

    # Keep only the fields needed for the team dimension table.
    final_columns = [
        "team_id",
        "team_full_name",
        "team_city",
        "team_name",
        "team_abbrev",
        "season_founded",
        "season_active_till",
        "league"
    ]

    df = df[final_columns]

    # Sort team history records by team and active period.
    df = df.sort_values(
        by=["team_id", "season_founded"]
    )

    # Define the cleaned output file path.
    output_file = (
        PROCESSED_DIR /
        "dim_teams.csv"
    )

    # Save the cleaned team dimension table for dashboard joins.
    df.to_csv(output_file, index=False)

    print(f"\nSaved team dimension table:")
    print(output_file)

    print("\nFinal preview:")
    print(df.head())


# Run the cleaning script only when this file is executed directly.
if __name__ == "__main__":
    main()
