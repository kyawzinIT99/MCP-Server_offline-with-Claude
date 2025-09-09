# -----------------------------
# Local MCP Server for Crypto
# -----------------------------
from fastmcp import FastMCP
import asyncio
import httpx

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# Initialize FastMCP server
mcp = FastMCP("crypto-server")

@mcp.tool()
async def get_crypto_price(crypto_id: str, currency: str = "usd") -> str:
    url = f"{COINGECKO_BASE_URL}/simple/price"
    params = {"ids": crypto_id, "vs_currencies": currency}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if crypto_id not in data:
                return f"Crypto '{crypto_id}' not found."
            price = data[crypto_id][currency]
            return f"The current price of {crypto_id.capitalize()} is {price} {currency.upper()}."
    except Exception as e:
        return f"Error fetching price: {str(e)}"

@mcp.tool()
async def get_crypto_market_info_mock(crypto_ids: str, currency: str = "usd") -> str:
    """
    Mock tool for testing crypto market info locally.
    Returns detailed market data for one or more cryptocurrencies.
    """
    # Mock data for testing
    mock_data = {
        "bitcoin": {
            "price": 112611,
            "volume_24h": 37333114133,
            "change_24h": 1.16
        },
        "ethereum": {
            "price": 4352,
            "volume_24h": 21543321123,
            "change_24h": 2.03
        },
        "dogecoin": {
            "price": 0.068,
            "volume_24h": 432112233,
            "change_24h": -0.85
        }
    }

    result = ""
    for crypto_id in crypto_ids.split(","):
        crypto_id = crypto_id.strip().lower()
        data = mock_data.get(crypto_id)
        if not data:
            result += f"Crypto '{crypto_id}' not found in mock data.\n\n"
            continue
        result += (
            f"{crypto_id.capitalize()} ({crypto_id.upper()}):\n"
            f"Current price: {data['price']} {currency.upper()}\n"
            f"24h trading volume: {data['volume_24h']} {currency.upper()}\n"
            f"24h price change: {data['change_24h']}%\n\n"
        )

    return result.strip()


# -----------------------------
# Tool 2: Get multiple crypto market info
# -----------------------------
@mcp.tool()
async def get_crypto_market_info(crypto_ids: str, currency: str = "usd") -> str:
    """
    Get market information for one or more cryptocurrencies.
    """
    url = f"{COINGECKO_BASE_URL}/coins/markets"
    params = {
        "vs_currency": currency,
        "ids": crypto_ids,
        "order": "market_cap_desc",
        "page": 1,
        "sparkline": "false"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if not data:
                return f"No data found for '{crypto_ids}'."
            
            result = ""
            for crypto in data:
                name = crypto.get("name", "Unknown")
                symbol = crypto.get("symbol", "???").upper()
                price = crypto.get("current_price", "Unknown")
                market_cap = crypto.get("market_cap", "Unknown")
                volume = crypto.get("total_volume", "Unknown")
                change = crypto.get("price_change_percentage_24h", "Unknown")
                result += f"{name} ({symbol}): Price: {price} {currency.upper()}, Market Cap: {market_cap}, Volume(24h): {volume}, Change(24h): {change}%\n"
            return result
    except Exception as e:
        return f"Error fetching market info: {str(e)}"

# -----------------------------
# Start the MCP server
# -----------------------------
if __name__ == "__main__":
    print("Starting local MCP server for crypto tools...")
    asyncio.run(mcp.run())