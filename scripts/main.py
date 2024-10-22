import json
import logging
from datetime import datetime, timezone

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from settings import (
    BOT_TOKEN,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

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

with open("timetable.json", encoding="utf-8") as json_file:
    timetable = json.load(json_file)
    # for p in timetable["Monday"]:
    #     monday = f"id: {str(p['id'])} \n name: {p['name']} \n code: {p['code']} \n place: {p['place']} \n time: {str(p['startTime'])}-{str(p['endTime'])} \n"
    #     print(monday)


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started %s the conversation.", user.first_name, user.id)
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
    await update.message.reply_text("CS2 Timetable ", reply_markup=reply_markup)
    # context.job_queue.run_repeating(callback_minute, interval=10, first=30,
    #                                 context=update.message.chat_id)
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


async def start_over(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
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
    await query.edit_message_text(text="CS2 Timetable", reply_markup=reply_markup)

    return FIRST


async def one(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """Show new choice of buttons"""
    x = []
    for p in timetable["Monday"]:
        x.append(
            f"*course*:` {p['name']}`\n*code*:` {p['code']}`\n*place*:` {p['place']}`\n*time*:` {str(p['startTime'])}-{str(p['endTime'])}` \n\n"
        )
    query = update.callback_query
    await query.answer()
    keyboard = [[Tue, Wed, Thurs, Fri, back]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f" *Monday*\n{''.join(x)}",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup,
    )

    return FIRST


async def two(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """Show new choice of buttons"""
    x = []
    for p in timetable["Tuesday"]:
        x.append(
            f"*course*:` {p['name']}`\n*code*:` {p['code']}`\n*place*:` {p['place']}`\n*time*:` {str(p['startTime'])}-{str(p['endTime'])}` \n\n"
        )

    query = update.callback_query
    await query.answer()
    keyboard = [[Mon, Wed, Thurs, Fri, back]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f" *Tuesday*\n{''.join(x)}",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup,
    )
    return FIRST


async def three(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """Show new choice of buttons"""
    x = [
        f"*course*:` {p['name']}`\n*code*:` {p['code']}`\n*place*:` {p['place']}`\n*time*:` {str(p['startTime'])}-{str(p['endTime'])}` \n\n"
        for p in timetable["Wednesday"]
    ]

    query = update.callback_query
    await query.answer()
    keyboard = [[Mon, Tue, Thurs, Fri, back]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"*Wednesday* \n{''.join(x)}",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup,
    )
    return FIRST


async def four(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """Show new choice of buttons"""
    x = []
    for p in timetable["Thursday"]:
        x.append(
            f"*course*:` {p['name']}`\n*code*:` {p['code']}`\n*place*:` {p['place']}`\n*time*:` {str(p['startTime'])}-{str(p['endTime'])}` \n\n"
        )

    query = update.callback_query
    await query.answer()
    keyboard = [[Mon, Tue, Wed, Fri, back]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f" *Thursday* \n{''.join(x)}",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup,
    )
    return FIRST


async def five(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """Show new choice of buttons"""
    x = []
    for p in timetable["Friday"]:
        x.append(
            f"*course*:` {p['name']}`\n*code*:` {p['code']}`\n*place*:` {p['place']}`\n*time*:` {str(p['startTime'])}-{str(p['endTime'])}` \n\n"
        )

    query = update.callback_query
    await query.answer()
    keyboard = [[Mon, Tue, Wed, Thurs, back]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"*Friday* \n{''.join(x)}",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=reply_markup,
    )
    return FIRST


async def end(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    await query.answer()
    keyboard = [[restart]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="See you next time!", reply_markup=reply_markup)

    # Send message with text and appended InlineKeyboard
    # update.message.reply_text("CS2 Timetable ", reply_markup=reply_markup)
    # return ConversationHandler.END
    return FIRST


async def next_course(update: Update, _):
    day = datetime.now(timezone.utc).strftime("%A")
    try:
        for day in timetable[day]:
            current_time = datetime.strptime(
                (f"{datetime.now().hour}:{datetime.now().minute}"), "%H:%M"
            )
            course_start_time = datetime.strptime(
                str(day["startTime"]).replace(" ", ""), "%H:%M"
            )
            course_end_time = datetime.strptime(
                str(day["endTime"]).replace(" ", ""), "%H:%M"
            )
            if not current_time >= course_start_time:
                print(current_time, "current", course_end_time)
                await update.message.reply_text(
                    f"*course*: ` {day['name']}`\n*place*:` {day['place']}`\n*time*: ` {str(day['startTime'])}-{str(day['endTime'])}`",
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
                # print(time, ' works?')
                break
            await update.message.reply_text(
                " ` Nothing to see here\n No more courses for the day🏃‍♂️🛌!\n Enjoy the rest of the day😴!` ",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
    except KeyError:
        await update.message.reply_text(
            "*course*:` F**kin' relax, it's the Weekend my dudes!!👌👌` \n*time*: ` All Weekend`😎",
            parse_mode=ParseMode.MARKDOWN_V2,
        )


async def help_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "*Commands*\n\\- /start: Starts the bot with timetable\\.\n\\- /tt: To view the timetable \\.\n\\- /next: Shows the next course for the day or not",
        parse_mode=ParseMode.MARKDOWN_V2,
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


def main():
    """Start the bot."""

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("tt", start)],
        states={
            FIRST: [
                CallbackQueryHandler(one, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(two, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(three, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(four, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(five, pattern="^" + str(FIVE) + "$"),
                CallbackQueryHandler(start_over, pattern="^" + str(SIX) + "$"),
                CallbackQueryHandler(end, pattern="^" + str("end") + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start), CommandHandler("tt", start)],
    )
    application.add_handler(conv_handler)

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("next", next_course))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Run the bot until the user presses Ctrl-C
    # job_queue = application.job_queue
    # job_queue.run_repeating(callback_minute, interval=5, first=5)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
