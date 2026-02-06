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
                callback_data="rules"
            ),
            InlineKeyboardButton(
                text="💬 Поддержка",
                url="https://t.me/stellar_support_en"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "<b>Добро пожаловать в 15 Puzzle!</b>\n\n"
        "https://t.me/modern_15_bot/game",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )


# --- Правила ---
async def rules_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    rules_text = (
        "📜 <b>Правила 15 Puzzle:</b>\n\n"
        "1. Это тестовая версия игры.\n"
        "2. Прогресс может не сохраняться.\n"
        "3. Баланс и механики могут меняться.\n"
        "4. Использование багов запрещено.\n\n"
        "Полные правила будут позже."
    )

    await query.message.reply_text(
        rules_text,
        parse_mode="HTML"
    )


# --- App ---
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(rules_handler, pattern="^rules$"))

print("Bot started...")

app.run_polling(allowed_updates=Update.ALL_TYPES)