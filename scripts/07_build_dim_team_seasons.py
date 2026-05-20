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
    """Create a team-season dimension table from team histories and games."""

    # Identify the raw team histories file and processed games dimension file.
    teams_file = RAW_DIR / "TeamHistories.csv"
    games_file = PROCESSED_DIR / "dim_games.csv"

    print("Loading team histories...")
    teams = pd.read_csv(teams_file)
    teams = clean_column_names(teams)

    print("Loading games dimension...")
    games = pd.read_csv(games_file)

    # Map raw team history columns to clearer analysis-friendly names.
    teams = teams.rename(columns={
        "teamid": "team_id",
        "teamcity": "team_city",
        "teamname": "team_name",
        "teamabbrev": "team_abbrev",
        "seasonfounded": "season_founded",
        "seasonactivetill": "season_active_till"
    })

    # Get the playoff seasons that actually appear in the games dimension table.
    seasons = (
        games["season_year"]
        .dropna()
        .astype(int)
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    # Store one output row for each valid team-season combination.
    rows = []

    # Expand each team history record across all playoff seasons when active.
    for _, team in teams.iterrows():
        start_year = int(team["season_founded"])
        end_year = int(team["season_active_till"])

        for season in seasons:
            # Include the team only if it was active during that season.
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

    # Convert the accumulated team-season records into a DataFrame.
    dim_team_seasons = pd.DataFrame(rows)

    # Sort by team and season for easier inspection and stable output.
    dim_team_seasons = dim_team_seasons.sort_values(
        by=["team_id", "season_year"]
    )

    # Define the cleaned output file path.
    output_file = PROCESSED_DIR / "dim_team_seasons.csv"

    # Save the team-season dimension table for dashboard joins.
    dim_team_seasons.to_csv(output_file, index=False)

    print(f"\nSaved team-season dimension table:")
    print(output_file)

    print("\nFinal preview:")
    print(dim_team_seasons.head())


# Run the dimension-building script only when this file is executed directly.
if __name__ == "__main__":
    main()
