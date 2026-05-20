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
    teams_file = RAW_DIR / "TeamHistories.csv"
    games_file = PROCESSED_DIR / "dim_games.csv"

    print("Loading team histories...")
    teams = pd.read_csv(teams_file)
    teams = clean_column_names(teams)

    print("Loading games dimension...")
    games = pd.read_csv(games_file)

    teams = teams.rename(columns={
        "teamid": "team_id",
        "teamcity": "team_city",
        "teamname": "team_name",
        "teamabbrev": "team_abbrev",
        "seasonfounded": "season_founded",
        "seasonactivetill": "season_active_till"
    })

    # Use actual playoff seasons in the data
    seasons = (
        games["season_year"]
        .dropna()
        .astype(int)
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    rows = []

    for _, team in teams.iterrows():
        start_year = int(team["season_founded"])
        end_year = int(team["season_active_till"])

        for season in seasons:
            if start_year <= season <= end_year:
                rows.append({
                    "team_season_key": f"{int(team['team_id'])}_{season}",
                    "team_id": int(team["team_id"]),
                    "season_year": season,
                    "team_full_name": f"{team['team_city']} {team['team_name']}",
                    "team_city": team["team_city"],
                    "team_name": team["team_name"],
                    "team_abbrev": team["team_abbrev"],
                    "league": team["league"],
                    "season_founded": start_year,
                    "season_active_till": end_year
                })

    dim_team_seasons = pd.DataFrame(rows)

    dim_team_seasons = dim_team_seasons.sort_values(
        by=["team_id", "season_year"]
    )

    output_file = PROCESSED_DIR / "dim_team_seasons.csv"
    dim_team_seasons.to_csv(output_file, index=False)

    print(f"\nSaved team-season dimension table:")
    print(output_file)

    print("\nFinal preview:")
    print(dim_team_seasons.head())


if __name__ == "__main__":
    main()