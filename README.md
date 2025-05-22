## Kepler RSS : An RSS Feed Parser


- Access to your feeds both from the web interface and from the command-line.

### How it's made (website):
- Python Flask api and feedparser
- Jinja2 Templating engine and HTMX

Start the app:
```sh
poetry run python app.py
```

### Features (website):
- A retro-futuristic UI
- Paste an RSS link in the input form, click Fetch Feed and you will retrieve articles.

### How it's made (cli):
- It's just a single python file


🧼 Clean file generation flow?

Let’s say your RSS parser generates the file on request. You can:

    Generate a tempfile

    Write the parsed feed contents

    Use send_file or send_from_directory to let users download the file.

    Optionally delete it after (unless you like digital hoarding)

Bonus move? Timestamp the filename with datetime.now().strftime(...) so users get:

feed_export_2025-05-21.txt
