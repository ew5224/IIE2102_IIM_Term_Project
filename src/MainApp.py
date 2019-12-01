import tkinter as tk
from tkinter import *
from tkinter import DISABLED
from tkinter import font  as tkfont  # python 3
from tkinter import ttk
from tkinter import filedialog
import dbModule
import datetime
import tkinter.messagebox
from tkinter.messagebox import showinfo

class MainApp(tk.Tk):
    def __init__(self, db, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Linked Schedule")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.db = db
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainPage, TimeTable, ScheduleList, MakePersonalSchedule, ShowRequest, FindUser, FindGroup, Select_GroupTask_Term, Select_from_group_available):
            page_name = F.__name__
            frame = F(parent=container, controller=self, db = db)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        b1 = Button(self, text="내 시간표 보기", command = lambda :  controller.show_frame("TimeTable"),width=40,height=3)
        b2 = Button(self, text="일정보기(리스트)", command = lambda : controller.show_frame("ScheduleList"),width=40,height=3)
        b3 = Button(self, text="개인 일정 생성", command = lambda : controller.show_frame("MakePersonalSchedule"), width=40, height=3)
        b4 = Button(self, text="그룹 일정 생성", command = lambda : controller.show_frame("Select_GroupTask_Term"),width=40,height=3)
        b5 = Button(self, text="받은 초대 확인", command = lambda : controller.show_frame("ShowRequest"),width=40,height=3)
        b6 = Button(self, text="그룹원 찾기", command = lambda : controller.show_frame("FindUser"),width=40,height=3)
        b7 = Button(self, text="그룹 찾기", command = lambda : controller.show_frame("FindGroup"),width=40,height=3)

        b1.grid(row=0, column=0)
        b2.grid(row=1, column=0)
        b3.grid(row=2, column=0)
        b4.grid(row=3, column=0)
        b5.grid(row=4, column=0)
        b6.grid(row=5, column=0)
        b7.grid(row=6, column=0)


