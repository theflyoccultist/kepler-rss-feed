#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
import feedparser
# import os
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from flask import Flask, render_template, request, send_file  # after_this_request

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
    return render_template("_articles.html", articles=articles,
                           rss_url=rss_url)


@app.route("/download", methods=["POST"])
def download_file():
    rss_url = request.form.get("rss_url", 'not fetched')

    feed = feedparser.parse(rss_url)
    articles = [{"title": entry.title, "link": entry.link}
                for entry in feed.entries[:5]]

    outpt = '\n'.join(f"{a['title']} --> {a['link']}" for a in articles)
    tmp = tempfile.NamedTemporaryFile(delete=False, mode='wb')
    tmp.write(outpt.encode('utf-8'))
    tmp_path = tmp.name
    tmp.close()

    return send_file(tmp_path, as_attachment=True, mimetype="text/plain",
                     download_name="feeds.txt")


if __name__ == "__main__":
    app.run(debug=True)
