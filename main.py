from classes.DBWorker import DBWorker
from classes.PushAppBot import PushAppBot

def main():
    dbWorker = DBWorker()
    bot = PushAppBot(dbWorker, '661890208:AAGM4teEYBS_R_CtfnC383uawOKk3a7Z8JQ')
    bot.polling()
    pass

if __name__=='__main__':
    main()