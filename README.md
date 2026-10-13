# Automation Starter Pack

Small, useful Python automation scripts — the kinds of tiny tools Squeak Co. ships for clients. All MIT-licensed.

## What's here

- **`csv_to_markdown.py`** — Convert a CSV file into a Markdown table. Handy for pasting data into docs or GitHub issues.
- **`url_health_check.py`** — Ping a list of URLs and report HTTP status, response time, and redirects. Useful for monitoring a client's site or a competitor landscape.
- **`invoice_pdf.py`** — Generate a clean one-page PDF invoice from a JSON spec. The template we start every client invoice from.

## Running

```bash
pip install -r requirements.txt
python csv_to_markdown.py sample.csv
python url_health_check.py urls.txt
python invoice_pdf.py example_invoice.json
```

## Hire Squeak Co.

Need a custom automation? Email **jakeg@thefloortimecenter.com** or see [squeak007.github.io](https://squeak007.github.io/).

## License

MIT
