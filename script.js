
const REFRESH_MS = 60 * 1000;      // matches the server's 60s cache
const SYMBOLS = ["BTC", "ETH", "BNB"];

function formatPrice(value) {
    return value.toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: value < 1 ? 6 : 2,
    });
}

function updateCoin(symbol, info) {
    const id = symbol.toLowerCase();
    const priceEl = document.getElementById(`${id}-price`);
    const changeEl = document.getElementById(`${id}-change`);
    if (!priceEl || !changeEl || !info) return;

    priceEl.textContent = formatPrice(info.price);

    changeEl.classList.remove("positive", "negative");
    if (info.change24h == null) {
        changeEl.textContent = "N/A";
        return;
    }
    const sign = info.change24h > 0 ? "+" : "";
    changeEl.textContent = `${sign}${info.change24h.toFixed(2)}%`;
    changeEl.classList.add(info.change24h >= 0 ? "positive" : "negative");
}

async function refresh() {
    const status = document.getElementById("status");
    try {
        const response = await fetch("/prices");
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);

        SYMBOLS.forEach((symbol) => updateCoin(symbol, data[symbol]));

        const meta = data._meta || {};
        status.textContent = meta.stale
            ? "CoinGecko is unreachable, showing the last known prices"
            : "Prices are live";

        const updated = meta.updated ? new Date(meta.updated * 1000) : new Date();
        document.getElementById("last-updated").textContent =
            `Last updated: ${updated.toLocaleTimeString()}`;
    } catch (error) {
        console.error("Could not load prices:", error);
        status.textContent =
            error instanceof TypeError
                ? "Can't reach the server. Open http://127.0.0.1:5000."
                : `Couldn't load prices: ${error.message}`;
    }
}

refresh();
setInterval(() => { if (!document.hidden) refresh(); }, REFRESH_MS);
document.addEventListener("visibilitychange", () => { if (!document.hidden) refresh(); });
