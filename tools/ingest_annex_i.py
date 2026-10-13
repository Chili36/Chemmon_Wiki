#!/usr/bin/env python3
"""Pin the EU Annex I product list (codes and names) into chemmon_docs/datasets/eu-annex-i/.

The names label Annex I commodity codes on generated pages. Rows come from the
EU Pesticides Database `pesticide-residues-products` API (DG SANTE), English.
Only the identifying fields are kept; nothing is renamed or reworded.

Usage:
  python tools/ingest_annex_i.py
  python tools/ingest_annex_i.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from wiki_api.datasets import DATASETS_DIR, MANIFEST_NAME, sha256_bytes  # noqa: E402

URL = ("https://api.datalake.sante.service.ec.europa.eu/sante/pesticides/pesticide-residues-products"
       "?format=json&language=EN&api-version=v3.0")
FIELDS = ("product_id", "product_parent_id", "product_code", "product_name")
TARGET = DATASETS_DIR / "eu-annex-i"
MAX_PAGES = 100


def curl_json(url: str) -> dict:
    # curl uses the system trust store, which some Python installs lack.
    out = subprocess.run(["curl", "-sfS", "-m", "120", url], check=True, capture_output=True).stdout
    return json.loads(out)


def fetch(get: Callable[[str], dict] = curl_json) -> list[dict]:
    rows, url, pages = [], URL, 0
    while url:
        pages += 1
        if pages > MAX_PAGES:
            raise ValueError("pagination did not finish")
        page = get(url)
        if not isinstance(page.get("value"), list):
            raise ValueError("unexpected API response")
        rows += page["value"]
        url = page.get("nextLink")
    return rows


def validate(rows: list[dict]) -> list[dict]:
    if len(rows) < 100:
        raise ValueError(f"only {len(rows)} products; refusing a suspiciously small list")
    products, seen = [], set()
    for row in rows:
        code = row.get("product_code")
        if not isinstance(code, str) or not re.fullmatch(r"\d{7}", code) or not row.get("product_name"):
            raise ValueError(f"invalid product row {row!r:.200}")
        if code in seen:
            raise ValueError(f"duplicate product_code {code}")
        seen.add(code)
        products.append({k: row.get(k) for k in FIELDS})
    return sorted(products, key=lambda p: p["product_code"])


def ingest(root: Path, get: Callable[[str], dict] = curl_json, dry_run: bool = False) -> tuple[str, bool]:
    products = validate(fetch(get))
    data = (json.dumps(products, indent=1, ensure_ascii=False) + "\n").encode()
    target = root / TARGET
    old = target / "products.json"
    changed = not old.is_file() or old.read_bytes() != data
    if changed and not dry_run:
        target.mkdir(parents=True, exist_ok=True)
        (target / "products.json").write_bytes(data)
        manifest = {
            "version": 1,
            "kind": "api",
            "dataset": "eu-annex-i",
            "description": "Annex I product codes and English names from the EU Pesticides Database "
                           "(European Commission, DG SANTE); fields: " + ", ".join(FIELDS) + ".",
            "url": URL,
            "retrieved_at": date.today().isoformat(),
            "files": {"products.json": {"sha256": sha256_bytes(data)}},
            "summary": {"products": len(products)},
        }
        (target / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return f"Annex I products: {len(products)}; {'written' if changed and not dry_run else 'not written'}" + \
        ("" if changed else " (unchanged)") + "\n", changed and not dry_run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        report, _ = ingest(ROOT, dry_run=args.dry_run)
    except (subprocess.CalledProcessError, ValueError, json.JSONDecodeError) as exc:
        print(f"rejected, nothing written: {exc}", file=sys.stderr)
        return 1
    print(report, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
