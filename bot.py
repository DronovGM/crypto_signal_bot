import asyncio
from aiogram import Bot, Dispatcher
import config
from services.binance_api import get_top_volume_symbols
from scanners.price_scanner import scanner

bot = Bot(token=config.TOKEN)
dp = Dispatcher()

async def main():
    print("BOT STARTED")
    symbols = await get_top_volume_symbols(100)
    print(f"Loaded coins: {len(symbols)}")
    asyncio.create_task(scanner(bot, symbols))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())