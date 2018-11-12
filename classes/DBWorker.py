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
        sql = "INSERT INTO `pushapp`.`pushup` (`user_id`, `date_rec`, `count`) VALUES ((SELECT id from user where user.chat_id = {}), '{}', '{}');".format(chat_id, datetime.now(), count)
        cursor.execute(sql)
        self.connection.commit()

    def deleteStats(self, chat_id):
        cursor = self.connection.cursor()
        sql = "DELETE FROM `pushapp`.`pushup` WHERE (`user_id` = (SELECT id from user where user.chat_id = {}))".format(chat_id)
        cursor.execute(sql)
        self.connection.commit()

    def getStat(self, chat_id):
        result = {}
        cursor = self.connection.cursor()
        todaySql = "SELECT sum(count) from pushup where user_id = (SELECT id from pushapp.user where user.chat_id = {}) and date_rec BETWEEN '{} 00:00:00' AND '{} 23:59:00'".format(chat_id, datetime.now().date(), datetime.now().date())
        cursor.execute(todaySql)
        today = cursor.fetchall()[0][0]

        weekSql = "SELECT sum(count) FROM pushapp.pushup where user_id = (SELECT id from pushapp.user where user.chat_id = {}) and date_rec >= (curdate()-7) AND date_rec < (curdate() + 1)".format(chat_id)
        cursor.execute(weekSql)
        week = cursor.fetchall()[0][0]

        monthSql = "SELECT sum(count) FROM pushapp.pushup where user_id = (SELECT id from pushapp.user where user.chat_id = {}) and date_rec >= (curdate()-30) AND date_rec < (curdate() + 1)".format(chat_id)
        cursor.execute(monthSql)
        month = cursor.fetchall()[0][0]

        averageTodaySql = "SELECT sum(count)/count(*) FROM pushapp.pushup where user_id = (SELECT id from pushapp.user where user.chat_id = {}) and date_rec BETWEEN '{} 00:00:00' AND '{} 23:59:00'".format(chat_id, datetime.now().date(), datetime.now().date())
        cursor.execute(averageTodaySql)
        averageToday = cursor.fetchall()[0][0]

        averageWeekSql = "SELECT sum(count)/count(*) FROM pushapp.pushup where user_id = (SELECT id from pushapp.user where user.chat_id = {}) and date_rec >= (curdate()-7) AND date_rec < (curdate() + 1)".format(chat_id)
        cursor.execute(averageWeekSql)
        averageWeek = cursor.fetchall()[0][0]

        averageMonthSql = "SELECT sum(count)/count(*) FROM pushapp.pushup where user_id = (SELECT id from pushapp.user where user.chat_id = {}) and date_rec >= (curdate()-30) AND date_rec < (curdate() + 1)".format(chat_id)
        cursor.execute(averageMonthSql)
        averageMonth = cursor.fetchall()[0][0]
        result.update({'today': today})
        result.update({'week': week})
        result.update({'month': month})
        result.update({'averageToday': averageToday})
        result.update({'averageWeek': averageWeek})
        result.update({'averageMonth': averageMonth})
        for key in result:
            if result[key] is None:
                result[key] = 0

        #todo обойти все результаты и если они None - сделать их нулями
        return result
        pass
