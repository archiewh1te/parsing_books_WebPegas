import asyncio
import uuid

from aiogram import types
from aiogram.dispatcher import FSMContext
import aiohttp
from openpyxl import Workbook
from aiogram.types import InputFile
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urljoin
from filters import IsMessagePrivate
from loader import dp, bot
from state import reg_user


@dp.message_handler(IsMessagePrivate(), commands=['старт', 'start'])
async def client_start(message: types.Message):
    await message.answer(f'Введите своё Имя: ')
    await reg_user.text.set()


@dp.message_handler(IsMessagePrivate(), state=reg_user.text)
async def hello_user(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name=answer)
    data = await state.get_data()
    user_name = data.get('name')
    await message.answer(f"Привет, {user_name}! Пожалуйста, вставьте ссылку:")
    await reg_user.url.set()


@dp.message_handler(IsMessagePrivate(), state=reg_user.url)
async def get_url(message: types.Message, state: FSMContext):
    url = message.text
    new_url = urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
    msg_search = await message.answer('🔄 Собираю информацию...')
    await asyncio.sleep(0.33)
    parsed_data = await parse_book_total(new_url)
    if parsed_data:
        excel_file = f'books/book_info_{uuid.uuid4()}.csv'
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["Название", "Цена", "Доступность", "Ссылка", "UPC", "Product Type", "Price (excl. tax)",
                      "Price (incl. tax)", "Tax", "Availability", "Number of reviews"])

        for data in parsed_data:
            row = [data.get("Название", ""),
                   data.get("Цена", ""),
                   data.get("Доступность", ""),
                   data.get("Ссылка", ""),
                   data.get("UPC", ""),
                   data.get("Product Type", ""),
                   data.get("Price (excl. tax)", ""),
                   data.get("Price (incl. tax)", ""),
                   data.get("Tax", ""),
                   data.get("Availability", ""),
                   data.get("Number of reviews", "")]
            sheet.append(row)

        workbook.save(excel_file)

        ready_file = InputFile(excel_file)
        await bot.send_document(message.chat.id, ready_file, caption='📎 Данные сохранены в формате CSV.')
    else:
        await message.answer('❌ Не удалось получить данные. Повторите попытку.')
    await msg_search.delete()
    await state.finish()


async def parse_book_total(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            books = soup.find_all("article", class_="product_pod")

            parsed_data = []
            for book in books:
                title = book.h3.a.get('title')
                price = book.find("p", class_="price_color").get_text()
                availability = "In stock" in str(book)
                links = urljoin(url, book.h3.a.get('href'))
                product_all_info = await parse_book_link(links)
                product_all_info.update({
                    "Название": title,
                    "Цена": price,
                    "Доступность": "В наличии" if availability else "Распродано",
                    "Ссылка": links
                })
                parsed_data.append(product_all_info)
            return parsed_data


async def parse_book_link(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            product_information = soup.find("table", class_="table table-striped").find_all("tr")
            product_info = {info.find('th').get_text().strip(): info.find('td').get_text().strip() for info in
                            product_information}

            return product_info
