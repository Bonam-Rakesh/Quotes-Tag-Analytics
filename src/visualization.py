from collections import Counter
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "quotes_clean.csv"
OUTPUT_DIR = PROJECT_ROOT / "visualizations"


def load_data():
    """Load the cleaned quote dataset."""

    return pd.read_csv(DATA_FILE)


def save_figure(filename):
    """Save the current matplotlib figure."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filepath = OUTPUT_DIR / filename

    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Saved visualization: {filepath}")


def plot_top_tags(df):
    """Create a chart of the most frequently used tags."""

    all_tags = []

    for tags in df["tags"].fillna(""):
        for tag in str(tags).split(","):
            tag = tag.strip()

            if tag:
                all_tags.append(tag)

    tag_counts = (
        pd.Series(Counter(all_tags))
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=tag_counts.values,
        y=tag_counts.index,
    )

    plt.title("Top 10 Most Frequent Tags")
    plt.xlabel("Number of Quotes")
    plt.ylabel("Tag")

    save_figure("top_10_tags.png")


def plot_top_authors(df):
    """Create a chart of authors with the most quotes."""

    author_counts = (
        df["author"]
        .value_counts()
        .head(10)
        .sort_values()
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=author_counts.values,
        y=author_counts.index,
    )

    plt.title("Top 10 Authors by Number of Quotes")
    plt.xlabel("Number of Quotes")
    plt.ylabel("Author")

    save_figure("top_10_authors.png")


def plot_quote_length_distribution(df):
    """Show the distribution of quote lengths."""

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["quote_length"],
        bins=15,
        kde=True,
    )

    plt.title("Distribution of Quote Length")
    plt.xlabel("Quote Length (Characters)")
    plt.ylabel("Number of Quotes")

    save_figure("quote_length_distribution.png")


def plot_word_count_distribution(df):
    """Show the distribution of words per quote."""

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["word_count"],
        bins=15,
        kde=True,
    )

    plt.title("Distribution of Words per Quote")
    plt.xlabel("Number of Words")
    plt.ylabel("Number of Quotes")

    save_figure("word_count_distribution.png")


def plot_tag_combinations(df):
    """Visualize the most common tag combinations."""

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
        print("No tag combinations available.")
        return

    top_combinations = combinations_counter.most_common(10)

    labels = [
        f"{pair[0]} + {pair[1]}"
        for pair, _ in top_combinations
    ]

    values = [
        count
        for _, count in top_combinations
    ]

    combination_series = pd.Series(
        values,
        index=labels,
    ).sort_values()

    plt.figure(figsize=(11, 6))

    sns.barplot(
        x=combination_series.values,
        y=combination_series.index,
    )

    plt.title("Top 10 Tag Combinations")
    plt.xlabel("Number of Occurrences")
    plt.ylabel("Tag Combination")

    save_figure("top_tag_combinations.png")


def main():
    """Generate all project visualizations."""

    df = load_data()

    print("Generating visualizations...\n")

    plot_top_tags(df)
    plot_top_authors(df)
    plot_quote_length_distribution(df)
    plot_word_count_distribution(df)
    plot_tag_combinations(df)

    print("\nAll visualizations generated successfully.")


if __name__ == "__main__":
    main()