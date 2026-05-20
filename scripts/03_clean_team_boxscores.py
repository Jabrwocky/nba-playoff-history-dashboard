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

    team_file = RAW_DIR / "TeamStatistics.csv"

    print("Loading team statistics...")
    df = pd.read_csv(team_file)

    print(f"Original shape: {df.shape}")

    # Clean columns
    df = clean_column_names(df)

    # Keep only playoff games
    df = df[df["gametype"] == "Playoffs"].copy()

    print(f"Playoff-only shape: {df.shape}")

    # Rename columns
    rename_dict = {
        "gameid": "game_id",
        "teamid": "team_id",
        "opponentteamid": "opponent_team_id",
        "teamname": "team_name",
        "opponentteamname": "opponent_team_name",
        "teamcity": "team_city",
        "opponentteamcity": "opponent_team_city",
        "teamscore": "team_score",
        "opponentscore": "opponent_score",
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

    # Convert game date
    df["gamedatetimeest"] = pd.to_datetime(
        df["gamedatetimeest"],
        errors="coerce"
    )

    # Create season year
    df["season_year"] = (
        df["gamedatetimeest"]
        .dt.year.astype("Int64")
    )

    # Create team-season key
    df["team_season_key"] = (
        df["team_id"].astype("Int64").astype(str)
        + "_"
        + df["season_year"].astype(str)
    )

    # Select final columns
    final_columns = [
        "game_id",
        "gamedatetimeest",
        "season_year",
        "team_season_key",
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
        "team_score",
        "opponent_score",
        "minutes",
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
        "seasonwins",
        "seasonlosses",
        "seed"
    ]

    df = df[final_columns]

    # Sort rows
    df = df.sort_values(
        by=["gamedatetimeest", "game_id", "team_name"]
    )

    output_file = (
        PROCESSED_DIR /
        "processed_team_boxscores.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"\nSaved cleaned playoff team dataset:")
    print(output_file)

    print("\nFinal preview:")
    print(df.head())


if __name__ == "__main__":
    main()