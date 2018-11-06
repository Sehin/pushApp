import time

from . import TelegramBot


class PushAppBot(TelegramBot.TelegramBot):
    def polling(self):
        while 1:

            for message in self.getMessages():
                # -----------------------------
                # ОСНОВНАЯ ОБРАБОТКА СОБЩЕНИЙ!!!
                # -----------------------------
                print(message.text)
                self.parseMessage(message)

            time.sleep(self.repeatRequestTime)


    def parseMessage(self, message):
        # Проход по листу состояния пользователей
        state = self._getUserFromStateList(message.chatId)
        if (state['state']==None):
            if message.text == '/start':
                self.sendMessage(message.chatId, 'Привет! Я создан для помощи с отслеживанием статистики по отжиманиям (или чем-либо подобным)\nПросто присылай мне количество твоих отжиманий в подходе\nДля статистики - /stat')

        # Часть парсинга, когда есть состояние
        elif state['state'] == 'someState':

            state['state'] = None