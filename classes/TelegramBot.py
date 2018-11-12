import requests
from classes.DBWorker import DBWorker

class Message:
    text = ""
    chatId = ""
    updateId = ""
    def __init__(self, text, chatId, updateId):
        self.text = text
        self.chatId = chatId
        self.updateId = updateId

class TelegramBot():
    URL = 'https://api.telegram.org/bot'
    offsetId = 1
    repeatRequestTime = 1

    usersState = []
    #users = DBWorker.getUsers()

    def __init__(self, dbWorker, token):
        self.dbWorker = dbWorker
        self.token = token

    def getUpdates(self):
        url = self.URL + self.token + '/getupdates?offset=' + str(self.offsetId)
        answer = requests.get(url)
        return answer.json()

    def getMessages(self):
        # take last msg update id and set it to offsetId + 1
        data = self.getUpdates()
        messages = list()
        for message in data["result"]:
            messages.append(Message(message["message"]["text"],
                                        str(message["message"]["chat"]["id"]),
                                        message["update_id"]))
        if data["result"] != []:
            self.offsetId = int(data["result"][-1]["update_id"]) + 1
        return messages

    def sendMessage(self, chat_id, text):
        url = self.URL + self.token + '/sendmessage?chat_id={}&text={}'.format(chat_id, text)
        requests.get(url)

    def sendMsgToAllUsers(self, text, users):
        for user in users:
            self.sendMessage(user, text)

    '''
    Функция возвращает состояние для конкретного пользователя
    '''
    def _getUserFromStateList(self, chat_id):
        for state in self.usersState:
            if (chat_id == state['chat_id']):
                return state
        state = {'chat_id': chat_id, 'state': None}
        self.usersState.append(state)
        return state

    def _getChatIdFromList(self, chat_id):
        for user in self.users:
            if user['chatId'] == chat_id:
                return user
        return None


