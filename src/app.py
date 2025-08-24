#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
import threading
import time
from datetime import date
from typing import Any, Dict, List, Optional, Union

import feedparser
from flask import Flask, Response, render_template, request, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    get_remote_address, app=app, default_limits=["50 per hour"], storage_uri="memory://"
)


@limiter.limit("5 per minute")
@app.route("/")
def index():
    return render_template("index.html", articles=[])


@app.route("/fetch", methods=["POST"])
def fetch() -> Union[str, Response]:
    rss_url: Optional[str] = request.form.get("rss_url")
    if not rss_url:
        return render_template("_error.html", error_message="not an URL!")

    feed: Any = feedparser.parse(rss_url)
    if "title" not in feed.get("feed", {}):
        return render_template("_error.html", error_message="not an URL!")

    articles: List[Dict[str, str]] = [
        {"title": entry.title, "link": entry.link} for entry in feed.entries[:5]
    ]
    return render_template("_articles.html", articles=articles, rss_url=rss_url)


@app.route("/download", methods=["POST"])
def download_file() -> Response:
    rss_url: Optional[str] = request.form.get("rss_url", "not fetched")

    feed: Any = feedparser.parse(rss_url)
    articles: List[Dict[str, str]] = [
        {"title": entry.title, "link": entry.link} for entry in feed.entries[:5]
    ]

    outpt: str = "\n".join(f"{a['title']} --> {a['link']}" for a in articles)
    tmp = tempfile.NamedTemporaryFile(delete=False, mode="wb")
    tmp.write(outpt.encode("utf-8"))
    tmp_path = tmp.name
    tmp.close()

    today: date = date.today()
    filename: str = "feed_export_" + date.isoformat(today) + ".txt"

    return send_file(
        tmp_path, as_attachment=True, mimetype="text/plain", download_name=filename
    )

    threading.Thread(target=delayed_delete, args=(tmp_path,), daemon=True).start()


def delayed_delete(path, delay=10):
    time.sleep(delay)
    os.remove(path)


if __name__ == "__main__":
    app.run(debug=True)
