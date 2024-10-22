import ollama

qwen = 'qwen2.5-coder:7b'
mistral_nemo = "mistral-nemo:12b"

import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

from SECRET import TOKEN





logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot powered by AI, please talk to me! Отвечаю на русском и ангийском юноу. (ПЫ.СЫ. ребята пожелейте мою видюху и счет за электроэнергию много не пишите ахвхахва)")

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    sender_info = f"Sender ID: {update.effective_user.id}, Username: {update.effective_user.username}"
    # Log the received message and sender's information
    logging.info(f'Received message from {sender_info} MESSAGE: "{user_prompt}"')

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Working on the answer please wait....")
    user_prompt = update.message.text
    response = ollama.generate(model=mistral_nemo, prompt=user_prompt)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response['response'])

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    answer_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), answer)
    application.add_handler(start_handler)
    application.add_handler(answer_handler)
    application.run_polling()
