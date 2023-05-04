import imports

API_TOKEN = '6017273644:AAG3sXCRWYYBfeXb8gUPueFaJi06CtJmzXw'

storage = imports.MemoryStorage()
bot = imports.Bot(token=API_TOKEN)
dp = imports.Dispatcher(bot, storage=storage)
