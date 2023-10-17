import string
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


@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("letters+digits")
    item2 = types.KeyboardButton("letters+digits+special_chars")
    markup.add(item1, item2)
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


bot.infinity_polling()