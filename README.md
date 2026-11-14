# cryptotracker
# cryptotracker

A lightweight cryptocurrency price dashboard for tracking market prices and daily movements.

**[Live Demo](https://cryptotracker-zeta-liard.vercel.app/)**

---

## Overview

`cryptotracker` is a small web application that fetches cryptocurrency market data from the CoinGecko API and displays it through a simple dashboard.

The project uses a Python backend to handle API requests and caching, with a JavaScript frontend that periodically refreshes displayed prices.

## Features

- **Live price tracking** — Monitor Bitcoin (BTC), Ethereum (ETH), and BNB.
- **24-hour price changes** — View daily percentage movements.
- **Automatic updates** — Refreshes market data every 60 seconds.
- **API caching** — Reduces unnecessary requests to CoinGecko.
- **Cached fallback** — Displays the last available prices if the API becomes temporarily unavailable.
- **Responsive status updates** — Shows whether prices are live or using cached data.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic |
| Flask | API and application server |
| JavaScript | Frontend functionality |
| HTML & CSS | Structure and styling |
| CoinGecko API | Cryptocurrency market data |

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

Clone the repository:

```bash
git clone https://github.com/pachagolchowdhury-beep/cryptotracker.git
cd cryptotracker
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

The application supports optional CoinGecko API credentials.

Create a `.env` file in the project directory:

```env
COINGECKO_API_KEY=your_api_key
COINGECKO_PLAN=demo
CACHE_SECONDS=60
```

The application can also use CoinGecko's public endpoint without an API key.

### Run Locally

```bash
python stocks.py
```

Open the application at:

```text
http://127.0.0.1:5000
```

## API

The backend exposes a simple endpoint:

| Endpoint | Description |
|---|---|
| `GET /prices` | Returns cryptocurrency prices and metadata |

Example response structure:

```json
{
  "BTC": {
    "price": 0,
    "change24h": 0
  },
  "ETH": {
    "price": 0,
    "change24h": 0
  },
  "BNB": {
    "price": 0,
    "change24h": 0
  },
  "_meta": {
    "updated": 0,
    "stale": false
  }
}
```

*Values above are placeholders illustrating the response structure.*

## Project Structure

```text
cryptotracker/
├── stocks.py          # Flask backend and price fetching
├── script.js          # Frontend updates and data handling
├── style.css          # Dashboard styling
├── index.html         # Main frontend page
├── requirements.txt   # Python dependencies
└── .env               # Local environment configuration
```

## Notes

- Market data is provided by CoinGecko.
- Prices are displayed in USD.
- Data availability depends on the external API.
- This project is a market-data dashboard, not a trading platform or financial advice service.

---
## What I Learned
- Working with external APIs was one of my biggest challenges.
- Learned to handle API responses, errors, and caching.
- Improved my Python and JavaScript skills through hands-on debugging.
- Gained a better understanding of how frontend and backend systems communicate.

## Future Improvements
- Explore more APIs and integrations.
- Improve the UI and overall user experience.
- Add historical price data and interactive charts.
- Strengthen backend functionality and error handling.
- Keep experimenting and learning through new projects.
- Would love any insight on any other improvements, I'm always in for learning.




(shot my shot at online trading(OHMYGODHFBGJDFSJDNV))

- made by
- @courtcurtain
