import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

global amazon_link
Amazon_TAG = "/?tag=linm02-21"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello, I Am middle2max bot, Am here to serve about amazon products Enter : /help for more details.")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"""Hello {update.effective_user.first_name}, How can i help you? Do you want to Buy any Products in amazon?(/Yes or /No)""")

async def Yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Kindly provide the Product link to Analysis")

async def No(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"This bot is Only here to provide the Suggestions on Amazon Products by analysing the Previous Prices :)")

async def get_url(update: Update, context: CallbackContext):
    if "tag=linm02-21" in update.message.text:
        await update.message.reply_text(f"""Existing Affiliate link, Enter new one from amazon share product.""")
    elif "amzn" in update.message.text or "amazon" in update.message.text:
        amazon_link = update.message.text
        await update.message.reply_text(f"""Thank you! URL received, The Analysis on the given product is Started Successfully""")
        await update.message.reply_text(f"Your URL is ready : {amazon_link+Amazon_TAG}")
    else:
        await update.message.reply_text(f"""Accept Commands -> '/' or products links only""")

bot = ApplicationBuilder().token("6618065718:AAEK-FpTPeruUrxzZ4MXuDUFJgWT-9nYmvM").build()

bot.add_handler(CommandHandler("hello", hello))
bot.add_handler(CommandHandler("help", help))
bot.add_handler(CommandHandler("start", start))
bot.add_handler(MessageHandler(callback=get_url, filters=~filters.COMMAND))
bot.add_handler(CommandHandler("Yes", Yes))
bot.add_handler(CommandHandler("No", No))

bot.run_polling()   
