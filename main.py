import telebot
from openai import OpenAI

# Initialize the bot and DALL-E client
bot_token = 'YOUR TOKEN FROM TELEGRAM'
client = OpenAI(api_key="YOUR TOKEN FROM OPENAI")
bot = telebot.TeleBot(bot_token)

awaiting_prompt = set()


# Start handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi! What would like to do?\n\nType /generate to generate an image from prompt'
                                      '\n\nType /variation to make various pictures from initial one\n\nType /modify to modify a picture'
                                      ' from prompt')


@bot.message_handler(commands=['generate'])
def ask_for_prompt(message):
    chat_id = message.chat.id
    awaiting_prompt.add(chat_id)
    bot.send_message(chat_id, "What would you like to generate? Send /endgenerate to stop.")


@bot.message_handler(commands=['endgenerate'])
def end_generate(message):
    chat_id = message.chat.id
    if chat_id in awaiting_prompt:
        awaiting_prompt.remove(chat_id)
        bot.send_message(chat_id, "You have exited the generate mode.")


@bot.message_handler(func=lambda message: message.chat.id in awaiting_prompt)
def handle_prompt(message):
    chat_id = message.chat.id
    try:
        prompt = message.text
        response = client.images.generate(prompt=prompt, n=1, size="1024x1024")
        image_url = response.data[0].url
        bot.send_photo(chat_id, image_url)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")


# Start the bot
bot.polling(none_stop=True)
