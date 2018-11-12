import mysql.connector
from datetime import datetime

class DBWorker:
    # connection = mysql.connector.connect(user='root', password='root',
    #                                   host='localhost',
    #                                   database='csgostats',
    #                                   auth_plugin='mysql_native_password')
    connection = mysql.connector.connect(user='root', password='Da!@#$%^&*()1',
                                         host='62.109.16.63',
                                         database='pushapp',
                                         auth_plugin='mysql_native_password')
    def createNewUser(self, chat_id):
        pass

    def isUserInDB(self, chat_id):
        sql = 'select * from user where user.chat_id = {}'.format(chat_id)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        if (res == []):
            return False
        else:
            return True

    def addUser(self, chat_id):
        cursor = self.connection.cursor()
        sql = "INSERT INTO `pushapp`.`user` (`chat_id`) VALUES ('{}');".format(chat_id)
        cursor.execute(sql)
        self.connection.commit()

    def addStat(self, chat_id, count):
        cursor = self.connection.cursor()
        sql = "INSERT INTO `pushapp`.`pushup` (`user_id`, `date`, `count`) VALUES ((SELECT id from user where user.chat_id = {}), '{}', '{}');".format(chat_id, datetime.now(), count)
        cursor.execute(sql)
        self.connection.commit()

    def getStat(self, chat_id):
        cursor = self.connection.cursor()
        todaySql = "SELECT sum(count) from pushup where user_id = (SELECT id from user where user.chat_id = {}) and date BETWEEN '{} 00:00:00' AND '{} 23:59:00'".format(chat_id, datetime.now().date(), datetime.now().date())
        cursor.execute(todaySql)
        today = cursor.fetchall()[0][0]

        weekSql = "SELECT sum(count) from pushup where user_id = (SELECT id from user where user.chat_id = {}) and date BETWEEN '{} 00:00:00' AND '{} 23:59:00'".format(chat_id, datetime.now().date(), datetime.now().date())
        cursor.execute(todaySql)
        today = cursor.fetchall()[0][0]

        monthSql = "SELECT sum(count) from pushup where user_id = (SELECT id from user where user.chat_id = {}) and date BETWEEN '{} 00:00:00' AND '{} 23:59:00'".format(chat_id, datetime.now().date(), datetime.now().date())
        cursor.execute(todaySql)
        today = cursor.fetchall()[0][0]
        pass
