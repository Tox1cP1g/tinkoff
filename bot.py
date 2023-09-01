import os
import datetime
import requests
import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
bot = Bot(token='6587233825:AAHviBdEnzXZf2foPU0F8SCQhcZY8GPBStw')
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
        await message.reply("Привет! Напиши мне название дизайна и я пришлю информацию")

@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        # response = requests.get('/Users/kobelev/tinkoff_cards/accounts-design.json')
        with open('accounts-design.json') as file:
            cards = json.load(file)
        for i in range(0, 321):
            name = cards[i]['card_name']  # ['5G', 'HD display', 'Dual camera']
            if name == message.text:
                await message.reply(cards[i])


    except:
        await message.reply("Проверьте название дизайна!")
        # print(response)
        # data = response.json()
        # print(data)
        # card_name = data["card_name"]
        # hash_card = data["card_hash_ID"]
        # print(card_name, hash_card)
        # humidity = data["main"]["humidity"]
        # pressure = data["main"]["pressure"]
        # wind = data["wind"]["speed"]
        # await message.reply(f"Дизайн: {card_name}\n",
        #                     f"ХЭШ: {hash_card}")


if __name__ == "__main__":
        # С помощью метода executor.start_polling опрашиваем
    # Dispatcher: ожидаем команду /start
        executor.start_polling(dp)
