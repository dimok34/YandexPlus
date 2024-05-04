import telebot
import random
import time
import subprocess
import threading
from telebot import types
from yookassa import Configuration, Payment
def start_bot():
        YOUR_CHAT_ID = 'xxxxx'
        Configuration.account_id = 'xxxxx'
        Configuration.secret_key = 'xxxxx'
        bot = telebot.TeleBot('xxxxxxx')

        @bot.message_handler(commands=['start'])
        def start(message):
            caption = "Добро пожаловать в нашего умного Телеграм бота, который поможет тебе приобрести подписку на Яндекс Плюс! 🚀"
            photopath = 'plus.jpg'
            with open(photopath, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=caption)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(text='3 месяца', callback_data='promo_3'))
                markup.add(telebot.types.InlineKeyboardButton(text='💥12 месяцев💥', callback_data='promo_12'))
                bot.send_message(message.chat.id, 'Выберите продолжительность подписки:', reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            try:
                caption = ''
                photo = ''

                if call.data == 'promo_3':
                    bot.answer_callback_query(call.id, 'Выполнено')
                    photo = open('3.jpg', 'rb')
                    caption = 'После оплаты, бот отправит вам промокод сервиса "Яндекс Плюс" сроком на 3 месяца.\n\nЧтобы воспользоваться промокодом, просто останови текущую подписку и активируй промокод в своем аккаунте на Яндексе Плюс 📲\nПосле активации промокода у вас будет личная подписка, в которую вы сможете пригласить еще 3 человек.\n\n/pay3 - купить промокод (клик)'
                elif call.data == 'promo_12':
                    bot.answer_callback_query(call.id, 'Выполнено')
                    photo = open('12.jpg', 'rb')
                    caption = 'После оплаты, бот отправит вам промокод сервиса "Яндекс Плюс" сроком на 12 месяцев.\n\nЧтобы воспользоваться промокодом, просто останови текущую подписку и активируй промокод в своем аккаунте на Яндексе Плюс 📲\nПосле активации промокода у вас будет личная подписка, в которую вы сможете пригласить еще 3 человек.\n\n/pay12 - купить промокод (клик)'

                bot.send_photo(call.message.chat.id, photo, caption=caption)

            except Exception as e:
                print(f"Ошибка: {e}")
                bot.send_message(call.chat.id, 'Произошла ошибка. \nВыполните команду /start.')

        @bot.message_handler(commands=['pay3'])
        def start_payment(message):
            def payment_thread():
                try:
                    payment = Payment.create({
                        "amount": {
                            "value": "499.00",
                            "currency": "RUB"
                        },
                        "confirmation": {
                            "type": "redirect",
                            "return_url": "https://t.me/WalleRobottbot"
                        },
                        "capture": True,
                        "description": "Оплата подписки 'Яндекс Плюс на 3 месяца'"
                    })
                    payment_url = payment.confirmation.confirmation_url
                    keyboard = types.InlineKeyboardMarkup()
                    url_button = types.InlineKeyboardButton(text='Нажми на меня', url=payment_url)
                    keyboard.add(url_button)
                    bot.send_message(message.chat.id,
                                     f"Оплатите 499 рублей, чтобы приобрести промокод, нажав на кнопку ниже:\n",
                                     reply_markup=keyboard)
                    while True:
                        payment = Payment.find_one(payment.id)
                        if payment.status == 'succeeded':
                            bot.send_message(message.chat.id, "Оплата прошла успешно!\nСейчас бот отправит вам промокод🤩")
                            time.sleep(1)
                            bot.send_message(YOUR_CHAT_ID, "У вас купили подписку за 499р")
                            promo = random.choice(get_promo_lines('promo3.txt'))
                            delete_promo_line('promo3.txt', promo)
                            bot.send_message(message.chat.id, promo)
                            bot.send_message(message.chat.id, "Приятного прослушивания💙")
                            break
                        elif payment.status == 'canceled':
                            bot.send_message(message.chat.id, "Оплата отменена!")
                            break
                        else:
                            time.sleep(5)
                except Exception as e:
                    print(f"Ошибка: {e}")
                    bot.send_message(message.chat.id, 'Произошла ошибка. \nВыполните команду /start')

            threading.Thread(target=payment_thread).start()



        @bot.message_handler(commands=['pay12'])
        def start_payment(message):
            def payment_thread():
                try:
                    payment = Payment.create({
                        "amount": {
                            "value": "1499.00",
                            "currency": "RUB"
                        },
                        "confirmation": {
                            "type": "redirect",
                            "return_url": "https://t.me/WalleRobottbot"
                        },
                        "capture": True,
                        "description": "Оплата подписки 'Яндекс Плюс на 12 месяцев'"
                    })
                    payment_url = payment.confirmation.confirmation_url
                    keyboard = types.InlineKeyboardMarkup()
                    url_button = types.InlineKeyboardButton(text='Нажми на меня', url=payment_url)
                    keyboard.add(url_button)
                    bot.send_message(message.chat.id,
                                     f"Оплатите 1499 рублей, чтобы приобрести промокод, нажав на кнопку ниже:\n",
                                     reply_markup=keyboard)
                    while True:
                        payment = Payment.find_one(payment.id)
                        if payment.status == 'succeeded':
                            bot.send_message(message.chat.id, "Оплата прошла успешно!\nСейчас бот отправит вам промокод🤩")
                            time.sleep(1)
                            bot.send_message(YOUR_CHAT_ID, "У вас купили подписку за 1499р")
                            promo = random.choice(get_promo_lines('promo12.txt'))
                            delete_promo_line('promo12.txt', promo)
                            bot.send_message(message.chat.id, promo)
                            bot.send_message(message.chat.id, "Приятного прослушивания💙")
                            break
                        elif payment.status == 'canceled':
                            bot.send_message(message.chat.id, "Оплата отменена!")
                            break
                        else:
                            time.sleep(5)
                except Exception as e:
                    print(f"Ошибка: {e}")
                    bot.send_message(message.chat.id, 'Произошла ошибка.\nВыполняю команду /start')

            threading.Thread(target=payment_thread).start()


        def get_promo_lines(filename):
            with open(filename, 'r') as file:
                lines = [line.strip() for line in file]
            return lines


        def delete_promo_line(filename, line):
            with open(filename, 'r') as f:
                lines = f.readlines()
            with open(filename, 'w') as f:
                for l in lines:
                    if l.strip() != line:
                        f.write(l)


        bot.polling()


def restart_bot():
    while True:
        try:
            start_bot()
        except Exception as e:
            print(f"Ошибка при работе бота: {e}")
            print("Перезапускаю бота...")
            subprocess.run("main.py", shell=True)


restart_bot()