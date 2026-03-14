import asyncio
import json
import websockets

BINANCE_WS = "wss://stream.binance.com:9443/ws/!ticker@arr"


async def websocket_scanner(bot):

    async with websockets.connect(BINANCE_WS) as ws:

        while True:

            data = await ws.recv()
            tickers = json.loads(data)

            for ticker in tickers:

                symbol = ticker["s"]
                change = float(ticker["P"])

                if symbol.endswith("USDT"):

                    if abs(change) > 5:

                        text = f"""
🚀 PUMP DETECTED

{symbol}
24h Change: {change}%
"""

                        await bot.send_message(
                            config.CHANNEL_ID,
                            text
                        )
