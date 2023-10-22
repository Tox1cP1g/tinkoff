import os
import datetime
import requests
import json
import pathlib
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import config
# from config.py import TOKEN


class Form(StatesGroup):
    first_button = State()
    second_button = State()


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
base_dir = pathlib.Path(__file__).absolute().parent
USER_INPUT = 'user_input'


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

    write_user_to_file(message.from_user.id)
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
    button1 = types.KeyboardButton('Поиск по названию')
    button2 = types.KeyboardButton('Поиск по хэшу')
    keyboard_markup.add(button1)
    keyboard_markup.add(button2)
    # await message.answer('Нажми на кнопку', reply_markup=keyboard_markup)
    # await dp.current_state(user=message.from_user.id).set_state(USER_INPUT)  # устанавливаем состояние
    await message.reply("Привет, {0.first_name}! <b>Следуй кнопкам для поиска необходимой информации.</b>".format(message.from_user), parse_mode="HTML")


@dp.message_handler(Text(equals='Поиск по названию'))
async def first_button_handler(message: types.Message):
    await Form.first_button.set()
    await message.reply("Напиши <b>название дизайна карты Тинькофф</b> для дальнейшего поиска.", parse_mode='HTML')


@dp.message_handler(Text(equals='Поиск по хэшу'))
async def first_button_handler(message: types.Message):
    await Form.second_button.set()
    await message.reply('Напиши <b>хэш дизайна карты Тинькофф</b> для дальнейшего поиска.', parse_mode='HTML')


@dp.message_handler(state=Form.first_button)
async def get_info(message: types.Message, state: FSMContext):
    name_of_card = message.text
    FLAG = False
    print(name_of_card)
    with open('accounts-design.json') as file:
        cards = json.load(file)
    for i in range(0, len(cards)):
        name = cards[i]['card_name']  # card name
        hash = cards[i]['card_hash_ID']  # hash of card
        loyality = cards[i]["premial_card"] # premium card or not
        if name == name_of_card:
            FLAG = True
                # hash = cards[i]["card_hash_ID"]
            await message.reply(f'<b>Найденная информация </b>(attention!): \n'
                                    f'<b>Название: </b> <code>{cards[i]["card_name"]}</code> \n'
                                    f'<b>Хэш (hash): </b> <code>{comeback_hash_red(hash)}</code>\n'
                                    f'<b>Картинки дизайна: </b>  \n'
                                    f'<b>real:</b> {cards[i]["images"]["real"]} \n'
                                    f'<b>big:</b> {cards[i]["images"]["big"]} \n'
                                    f'<b>small:</b> {cards[i]["images"]["small"]} \n'
                                    f'Премиальная ли карта? = <b>{cards[i]["premial_card"]}</b> \n'
                                    f'Программа лояльности: <b>{cards[i]["baseLoyalty"]}</b>', parse_mode='HTML')
            await state.finish()  # завершаем состояние

    if FLAG == False:
        await message.reply('Такого названия найдено НЕ БЫЛО. Повторите попытку, нажав соответствующую кнопку заново.')
        await state.finish()  # завершаем состояние

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
        # except:
        # await message.reply('По данному запросу ничего найти не удалось. ')
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


@dp.message_handler(state=Form.second_button)
async def get_info2(message: types.Message, state: FSMContext):
    FLAG = False
    hash_of_card = str(message.text)
    print(hash_of_card)
    with open('accounts-design.json') as file:
        cards = json.load(file)
    for i in range(0, len(cards)):
        name = cards[i]['card_name']  # card name
        hash = cards[i]['card_hash_ID']  # hash of card
        loyality = cards[i]["premial_card"] # premium card or not
        # print(hash)
        found = any(item in hash_of_card for item in hash)
        if found:
            FLAG = True
                # hash = cards[i]["card_hash_ID"]
            await message.reply(f'<b>Найденная информация </b>(attention!): \n'
                                    f'<b>Название: </b> <code>{cards[i]["card_name"]}</code> \n'
                                    f'<b>Хэш (hash): </b> <code>{comeback_hash_red(hash)}</code>\n'
                                    f'<b>Картинки дизайна: </b>  \n'
                                    f'<b>real:</b> {cards[i]["images"]["real"]} \n'
                                    f'<b>big:</b> {cards[i]["images"]["big"]} \n'
                                    f'<b>small:</b> {cards[i]["images"]["small"]} \n'
                                    f'Премиальная ли карта? = <b>{cards[i]["premial_card"]}</b> \n'
                                    f'Программа лояльности: <b>{cards[i]["baseLoyalty"]}</b>', parse_mode='HTML')
            await state.finish()  # завершаем состояние
    if FLAG == False:
        await message.reply('Такого хэша найдено НЕ БЫЛО. Повторите попытку, нажав соответствующую кнопку заново.')
        await state.finish()  # завершаем состояние


if __name__ == "__main__":
        # С помощью метода executor.start_polling опрашиваем
    # Dispatcher: ожидаем команду /start
        executor.start_polling(dp)