class Select_GroupTask_Term(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #self.title("과업 이름, 과업 시작일, 과업 종료일을 말해주세요")
        self.db = db
        UserID = "2015147040" # 삭제 필
        Label1 = Label(self, text = "그룹 선택", width=40, height=2)
        Label1.grid(row=1, column=0)
        sql = """Select GroupID, GroupName From Gr0up
        Where GroupID IN (Select GroupId From Participant Where UserID=%s and IsCaptain=1)
        """
        my_groups = self.db.executeAll(sql, (UserID))

        no_group = (len(my_groups) == 0)

        my_groups_dict = {}
        for group in my_groups:
            my_groups_dict[(str(group["GroupID"]) + " : " +str(group["GroupName"]))] = group["GroupID"]
        options = ["그룹을 선택해주세요"]
        dict_key = list(my_groups_dict.keys())
        for i in dict_key:
            options.append(str(i))

        var1 = StringVar(self)
        var1.set(options[0])

        option_menu = OptionMenu(self, var1, *options)
        option_menu.grid(row=2,column=0)

        Label2 = Label(self, text="과업 이름", width=40, height=2)
        Label2.grid(row=3, column=0)

        TaskNameVar = StringVar()

        Task_Name_Entry = Entry(self, width=40, textvariable = TaskNameVar)
        Task_Name_Entry.insert(END, "과업 이름을 입력해주세요")
        Task_Name_Entry.grid(row=4, column=0)

        Label3 = Label(self, text="시작날짜", width=40, height=2)
        Label3.grid(row=5, column=0)

        StartDateVar = StringVar()

        StartDate_Entry = Entry(self, width=40 ,textvariable=StartDateVar)
        StartDate_Entry.insert(END, "시작날짜를 입력해주세요(YYYY-MM-DD)")
        StartDate_Entry.grid(row=6, column=0)

        Label4 = Label(self, text="종료날짜", width=40, height=2)
        Label4.grid(row=7, column=0)

        EndDateVar = StringVar()

        EndDate_Entry = Entry(self, width=40, textvariable=EndDateVar)
        EndDate_Entry.insert(END, "종료날짜를 입력해주세요(YYYY-MM-DD)")
        EndDate_Entry.grid(row=8, column=0)

        global selected_GroupID
        global CurrentTaskName
        global selected_StartDate
        global selected_EndDate

        def confirm():
            #selected_GroupID = my_groups_dict[var1.get()]
            #TODO
            selected_GroupID = "2015147040"
            CurrentTaskName = TaskNameVar.get()
            selected_StartDate = StartDateVar.get()
            selected_EndDate = EndDateVar.get()

            controller.show_frame("Select_from_group_available")



        b1 = Button(self, text="뒤로가기",command=lambda : controller.show_frame("MainPage"), width=40,height=2)
        b2 = Button(self, text="확인", command= confirm, width=40, height=2)
        b1.grid(row=0, column=0)
        b2.grid(row=9, column=0)


class Select_from_group_available(tk.Frame):
    def __init__(self, parent, controller,db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #self.title("원하는 과업시간을 체크해주세")
        self.db = db
        rows = 24
        columns = 7

        boxes = []
        boxVars = []
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("Select_GroupTask_Term"), width=40, height=2)
        b1.grid(row=0, column=0, columnspan=12)
        label = Label(self, text = "원하는 과업시간을 체크해주세요")
        label.grid(row=1, column = 0, columnspan=12)
        for i in range(rows):
            boxVars.append([])
            for j in range(columns):
                boxVars[i].append(IntVar())
                boxVars[i][j].set(0)

        def checkRow(i):
            global boxVars, boxes
            row = boxVars[x]
            deselected = []

            for j in range(len(row)):
                if row[j].get() == 0:
                    deselected.append(j)

        def getSelected():
            selected = []
            for i in range(len(boxVars)):
                for j in range(len(boxVars[i])):
                    if boxVars[i][j].get() == 1:
                        selected.append({'TaskDayOfWeek': i, 'TaskTime': j})
            query = """INSERT INTO GROUP_TASK(GroupID, TaskName, TaskDayOfWeek, TaskTime, StartDate, EndDate)
            VALUES(%s,%s,%s,%s,%s,%s)
            """
            for selected_dict in selected:
                self.db.execute(query,(selected_GroupID, CurrentTaskName, selected_dict["TaskDayOfWeek"],
                                       selected_dict["TaskTime"],selected_StartDate, selected_EndDate))

            controller.show_frame("mainPage")

        #ExOfUnT = db.getGroupAvailableTime(selected_GroupID, selected_StartDate, selected_EndDate)
        #TODO
        ExOfUnT = [{'TaskDayOfWeek': 3, 'TaskTime': 12},
                   {'TaskDayOfWeek': 3, 'TaskTime': 13},
                   {'TaskDayOfWeek': 2, 'TaskTime': 18},
                   {'TaskDayOfWeek': 1, 'TaskTime': 18},
                   {'TaskDayOfWeek': 6, 'TaskTime': 18},
                   {'TaskDayOfWeek': 0, 'TaskTime': 6},
                   {'TaskDayOfWeek': 4, 'TaskTime': 10}]

        dayofweek = list("월 화 수 목 금 토 일".split(" "))
        for x in range(rows):  # times
            boxes.append([])
            for y in range(columns):  # dayofweek
                Label(self, text="%s" % (dayofweek[y])).grid(row=2, column=y + 1)
                Label(self, text="%s" % (x)).grid(row=x + 3, column=0)
                if {'TaskDayOfWeek': y, 'TaskTime': x} in ExOfUnT:
                    boxes[x].append(Checkbutton(self, state=DISABLED, background="#000000"))
                else:
                    boxes[x].append(Checkbutton(self, variable=boxVars[x][y]))
                boxes[x][y].grid(row=x + 3, column=y + 1)

        b = Button(self, text="확인", command=getSelected, width=10)
        b.grid(row=12, column=11)

class MakePersonalSchedule(tk.Frame):
    def __init__(self,parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        label1 = Label(self, text = "스케줄 이름")
        label1.grid(row=1, column=0)

        ScheduleNameVar = StringVar()

        ScheduleName_Entry = Entry(self, width=40, textvariable=ScheduleNameVar)
        ScheduleName_Entry.insert(END, "스케줄 이름을 입력해주세요")
        ScheduleName_Entry.grid(row=2, column=0)

        label2 = Label(self, text="스케줄 날짜")
        label2.grid(row=3, column=0)

        ScheduleDateVar = StringVar()

        ScheduleDate_Entry = Entry(self, width=40, textvariable=ScheduleDateVar)
        ScheduleDate_Entry.insert(END, "스케줄 날짜를 입력해주세요(YYYY-MM-DD)")
        ScheduleDate_Entry.grid(row=4, column=0)

        label3 = Label(self, text="스케줄 시간")
        label3.grid(row=5, column=0)

        ScheduleTimeVar = StringVar()
        ScheduleTime_Entry = Entry(self, width=40, textvariable=ScheduleTimeVar)
        ScheduleTime_Entry.insert(END, "스케줄 시작 시간을 입력해주세요(24시간 단위, 0~23)")
        ScheduleTime_Entry.grid(row=6, column=0)

        label4 = Label(self, text="스케줄 길이")
        label4.grid(row=7, column=0)

        ScheduleTermVar = StringVar()
        ScheduleTerm_Entry = Entry(self, width=40, textvariable=ScheduleTermVar)
        ScheduleTerm_Entry.insert(END, "스케줄 시간을 입력해주세요(시간 단위)")
        ScheduleTerm_Entry.grid(row=8, column=0)

        def validate_schedule():
            name = ScheduleNameVar.get()
            date = ScheduleDateVar.get()
            time = ScheduleTimeVar.get()
            term = ScheduleTermVar.get()

            print(name, date, time, term)
            term = int(term)-1
            time = int(time)
            lst = [time]
            if term!=0:
                for i in range(1,term+1):
                    lst.append(time+i)
            print(lst)
            cnt = 0
            #TODO
            UserID = "2015147040"
            sql = """select TaskTime
                From Group_Schedule
                WHERE TaskDate = %s and TaskTime = %s and UserID = %s
                union
                select ScheduleTime
                from Personal_Schedule 
                WHERE ScheduleDate = %s and ScheduleTime = %s and UserID = %s
            """

            for t in lst:
                data = db.executeAll(sql,(date, str(t), UserID, date, str(t), UserID))
                cnt += len(data)

            if cnt!=0:
                showinfo("Error", "겹치는 시간이 있습니다.")
            else:
                convert_date = datetime.datetime.strptime(date,"%Y-%m-%d").date()
                dayofweek = convert_date.weekday()
                sql = """INSERT INTO PERSONAL_SCHEDULE(UserID, ScheduleName, ScheduleDate, ScheduleDayOfWeek, ScheduleTime)
                values(%s,%s,%s,%s,%s)
                """

                for t in lst:
                    db.execute(sql,(UserID,name, date, str(dayofweek), t))

                controller.show_frame("mainPage")
        b2 = Button(self, text = "확인", command = validate_schedule)
        b2.grid(row = 9,column =0)
class TimeTable(tk.Frame):
    def __init__(self,parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

class ScheduleList(tk.Frame):
    def __init__(self,parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)



class ShowRequest(tk.Frame):
    def __init__(self,parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0,columnspan=4)
        #TODO
        UserID = "2015147040"
        request = db.getRequestList(UserID)

        label1 = Label(self, text = "요청자", width =8)
        label1.grid(row=1, column=0)
        label2 = Label(self, text="그룹명", width=8)
        label2.grid(row=1, column=1)
        label3 = Label(self, text="초대/신청여부", width=8)
        label3.grid(row=1, column=2)
        label4 = Label(self, text="수락하기", width =8)
        label4.grid(row=1, column=3)
        label5 = Label(self, text="거절하기", width =8)
        label5.grid(row=1, column=4)

        def accept(idx):
            sql = """Insert into Participant(GroupID, UserID, isCaptain)
            values(%s, %s, 0)"""
            req = request[idx]
            if int(req["isInvite"]):
                db.execute(sql,(req["GroupID"],req["ToID"]))
            else:
                db.execute(sql,(req["GroupID"],req["FromID"]))

            for item in requests_implement[idx]:
                item.destroy()
        def refuse(idx):
            req = request[idx]
            sql = """Delete From Request WHERE RequestNo =%s"""
            db.execute(sql,(req["RequestNo"]))


            for item in requests_implement[idx]:
                item.destroy()

        i = 2
        cnt = 0
        requests_implement = []

        # request = [{"RequestNo" : "1", "FromID": "2015147040", "ToID":"2015147001","GroupID":1,"isInvite":"1"},
        #            {"RequestNo" : "2", "FromID": "2015147032", "ToID":"2015147010","GroupID":2,"isInvite":"0"},
        #            {"RequestNo" : "3", "FromID": "2015147012", "ToID":"2015147012","GroupID":3,"isInvite":"1"}]
        # PersonName = ["황동영","김용우","조동규"]
        # GroupNames = ["와이빅타","산정관","야이"]

        for req in request:
            cnt +=1
            item = []
            sql = """Select Name FROM USERS WHERE UserID = %s"""
            row = db.executeOne(sql, req["FromID"])
            inviter_name = row["Name"]
            #inviter_name = PersonName[cnt-1]
            sql = """SELECT GroupName From Gr0up where GroupID = %s"""
            row = db.executeOne(sql, req["GroupID"])
            group_name = row["GroupName"]
            #group_name = GroupNames[cnt-1]

            item.append(Label(self, text = inviter_name, width = 8))
            item.append(Label(self, text = group_name, width = 8))

            if int(req["isInvite"]) :
                item.append(Label(self, text = "초대",width = 8))
            else:
                item.append(Label(self, text = "신청",width = 8))
            self.button = Button(self, text="수락", width = 8)
            self.button['command'] = lambda idx=cnt-1 : accept(idx)
            item.append(self.button)
            self.button = Button(self, text="거절", width = 8)
            self.button['command'] = lambda idx=cnt-1: refuse(idx)
            item.append(self.button)
            requests_implement.append(item)

        for kk in range(len(requests_implement)):
            requests_implement[kk][0].grid(row = i, column = 0)
            requests_implement[kk][1].grid(row = i, column = 1)
            requests_implement[kk][2].grid(row = i, column = 2)
            requests_implement[kk][3].grid(row = i, column = 3)
            requests_implement[kk][4].grid(row=i, column=4)

            i+=1



class FindUser(tk.Frame):
    def __init__(self,parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)
class FindGroup(tk.Frame):
    def __init__(self,parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)
# Create the entire GUI program
db = dbModule.Database()
program = MainApp(db)

# Start the GUI event loop
program.mainloop()