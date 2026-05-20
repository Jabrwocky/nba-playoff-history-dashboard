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

    # Standardize column names so they are easier to reference consistently.
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    return df


def main():
    """Clean raw NBA player statistics and save playoff box score data."""

    # Identify the raw player statistics file.
    player_file = RAW_DIR / "PlayerStatistics.csv"

    print("Loading player statistics...")
    df = pd.read_csv(player_file)

    print(f"Original shape: {df.shape}")

    # Standardize column names before filtering or selecting variables.
    df = clean_column_names(df)

    # Keep only playoff games for the playoff dashboard dataset.
    df = df[df["gametype"] == "Playoffs"].copy()

    print(f"Playoff-only shape: {df.shape}")

    # Map raw column names to clearer analysis-friendly names.
    rename_dict = {
        "personid": "player_id",
        "gameid": "game_id",
        "playerteamid": "team_id",
        "opponentteamid": "opponent_team_id",
        "playerteamname": "team_name",
        "opponentteamname": "opponent_team_name",
        "playerteamcity": "team_city",
        "opponentteamcity": "opponent_team_city",
        "numminutes": "minutes",
        "reboundstotal": "rebounds",
        "reboundsoffensive": "offensive_rebounds",
        "reboundsdefensive": "defensive_rebounds",
        "fieldgoalsmade": "fgm",
        "fieldgoalsattempted": "fga",
        "fieldgoalspercentage": "fg_pct",
        "threepointersmade": "three_pm",
        "threepointersattempted": "three_pa",
        "threepointerspercentage": "three_pct",
        "freethrowsmade": "ftm",
        "freethrowsattempted": "fta",
        "freethrowspercentage": "ft_pct",
        "plusminuspoints": "plus_minus"
    }

    df = df.rename(columns=rename_dict)

    # Combine first and last name fields into one player display name.
    df["player_name"] = (
        df["firstname"].fillna("")
        + " "
        + df["lastname"].fillna("")
    ).str.strip()

    # Convert game dates to datetime format for sorting and season features.
    df["gamedatetimeest"] = pd.to_datetime(
        df["gamedatetimeest"],
        errors="coerce"
    )

    # Extract the calendar year from the game date.
    df["season_year"] = (
        df["gamedatetimeest"]
        .dt.year.astype("Int64")
    )

    # Create a unique team-season identifier for joins and dashboard grouping.
    df["team_season_key"] = (
        df["team_id"].astype("Int64").astype(str)
        + "_"
        + df["season_year"].astype(str)
    )

    # Keep only the fields needed for player-level playoff box score analysis.
    final_columns = [
        "game_id",
        "gamedatetimeest",
        "season_year",
        "team_season_key",
        "player_id",
        "player_name",
        "team_id",
        "team_name",
        "team_city",
        "opponent_team_id",
        "opponent_team_name",
        "opponent_team_city",
        "gamelabel",
        "gamesublabel",
        "seriesgamenumber",
        "home",
        "win",
        "minutes",
        "points",
        "assists",
        "rebounds",
        "offensive_rebounds",
        "defensive_rebounds",
        "steals",
        "blocks",
        "turnovers",
        "fgm",
        "fga",
        "fg_pct",
        "three_pm",
        "three_pa",
        "three_pct",
        "ftm",
        "fta",
        "ft_pct",
        "plus_minus",
        "startingposition"
    ]

    df = df[final_columns]

    # Sort records chronologically, then by game and player name.
    df = df.sort_values(
        by=["gamedatetimeest", "game_id", "player_name"]
    )

    # Define the cleaned output file path.
    output_file = (
        PROCESSED_DIR /
        "processed_player_boxscores.csv"
    )

    # Save the cleaned playoff box score dataset for dashboard use.
    df.to_csv(output_file, index=False)

    print(f"\nSaved cleaned playoff dataset:")
    print(output_file)

    print("\nFinal preview:")
    print(df.head())


# Run the cleaning script only when this file is executed directly.
if __name__ == "__main__":
    main()
