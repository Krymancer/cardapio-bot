from Utils import *
from Config import API_KEY_TelegramBot
from time import sleep
from telepot import Bot, glance
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

users = []

# A Fazeres:
# - Colocar os botões de ações do bot na conversa.
# - Novas features: como por exemplo notificação automatizada.
# - Corrigir problema de fim de semana


def onChatMessage(msg):
    contentType, chatType, chatid = glance(msg)
    try:
        if contentType == 'text':  # Mensagens de texto
            if chatid not in users:
                users.append(chatid)

            command = msg['text']
            if '/start' in command or '/help' in command:  # Resposta de ajuda
                sendMessage(chatid, f'Olá {msg["from"]["first_name"]}, *seja bem vido*! :thumbsup:')
                if chatid not in users:
                    users.append(chatid)
                    # Aqui haveria uma parte de persistência do chatid, assumindo que o user deseja receber as notificações
            elif '/almoco' in command or '/janta' in command:
                sendMenu(chatid, command[1:])
            else:
                sendMessage(chatid, ':disappointed_relieved: Desculpe, não entendi o que você me falou.')
        else:  # Caso seja enviado mensagens de tipos diferentes de 'text'
            sendMessage(chatid, ':pensive: Desculpe, ainda não fui preparado para receber este tipo de mensagem.')
    except Exception as error:
        sendMessage(chatid, ':disappointed_relieved: Desculpe, ocorreu um erro ainda não tratado.')
        print(f'Ocorreu um erro ainda não tratado: {error}')


def sendMenu(chatid, typeof):
    dishes = getTodayDishes(getDate())
    default = ' \n:heavy_exclamation_mark: Contém LEITE/LACTOSE\n:bangbang: Contém GLÚTEN'

    text = f':stew: *{typeof.upper()} ({getDate()}):*\n'
    for k, v in dishes[typeof].items():
        text += f'{k}: *{v}*.\n'.replace(' /*', '*').replace('*/ ', '*')
    sendMessage(chatid, text+default, markup)


def sendMessage(chatid, text, markup=None, action=True):  # Função de envio de mensagem para o chat específico
    if action:
        bot.sendChatAction(chatid, 'typing')
        sleep(1)
    bot.sendMessage(chatid, emojize(text, use_aliases=True), parse_mode='Markdown', reply_markup=markup)


markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Confira no site.', url='http://www.sobral.ufc.br/ru/cardapio/')]])

bot = Bot(API_KEY_TelegramBot)
MessageLoop(bot, onChatMessage).run_as_thread()

# print(bot.getMe())
print('Escutando ...')

while True:
    try:
        pass
    except KeyboardInterrupt:
        print('Desligando...')
        break
