import friends
import imports
import settings
import messages
import users


@settings.dp.message_handler(commands=['send'])
async def helping_sending(message: imports.types.Message):
    markup = imports.types.InlineKeyboardMarkup()
    item_yes = imports.types.InlineKeyboardButton(text="ДА", callback_data="yes")
    item_no = imports.types.InlineKeyboardButton(text="НЕТ", callback_data="no")
    markup.add(item_yes, item_no)
    await message.reply("Этот бот умеет отправлять сообщения командой /sendmessage! Желаете написать кому-то?",
                        reply_markup=markup)


@settings.dp.message_handler(commands=['help'])
async def show_help(message: imports.types.Message):
    markup_inline = imports.types.InlineKeyboardMarkup()
    item_text = imports.types.InlineKeyboardButton(text="Text", callback_data="text")
    item_delete = imports.types.InlineKeyboardButton(text="Delete", callback_data="delete")
    item_add = imports.types.InlineKeyboardButton(text="Add Friend", callback_data="add")
    item_show = imports.types.InlineKeyboardButton(text="Show Friends", callback_data="show")
    item_del_friend = imports.types.InlineKeyboardButton(text="Del Friend", callback_data="delf")
    markup_inline.add(item_text, item_delete, item_add, item_show, item_del_friend)
    await settings.bot.send_message(message.chat.id, "Привет! Это мини-мессенджер бот. Ты можешь воспользоваться "
                                                     "командами:\n /sendmessage - отправить сообщение \n /addfriend - "
                                                     "добавить друга \n /friends - посмотреть список друзей \n "
                                                     "/delete - удалить аккаунт \n /start - зарегистрироваться \n "
                                                     "/deletefriend - удалить друга",
                                    reply_markup=markup_inline)


@settings.dp.callback_query_handler(text=["add"])
async def add_button(callback: imports.types.CallbackQuery):
    await friends.add_friend(callback.message)
    await callback.answer()


@settings.dp.callback_query_handler(text=["show"])
async def show_button(callback: imports.types.CallbackQuery):
    await friends.see_friends(callback.message)
    await callback.answer()


@settings.dp.callback_query_handler(text=["delf"])
async def del_friend_button(callback: imports.types.CallbackQuery):
    await friends.delete_friend(callback.message)
    await callback.answer()


@settings.dp.callback_query_handler(text=["text"])
async def text_smb(callback: imports.types.CallbackQuery):
    await messages.show_info(callback.message)
    await callback.answer()


@settings.dp.callback_query_handler(text=["delete"])
async def delete_process(callback: imports.types.CallbackQuery):
    await users.delete_user(callback.message)
    await callback.answer()


@settings.dp.callback_query_handler(text=["yes"])
async def send_msg(callback: imports.types.CallbackQuery):
    await messages.show_info(callback.message)
    await callback.answer()


@settings.dp.callback_query_handler(text=["no"])
async def not_send_msg(callback: imports.types.CallbackQuery):
    await callback.message.reply("Очень жаль:( Если все-таки захочешь воспользоваться ботом, введи команду /info! "
                                 "До новых встреч!")
    await callback.answer()
