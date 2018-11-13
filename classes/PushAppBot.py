import time

from . import TelegramBot


class PushAppBot(TelegramBot.TelegramBot):
    def polling(self):
        self.users = self.dbWorker.getUsers()
        while 1:

            for message in self.getMessages():
                # -----------------------------
                # ОСНОВНАЯ ОБРАБОТКА СОБЩЕНИЙ!!!
                # -----------------------------
                self.parseMessage(message)

            time.sleep(self.repeatRequestTime)

    def sendStat(self, chatId, stat):
        self.sendMessage(chatId, u'\U0001F4AA' + 'Статистика отжиманий (всего, в среднем за подход):\n'
                         + u'\U000026A1' + ' Сегодня: {} - {}\n'.format(stat['today'], int(stat['averageToday']))
                         + u'\U0001F32A' + ' За последние 7 дней: {} - {}\n'.format(stat['week'], int(stat['averageWeek']),)
                         + u'\U0001F317' + ' За последние 30 дней: {} - {}\n'.format(stat['month'], int(stat['averageMonth'])))

    def parseMessage(self, message):
        print(message.text)
        # todo хранить существующих пользователей в каком-нибудь листе, чтобы не дергать каждый раз БД! (можно считывать всех юзеров единажды при запуске функции polling?)
        if (message.chatId not in self.users):
            # Проверка, есть ли уже пользователь в БД
            if (not self.dbWorker.isUserInDB(message.chatId)):
                print('User {} not in DB. Add...'.format(message.chatId))
                self.dbWorker.addUser(message.chatId)
                self.users.append(message.chatId)
                pass
            else:
                print('User {} is in DB.'.format(message.chatId))


        # Проход по листу состояния пользователей
        state = self._getUserFromStateList(message.chatId)
        if (state['state']==None):
            if message.text == '/start':
                self.sendMessage(message.chatId, 'Привет! \U0000270C Я создан для помощи с отслеживанием статистики по отжиманиям (или чем-либо подобным)\nПросто присылай мне количество твоих отжиманий в подходе \U0000270D \nДля статистики - /stat')
            if message.text == '/stat':
                stat = self.dbWorker.getStat(message.chatId)
                self.sendStat(message.chatId, stat)
            if message.text == '/clear':
                self.dbWorker.deleteStats(message.chatId)
                self.sendMessage(message.chatId, 'Статистика очищена! ' + u'\U0001F44C')
                pass
            if message.text.isdigit():
                self.dbWorker.addStat(message.chatId, message.text)
                stat = self.dbWorker.getStat(message.chatId)
                self.sendStat(message.chatId, stat)
                pass

        # Часть парсинга, когда есть состояние
        elif state['state'] == 'someState':

            state['state'] = None