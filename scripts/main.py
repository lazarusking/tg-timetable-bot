import logging
import json
from datetime import datetime, time
from telegram import Message, Chat, Bot, User
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler, Filters
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX = range(6)

Mon = InlineKeyboardButton("Mon", callback_data=str(ONE))
Tue = InlineKeyboardButton("Tue", callback_data=str(TWO))
Wed = InlineKeyboardButton("Wed", callback_data=str(THREE))
Thurs = InlineKeyboardButton("Thurs", callback_data=str(FOUR))
Fri = InlineKeyboardButton("Fri", callback_data=str(FIVE))
back = InlineKeyboardButton("❌", callback_data=str("end"))
restart = InlineKeyboardButton("🔄", callback_data=str(SIX))

with open("timetable.json") as json_file:
    timetable = json.load(json_file)
    # for p in timetable['Monday']:
    #     monday = f"id: {str(p['id'])} \n name: {p['name']} \n code: {p['code']} \n place: {p['place']} \n time: {str(p['startTime'])}-{str(p['endTime'])} \n"
    #     print(type(monday))


def start(update: Update, context: CallbackContext) -> None:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started %s the conversation.",
                user.first_name, user.id)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            Mon,
            Tue,
            Wed,
            Thurs,
            Fri,
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("CS2 Timetable ", reply_markup=reply_markup)
    # context.job_queue.run_repeating(callback_minute, interval=10, first=30,
    #                                 context=update.message.chat_id)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def start_over(update: Update, context: CallbackContext) -> None:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    keyboard = [
        [
            Mon,
            Tue,
            Wed,
            Thurs,
            Fri,
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    query.edit_message_text(
        text="CS2 Timetable", reply_markup=reply_markup)

    return FIRST


def one(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    x = []
    for p in timetable['Monday']:
        x.append(
            f"*course*:``` {p['name']}```\n*code*:``` {p['code']}```\n*place*:``` {p['place']}```\n*time*:``` {str(p['startTime'])}-{str(p['endTime'])}``` \n\n")

    query = update.callback_query
    query.answer()
    keyboard = [
        [
            Tue,
            Wed,
            Thurs,
            Fri,
            back
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f" *Monday*\n{''.join(x)}", parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

    return FIRST


def two(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    x = []
    for p in timetable['Tuesday']:
        x.append(
            f"*course*:``` {p['name']}```\n*code*:``` {p['code']}```\n*place*:``` {p['place']}```\n*time*:``` {str(p['startTime'])}-{str(p['endTime'])}``` \n\n")

    query = update.callback_query
    query.answer()
    keyboard = [
        [
            Mon,
            Wed,
            Thurs,
            Fri,
            back
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f" *Tuesday*\n{''.join(x)}", parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup
    )
    return FIRST


def three(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    x = []
    for p in timetable['Wednesday']:
        x.append(
            f"*course*:``` {p['name']}```\n*code*:``` {p['code']}```\n*place*:``` {p['place']}```\n*time*:``` {str(p['startTime'])}-{str(p['endTime'])}``` \n\n")

    query = update.callback_query
    query.answer()
    keyboard = [
        [
            Mon,
            Tue,
            Thurs,
            Fri,
            back
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"*Wednesday* \n{''.join(x)}", parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return FIRST


def four(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    x = []
    for p in timetable['Thursday']:
        x.append(
            f"*course*:``` {p['name']}```\n*code*:``` {p['code']}```\n*place*:``` {p['place']}```\n*time*:``` {str(p['startTime'])}-{str(p['endTime'])}``` \n\n")

    query = update.callback_query
    query.answer()
    keyboard = [
        [
            Mon,
            Tue,
            Wed,
            Fri,
            back
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f" *Thursday* \n{''.join(x)}", parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup
    )
    return FIRST


def five(update: Update, context: CallbackContext) -> None:
    """Show new choice of buttons"""
    x = []
    for p in timetable['Friday']:
        x.append(
            f"*course*:``` {p['name']}```\n*code*:``` {p['code']}```\n*place*:``` {p['place']}```\n*time*:``` {str(p['startTime'])}-{str(p['endTime'])}``` \n\n")

    query = update.callback_query
    query.answer()
    keyboard = [
        [
            Mon,
            Tue,
            Wed,
            Thurs,
            back
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"*Friday* \n{''.join(x)}", parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup
    )
    return FIRST


def end(update: Update, context: CallbackContext) -> None:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            restart
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="See you next time!",
                            reply_markup=reply_markup)

    # Send message with text and appended InlineKeyboard
    # update.message.reply_text("CS2 Timetable ", reply_markup=reply_markup)
    # return ConversationHandler.END
    return FIRST


# def callback_minute(context):
#     # user = update.message.from_user
#     chat_id = context.job.context
#     context.bot.send_message(
#         chat_id='500122115', text='One message every minute')


def next_course(update: Update, context: CallbackContext):
    day = datetime.utcnow().strftime("%A")
    try:
        for day in timetable[day]:
            time = datetime.now().strptime(str(day['endTime']), "%H:%M")
            # print(time)
            # print(datetime.utcnow().strptime(str(datetime.now().strftime("%H:%M")),
            #                                  "%H:%M")-time)
            current_time = datetime.strptime(
                (f"{datetime.now().hour}:{datetime.now().minute}"), "%H:%M")
            course_start_time = datetime.strptime(
                str(day['startTime']), "%H:%M")
            course_end_time = datetime.strptime(str(day['endTime']), "%H:%M")
            # print((datetime.now().time()))
            # print(datetime.utcnow().strftime(
            #     "%H:%M"))
            # print(current_time, "now...")
            # print(((day['endTime'])))

            if not((current_time >= course_start_time)):
                print(current_time, "current", course_end_time)
                update.message.reply_text(
                    f"*course*: ``` {day['name']}```\n*place*:``` {p['place']}```\n*time*: ``` {str(p['startTime'])}-{str(p['endTime'])}```", parse_mode=ParseMode.MARKDOWN)
            # print(time, ' works?')
                break
            else:
                update.message.reply_text(
                    f" ``` Nothing to see here\n No more courses for the day🏃‍♂️🛌!\n Enjoy the rest of the day😴!``` ", parse_mode=ParseMode.MARKDOWN)
    except KeyError:
        update.message.reply_text(
            f"*course*:``` F**kin' relax, it's the Weekend my dudes!!👌👌``` \n*time*: ``` All Weekend```😎", parse_mode=ParseMode.MARKDOWN_V2)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f"*Commands*\n\- /start: Starts the bot with timetable\.\n\- /tt: To view the timetable\.\n\- /next: Shows the next course for the day or not\.", parse_mode=ParseMode.MARKDOWN_V2)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")


def main():
    # Create the Updater and pass it your bot's token.
    TOKEN = "replace with your token"
    updater = Updater(
        TOKEN, use_context=True)
    j = updater.job_queue
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # j.run_repeating(callback_minute, interval=60, first=3)

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('tt', start)],
        states={
            FIRST: [
                CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
                CallbackQueryHandler(five, pattern='^' + str(FIVE) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(SIX) + '$'),
                CallbackQueryHandler(end, pattern='^' + str("end") + '$'),
            ]

        },
        fallbacks=[CommandHandler('start', start),
                   CommandHandler('tt', start)]
    )

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dispatcher.add_handler(conv_handler)
    # Start the Bot
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('next', next_course))
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
