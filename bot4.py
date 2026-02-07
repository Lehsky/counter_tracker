import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("STELLAR_COUNTER_TOKEN")

if not BOT_TOKEN:
    raise ValueError("STELLAR_COUNTER_TOKEN is not set")


# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                text="📜 Правила",
                url="https://vldlnz.tilda.ws/apps"
            ),
            InlineKeyboardButton(
                text="💬 Поддержка",
                url="https://t.me/stellar_support_en"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "<b>Добро пожаловать в Counter Tracker!</b>\n\n"
        "https://t.me/FriendlyCounterBot/tracker",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )


# --- App ---
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot started...")

app.run_polling(allowed_updates=Update.ALL_TYPES)