async def on_startup(dp):
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    from utils.logging import logging
    print('Бот запущен')

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)