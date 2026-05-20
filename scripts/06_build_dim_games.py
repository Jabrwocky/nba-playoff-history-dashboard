from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_column_names(df):
    """
    Convert columns to lowercase snake_case.
    """
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    return df


def main():

    games_file = RAW_DIR / "Games.csv"

    print("Loading games table...")
    df = pd.read_csv(games_file)

    print(f"Original shape: {df.shape}")

    # Clean columns
    df = clean_column_names(df)

    # Keep only playoff games
    df = df[df["gametype"] == "Playoffs"].copy()

    print(f"Playoff-only shape: {df.shape}")

    # Rename columns
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

    # Convert dates
    df["gamedatetimeest"] = pd.to_datetime(
        df["gamedatetimeest"],
        errors="coerce"
    )

    df["gamedate"] = pd.to_datetime(
        df["gamedate"],
        errors="coerce"
    )

    # Create season year
    df["season_year"] = df["gamedatetimeest"].dt.year

    # Create winner team
    df["winner_team"] = df["winner"]

    # Select final columns
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

    # Remove duplicate games
    df = df.drop_duplicates(subset="game_id")

    # Sort nicely
    df = df.sort_values(
        by=["gamedatetimeest", "game_id"]
    )

    output_file = (
        PROCESSED_DIR /
        "dim_games.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"\nSaved games dimension table:")
    print(output_file)

    print("\nFinal preview:")
    print(df.head())


if __name__ == "__main__":
    main()