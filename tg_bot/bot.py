import string
from random import choices
import secrets
import telebot
from telebot import types


with open("/run/secrets/capybara_token", "r") as file:
    token = file.read().strip()
bot = telebot.TeleBot(token)


def gen_passwd(alphabet: str, add_special_chars: bool, passwd_len: int) -> str:
    # generates a random password, consisting of letters, digits,
    # and maybe special characters. The password must contain at least
    # one lowercase letter, at least one uppercase letter and at least three digits.
    while True:
        passwd = ""
        for i in range(passwd_len):
            passwd += secrets.choice(alphabet)
        if (
            any(char.islower() for char in passwd)
            and any(char.isupper() for char in passwd)
            and sum(char.isdigit() for char in passwd) >= 3
        ):
            if add_special_chars:
                if sum(char in string.punctuation for char in passwd) == 2:
                    break
            else:
                break

    return passwd


def truth() -> str:
    res = choices(["тЕмур", "Онтоха"], weights=[0.95, 0.05])
    return res

def ac() -> str:
    res = choices(["все ещё Онтоха", "наверн Онтоха", "думаю Онтоха", "тЕмур ни в чем не виноват", "Онтоха полагаю", "байбак", "проныра", "филон"], weights=[0.2, 0.2, 0.2, 0.05, 0.2, 0.05, 0.05, 0.05])
    return res

@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("letters+digits")
    item2 = types.KeyboardButton("letters+digits+special_chars")
    item3 = types.KeyboardButton("Кто главный сачок")
    item4 = types.KeyboardButton("weather")
    item5 = types.KeyboardButton("Кто ответственный за акведук")
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(
        message.chat.id,
        "Use the buttons to generate a password",
        reply_markup=markup,
    )


@bot.message_handler(content_types="text")
def message_reply(message):
    if message.text == "letters+digits":
        bot.send_message(
            message.chat.id,
            gen_passwd(
                string.ascii_letters + string.digits,
                add_special_chars=False,
                passwd_len=14,
            ),
        )
    elif message.text == "letters+digits+special_chars":
        bot.send_message(
            message.chat.id,
            gen_passwd(
                string.ascii_letters + string.digits + string.punctuation,
                add_special_chars=True,
                passwd_len=14,
            ),
        )
    elif message.text == "Кто главный сачок":
        bot.send_message(message.chat.id, truth())
    elif message.text == "weather":
        with open("/usr/src/app/weather/weather.txt", "r", encoding="utf-8") as file:
            weather = file.read()
        bot.send_message(message.chat.id, weather)
    elif message.text == "Кто ответственный за акведук":
        bot.send_message(message.chat.id, ac())


bot.infinity_polling()
