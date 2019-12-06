import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TimeTable(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        def show_list():
            frame = ShowTable(parent=parent, controller=controller, db=db)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()

        b2 = Button(self, text="보기", command=show_list, width=40,
                    height=2)
        b2.grid(row=1, column=0)
        # Get your db here !


class ShowTable(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        # DB
        sql = """select *
        From Personal_Schedule
        WHERE UserID = %s AND ScheduleDayOfWeek = %s
        """
        current_date = datetime.datetime.today()
        week = current_date.isocalendar()[1]

        personal_fetch = db.executeAll(sql, (UserID, week))

        sql = """select *
        From group_Schedule
        WHERE UserID = %s AND TaskDayOfWeek = %s
        """

        group_fetch = db.executeAll(sql, (UserID, week))

        group_list = []
        for row in group_fetch:
            tempdic = {}
            tempdic["ScheduleName"] = row["TaskName"]
            tempdic["ScheduleDate"] = row["TaskDate"]
            tempdic["ScheduleTime"] = row["TaskTime"]
            group_list.append(tempdic)

        dic = []
        dic.extend(personal_fetch)
        dic.extend(group_list)

        mpl.rc('font', family='Malgun Gothic')  # Mac의 경우는 AppleGothic, 윈도우의 경우는 Malgun Gothic을 사용하면 됩니다 :)
        mpl.rc('axes', unicode_minus=False)

        fig, ax = plt.subplots()
        fig.set_size_inches(10, 5.89)

        # root = self.controller

        wdi = {
            0: "Mon",
            1: "Tue",
            2: "Wed",
            3: "Thu",
            4: "Fri",
            5: "Sat",
            6: "Sun"
        }
        colors = ['pink', 'lightgreen', 'lightblue', 'wheat', 'salmon', 'red']
        # Setting Axis x for WeekDays

        ax.set_xlim(0, 7.5)
        ax.set_ylim(0, 24)
        ax.set_yticks(range(0, 24))
        ax.set_yticklabels(range(0, 24))

        ax.yaxis.grid()
        ax.set_xticks([i + 0.5 for i in range(0, 8)])
        ax.set_xticklabels(wdi.values(), rotation=0)

        j = 0
        for row in dic:
            j += 1

            name = row["ScheduleName"]
            # print(name)
            date = row["ScheduleDate"]

            date = str(date)
            date = date.split("-")
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            dt = datetime.datetime(year, month, day)
            # will be used to measure X
            weekday = dt.weekday() + 0.5

            start = row["ScheduleTime"]
            ax.fill_between([weekday - 0.4, weekday + 0.4], [start, start], [start + 1, start + 1], color=colors[j],
                            edgecolor='k', linewidth=0.5)

            ax.text(weekday, start + 0.5, name, va="top", fontsize=15)

        chart_type = FigureCanvasTkAgg(fig, self)
        chart_type.get_tk_widget().grid(row=1, column=0)


class ScheduleList(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        def show_list():
            frame = ShowList(parent=parent, controller=controller, db=db)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()

        b2 = Button(self, text="보기", command=show_list, width=40,
                    height=2)
        b2.grid(row=1, column=0)


class ShowList(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        sql = """select *
        From Personal_Schedule
        WHERE UserID = %s
        """

        personal_fetch = db.executeAll(sql, (UserID))
        personal_list = []

        for row in personal_fetch:
            ScheduleName = row["ScheduleName"]
            ScheduleTime = row["ScheduleTime"]
            date = row["ScheduleDate"]
            date = str(date)
            date = date.split("-")
            year = str(date[0]) + "년"
            month = str(date[1]) + "월"
            day = str(date[2]) + "일"

            ScheduleName = self.truncate(ScheduleName, 10)

            result = ScheduleName + " " + year + " " + month + " " + day + " " + str(ScheduleTime) + "시"

            personal_list.append(result)

        sql = """select *
        From group_Schedule
        WHERE UserID = %s
        """

        group_fetch = db.executeAll(sql, (UserID))

        for row in group_fetch:
            ScheduleName = row["TaskName"]
            ScheduleTime = row["TaskTime"]
            date = row["TaskDate"]
            date = str(date)
            date = date.split("-")
            year = str(date[0]) + "년"
            month = str(date[1]) + "월"
            day = str(date[2]) + "일"

            ScheduleName = self.truncate(ScheduleName, 10)

            result = ScheduleName + " " + year + " " + month + " " + day + " " + str(ScheduleTime) + "시"

            personal_list.append(result)

        result_list = []
        result_list.extend(personal_fetch)
        result_list.extend(group_fetch)

        self.row_num = len(personal_fetch)

        self.result_list = result_list

        self.list = tk.Listbox(self, width=50)
        self.list.insert(0, *personal_list)
        self.print_btn = tk.Button(self, text="일정 삭제하기",
                                   command=self.exe_selection)

        self.list.grid()
        self.print_btn.grid()

    def exe_selection(self):
        selection = self.list.curselection()
        # print(selection)
        # I made temporal list incase of "Multiple choices",
        # But that wont be the case in general situations,
        # Whatever,computation is cheap.
        i = [i for i in selection][0]

        print(self.result_list[i])

        if i <= self.row_num:
            # in this case, personal schedule will be deleted
            sql = """
            delete From personal_schedule WHERE UserID=%s and ScheduleID = %s
            """
            self.db.execute(sql, (UserID, self.result_list[i]["ScheduleID"]))
        else:
            # otherwise group schedule will be deleted
            sql = """
            delete From group_schedule WHERE GroupID=%s and TaskName = %s and TaskDayOfWeek = %s and TaskTime = %s and TaskTime = %s and TaskDate = %s and UserID = %s
            """
            print(self.result_list[i]["TaskDate"])
            self.db.execute(sql, (
            self.result_list[i]["GroupID"], self.result_list[i]["TaskName"], self.result_list[i]["TaskDayOfWeek"],
            self.result_list[i]["TaskTime"], self.result_list[i]["TaskTime"], self.result_list[i]["TaskDate"], UserID))

        self.db.commit()
        # frame = ScheduleList(parent=container, controller=self.controller, db=self.db)
        # frame.grid(row=0, column=0, sticky="nsew")
        # frame.tkraise()

        self.controller.show_frame("ScheduleList")

    def truncate(self, string, length):
        if length > len(string):
            diff = length - len(string)
            for i in range(diff):
                string += " "
        return string


class AddClasses(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        label1 = Label(self, text="수업 이름")
        label1.grid(row=1, column=0)

        ScheduleNameVar = StringVar()

        ScheduleName_Entry = Entry(self, width=40, textvariable=ScheduleNameVar)
        ScheduleName_Entry.insert(END, "수업 이름을 입력해주세요")
        ScheduleName_Entry.grid(row=2, column=0)

        # print(ScheduleName_Entry)

        def show_class(name, fe_data):
            # MODES = [tk.SINGLE, tk.BROWSE, tk.MULTIPLE, tk.EXTENDED]

            temp_list = []
            for row in fe_data:
                if row["ClassName"] == name:
                    temp_list.append(
                        name + "    " + row["Major"] + "  " + row["ClassProfessor"] + "  " + str(row["GroupID"]))

            self.list = tk.Listbox(self, width=50)
            self.list.insert(0, *temp_list)
            self.print_btn = tk.Button(self, text="수업 추가하기",
                                       command=self.exe_selection)

            self.list.grid()
            self.print_btn.grid()

        def verify_class():
            name = ScheduleNameVar.get()

            print(name)

            sql = """
            select * 
            from class
            """
            # Get data from SQL
            fe_data = db.executeAll(sql)

            if name in [i["ClassName"] for i in fe_data]:
                show_class(name, fe_data)
                # print("일치확인")

            else:
                showinfo("Error", "해당 수업이 없습니다!")
                # controller.show_frame("mainPage")

        b2 = Button(self, text="검색", command=verify_class)
        b2.grid(row=9, column=0)

    def exe_selection(self):
        selection = self.list.curselection()
        # print(selection)
        # I made temporal list incase of "Multiple choices",
        # But that wont be the case in general situations,
        # Whatever,computation is cheap.
        select = [self.list.get(i) for i in selection][0]

        groupid = select.split(" ")[-1]
        sql = """INSERT INTO PARTICIPANT(GroupID, UserID, IsCaptain)
        values(%s,%s,%s)
        """
        # print(groupid, UserID)

        self.db.execute(sql, (groupid, UserID, 0))
        self.db.commit()


class MakeGroup(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        label1 = Label(self, text="그룹 이름")
        label1.grid(row=1, column=0)

        ScheduleNameVar = StringVar()

        ScheduleName_Entry = Entry(self, width=40, textvariable=ScheduleNameVar)
        ScheduleName_Entry.insert(END, "그룹 이름을 입력해주세요")
        ScheduleName_Entry.grid(row=2, column=0)

        self.groupname = ScheduleNameVar.get()

        b2 = Button(self, text="추가", command=self.exe_selection)
        b2.grid(row=9, column=0)

    def exe_selection(self):
        sql = """INSERT INTO gr0up( GroupName, IsCaptain)
        values(%s,%s)
        """
        # print(groupid, UserID)

        self.db.execute(sql, (self.groupname, 1))
        self.db.commit()

        sql = """
        SELECT GroupID
        FROM gr0up
        WHERE GroupName == (GroupName)
        values(%s)
        """

        self.db.executeAll(sql, (self.groupname))