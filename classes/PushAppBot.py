import time

from . import TelegramBot


class PushAppBot(TelegramBot.TelegramBot):
    def polling(self):
        while 1:

            for message in self.getMessages():
                # -----------------------------
                # ОСНОВНАЯ ОБРАБОТКА СОБЩЕНИЙ!!!
                # -----------------------------
                self.parseMessage(message)

            time.sleep(self.repeatRequestTime)


    def parseMessage(self, message):
        print(message.text)
        # todo хранить существующих пользователей в каком-нибудь листе, чтобы не дергать каждый раз БД! (можно считывать всех юзеров единажды при запуске функции polling?)
        # Проверка, есть ли уже пользователь в БД
        if (not self.dbWorker.isUserInDB(message.chatId)):
            print('User {} not in DB. Add...'.format(message.chatId))
            self.dbWorker.addUser(message.chatId)
            pass
        else:
            print('User {} is in DB.'.format(message.chatId))


        # Проход по листу состояния пользователей
        state = self._getUserFromStateList(message.chatId)
        if (state['state']==None):
            if message.text == '/start':
                self.sendMessage(message.chatId, 'Привет! Я создан для помощи с отслеживанием статистики по отжиманиям (или чем-либо подобным)\nПросто присылай мне количество твоих отжиманий в подходе\nДля статистики - /stat')

            if message.text.isdigit():
                self.dbWorker.addStat(message.chatId, message.text)
                self.dbWorker.getStat(message.chatId)
               # self.dbWorker.getStat(message.chatId)
                pass

        # Часть парсинга, когда есть состояние
        elif state['state'] == 'someState':

            state['state'] = None