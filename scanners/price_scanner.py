import asyncio
import config
from services.binance_api import get_candle, get_24h_volume
from aiogram import Bot

def format_volume(vol):
    if vol >= 1_000_000_000:
        return f"{vol/1_000_000_000:.1f}B"
    elif vol >= 1_000_000:
        return f"{vol/1_000_000:.1f}M"
    elif vol >= 1_000:
        return f"{vol/1_000:.1f}K"
    else:
        return str(vol)

async def check_symbol(bot: Bot, symbol: str, tf: str):
    try:
        change, open_price, close_price = await get_candle(symbol, tf)
        if change is None or open_price is None or close_price is None:
            return
        if abs(change) < config.PRICE_CHANGE_THRESHOLD:
            return

        volume = await get_24h_volume(symbol)
        direction = "🟢" if change > 0 else "🔴"

        def format_price(price):
            if price < 0.001:
                return f"{price:.8f}"
            elif price < 1:
                return f"{price:.6f}"
            else:
                return f"{price:.2f}"

        open_str = format_price(open_price)
        close_str = format_price(close_price)
        vol_str = format_volume(volume)

        text = f"""
{direction} *MARKET MOVE* {direction}

💎 *{symbol}*
📍 *Exchange:* Binance
📊 *Change:* {change}% ({tf})
💵 *Price:* {open_str} → {close_str}
📈 *24h Volume:* ${vol_str}
"""
        await bot.send_message(chat_id=config.CHANNEL_ID, text=text, parse_mode="Markdown")

    except Exception as e:
        print(f"Ошибка с {symbol} {tf}: {e}")

async def scanner(bot: Bot, symbols: list):
    while True:
        tasks = []
        for symbol in symbols:
            tasks.append(check_symbol(bot, symbol, "5m"))  # или config.TIMEFRAMES
        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(config.SCAN_INTERVAL)