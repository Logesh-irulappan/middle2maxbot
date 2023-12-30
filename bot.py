import re
import asyncio
import aiohttp
import concurrent.futures
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time

global amazon_link
Amazon_TAG = "/?tag=linm02-21"

def find_div_by_class_sync(site_url):
    response = requests.get(site_url)
    out = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        target_div = soup.find('div', "flex flex-col mt-4 space-y-0 md:bg-gray-50 md:dark:bg-gray-700 md:p-5 w-full lg:w-2/3")
        target_div1 = soup.find('div', class_="content-width mx-auto px-3")

        if target_div:
            p_tag = soup.find('p', class_="text-gray-500 dark:text-gray-400 text-sm")
            if p_tag:
                out.append(p_tag.text)

        if target_div1:
            out.append(target_div1.text)

    return out

async def find_div_by_class(site_url):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, find_div_by_class_sync, site_url)
    return result

async def activate_browser(amazon_link):
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(options=firefox_options)
    driver.get("https://pricehistoryapp.com")
    search_box = driver.find_element(By.CSS_SELECTOR, ".w-full.outline-none.px-5.bg-white.text-gray-800.disabled\\:bg-gray-200")
    search_box.send_keys(amazon_link)
    wait = WebDriverWait(driver, 2)
    search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".bg-secondary-600")))
    search_button.click()
    await asyncio.sleep(3)
    current_url = driver.current_url
    driver.quit()
    return current_url

async def get_full_amazon_url(shortened_url):
    response = requests.get(shortened_url, allow_redirects=False)

    if response.status_code == 301 or response.status_code == 302:
        redirected_url = response.headers['Location']
        asin = re.search(r'/dp/(\w+)', redirected_url)
        if asin:
            full_url = f'https://www.amazon.in/dp/{asin.group(1)}'
            return full_url
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello, I Am middle2max bot, Am here to serve about amazon products Enter : /help for more details.")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"""Hello {update.effective_user.first_name}, How can i help you? Do you want to Buy any Products in amazon?(/Yes or /No)""")

async def Yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Kindly provide the URL of the Product to Analysis")

async def No(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"This bot is Only here to provide the Suggestions on Amazon Products by analysing the Previous Prices :)")

async def get_url(update: Update, context: CallbackContext):
    amazon_link = update.message.text
    await update.message.reply_text(f"URL received, The Analysis is Started wait for some seconds : )")
    url_pattern = r'https?://\S+'
    match = re.search(url_pattern, amazon_link)
    if match:
        amazon_link = match.group()
    og_url = amazon_link
    if 'amzn.eu' in amazon_link:
        amazon_link = await get_full_amazon_url(amazon_link)
    ph_link = await activate_browser(amazon_link)
    fa = await find_div_by_class(ph_link)
    await update.message.reply_text(f"{fa[0]}")
    await update.message.reply_text(f"{fa[1]}")
    await update.message.reply_text(f"You can buy here : {og_url+Amazon_TAG}")

bot = ApplicationBuilder().token("6613064111:AAHif1APt8e-ssjvSiaKPrALKcnlyTKRZoc").build()

bot.add_handler(CommandHandler("hello", hello))
bot.add_handler(CommandHandler("help", help))
bot.add_handler(CommandHandler("start", start))
bot.add_handler(MessageHandler(callback=get_url, filters=~filters.COMMAND))
bot.add_handler(CommandHandler("Yes", Yes))
bot.add_handler(CommandHandler("No", No))

bot.run_polling()
