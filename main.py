from aiogram import executor
from handlers import dp
# создаем экзекутер, команда - которая пренадлежит айограм, он принимает сообщение. Пока бот не активен - сообщение пропускает (skip_updates)

async def on_start(_): # библиотека работает ассинхронно ( поэтому async)
    print('Бот запущен')

executor.start_polling(dp, skip_updates=True, on_startup=on_start)