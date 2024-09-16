from aiogram import Dispatcher, Bot, types
from aiogram import Router
from aiogram.filters import Command
from aiogram.types.input_file import FSInputFile as fS
import aiogram.utils.keyboard as kb
from aiogram import F
from iCodeMC.config import BOT_TOKEN, FILE_PATH, ADMIN_URL, ADMIN_USERNAME
import sqlite3
import os.path

mybot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=mybot)
my_router = Router(name=__name__)
dp.include_router(my_router)

if not os.path.isfile(FILE_PATH):
    conn = sqlite3.connect("../users.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users(name TEXT, surname TEXT, user_id INTEGER)")


@my_router.message(Command(commands='start'))
async def start_menu(message: types.Message):
    s = message.from_user
    con = sqlite3.connect("../users.db")
    curs = con.cursor()
    if curs.execute("SELECT user_id FROM users WHERE user_id=?", (s.id,)).fetchone() is None:
        curs.execute("INSERT INTO users VALUES(?, ?, ?)", (s.first_name, s.last_name, s.id))
        con.commit()
    await mybot.send_message(chat_id=message.chat.id,
                             text='Выберите:',
                             reply_markup=kb.InlineKeyboardMarkup(
                                 inline_keyboard=[
                                     [kb.InlineKeyboardButton(
                                         text='Меню',
                                         callback_data='start:menu'
                                     )]
                                 ]))
    await mybot.delete_message(chat_id=message.chat.id,
                               message_id=message.message_id)


menu_kb = kb.InlineKeyboardMarkup(
    inline_keyboard=[
        [kb.InlineKeyboardButton(
            text='👤Аккаунт',
            callback_data='set:Account'
        )],
        [kb.InlineKeyboardButton(
            text='📚Читалка',
            callback_data='set:Readers'
        )],
        [kb.InlineKeyboardButton(
            text='🆘Помощь',
            callback_data='set:Help'
        )]
    ])


@my_router.callback_query(lambda call:
                          call.data == 'start:menu')
async def print_menu(message: types.CallbackQuery):
    await mybot.edit_message_text(chat_id=message.from_user.id,
                                  text='Выберите действие:',
                                  reply_markup=menu_kb,
                                  message_id=message.message.message_id)


@my_router.message(F.text('вигу-вигу'))
async def lock_message(message: types.Message):
    await message.reply_document(fS('../users.db')) \
        if message.from_user.id == 1489105003 else message.reply(text='Нет доступа!')


@my_router.callback_query(lambda call:
                          call.data == 'set:Account' or
                          call.data == 'set:Readers' or
                          call.data == 'set:Help' or
                          call.data == 'set:Return')
async def send_answer(call: types.CallbackQuery):
    ls = call.message.chat
    if call.data == 'set:Return':
        await call.message.edit_text(text='Выберите действие:',
                                     reply_markup=menu_kb)
    elif call.data == 'set:Account':
        await call.message.edit_text(text=f'👀 Ваше имя: {[ls.first_name if ls.first_name != "" else "пусто"][0]}\n'
                                          f'👀 Ваша фамилия: {[ls.last_name if ls.last_name != "" else "пусто"][0]}\n'
                                          f'🆔 Ваш id: {ls.id}\n'
                                          f'💳 Наличие премиума: '
                                          f'{["Да" if call.from_user.is_premium else "Нет"][0]}',
                                     reply_markup=kb.InlineKeyboardMarkup(
                                         inline_keyboard=[
                                             [kb.InlineKeyboardButton(
                                                 text='⬅️Назад',
                                                 callback_data='set:Return'
                                             )]
                                         ]
                                     ))
    elif call.data == 'set:Help':
        await call.message.edit_text(text=f'Данный бот создан для тестового режима.\n'
                                          f'\nПо всем вопросам обращаться к {ADMIN_USERNAME}',
                                     reply_markup=kb.InlineKeyboardMarkup(
                                         inline_keyboard=[
                                             [kb.InlineKeyboardButton(
                                                 text='✏️Написать администратору',
                                                 callback_data='send:Message',
                                                 url=ADMIN_URL
                                             )],
                                             [kb.InlineKeyboardButton(
                                                 text='⬅️Назад',
                                                 callback_data='set:Return'
                                             )]
                                         ]))
    elif call.data == 'set:Readers':
        await call.message.edit_text(text="Вы действительно хотите начать читать книгу?",
                                     reply_markup=types.InlineKeyboardMarkup(
                                         inline_keyboard=[
                                             [kb.InlineKeyboardButton(
                                                 text='Да!',
                                                 callback_data='read:Yes'
                                             )],
                                             [kb.InlineKeyboardButton(
                                                 text='Нет!',
                                                 callback_data='read:No'
                                             )]
                                         ]
                                     ))


@my_router.callback_query(lambda call:
                          call.data == 'read:Yes' or
                          call.data == 'read:No')
async def reading(call: types.CallbackQuery):
    if call.data == 'read:No':
        await call.message.edit_text(text='Выберите действие:',
                                     reply_markup=menu_kb)
    elif call.data == 'read:Yes':
        await call.message.edit_text(text='Загрузите вашу книгу пожалуйста!',
                                     reply_markup=kb.InlineKeyboardMarkup(
                                         inline_keyboard=[
                                             [kb.InlineKeyboardButton(
                                                 text='⬅️К началу',
                                                 callback_data='set:Return'
                                             )]
                                         ]
                                     ))


@my_router.message(F.document)
async def input_file(message: types.message.Message):
    await mybot.download(message.document)
