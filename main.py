import imports
import settings
import users
import help
import database
import friends
import messages
import classes


if __name__ == '__main__':
    imports.executor.start_polling(settings.dp, skip_updates=True)
