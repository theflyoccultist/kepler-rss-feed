#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
import feedparser
import threading
import time
import os
from datetime import date
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["50 per hour"],
    storage_uri="memory://"
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

    today = date.today()
    filename = "feed_export_" + date.isoformat(today) + ".txt"

    return send_file(tmp_path, as_attachment=True, mimetype="text/plain",
                     download_name=filename)

    threading.Thread(target=delayed_delete, args=(
        tmp_path,), daemon=True).start()


def delayed_delete(path, delay=10):
    time.sleep(delay)
    os.remove(path)


if __name__ == "__main__":
    app.run(debug=True)
