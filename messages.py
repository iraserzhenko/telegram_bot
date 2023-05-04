import imports
import classes
import settings


@settings.dp.message_handler(commands=['sendmessage'])
async def show_info(message: imports.types.Message):
    await settings.bot.send_message(message.chat.id, "Напиши сообщение, которое хочешь отправить:")
    await classes.Form.msg.set()


@settings.dp.message_handler(state=classes.Form.msg)
async def send_message(message: imports.types.Message, state: imports.FSMContext):
    async with state.proxy() as proxy:
        proxy['msg'] = message.text
    await classes.Form.next()
    await message.reply("Кому вы хотите отправить сообщение? Напишите username пользователя (без @)")


@settings.dp.message_handler(state=classes.Form.username)
async def send_process(message: imports.types.Message, state: imports.FSMContext):
    async with state.proxy() as proxy:
        proxy['username'] = message.text

        connect = imports.sqlite3.connect("users.db")
        cursor = connect.cursor()
        cursor.execute("SELECT id FROM logins WHERE username = ?", (message.text,))
        data = cursor.fetchone()
        if data is None:
            await settings.bot.send_message(message.chat.id,
                                            "Этот пользователь не зарегистрирован, нельзя отправить сообщение"
                                            ":( Поделись с ним ссылкой на бот, чтобы общаться вместе!")
        else:
            await settings.bot.send_message(data[0], proxy['msg'])
            await settings.bot.send_message(data[0],
                                            f"Cooбщение отправлено Вам от пользователя {message.chat.username}")
            await message.reply("Сообщение отправлено!")
    await state.finish()
