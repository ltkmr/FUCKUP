from datetime import date
from pathlib import Path

import feedparser

# Configurable feeds:
FEEDS = {
    # "world_news_BBC": "http://feeds.bbci.co.uk/news/world/rss.xml",
    # "world_news_nyt": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "the_guardian_world": "https://www.theguardian.com/world/rss",
    "sky_this_week": "https://www.astronomy.com/tags/sky-this-week/feed/",
    "cnn_money": "http://rss.cnn.com/rss/money_news_economy.rss",
    "the_guardian_science": "https://www.theguardian.com/science/rss",
    "NPR": "https://feeds.npr.org/1019/rss.xml",
    "NPR": "https://feeds.npr.org/1001/rss.xml",
    "DW_EU": "https://rss.dw.com/rdf/rss-en-eu",
    "DW_BIZ": "https://rss.dw.com/rdf/rss-en-bus"
    # Add more if you like!
}


def fetch_feed(name, url, output_dir):
    print(f"🔍 Fetching {name}...")
    feed = feedparser.parse(url)
    output_file = output_dir / f"{name}.txt"
    with output_file.open("w", encoding="utf-8") as f:
        for entry in feed.entries:
            f.write(f"Title: {entry.get('title', 'No title')}\n")
            f.write(f"Link: {entry.get('link', 'No link')}\n")
            f.write(f"Published: {entry.get('published', 'No date')}\n")
            f.write(f"Summary: {entry.get('summary', 'No summary')}\n")
            f.write("-" * 40 + "\n")
    print(f"✅ Saved {name} feed to {output_file}")

    target_directory.mkdir(exist_ok=True)

    for name, url in FEEDS.items():
        try:
            fetch_feed(name, url, target_directory)
        except Exception as e:
            print(f"⚠️ Error fetching {name}: {e}")

    print("🎉 Data collection complete!")


# Optional: Support standalone running for testing
if __name__ == "__main__":
    today = date.today().isoformat()
    base_dir = Path(__file__).parent.parent / "data" / today / "raw"
    main(base_dir)
