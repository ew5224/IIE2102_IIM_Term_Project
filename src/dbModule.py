
import pymysql
from datetime import datetime, timedelta

class Database():
    def __init__(self):
        self.db= pymysql.connect(host='localhost', port= 3306,
                                  user='root',
                                  password='yourpasswd',
                                  db='pro',
                                  charset='utf8')
        self.cursor= self.db.cursor(pymysql.cursors.DictCursor)



    def logcheck(self,id,password):
        sql = "select Name from USERS WHERE UserID=%s AND PW = %s"
        result = self.cursor.execute(sql,(id,password))
        name = self.cursor.fetchone()
        if result ==0:
            return False
        else :
            return True,name
        #logcheck 이후에 당연하게도 UserID 및 Name 등은 Global variable이 되어야함.

    def getRequestList(self,UserID):
        sql ="""select RequestNo, FromID, ToID, GroupID, isInvite
                from Request
                where ToID = %s"""
        self.cursor.execute(sql,(UserID))
        data = self.cursor.fetchall()
        return data

    def getGroupAvailableTime(self, GroupID, StartDate, EndDate): #TaskTerm은 주 단위로 가
        Universe = []
        for i in range(0, 7):
            for j in range(0, 23):
                Universe.append({'TaskDayOfWeek': i, 'TaskTime': j})
        sql = """select distinct TaskDayOfWeek, TaskTime
                From Group_Schedule
                WHERE TaskDate <= %s and TaskDate >= %s and UserID in
                        (select UserID
                        from Participant
                        where GroupID = %s)
                union
                select distinct ScheduleDayOfWeek, ScheduleTime
                from Personal_Schedule 
                WHERE ScheduleDate <= %s and ScheduleDate >= %s and UserID in
                        (select UserID
                        from Participant
                        where GroupID = %s)
        """
        self.cursor.execute(sql,(StartDate, EndDate, GroupID, StartDate, EndDate, GroupID))
        unavailable = self.cursor.fetchall()

        return unavailable



    def getdata (self):
        sql= """select work.Title, artist.LastName, trans.AcquisitionPrice, trans.TransactionID
                from work, artist, trans
                where trans.WorkID = work.WorkID and work.ArtistID = artist.ArtistID AND trans.CustomerID is null"""
        num=self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return num, data

    def update_work(self,TransactionID,CustomerID,DateSold,SalesPrice):
        sql= "UPDATE trans SET DateSold=%s, SalesPrice=%s, CustomerID = %s WHERE TransactionID =%s ;"
        result = self.cursor.execute(sql,(DateSold, SalesPrice, CustomerID, TransactionID))
        self.db.commit()



    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()
