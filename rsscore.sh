#!/bin/bash

feed_url=$1
if [[ -z "$feed_url" ]]; then
  echo "Usage: $0 <rss-feed-url>"
  exit 1
fi

curl -s "$feed_url" | grep -oP '(?<=<title>).*?(?=</title>)' | head -10
