#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Equivalente a: componente_nlp/entrenamiento/1testApi.ipynb

Búsqueda reciente en X (Twitter) API v2. Requiere variable de entorno TWITTER_BEARER_TOKEN.
No definas el token en el código; usa .env o el entorno del sistema.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import pandas as pd
import requests

from _paths import DATA_DIR, REPO_ROOT

try:
    from dotenv import load_dotenv

    load_dotenv(REPO_ROOT / ".env")
except ImportError:
    pass

DEFAULT_QUERY = (
    ' "busco a mi perro" OR "busco a mi perrito"  -is:retweet -is:reply'
)


def bearer_oauth(r, token: str):
    r.headers["Authorization"] = f"Bearer {token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url: str, params: dict, token: str) -> dict:
    response = requests.get(url, auth=lambda req: bearer_oauth(req, token), params=params, timeout=60)
    if response.status_code != 200:
        raise RuntimeError(f"HTTP {response.status_code}: {response.text}")
    return response.json()


def main():
    parser = argparse.ArgumentParser(description="Descarga tweets recientes (API v2).")
    parser.add_argument("--query", default=DEFAULT_QUERY, help="Query de búsqueda")
    parser.add_argument(
        "--out",
        type=Path,
        default=DATA_DIR / "1_raw" / "extracc_twitter.csv",
        help="CSV de salida (;)",
    )
    args = parser.parse_args()

    token = os.environ.get("TWITTER_BEARER_TOKEN", "").strip()
    if not token:
        print("Define TWITTER_BEARER_TOKEN en el entorno o en .env", file=sys.stderr)
        sys.exit(1)

    search_url = "https://api.x.com/2/tweets/search/recent"
    query_params = {"query": args.query, "tweet.fields": "author_id"}

    args.out.parent.mkdir(parents=True, exist_ok=True)

    json_response = connect_to_endpoint(search_url, query_params, token)
    if "data" not in json_response:
        print("Respuesta sin 'data':", json.dumps(json_response, indent=2)[:2000])
        sys.exit(1)

    frames = [pd.json_normalize(json_response["data"])]
    while "next_token" in json_response.get("meta", {}):
        new_params = dict(query_params)
        new_params["next_token"] = json_response["meta"]["next_token"]
        json_response = connect_to_endpoint(search_url, new_params, token)
        if "data" in json_response:
            frames.append(pd.json_normalize(json_response["data"]))

    df = pd.concat(frames, ignore_index=True)
    pd.set_option("display.max_colwidth", None)
    df.to_csv(args.out, sep=";", index=False)
    print(f"Guardado: {args.out} ({len(df)} filas)")


if __name__ == "__main__":
    main()
