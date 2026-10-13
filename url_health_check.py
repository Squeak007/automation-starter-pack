"""url_health_check.py — Ping a list of URLs and report status + response time.

Usage:
    python url_health_check.py urls.txt           # one URL per line
    python url_health_check.py --json urls.txt    # JSON output
"""

import argparse
import json
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def check(url: str, timeout: float = 10.0) -> dict:
    start = time.perf_counter()
    req = Request(url, headers={"User-Agent": "squeak-health-check/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            return {
                "url": url,
                "status": resp.status,
                "final_url": resp.geturl(),
                "elapsed_ms": elapsed_ms,
                "redirected": resp.geturl() != url,
                "error": None,
            }
    except HTTPError as e:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return {"url": url, "status": e.code, "elapsed_ms": elapsed_ms, "error": str(e)}
    except URLError as e:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return {"url": url, "status": None, "elapsed_ms": elapsed_ms, "error": str(e.reason)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="File with one URL per line")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    urls = [line.strip() for line in open(args.input, encoding="utf-8") if line.strip()]
    results = [check(u, timeout=args.timeout) for u in urls]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"{'URL':<60} {'STATUS':>6} {'MS':>6}  NOTE")
        print("-" * 90)
        for r in results:
            note = r.get("error") or ("redirected" if r.get("redirected") else "")
            print(f"{r['url'][:58]:<60} {str(r.get('status') or '-'):>6} {r['elapsed_ms']:>6}  {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
