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

    players_file = RAW_DIR / "Players.csv"

    print("Loading players table...")
    df = pd.read_csv(players_file)

    print(f"Original shape: {df.shape}")

    # Clean columns
    df = clean_column_names(df)

    # Rename important columns
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

    # Create full player name
    df["player_name"] = (
        df["first_name"].fillna("")
        + " "
        + df["last_name"].fillna("")
    ).str.strip()

    # Convert dates
    df["birth_date"] = pd.to_datetime(
        df["birth_date"],
        errors="coerce"
    )

    # Create position label
    df["position"] = ""

    df.loc[df["guard"] == 1, "position"] += "G"
    df.loc[df["forward"] == 1, "position"] += "F"
    df.loc[df["center"] == 1, "position"] += "C"

    # Select final columns
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

    # Remove duplicates
    df = df.drop_duplicates(subset="player_id")

    # Sort nicely
    df = df.sort_values(by="player_name")

    output_file = (
        PROCESSED_DIR /
        "dim_players.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"\nSaved player dimension table:")
    print(output_file)

    print("\nFinal preview:")
    print(df.head())


if __name__ == "__main__":
    main()