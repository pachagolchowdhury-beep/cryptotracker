export default async function handler(req, res) {
  try {
    const response = await fetch("/api/prices");
      "https://pro-api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin&vs_currencies=usd&include_24hr_change=true",
      {
        headers: {
          "CG-end9mXeYK4r5V4k8xwQBUTpQ": process.env.COINGECKO_API_KEY,
        },
      }
    );

    const data = await response.json();

    res.status(200).json({
      BTC: {
        price: data.bitcoin.usd,
        change24h: data.bitcoin.usd_24h_change,
      },
      ETH: {
        price: data.ethereum.usd,
        change24h: data.ethereum.usd_24h_change,
      },
      BNB: {
        price: data.binancecoin.usd,
        change24h: data.binancecoin.usd_24h_change,
      },
    });
  } catch (error) {
    res.status(500).json({
      error: "Failed to fetch prices",
    });
  }
}