import argparse
import feedparser


def fetch_feed(url, save=False):
    feed = feedparser.parse(url)
    if not feed.entries:
        print("No articles found or invalid RSS URL.")
        return

    articles = [
        f"{entry.title} --> {entry.link}" for entry in feed.entries[:5]
    ]

    print("\n=== Headlines ===")
    for a in articles:
        print(a)

    if save:
        with open("rssfeeds.txt", "a") as f:
            for a in articles:
                f.write(a + "\n")
        print("\nArticles saved to rss_output.txt")


def main():
    parser = argparse.ArgumentParser(description="Fetch RSS feed headlines.")
    parser.add_argument('url', help='RSS Feed URL')
    parser.add_argument(
        '--save',
        action='store_true',
        help='save results into ./rssfeeds.txt'
    )
    args = parser.parse_args()

    fetch_feed(args.url, args.save)


if __name__ == "__main__":
    main()
