import os
import time
from pathlib import Path

import requests
from flask import Flask, jsonify, send_from_directory

APP_DIR = Path(__file__).resolve().parent


try:
    from dotenv import load_dotenv
    load_dotenv(APP_DIR / ".env")
except ImportError:
    pass


PLANS = {
    "demo": ("https://api.coingecko.com/api/v3", "api key"),
     "pro": ("https://pro-api.coingecko.com/api/v3", "x-cg-pro-api-key"),
    
}

API_KEY = os.environ.get("COINGECKO_API_KEY", "").strip()
PLAN = os.environ.get("COINGECKO_PLAN", "demo").strip().lower()
if PLAN not in PLANS:
    PLAN = "demo"


if API_KEY:
    BASE_URL, KEY_HEADER = PLANS[PLAN]
else:
    BASE_URL, KEY_HEADER = PLANS["demo"][0], None

API_URL = f"{BASE_URL}/simple/price"
API_PARAMS = {
    "ids": "bitcoin,ethereum,binancecoin",
    "vs_currencies": "usd",
    "include_24hr_change": "true",
}

COIN_MAP = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "binancecoin": "BNB",
}


CACHE_SECONDS = int(os.environ.get("CACHE_SECONDS", "60"))
_cache = {"data": None, "time": 0.0}


app = Flask(__name__, static_folder=None)


class PriceError(Exception):
    def __init__(self, message, status=502):
        super().__init__(message)
        self.message = message
        self.status = status


def fetch_from_coingecko():
    headers = {KEY_HEADER: API_KEY} if KEY_HEADER else {}

    try:
        response = requests.get(API_URL, params=API_PARAMS, headers=headers, timeout=10)
    except requests.RequestException as error:
        raise PriceError(f"Could not reach CoinGecko: {error.__class__.__name__}")

    if response.status_code == 429:
        raise PriceError("CoinGecko rate limit reached. Try again in a minute.", 429)
    if response.status_code in (401, 403):
        raise PriceError(
            "CoinGecko rejected the API key. Check COINGECKO_API_KEY, and that "
            "COINGECKO_PLAN matches the key type (demo or pro).",
            502,
        )
    if not response.ok:
        raise PriceError(f"CoinGecko returned HTTP {response.status_code}.")

    try:
        raw = response.json()
    except ValueError:
        raise PriceError("Invalid response from CoinGecko.")

    prices = {}
    for coin_id, symbol in COIN_MAP.items():
        coin_data = raw.get(coin_id) or {}
        price = coin_data.get("usd")
        change = coin_data.get("usd_24h_change")
        if price is None:
            raise PriceError(f"Missing data for {coin_id}.")
        prices[symbol] = {"price": price, "change24h": change}
    return prices


def get_prices():
    """Returns (prices, timestamp, is_stale)."""
    now = time.time()
    if _cache["data"] and now - _cache["time"] < CACHE_SECONDS:
        return _cache["data"], _cache["time"], False

    try:
        data = fetch_from_coingecko()
    except PriceError:
        if _cache["data"]:  
            return _cache["data"], _cache["time"], True
        raise

    _cache["data"], _cache["time"] = data, now
    return data, now, False


@app.route("/")
def home():
    return send_from_directory(APP_DIR, "index.html")


@app.route("/script.js")
def javascript():
    return send_from_directory(APP_DIR, "script.js")


@app.route("/style.css")
def stylesheet():
    return send_from_directory(APP_DIR, "style.css")


@app.route("/prices")
def prices_api():
    try:
        prices, updated, stale = get_prices()
    except PriceError as error:
        return jsonify({"error": error.message}), error.status

    return jsonify({**prices, "_meta": {"updated": updated, "stale": stale}})


if __name__ == "__main__":
    if not API_KEY:
        print("No COINGECKO_API_KEY found: using the keyless public endpoint (5 calls/min).")
    else:
        print(f"Using CoinGecko {PLAN} plan.")
    app.run(debug=True)