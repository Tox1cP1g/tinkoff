import os
import datetime
import requests
import json
import pathlib
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import config
# from config.py import TOKEN
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
base_dir = pathlib.Path(__file__).absolute().parent


def write_user_to_file(user_id):
    users = set()
    if os.path.exists(base_dir / "users.txt"):
        with open(base_dir / "users.txt") as log:
            for row in log.read().split("\n"):
                users.add(int(row))
    users.add(int(user_id))
    with open(base_dir / "users.txt", "w") as log:
        log.write("\n".join([str(i) for i in users]))

def comeback_hash_red (hash):
    return hash


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # buttons = ["Поиск по названию", "Поиск по хэшу"]
    # keyboard.add(*buttons)
    write_user_to_file(message.from_user.id)
    await message.reply("Привет, {0.first_name}! Отправь мне название дизайна карты <b>Тинькофф</b> для поиска подробной информации. ".format(message.from_user), parse_mode="HTML")


@dp.message_handler()
async def get_info(message: types.Message):
    try:
        # response = requests.get('/Users/kobelev/tinkoff_cards/accounts-design.json')
        with open('accounts-design.json') as file:
            cards = json.load(file)
            print(len(cards))
        for i in range(0, len(cards)):
            name = cards[i]['card_name']  # card name
            hash = cards[i]['card_hash_ID']  # hash of card
            loyality = cards[i]["premial_card"] # premium card or not
            print(name)
            if name == message.text:
                hash = cards[i]["card_hash_ID"]
                await message.reply(f'<b>Найденная информация </b>(attention!): \n'
                                    f'<b>Название: </b> <code>{cards[i]["card_name"]}</code> \n'
                                    f'<b>Хэш (hash): </b> <code>{comeback_hash_red(hash)}</code>\n'
                                    f'<b>Картинки дизайна: </b>  \n'
                                    f'<b>real:</b> {cards[i]["images"]["real"]} \n'
                                    f'<b>big:</b> {cards[i]["images"]["big"]} \n'
                                    f'<b>small:</b> {cards[i]["images"]["small"]} \n'
                                    f'Премиальная ли карта? = <b>{cards[i]["premial_card"]}</b> \n'
                                    f'Программа лояльности: <b>{cards[i]["baseLoyalty"]}</b>', parse_mode='HTML')
            # elif hash == message.text:
            #     await message.reply(f'<b>Найденная информация </b>(attention!): \n'
            #                         f'<b>Название: </b> <code>{cards[i]["card_name"]}</code> \n'
            #                         f'<b>Хэш (hash): </b> <code>{comeback_hash_red(hash)}</code>\n'
            #                         f'<b>Картинки дизайна: </b>  \n'
            #                         f'<b>real:</b> {cards[i]["images"]["real"]} \n'
            #                         f'<b>big:</b> {cards[i]["images"]["big"]} \n'
            #                         f'<b>small:</b> {cards[i]["images"]["small"]} \n'
            #                         f'Премиальная ли карта? = <b>{cards[i]["premial_card"]}</b> \n'
            #                         f'Программа лояльности: <b>{cards[i]["baseLoyalty"]}</b>', parse_mode='HTML')
            # elif loyality == message.text:
            #     await message.reply(f'<b>Найденная информация </b>(attention!): \n'
            #                         f'<b>Название: </b> <code>{cards[i]["card_name"]}</code> \n'
            #                         f'<b>Хэш (hash): </b> <code>{comeback_hash_red(hash)}</code>\n'
            #                         f'<b>Картинки дизайна: </b>  \n'
            #                         f'<b>real:</b> {cards[i]["images"]["real"]} \n'
            #                         f'<b>big:</b> {cards[i]["images"]["big"]} \n'
            #                         f'<b>small:</b> {cards[i]["images"]["small"]} \n'
            #                         f'Премиальная ли карта? = <b>{cards[i]["premial_card"]}</b> \n'
            #                         f'Программа лояльности: <b>{cards[i]["baseLoyalty"]}</b>', parse_mode='HTML'
    except:
        await message.reply('По данному запросу ничего найти не удалось. ')
        # # response = requests.get('/Users/kobelev/tinkoff_cards/accounts-design.json')
        # with open('accounts-design.json') as file:
        #     cards = json.load(file)
        # for i in range(0, 321):
        #
        #     if hash == message.text:
        #         # hash = cards[i]["card_hash_ID"]
        #         await message.reply(f'<b>Найденная информация </b>(attention!): \n'
        #                             f'<b>Название: </b> <code>{cards[i]["card_name"]}</code> \n'
        #                             f'<b>Хэш (hash): </b> <code>{comeback_hash_red(hash)}</code>\n'
        #                             f'<b>Картинки дизайна: </b>  \n'
        #                             f'<b>real:</b> {cards[i]["images"]["real"]} \n'
        #                             f'<b>big:</b> {cards[i]["images"]["big"]} \n'
        #                             f'<b>small:</b> {cards[i]["images"]["small"]} \n'
        #                             f'Премиальная ли карта? = <b>{cards[i]["premial_card"]}</b> \n'
        #                             f'Программа лояльности: <b>{cards[i]["baseLoyalty"]}</b>', parse_mode='HTML')        # print(response)
        # # data = response.json()
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
