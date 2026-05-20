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

    print("Loading team histories...")
    df = pd.read_csv(teams_file)

    print(f"Original shape: {df.shape}")

    # Clean columns
    df = clean_column_names(df)

    # Rename columns
    rename_dict = {
        "teamid": "team_id",
        "teamcity": "team_city",
        "teamname": "team_name",
        "teamabbrev": "team_abbrev",
        "seasonfounded": "season_founded",
        "seasonactivetill": "season_active_till"
    }

    df = df.rename(columns=rename_dict)

    # Create full display name
    df["team_full_name"] = (
        df["team_city"].fillna("")
        + " "
        + df["team_name"].fillna("")
    ).str.strip()

    # Select columns
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

    # Sort nicely
    df = df.sort_values(
        by=["team_id", "season_founded"]
    )

    output_file = (
        PROCESSED_DIR /
        "dim_teams.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"\nSaved team dimension table:")
    print(output_file)

    print("\nFinal preview:")
    print(df.head())


if __name__ == "__main__":
    main()