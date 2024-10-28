# import ollama
#
# qwen = 'qwen2.5-coder:7b'
# mistral_nemo = "mistral-nemo:12b"

import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

from SECRET import TELEGRAM_TOKEN, HH_RU_TOKEN

from hh_ru_api import ApiHhRu




logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Бот для запуска сбора данных с API hh.ru")


async def scrape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Сбор данных запущен...")
    job_api = ApiHhRu(token=HH_RU_TOKEN, areas=['Пермский край', 'Свердловская область', 'Приморский край'])
    job_api.fetch_and_store_vacancies()





# async def ai_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_prompt = update.message.text
#     sender_info = f"Sender ID: {update.effective_user.id}, Username: {update.effective_user.username}"
#     # Log the received message and sender's information
#     logging.info(f'Received message from {sender_info} MESSAGE: "{user_prompt}"')
#
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="Working on the answer please wait....")
#     user_prompt = update.message.text
#     response = ollama.generate(model=mistral_nemo, prompt=user_prompt)
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=response['response'])

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    scrape_handler = CommandHandler('scrape', scrape)
    application.add_handler(scrape_handler)
    # ai_answer_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), ai_answer)
    # application.add_handler(ai_answer_handler)
    application.add_handler(start_handler)

    application.run_polling()
