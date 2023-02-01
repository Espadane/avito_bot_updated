import asyncio
import time
import aioschedule
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from config import BOT_TOKEN, ADMIN_ID, CHECK_FREQUENCY
from parser import get_posts_data
from database import *


bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start_command(msg: types.Message):
    """
        обработка команд start и help
    """
    await msg.answer('Бот который присылает объявления с avito.ru по запросу.\
 Чтобы отслеживать объявления - отправьте ссылку. Чтобы перестать - повторно\
 отправьте ссылку. Комманда "all" показывает выши ссылки.\n\
По вопросам писать @Espadane.')


@dp.message_handler(commands=['all'])
async def all_command(msg: types.Message):
    """
        обработка команды all для получения ссылок на все подписки
    """
    all_subscriptions = get_all_subscriptions()
    for subscription in all_subscriptions:
        await msg.answer(subscription.subscription,
                         disable_web_page_preview=True)


@dp.message_handler(Text)
async def text_gandler(msg: types.Message):
    """
        обработка сообщений пользователя
    """
    user_id = int(msg.from_id)
    if user_id !=int( ADMIN_ID):
        await msg.answer('Ты не авторизованный пользователь. Если хочешь\
 пользаться ботом напиши @espadane.')
    else:
        if 'avito.ru' in str(msg.text).lower():
            request_link = msg.text
            result = check_request_in_db(request_link)
            if result is None:
                insert_request_to_subscription(request_link)
                await msg.answer('Теперь мы будем следить за объявлениями по этому\
     запросу.')
            else:
                unsubscription(request_link=msg.text)
                await msg.answer('Вы отписались')
        else:
            await msg.answer('Я понимаю только ссылки на avito')


async def task():
    """
        получение новых постов с авито
    """
    all_subscriptions = get_all_subscriptions()
    if all_subscriptions != []:
        for subscription in all_subscriptions:
            request_link = subscription.subscription
            posts_data = get_posts_data(request_link)
            await send_new_posts(posts_data)


async def send_new_posts(posts_data):
    """
        отправка новых постов с авито пользователю
    """
    for post_data in posts_data:
        post_name = post_data['post_name']
        post_price = post_data['post_price']
        post_budge = post_data['post_budge']
        post_params = post_data['post_params']
        post_description = post_data['post_description']
        post_geo = post_data['post_geo']
        post_link = post_data['post_link']
        result = check_post_in_db(post_link)
        if result is None:
            await bot.send_message(ADMIN_ID,
                                   f'<a href="{post_link}">{post_name}</a>\n\
{post_price} {post_budge}\n\
{post_params}\n\
{post_description}\n\
район: {post_geo}', disable_web_page_preview=True)
            insert_post_to_posts(post_name, post_link)


async def scheduller():
    aioschedule.every(CHECK_FREQUENCY).minutes.do(task)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduller())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
