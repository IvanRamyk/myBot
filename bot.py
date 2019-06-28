import telebot
import constant
cardBot = telebot.TeleBot(constant.token)
cards = dict()
card_number = 0
card_owner = ''


@cardBot.message_handler(commands=['add', 'delete', 'start', 'all'])
def add_card_number(message):
    if message.text == '/add':
        cardBot.send_message(message.from_user.id, "Введите имя")
        cardBot.register_next_step_handler(message, get_name)
    elif message.text == '/delete':
        cardBot.send_message(message.from_user.id, "Введите имя")
        cardBot.register_next_step_handler(message, delete_number)
    elif message.text == '/start':
        f = open('cards')
        while True:
            name = f.readline()
            if len(name) == 0:
                break
            card = f.readline()
            cards[name[:-1]] = card;
        f.close()  # закрываем файл
        cardBot.send_message(message.from_user.id, 'Привет, база данных карт была успешно создана')


def delete_number(message):
    if cards.get(message.text) is None:
        cardBot.send_message(message.from_user.id, 'Нет указанного вами ключа')
    else:
        del cards[message.text]
        cardBot.send_message(message.from_user.id, 'Карта была успешно удалена')


def get_name(message):
    global card_owner
    card_owner = message.text
    cardBot.send_message(message.from_user.id, "Введите номер карты")
    cardBot.register_next_step_handler(message, get_card_number)


def get_card_number(message):
    global card_owner
    global card_number
    card_number = message.text
    cards[card_owner] = card_number
    f = open('cards', 'a')
    f.write(card_owner + '\n' + card_number + '\n')
    f.close()
    cardBot.send_message(message.from_user.id, 'Номер карты успешно добавлен.')


@cardBot.message_handler(func=lambda massage: True)
def send_number(message):
    if cards.get(message.text) is None:
        cardBot.send_message(message.from_user.id, 'Нет указанного вами ключа')
    else:
        cardBot.send_message(message.from_user.id, cards[message.text])


cardBot.polling()
