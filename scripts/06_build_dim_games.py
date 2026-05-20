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

    # Standardize column names for consistent filtering, renaming, and selection.
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    return df


def main():
    """Clean the raw games table and save a playoff games dimension table."""

    # Identify the raw games file.
    games_file = RAW_DIR / "Games.csv"

    print("Loading games table...")
    df = pd.read_csv(games_file)

    print(f"Original shape: {df.shape}")

    # Standardize column names before filtering or selecting variables.
    df = clean_column_names(df)

    # Keep only playoff games for the playoff dashboard dataset.
    df = df[df["gametype"] == "Playoffs"].copy()

    print(f"Playoff-only shape: {df.shape}")

    # Map raw game columns to clearer analysis-friendly names.
    rename_dict = {
        "gameid": "game_id",
        "hometeamid": "home_team_id",
        "awayteamid": "away_team_id",
        "hometeamname": "home_team_name",
        "awayteamname": "away_team_name",
        "hometeamcity": "home_team_city",
        "awayteamcity": "away_team_city",
        "homescore": "home_score",
        "awayscore": "away_score"
    }

    df = df.rename(columns=rename_dict)

    # Convert game date fields to datetime format.
    df["gamedatetimeest"] = pd.to_datetime(
        df["gamedatetimeest"],
        errors="coerce"
    )

    df["gamedate"] = pd.to_datetime(
        df["gamedate"],
        errors="coerce"
    )

    # Extract the calendar year from the game datetime.
    df["season_year"] = df["gamedatetimeest"].dt.year

    # Preserve the original winner field under a clearer dashboard column name.
    df["winner_team"] = df["winner"]

    # Keep only the fields needed for the games dimension table.
    final_columns = [
        "game_id",
        "gamedatetimeest",
        "gamedate",
        "season_year",
        "home_team_id",
        "home_team_name",
        "home_team_city",
        "away_team_id",
        "away_team_name",
        "away_team_city",
        "home_score",
        "away_score",
        "winner_team",
        "gamelabel",
        "gamesublabel",
        "gamesublabel",
        "seriesgamenumber",
        "attendance",
        "arenaname",
        "arenacity",
        "arenastate"
    ]

    df = df[final_columns]

    # Ensure each playoff game appears only once.
    df = df.drop_duplicates(subset="game_id")

    # Sort games chronologically, then by game identifier.
    df = df.sort_values(
        by=["gamedatetimeest", "game_id"]
    )

    # Define the cleaned output file path.
    output_file = (
        PROCESSED_DIR /
        "dim_games.csv"
    )

    # Save the cleaned games dimension table for dashboard joins.
    df.to_csv(output_file, index=False)

    print(f"\nSaved games dimension table:")
    print(output_file)

    print("\nFinal preview:")
    print(df.head())


# Run the cleaning script only when this file is executed directly.
if __name__ == "__main__":
    main()
