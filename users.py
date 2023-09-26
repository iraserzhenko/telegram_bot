import imports
import settings
import database
import main


@settings.dp.message_handler(commands=['start'])
async def start_command(message: imports.types.Message):
    connect = imports.sqlite3.connect('users.db')
    cursor = connect.cursor()
    database.create_tables()
    actual_id = message.chat.id
    cursor.execute(f"SELECT id FROM logins WHERE id = {actual_id}")
    df = cursor.fetchone()
    if df is None:
        user_id = message.chat.id
        username = message.chat.username
        user_fullname = message.chat.full_name
        cursor.execute("INSERT INTO logins VALUES(?,?,?);", [user_id, username, user_fullname])
        connect.commit()
        await settings.bot.send_message(message.chat.id, "Поздравляю, ты добавлен в систему! Теперь ты можешь "
                                                         "пользоваться этим мини-мессенджером! Используй команду /help")
    else:
        await settings.bot.send_message(message.chat.id, "Такой пользователь уже есть :( Используй команду /info или "
                                                         "/help, чтобы отправить сообщение")


@settings.dp.message_handler(commands=['delete'])
async def delete_user(message: imports.types.Message):
    connect = imports.sqlite3.connect('users.db')
    cursor = connect.cursor()

    actual_id = message.chat.id
    cursor.execute(f"DELETE FROM logins WHERE id = {actual_id}")
    connect.commit()
    cursor.execute(f"DELETE FROM friend WHERE id = {actual_id}")
    connect.commit()
    await settings.bot.send_message(message.chat.id, "Поздравляю, Вы успешно удалили аккаунт! Если захотите снова "
                                                     "использовать бот, введите команду /start!")


@settings.dp.message_handler(commands=['help'])
async def helping(message: imports.types.Message):
    markup = imports.types.InlineKeyboardMarkup()
    item_yes = imports.types.InlineKeyboardButton(text="ДА", callback_data="yes")
    item_no = imports.types.InlineKeyboardButton(text="НЕТ", callback_data="no")
    markup.add(item_yes, item_no)
    await message.reply("Этот бот умеет отправлять сообщения командой /sendmessage! Желаете написать кому-то?",
                        reply_markup=markup)
