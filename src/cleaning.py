from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "quotes_raw.csv"
PROCESSED_FILE = PROJECT_ROOT / "data" / "processed" / "quotes_clean.csv"


def load_data():
    """Load the raw scraped quote data."""

    return pd.read_csv(RAW_FILE)


def clean_data(df):
    """Clean the quote dataset and create useful analytical columns."""

    df = df.dropna(how="all").copy()

    df = df.drop_duplicates(
        subset=["quote"]
    ).copy()

    # Clean quote and author text.
    df["quote"] = (
        df["quote"]
        .astype(str)
        .str.strip()
    )

    df["author"] = (
        df["author"]
        .astype(str)
        .str.strip()
    )

    # Clean tags and normalize capitalization.
    df["tags"] = (
        df["tags"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    def clean_tags(tags):
        if not tags:
            return ""

        cleaned = []

        for tag in tags.split(","):
            tag = tag.strip().lower()

            if tag and tag not in cleaned:
                cleaned.append(tag)

        return ", ".join(cleaned)

    df["tags"] = df["tags"].apply(clean_tags)

    # Remove invalid rows.
    df = df[
        (df["quote"] != "")
        & (df["author"] != "")
    ].copy()

    # Create analytical features.
    df["tag_count"] = df["tags"].apply(
        lambda tags: len(tags.split(", "))
        if tags
        else 0
    )

    df["quote_length"] = df["quote"].str.len()

    df["word_count"] = (
        df["quote"]
        .str.split()
        .str.len()
    )

    return df


def save_data(df):
    """Save the cleaned dataset."""

    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        PROCESSED_FILE,
        index=False,
        encoding="utf-8"
    )

    print(f"\nSaved cleaned dataset to:")
    print(PROCESSED_FILE)


def main():
    """Run the complete data-cleaning process."""

    print("Loading raw data...")

    df = load_data()

    print(f"Raw rows: {len(df)}")

    cleaned_df = clean_data(df)

    print(f"Cleaned rows: {len(cleaned_df)}")

    save_data(cleaned_df)

    print("\nData cleaning completed successfully.")

    print("\nDataset preview:")
    print(cleaned_df.head())

    print("\nDataset information:")
    print(cleaned_df.info())


if __name__ == "__main__":
    main()