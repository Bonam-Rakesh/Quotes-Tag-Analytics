import json
import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "quotes_raw.csv"
QUOTABLE_FILE = PROJECT_ROOT / "data" / "raw" / "quotable_quotes.json"

BASE_URL = "https://quotes.toscrape.com/"

TARGET_QUOTES = 250


def scrape_quotes():
    """Scrape quotes from Quotes to Scrape."""

    quotes_data = []
    page_number = 1

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Quotes-Tag-Analytics)"
        }
    )

    print("\nCollecting quotes from Quotes to Scrape...\n")

    while True:
        url = f"{BASE_URL}page/{page_number}/"

        print(f"Scraping page {page_number}...")

        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()

        except requests.RequestException as error:
            print(f"Request failed: {error}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        quote_blocks = soup.select("div.quote")

        if not quote_blocks:
            break

        for quote_block in quote_blocks:

            quote_text = quote_block.select_one("span.text")
            author = quote_block.select_one("small.author")
            tag_elements = quote_block.select("div.tags a.tag")

            if quote_text is None or author is None:
                continue

            tags = [
                tag.get_text(strip=True)
                for tag in tag_elements
            ]

            quotes_data.append(
                {
                    "quote": quote_text.get_text(strip=True),
                    "author": author.get_text(strip=True),
                    "tags": ", ".join(tags),
                }
            )

        next_page = soup.select_one("li.next a")

        if next_page is None:
            print("Reached the last page.")
            break

        page_number += 1

        time.sleep(0.5)

    print(
        f"\nQuotes to Scrape collected: "
        f"{len(quotes_data)}"
    )

    return quotes_data


def load_quotable_data():
    """Load quotes from the Quotable JSON dataset."""

    if not QUOTABLE_FILE.exists():

        print(
            "\nERROR: quotable_quotes.json was not found."
        )

        print(
            "Download it first using the PowerShell command."
        )

        return []

    print("\nLoading additional quote dataset...")

    try:
        with open(
            QUOTABLE_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

    except (OSError, json.JSONDecodeError) as error:

        print(
            f"Could not read Quotable dataset: {error}"
        )

        return []

    quotes_data = []

    for item in data:

        quote = str(
            item.get("content", "")
        ).strip()

        author = str(
            item.get("author", "")
        ).strip()

        tags = item.get("tags", [])

        if not isinstance(tags, list):
            tags = []

        tags = [
            str(tag).strip()
            for tag in tags
            if str(tag).strip()
        ]

        if not quote or not author:
            continue

        quotes_data.append(
            {
                "quote": quote,
                "author": author,
                "tags": ", ".join(tags),
            }
        )

    print(
        f"Additional quotes available: "
        f"{len(quotes_data)}"
    )

    return quotes_data


def combine_quotes(scraped_quotes, additional_quotes):
    """Combine datasets and select 250 unique quotes."""

    scraped_df = pd.DataFrame(scraped_quotes)

    additional_df = pd.DataFrame(additional_quotes)

    combined_df = pd.concat(
        [
            scraped_df,
            additional_df,
        ],
        ignore_index=True,
    )

    if combined_df.empty:
        return combined_df

    combined_df["quote"] = (
        combined_df["quote"]
        .astype(str)
        .str.strip()
    )
    combined_df["author"] = (
        combined_df["author"]
        .astype(str)
        .str.strip()
    )
    combined_df["tags"] = (
        combined_df["tags"]
        .fillna("")
        .astype(str)
        .str.strip()
    )
    combined_df = combined_df.drop_duplicates(
        subset=["quote"],
        keep="first",
    )
    combined_df = combined_df[
        (combined_df["quote"] != "")
        & (combined_df["author"] != "")
    ]
    combined_df = combined_df.head(
        TARGET_QUOTES
    )

    return combined_df.reset_index(
        drop=True
    )


def save_data(df):
    """Save the final dataset."""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print("\nFinal dataset saved to:")
    print(OUTPUT_FILE)

def main():

    print("=" * 60)
    print("QUOTES TAG ANALYTICS - DATA COLLECTION")
    print("=" * 60)
    scraped_quotes = scrape_quotes()
    additional_quotes = load_quotable_data()
    final_df = combine_quotes(scraped_quotes,additional_quotes,)

    if final_df.empty:

        print("\nNo quotes collected.")
        return

    save_data(final_df)

    print("\n" + "=" * 60)
    print("DATA COLLECTION COMPLETED")
    print("=" * 60)
    print(f"Original scraped quotes : "f"{len(scraped_quotes)}")
    print(f"Additional quotes : "f"{len(additional_quotes)}")
    print(f"Final unique quotes : "f"{len(final_df)}")
    print("\nColumns:")
    print(list(final_df.columns))
    print("\nFirst 5 records:")
    print(final_df.head())

if __name__ == "__main__":
    main()