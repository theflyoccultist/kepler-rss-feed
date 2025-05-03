#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import feedparser

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per hour"]
)


@app.route("/")
@limiter.limit("5 per minute")
def index():
    return render_template("index.html", articles=[])


@app.route("/fetch", methods=["POST"])
def fetch():
    rss_url = request.form.get("rss_url")
    if not rss_url:
        return render_template("_articles.html", articles=[])

    feed = feedparser.parse(rss_url)
    if "title" not in feed.feed:
        return render_template("_articles.html", articles=[])

    articles = [{"title": entry.title, "link": entry.link}
                for entry in feed.entries[:5]]
    return render_template("_articles.html", articles=articles)


if __name__ == "__main__":
    app.run(debug=True)
