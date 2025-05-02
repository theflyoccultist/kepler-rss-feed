#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import feedparser

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per hour"]
)

rss_feeds = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://9to5linux.com/feed/atom"
]


@app.route('/')
@limiter.limit("5 per minute")
def index():
    articles = []
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:
            articles.append({"title": entry.title, "link": entry.link})
    return render_template("index.html", articles=articles)


if __name__ == "__main__":
    app.run(debug=True)
