import database
import imports
import classes
import settings


@settings.dp.message_handler(commands=['addfriend'])
async def add_friend(message: imports.types.Message):
    await settings.bot.send_message(message.chat.id, "Напиши username пользователя, "
                                                     "которого ты хочешь добавить в друзья:")
    await classes.Friend.friend.set()


@settings.dp.message_handler(state=classes.Friend.friend)
async def add_friend_id(message: imports.types.Message, state: imports.FSMContext):
    async with state.proxy() as proxy:
        proxy['friend'] = message.text
        connect = imports.sqlite3.connect('users.db')
        cursor = connect.cursor()
        database.create_tables()
        actual_id = message.chat.id
        cursor.execute("SELECT id FROM accepted WHERE id = ? and f_usn = ?", (actual_id, message.text))
        df = cursor.fetchone()
        if df is None:
            user_id = message.chat.id
            username = message.chat.username
            friend_username = message.text
            id_friend = cursor.execute("SELECT id FROM logins WHERE username = ?", (message.text,)).fetchone()
            if id_friend is None:
                await settings.bot.send_message(message.chat.id, "Этот пользователь не зарегистрирован. "
                                                                 "Отправь ему ссылку на бот, чтобы добавить его в "
                                                                 "друзья!")
            else:
                cursor.execute("INSERT INTO friends VALUES(?,?,?, ?);", [user_id, username, friend_username,
                                                                         id_friend[0]])
                connect.commit()
                await settings.bot.send_message(message.chat.id, f"Поздравляю, Вы отправили заявку в друзья "
                                                                 f"пользователю {friend_username}")
                await settings.bot.send_message(id_friend[0], f"{username} отправил Вам заявку в друзья! Если желаете "
                                                              f"ее принять, используйте команду /acceptfriend")
        else:
            await settings.bot.send_message(message.chat.id, "Такой пользователь уже есть у вас в друзьях!")
    await state.finish()


@settings.dp.message_handler(commands=['acceptfriend'])
async def accept_friend(message: imports.types.Message):
    await settings.bot.send_message(message.chat.id, "Напиши username пользователя, "
                                                     "заявку которого ты хочешь принять")
    await classes.AcceptFriend.acceptfriend.set()


@settings.dp.message_handler(state=classes.AcceptFriend.acceptfriend)
async def accept_friend_id(message: imports.types.Message, state: imports.FSMContext):
    async with state.proxy() as proxy:
        proxy['acceptfriend'] = message.text
        connect = imports.sqlite3.connect('users.db')
        cursor = connect.cursor()
        database.create_tables()
        actual_id = message.chat.id
        username = message.chat.username
        cursor.execute("SELECT id FROM friends WHERE username = ? and friend_id = ?", (message.text, actual_id))
        df = cursor.fetchone()
        if df is None:
            await settings.bot.send_message(message.chat.id, "Этот пользователь не отправлял Вам заявку:( Если хотите "
                                                             "добавить его в друзья, используйте команду /addfriend")
        else:
            id_accepted = cursor.execute("SELECT id FROM logins WHERE username = ?", (message.text,)).fetchone()
            cursor.execute("INSERT INTO friends VALUES(?,?,?, ?);", [actual_id, username, message.text,
                                                                     id_accepted[0]])
            connect.commit()
            cursor.execute("INSERT INTO accepted VALUES(?,?,?, ?);", [actual_id, username, message.text,
                                                                      id_accepted[0]])
            connect.commit()
            cursor.execute("INSERT INTO accepted VALUES(?,?,?, ?);",
                           [id_accepted[0], message.text, username, actual_id])
            connect.commit()
            await settings.bot.send_message(message.chat.id, f"Поздравляю, пользователь {message.text} добавлен в "
                                                             f"список Ваших друзей!")
            await settings.bot.send_message(id_accepted[0], f"Поздравляю, пользователь {username} принял Вашу "
                                                            f"заявку в друзья!")
    await state.finish()


@settings.dp.message_handler(commands=['friends'])
async def see_friends(message: imports.types.Message):
    connect = imports.sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("SELECT f_usn FROM accepted WHERE id = ? ", (message.chat.id,))
    your_friends = cursor.fetchall()
    friends_list = ""
    for f in your_friends:
        friends_list += f[0]
        friends_list += "\n"
    await settings.bot.send_message(message.chat.id, f"Список твоих друзей:\n {friends_list}")


@settings.dp.message_handler(commands=['deletefriend'])
async def delete_friend(message: imports.types.Message):
    await settings.bot.send_message(message.chat.id,
                                    "Введите username пользователя, которого хотите удалить из друзей:")
    await classes.DeletedFriend.nomorefriend.set()


@settings.dp.message_handler(state=classes.DeletedFriend.nomorefriend)
async def delete_friend_id(message: imports.types.Message, state: imports.FSMContext):
    async with state.proxy() as proxy:
        proxy['nomorefriend'] = message.text
        connect = imports.sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("SELECT friend_usn FROM friends WHERE id = ? and friend_usn = ?",
                       (message.chat.id, message.text))
        deleted_friend = cursor.fetchone()
        if deleted_friend is None:
            await settings.bot.send_message(message.chat.id, "Этот пользователь не находится в Вашем списке друзей:(")
        else:
            cursor.execute("DELETE FROM friends WHERE id = ? and friend_usn = ?", (message.chat.id, message.text))
            connect.commit()
            await settings.bot.send_message(message.chat.id,
                                            "Этот пользователь был успашно удален из Вашего списка друзей")
    await state.finish()
