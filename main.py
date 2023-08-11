import logging
import data

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CONTINUE, ADDRESS, VAX1, CITY, OPTION, LOCATION, BIO = range(7)


def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Continue']]
    update.message.reply_text(
        'Hi! This is the SAR Vaccination Bot. I will attempt to find a vaccine appointment for you in your area. '
        'By clicking continue you verify that you are eligible for the COVID-19 Vaccine in your area.  ',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return CONTINUE

def address(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Please enter your address: '
    )
    return ADDRESS

def vax(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    reply_keyboard = [['1', '2', '3', 'More']]

    update.message.reply_text(
        'Good News! I found a few options near you. Here are the three closest to your location: '
        '\n1️⃣ ' + data.get_title(update.message.text, 0) + ''
        '\n2️⃣ ' + data.get_title(update.message.text, 1) + ''
        '\n3️⃣ ' + data.get_title(update.message.text, 3) + ''
        '\n Type 1, 2 or 3 depending on which option you like best. For a list of new option type "more"',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return OPTION


def appointment_info(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        'Awesome! Now all you need to do is google the name of your location and make and appointment. Thanks for using the SAR High School Vaccine Finder!'
    )

    return LOCATION


def skip_photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'I bet you look great! Now, send me your location please, ' 'or send /skip.'
    )

    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    update.message.reply_text(
        'Maybe I can visit you sometime! ' 'At last, tell me something about yourself.'
    )

    return BIO


def skip_location(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text(
        'You seem a bit paranoid! ' 'At last, tell me something about yourself.'
    )

    return BIO


def bio(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONTINUE: [MessageHandler(Filters.regex('^(Continue)$'), address)],
            ADDRESS: [MessageHandler(Filters.text, vax)],
            OPTION: [MessageHandler(Filters.regex('^(1|2|3)$'), appointment_info)],
            OPTION: [MessageHandler(Filters.regex('^(More)$'), appointment_info)],
            LOCATION: [
                MessageHandler(Filters.location, location),
                CommandHandler('skip', skip_location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()