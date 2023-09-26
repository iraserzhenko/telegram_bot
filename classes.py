import imports


class Form(imports.StatesGroup):
    msg = imports.State()
    username = imports.State()


class Group(imports.StatesGroup):
    mesg = imports.State()
    id = imports.State()


class Friend(imports.StatesGroup):
    friend = imports.State()


class AcceptFriend(imports.StatesGroup):
    acceptfriend = imports.State()


class DeletedFriend(imports.StatesGroup):
    nomorefriend = imports.State()
