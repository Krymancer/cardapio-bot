from utils import *
from time import sleep
from telepot import Bot, glance
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from emoji import emojize, demojize

users = []

def on_chat_message(msg):
    content_type, chat_type, chat_id = glance(msg)
    try:
        if content_type == 'text':  # Mensagens de texto
            if chat_id not in users:
                users.append(chat_id)

            command = msg['text']
            command = demojize(command)

            if '/start' in command or '/help' in command:  # Resposta de ajuda
                markup = ReplyKeyboardMarkup(keyboard=[[emojize(':spaghetti: Almoço', use_aliases=True), emojize(':stew: Janta', use_aliases=True)]])
                send_message(chat_id, f'Olá {msg["from"]["first_name"]}, *seja bem vido*! :thumbsup:', markup=markup)
                if chat_id not in users:
                    users.append(chat_id)
                    # Aqui haveria uma parte de persistência do chat_id, assumindo que o user deseja receber as notificações
            elif 'almoco' in command.lower().replace('ç', 'c') or 'janta' in command.lower():  # TA para entrada pelos botões customizados
                send_menu(chat_id, demojize(command).lower().replace('ç', 'c').replace('/', '')[command.rfind(':')+1:].strip())
            else:
                send_message(chat_id, ':disappointed_relieved: Desculpe, não entendi o que você me falou.')
        else:  # Caso seja enviado mensagens de tipos diferentes de 'text'
            send_message(chat_id, ':pensive: Desculpe, ainda não fui preparado para receber este tipo de mensagem.')
    except Exception as error:
        send_message(chat_id, ':disappointed_relieved: Desculpe, ocorreu um erro ainda não tratado.')
        print(error)
        print(f'Ocorreu um erro ainda não tratado: {error}')


def send_menu(chat_id, typeof):
    dishes = get_today_dishes(get_date())
    if dishes is None:
        send_message(chat_id, ':sweat_smile: Desculpe mas não tem cardápio pra mostrar hoje, ou o site esta fora do ar? :thinking_face:')
    else:
        default = ' \n:heavy_exclamation_mark: Contém LEITE/LACTOSE\n:bangbang: Contém GLÚTEN'
        text = f':fork_and_knife_with_plate: *{typeof.upper().replace("C", "Ç")} ({get_date()}):*\n'
        for k, v in dishes[typeof].items():
            text += f'{k}: *{v}*.\n'.replace(' /*', '*').replace('*/ ', '*')
        send_message(chat_id, text + default, button)


def send_message(chat_id, text, markup=None, action=True):  # Função de envio de mensagem para o chat específico
    if action:
        bot.sendChatAction(chat_id, 'typing')
        sleep(1)
    bot.sendMessage(chat_id, emojize(text, use_aliases=True), parse_mode='Markdown', reply_markup=markup)


button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Confira no site.', url='http://www.sobral.ufc.br/ru/cardapio/')]])

bot = Bot(API_KEY_TelegramBot)
MessageLoop(bot, on_chat_message).run_as_thread()

# print(bot.getMe())
print('Escutando ...')

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        print('Desligando...')
        break
