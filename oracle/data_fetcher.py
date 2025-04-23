import os
import datetime
import feedparser

# Configurable RSS feeds
FEEDS = {
    # "world_news_BBC": "http://feeds.bbci.co.uk/news/world/rss.xml",
    # "world_news_nyt": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "the_guardian_world": "https://www.theguardian.com/world/rss",
    "sky_this_week": "https://www.astronomy.com/tags/sky-this-week/feed/",
    # "cnn_money": "http://rss.cnn.com/rss/money_news_economy.rss",
    "the_guardian_science": "https://www.theguardian.com/science/rss",
    "the_guardian_busines": "https://www.theguardian.com/business/rss",
    "NPR": "https://feeds.npr.org/1019/rss.xml",
    "NPR": "https://feeds.npr.org/1001/rss.xml",
    "DW_EU": "https://rss.dw.com/rdf/rss-en-eu",
    "DW_BIZ": "https://rss.dw.com/rdf/rss-en-bus"
}

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def fetch_feed(name, url, raw_dir, log_file):
    print(f"🔍 Fetching {name}...")
    feed = feedparser.parse(url)
    output_file = os.path.join(raw_dir, f"{name}.txt")


    total_length = 0
    count = 0

    with open(output_file, "w", encoding="utf-8") as f:
        for entry in feed.entries:
            title = entry.get('title', 'No title')
            summary = entry.get('summary', '')
            length = len(summary)
            total_length += length
            count += 1

            print(f"[{title[:60]}...] → Summary length: {length} chars")

            f.write(f"Title: {title}\n")
            f.write(f"Link: {entry.get('link', 'No link')}\n")
            f.write(f"Published: {entry.get('published', 'No date')}\n")
            f.write(f"Summary: {summary}\n")
            f.write("-" * 40 + "\n")

    if count > 0:
        average = total_length / count
        print(f"📊 Average summary length for {name}: {average:.1f} chars ({count} items)")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"{timestamp} | {name}: {average:.1f} chars avg from {count} items\n")
    else:
        print(f"⚠️ No entries found for {name}.")

    print(f"✅ Saved {name} feed to {output_file}")

def main(base_dir):
    raw_dir = os.path.join(base_dir, "raw")
    logs_dir = os.path.join(base_dir, "logs")
    ensure_dir(raw_dir)
    ensure_dir(logs_dir)

    log_file = os.path.join(logs_dir, "summary_lengths.log")

    for name, url in FEEDS.items():
        try:
            fetch_feed(name, url, raw_dir, log_file)
        except Exception as e:
            print(f"⚠️ Error fetching {name}: {e}")

    print("🎉 Data collection complete!")

if __name__ == "__main__":
    today = datetime.date.today().isoformat()
    base_dir = os.path.join(os.path.dirname(__file__), "..", "data", today)
    main(base_dir)
