import aiohttp
import asyncio

BASE = "https://api.binance.com/api/v3"
TIMEOUT = aiohttp.ClientTimeout(total=10)

async def fetch(session, url):
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                print(f"HTTP {resp.status} for {url}")
                return None
    except asyncio.TimeoutError:
        print(f"Timeout for {url}")
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def get_top_volume_symbols(limit=100):
    url = f"{BASE}/ticker/24hr"
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        data = await fetch(session, url)
        if not data:
            return []
        usdt_pairs = []
        for item in data:
            if item['symbol'].endswith('USDT'):
                try:
                    volume = float(item['quoteVolume'])
                    usdt_pairs.append({
                        'symbol': item['symbol'],
                        'volume': volume
                    })
                except:
                    continue
        top_pairs = sorted(usdt_pairs, key=lambda x: x['volume'], reverse=True)[:limit]
        return [pair['symbol'] for pair in top_pairs]

async def get_candle(symbol, interval):
    url = f"{BASE}/klines?symbol={symbol}&interval={interval}&limit=2"
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        data = await fetch(session, url)
        if not data or len(data) < 2:
            return None, None, None
        try:
            open_price = float(data[-1][1])
            close_price = float(data[-1][4])
            change = ((close_price - open_price) / open_price) * 100
            return round(change, 2), open_price, close_price
        except:
            return None, None, None

async def get_24h_volume(symbol):
    url = f"{BASE}/ticker/24hr?symbol={symbol}"
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        data = await fetch(session, url)
        if not data:
            return 0
        try:
            return float(data['quoteVolume'])
        except:
            return 0
