from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

POPULAR_COINS = ",".join([
    "bitcoin", "ethereum", "tether", "binancecoin", "solana", "usd-coin", "staked-ether", "xrp", "dogecoin", "cardano",
    "toncoin", "shiba-inu", "avalanche", "wrapped-bitcoin", "polkadot", "tron", "bitcoin-cash", "chainlink", "uniswap",
    "polygon", "litecoin", "binance-usd", "leo-token", "dai", "stellar", "okb", "ethereum-classic", "monero", "cosmos",
    "bitcoin-cash-sv", "filecoin", "internet-computer", "lido-dao", "aptos", "hedera", "arbitrum", "vechain", "cronos",
    "near", "quant", "the-graph", "algorand", "optimism", "rocket-pool", "synthetix", "flow", "tezos", "aave",
    "the-sandbox", "axie-infinity"
])

def fetch_crypto_list(currency="usd"):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": currency,
        "ids": POPULAR_COINS,
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "price_change_percentage": "24h"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route("/get_crypto_list", methods=["POST"])
def get_crypto_list():
    data = request.json
    currency = data.get("currency", "usd").lower()
    crypto_data = fetch_crypto_list(currency)
    
    if crypto_data:
        crypto_list = [
            {
                "name": item["name"],
                "price": item["current_price"],
                "change_24h": item["price_change_percentage_24h"]
            } for item in crypto_data
        ]
        return jsonify({"status": "success", "list": crypto_list})
    else:
        return jsonify({"status": "error", "message": "Veri alınamadı!"})

if __name__ == "__main__":
    app.run(port=1337, debug=True)
