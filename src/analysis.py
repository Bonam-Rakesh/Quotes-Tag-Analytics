from collections import Counter
from itertools import combinations
from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "processed" / "quotes_clean.csv"


def load_data():
    """Load the cleaned quote dataset."""

    return pd.read_csv(DATA_FILE)


def get_all_tags(df):
    """Extract individual tags from the dataset."""

    all_tags = []

    for tags in df["tags"].fillna(""):
        for tag in str(tags).split(","):
            tag = tag.strip()

            if tag:
                all_tags.append(tag)

    return all_tags


def dataset_summary(df):
    """Display high-level statistics about the dataset."""

    print("\n" + "=" * 50)
    print("DATASET OVERVIEW")
    print("=" * 50)

    all_tags = get_all_tags(df)

    print(f"Total quotes       : {len(df)}")
    print(f"Unique authors     : {df['author'].nunique()}")
    print(f"Unique tags        : {len(set(all_tags))}")
    print(f"Average word count : {df['word_count'].mean():.2f}")
    print(f"Average quote size : {df['quote_length'].mean():.2f} characters")
    print(f"Average tag count  : {df['tag_count'].mean():.2f}")


def author_analysis(df):
    """Analyze quote distribution across authors."""

    print("\n" + "=" * 50)
    print("TOP AUTHORS")
    print("=" * 50)

    author_counts = df["author"].value_counts()

    print(author_counts.head(10).to_string())


def tag_analysis(df):
    """Analyze the most frequently used tags."""

    print("\n" + "=" * 50)
    print("TOP TAGS")
    print("=" * 50)

    all_tags = get_all_tags(df)

    tag_counts = Counter(all_tags)

    top_tags = pd.Series(tag_counts).sort_values(ascending=False)

    print(top_tags.head(15).to_string())


def quote_length_analysis(df):
    """Analyze quote length and word count."""

    print("\n" + "=" * 50)
    print("QUOTE LENGTH ANALYSIS")
    print("=" * 50)

    longest_quote = df.loc[df["quote_length"].idxmax()]
    shortest_quote = df.loc[df["quote_length"].idxmin()]

    print(
        f"Average quote length : "
        f"{df['quote_length'].mean():.2f} characters"
    )

    print(
        f"Average word count   : "
        f"{df['word_count'].mean():.2f} words"
    )

    print("\nLongest quote:")
    print(longest_quote["quote"])
    print(f"Author: {longest_quote['author']}")

    print("\nShortest quote:")
    print(shortest_quote["quote"])
    print(f"Author: {shortest_quote['author']}")


def tag_combinations(df):
    """Find tag pairs that frequently appear together."""

    print("\n" + "=" * 50)
    print("COMMON TAG COMBINATIONS")
    print("=" * 50)

    combinations_counter = Counter()

    for tags in df["tags"].fillna(""):
        tag_list = sorted(
            {
                tag.strip()
                for tag in str(tags).split(",")
                if tag.strip()
            }
        )

        for pair in combinations(tag_list, 2):
            combinations_counter[pair] += 1

    if not combinations_counter:
        print("No tag combinations found.")
        return

    for pair, count in combinations_counter.most_common(10):
        print(f"{pair[0]} + {pair[1]} : {count}")


def main():
    """Run the complete quote analysis."""

    df = load_data()

    dataset_summary(df)
    author_analysis(df)
    tag_analysis(df)
    quote_length_analysis(df)
    tag_combinations(df)


if __name__ == "__main__":
    main()