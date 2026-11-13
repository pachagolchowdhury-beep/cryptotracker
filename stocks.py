import os
from pathlib import Path

import requests
from flask import Flask, jsonify, send_from_directory

APP_DIR = Path(__file__).resolve().parent

API_URL = (
    "https://pro-api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin,ethereum,binancecoin"
    "&vs_currencies=usd"
    "&include_24hr_change=true"
)

COIN_MAP = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "binancecoin": "BNB",
}

app = Flask(__name__, static_folder=None)


@app.route("/")
def home():
    return send_from_directory(APP_DIR, "index-1.html")


@app.route("/script.js")
def javascript():
    return send_from_directory(APP_DIR, "script.js")


@app.route("/style.css")
def stylesheet():
    return send_from_directory(APP_DIR, "style.css")


@app.route("/prices")
def prices_api():
    api_key = os.environ.get("COINGECKO_API_KEY")

    if not api_key:
        return jsonify({"error": "COINGECKO_API_KEY is not set"}), 500

    try:
        response = requests.get(
            API_URL,
            headers={"api from coingecko": api_key},
            timeout=10,
        )
        response.raise_for_status()
        raw = response.json()

        prices = {}

        for coin_id, symbol in COIN_MAP.items():
            coin_data = raw.get(coin_id, {})
            price = coin_data.get("usd")
            change = coin_data.get("usd_24h_change")

            if price is None or change is None:
                return jsonify({"error": f"Missing data for {coin_id}"}), 502

            prices[symbol] = {
                "price": price,
                "change24h": change,
            }

        return jsonify(prices)

    except requests.RequestException as error:
        return jsonify({"error": f"Could not fetch prices: {error}"}), 502
    except ValueError:
        return jsonify({"error": "Invalid response from CoinGecko"}), 502


if __name__ == "__main__":
    app.run(debug=True)
