import logging
import data

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
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

AREA, CITY, PHOTO, LOCATION, BIO = range(5)


def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['NYC', 'Long Island', 'Westchester', 'Hudson Valley']]

    update.message.reply_text(
        'Hi!. This is the SAR Vaccination Bot. I will attempt to find a vaccine appointment for you in your area. '
        'Send /cancel to stop.\n\n'
        'What area do you live in?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return AREA

def city(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Area of %s: %s", user.first_name, update.message.text)
    if (update.message.text == "NYC"):
        reply_keyboard = [['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']]
        update.message.reply_text(
            'Which of these boroughs do you live in?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
    elif (update.message.text == "Long Island"):
        reply_keyboard = [['Nassau', 'Suffolk']]
        update.message.reply_text(
            'Which of these counties do you live in?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

    elif (update.message.text == "Westchester"):
        reply_keyboard = [['Westchester']]
        update.message.reply_text(
            'Which of these counties do you live in?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
    elif (update.message.text == "Hudson Valley"):
        reply_keyboard = [['Dutchess', 'Orange', 'Rockland', 'Ulster']]
        update.message.reply_text(
            'Which of these counties do you live in?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

    return CITY

def gender(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'I found a few options for your area. Here is our reccomened option: '
        '\n' + data.get_title("125 Paine Avenue New Rochelle, New York", 0) + ''
        '\n Type Y if this is good or type N if you would like to view the next option',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
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
            AREA: [MessageHandler(Filters.regex('^(NYC|Long Island|Westchester|Hudson Valley)$'), city)],
            CITY: [MessageHandler(Filters.regex('^(Bronx|Brooklyn|Manhattan|Queens|Staten Island|Nassau|Suffolk|Westchester|)$'), gender)],
            PHOTO: [MessageHandler(Filters.regex('^(Y|N)$'), photo)],
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