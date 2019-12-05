import tkinter as tk
from tkinter import *
from tkinter import DISABLED
from tkinter import font  as tkfont  # python 3
from tkinter import ttk
from tkinter import filedialog
import pymysql
import dbModule
import datetime
import tkinter.messagebox
from tkinter.messagebox import showinfo

db = pymysql.connect(host='localhost', port=3306, user='root', password='yourpasswd', db='pro', charset='utf8')
cursor = db.cursor(pymysql.cursors.DictCursor)

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x600")

    global username
    global password
    global username_entry
    global password_entry
    global name
    global age
    global job
    global major
    global email
    global name_entry
    global age_entry
    global job_entry
    global major_entry
    global email_entry

    username = StringVar()
    password = StringVar()
    name = StringVar()
    age = StringVar()
    job = StringVar()
    major = StringVar()
    email = StringVar()

    Label(register_screen, text="계정등록", font=('맑은 고딕', 15)).pack()
    Label(register_screen, text="").pack()

    username_lable = Label(register_screen, text="ID")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()

    password_lable = Label(register_screen, text="Password")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()

    name_lable = Label(register_screen, text="이름")
    name_lable.pack()
    name_entry = Entry(register_screen, textvariable=name)
    name_entry.pack()

    age_lable = Label(register_screen, text="생년월일")
    age_lable.pack()
    age_entry = Entry(register_screen, textvariable=age)
    age_entry.pack()

    job_lable = Label(register_screen, text="직업")
    job_lable.pack()
    job_entry = Entry(register_screen, textvariable=job)
    job_entry.pack()

    major_lable = Label(register_screen, text="전공")
    major_lable.pack()
    major_entry = Entry(register_screen, textvariable=major)
    major_entry.pack()

    email_lable = Label(register_screen, text="Email")
    email_lable.pack()
    email_entry = Entry(register_screen, textvariable=email)
    email_entry.pack()

    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="white", command=register_user).pack()


def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verify).pack()


def register_user():
    username_info = username.get()
    password_info = password.get()
    name_info = name.get()
    age_info = age.get()
    name_info = name.get()
    job_info = job.get()
    major_info = major.get()
    email_info = email.get()

    User_temp = [username_info, password_info, name_info, age_info, job_info, major_info, email_info]
    #User.loc[len(User)] = User_temp #TODO

    sql_register_USERS = '''INSERT INTO users VALUES('{ID}','{password}','{name}',{age},'{job}','{major}','{email}');'''.format(
        ID=username_info, password=password_info, name=name_info, age=int(age_info), job=job_info, major=major_info,
        email=email_info)
    print(sql_register_USERS)
    cursor.execute(sql_register_USERS)
    db.commit()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="등록 성공", fg="green", font=("맑은 고딕", 15)).pack()


def login_verify():
    global username1
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    sql_call_USERS = '''SELECT * FROM USERS WHERE UserID= '{UserID}' and PW='{PW}';'''.format(UserID=username1,
                                                                                              PW=password1)
    cursor.execute(sql_call_USERS)
    global usingdata

    usingdata = cursor.fetchall()

    if len(usingdata) == 1:
        login_sucess()
        print(usingdata)

    else:
        password_not_recognized()


def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()


def password_not_recognized():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognized).pack()


def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()


def delete_login_success():
    login_success_screen.destroy()
    main_screen.destroy()
    db = dbModule.Database()
    program = MainApp(db, username1, usingdata[0]['Name'])
    program.mainloop()

def delete_password_not_recognized():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    #main_screen.grid(row=0, column=0, sticky="nsew")
    main_screen.configure(background='light yellow')
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()

    main_screen.mainloop()

def raise_frame(frame):
    frame.tkraise()

class MainApp(tk.Tk):
    def __init__(self, db, ID, Name, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Linked Schedule")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        global UserID
        global UserName

        UserID = ID
        UserName = Name
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.db = db
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)



        self.frames = {}
        for F in (MainPage, TimeTable, ScheduleList, MakePersonalSchedule, ShowRequest, FindUser, FindGroup, Select_GroupTask_Term,
                  AddEx, Lang, Licen, Intern, Cir, SelectGroup_forDeleteTask, SelectGroup_forDeleteTaskALL):
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

        b1 = Button(self, text="내 시간표 보기", command = lambda :  controller.show_frame("TimeTable"),width=40,height=2)
        b2 = Button(self, text="일정보기(리스트)", command = lambda : controller.show_frame("ScheduleList"),width=40,height=2)
        b3 = Button(self, text="개인 일정 생성", command = lambda : controller.show_frame("MakePersonalSchedule"), width=40, height=2)
        b4 = Button(self, text="그룹 일정 생성", command = lambda : controller.show_frame("Select_GroupTask_Term"),width=40,height=2)
        b5 = Button(self, text="받은 초대 확인", command = lambda : controller.show_frame("ShowRequest"),width=40,height=2)
        b6 = Button(self, text="그룹원 찾기", command = lambda : controller.show_frame("FindUser"),width=40,height=2)
        b7 = Button(self, text="그룹 찾기", command = lambda : controller.show_frame("FindGroup"),width=40,height=2)
        b8 = Button(self, text="경력 추가하기", command = lambda : controller.show_frame("AddEx"),width=40,height=2)
        b9 = Button(self, text="과업 관리하기", command = lambda : controller.show_frame("SelectGroup_forDeleteTask"),width=40,height=2)
        b10 = Button(self, text="과업(날짜별) 관리하기", command = lambda : controller.show_frame("SelectGroup_forDeleteTaskALL"),width=40,height=2)
        b1.grid(row=0, column=0)
        b2.grid(row=1, column=0)
        b3.grid(row=2, column=0)
        b4.grid(row=3, column=0)
        b5.grid(row=4, column=0)
        b6.grid(row=5, column=0)
        b7.grid(row=6, column=0)
        b8.grid(row=7, column=0)
        b9.grid(row=8, column=0)
        b10.grid(row=9,column=0)

class AddEx(tk.Frame):
    def __init__(self,parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)
        label = Label(self, text = "경력 종류를 선택해주세요", width=40, height=2)
        label.grid(row=1,column=0)
        b2 = Button(self, text="어학", command=lambda: controller.show_frame("Lang"), width=40, height=2)
        b2.grid(row=2, column=0)
        b3 = Button(self, text="자격증", command=lambda: controller.show_frame("Licen"), width=40, height=2)
        b3.grid(row=3, column=0)
        b4 = Button(self, text="인턴십", command=lambda: controller.show_frame("Intern"), width=40, height=2)
        b4.grid(row=4, column=0)
        b5 = Button(self, text="동아리/학회", command=lambda: controller.show_frame("Cir"), width=40, height=2)
        b5.grid(row=5, column=0)

class Lang(tk.Frame):
    def __init__(self,parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("AddEx"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        Label2 = Label(self, text="시험명", width=40, height=2)
        Label2.grid(row=1, column=0)

        NameVar = StringVar()

        Name_Entry = Entry(self, width=40, textvariable=NameVar)
        Name_Entry.insert(END, "어학시험명을 입력해주세요")
        Name_Entry.grid(row=2, column=0)

        Label3 = Label(self, text="점수", width=40, height=2)
        Label3.grid(row=3, column=0)

        ScoreVar = StringVar()

        Score_Entry = Entry(self, width=40, textvariable=ScoreVar)
        Score_Entry.insert(END, "시험 점수를 입력해주세요")
        Score_Entry.grid(row=4, column=0)

        Label4 = Label(self, text="취득일(YYYY-MM-DD, 공란가능)", width=40, height=2)
        Label4.grid(row=5, column=0)

        IssueVar = StringVar()

        Issue_Entry = Entry(self, width=40, textvariable=IssueVar)
        Issue_Entry.grid(row=6, column=0)

        Label5 = Label(self, text="만료일(YYYY-MM-DD, 공란가능)", width=40, height=2)
        Label5.grid(row=7, column=0)

        ExpirationVar = StringVar()

        Expiration_Entry = Entry(self, width=40, textvariable=ExpirationVar)
        Expiration_Entry.grid(row=8, column=0)

        def confirm():
            name = NameVar.get()
            score = ScoreVar.get()
            issue = IssueVar.get()
            expir = ExpirationVar.get()

            if len(issue)!=0 and len(expir)!=0:
                query = """INSERT INTO Language(UserID, TestName, Score, IssueDate, Expiration)
                VALUES(%s,%s,%s,%s,%s)
                """

                self.db.execute(query,(UserID, name, score, issue, expir))
            elif len(issue)!=0:
                query = """INSERT INTO Language(UserID, TestName, Score, IssueDate)
                                VALUES(%s,%s,%s,%s)
                                """

                self.db.execute(query, (UserID, name, score, issue))
            elif len(expir)!=0:
                query = """INSERT INTO Language(UserID, TestName, Score, Expiration)
                                                VALUES(%s,%s,%s,%s)
                                                """

                self.db.execute(query, (UserID, name, score, expir))
            else:
                query = """INSERT INTO Language(UserID, TestName, Score)
                                                                VALUES(%s,%s,%s)
                                                                """

                self.db.execute(query, (UserID, name, score))
            showinfo("Success", "정상적으로 추가되었습니다.")
            controller.show_frame("MainPage")

        b = Button(self, text="확인", command=confirm, width=10)
        b.grid(row=10, column=0)

class Licen(tk.Frame):
    def __init__(self,parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("AddEx"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        Label2 = Label(self, text="자격증 명", width=40, height=2)
        Label2.grid(row=1, column=0)

        NameVar = StringVar()

        Name_Entry = Entry(self, width=40, textvariable=NameVar)
        Name_Entry.insert(END, "자격증 이름을 입력해주세요")
        Name_Entry.grid(row=2, column=0)

        Label3 = Label(self, text="점수(등급)", width=40, height=2)
        Label3.grid(row=3, column=0)

        ScoreVar = StringVar()

        Score_Entry = Entry(self, width=40, textvariable=ScoreVar)
        Score_Entry.insert(END, "자격증 점수(등급) 입력해주세요")
        Score_Entry.grid(row=4, column=0)

        Label4 = Label(self, text="취득일(YYYY-MM-DD, 공란가능)", width=40, height=2)
        Label4.grid(row=5, column=0)

        IssueVar = StringVar()

        Issue_Entry = Entry(self, width=40, textvariable=IssueVar)
        Issue_Entry.grid(row=6, column=0)

        Label5 = Label(self, text="만료일(YYYY-MM-DD, 공란가능)", width=40, height=2)
        Label5.grid(row=7, column=0)

        ExpirationVar = StringVar()

        Expiration_Entry = Entry(self, width=40, textvariable=ExpirationVar)
        Expiration_Entry.grid(row=8, column=0)

        def confirm():
            name = NameVar.get()
            score = ScoreVar.get()
            issue = IssueVar.get()
            expir = ExpirationVar.get()

            if len(issue)!=0 and len(expir)!=0:
                query = """INSERT INTO License(UserID, LicenseName, Score, IssueDate, Expiration)
                VALUES(%s,%s,%s,%s,%s)
                """

                self.db.execute(query,(UserID, name, score, issue, expir))
            elif len(issue)!=0:
                query = """INSERT INTO License(UserID, LicenseName, Score, IssueDate)
                                VALUES(%s,%s,%s,%s)
                                """

                self.db.execute(query, (UserID, name, score, issue))
            elif len(expir)!=0:
                query = """INSERT INTO License(UserID, LicenseName, Score, Expiration)
                                                VALUES(%s,%s,%s,%s)
                                                """

                self.db.execute(query, (UserID, name, score, expir))
            else:
                query = """INSERT INTO License(UserID, LicenseName, Score)
                                                                VALUES(%s,%s,%s)
                                                                """

                self.db.execute(query, (UserID, name, score))
            showinfo("Success","정상적으로 추가되었습니다.")
            controller.show_frame("MainPage")


        b = Button(self, text="확인", command=confirm, width=10)
        b.grid(row=10, column=0)

class Intern(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("AddEx"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        Label2 = Label(self, text="직장명", width=40, height=2)
        Label2.grid(row=1, column=0)

        NameVar = StringVar()

        Name_Entry = Entry(self, width=40, textvariable=NameVar)
        Name_Entry.insert(END, "직장 이름을 입력해주세요")
        Name_Entry.grid(row=2, column=0)

        Label3 = Label(self, text="직무", width=40, height=2)
        Label3.grid(row=3, column=0)

        PosVar = StringVar()

        Pos_Entry = Entry(self, width=40, textvariable=PosVar)
        Pos_Entry.insert(END, "직무를 입력해주세요")
        Pos_Entry.grid(row=4, column=0)

        Label4 = Label(self, text="재직기간(주단위, 공란가능)", width=40, height=2)
        Label4.grid(row=5, column=0)

        LongVar = StringVar()

        Long_Entry = Entry(self, width=40, textvariable=LongVar)
        Long_Entry.grid(row=6, column=0)

        def confirm():
            name = NameVar.get()
            pos = PosVar.get()
            long = LongVar.get()

            if len(long) != 0 :
                query = """INSERT INTO INTERNSHIP(UserID, CompanyName, Position, HowLong)
                VALUES(%s,%s,%s,%s)
                """

                self.db.execute(query, (UserID, name, pos, long))

            else:
                query = """INSERT INTO INTERNSHIP(UserID, CompanyName, Position)
                VALUES(%s,%s,%s)
                """
                self.db.execute(query, (UserID, name, pos))
            showinfo("Success", "정상적으로 추가되었습니다.")
            controller.show_frame("MainPage")

        b = Button(self, text="확인", command=confirm, width=10)
        b.grid(row=10, column=0)

class Cir(tk.Frame):
    def __init__(self,parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("AddEx"), width=40,
                    height=2)
        b1.grid(row=0, column=0)
        Label2 = Label(self, text="동아리/학회명", width=40, height=2)
        Label2.grid(row=1, column=0)

        NameVar = StringVar()

        Name_Entry = Entry(self, width=40, textvariable=NameVar)
        Name_Entry.insert(END, "동아리(학회) 이름을 입력해주세요")
        Name_Entry.grid(row=2, column=0)

        Label3 = Label(self, text="직책(공란가능)", width=40, height=2)
        Label3.grid(row=3, column=0)

        PosVar = StringVar()

        Pos_Entry = Entry(self, width=40, textvariable=PosVar)
        Pos_Entry.grid(row=4, column=0)

        Label4 = Label(self, text="활동기간(주단위, 공란가능)", width=40, height=2)
        Label4.grid(row=5, column=0)

        LongVar = StringVar()

        Long_Entry = Entry(self, width=40, textvariable=LongVar)
        Long_Entry.grid(row=6, column=0)

        def confirm():
            name = NameVar.get()
            pos = PosVar.get()
            long = LongVar.get()

            if len(long) != 0 and len(pos)!=0:
                query = """INSERT INTO Circle(UserID, CircleName, Position, HowLong)
                        VALUES(%s,%s,%s,%s)
                        """

                self.db.execute(query, (UserID, name, pos, long))
            elif len(long)!=0:
                query = """INSERT INTO Circle(UserID, CircleName, HowLong)
                                        VALUES(%s,%s,%s)
                                        """

                self.db.execute(query, (UserID, name, long))
            elif len(long)!=0:
                query = """INSERT INTO Circle(UserID, CircleName, Position)
                                        VALUES(%s,%s,%s)
                                        """

                self.db.execute(query, (UserID, name, pos))
            else:
                query = """INSERT INTO Circle(UserID, CircleName)
                        VALUES(%s,%s)
                        """
                self.db.execute(query, (UserID, name))
            showinfo("Success", "정상적으로 추가되었습니다.")
            controller.show_frame("MainPage")

        b = Button(self, text="확인", command=confirm, width=10)
        b.grid(row=10, column=0)

class Select_GroupTask_Term(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #self.title("과업 이름, 과업 시작일, 과업 종료일을 말해주세요")
        self.db = db
        #UserID = "2015147040" # 삭제 필
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

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

        Label3 = Label(self, text="과업기간", width=40, height=2)
        Label3.grid(row=5, column=0)

        TaskTermVar = StringVar()

        TaskTerm_Entry = Entry(self, width=40 ,textvariable=TaskTermVar)
        TaskTerm_Entry.insert(END, "과업 기간을 설정해주세요.(주단위)")
        TaskTerm_Entry.grid(row=6, column=0)


        global selected_GroupID
        global CurrentTaskName
        global tterm

        def confirm():
            #selected_GroupID = my_groups_dict[var1.get()]
            #TODO
            selected_GroupID = my_groups_dict[var1.get()]
            CurrentTaskName = TaskNameVar.get()
            tterm = TaskTermVar.get()
            frame = Select_from_group_available(parent=parent, controller=controller, db = db ,
                                                GID = selected_GroupID,
                                                TName = CurrentTaskName,
                                                tterm = tterm)

            frame.grid(row = 0, column = 0, sticky = "nsew")
            frame.tkraise()
            #controller.show_frame("Select_from_group_available")



        b1 = Button(self, text="뒤로가기",command=lambda : controller.show_frame("MainPage"), width=40,height=2)
        b2 = Button(self, text="확인", command= confirm, width=40, height=2)
        b1.grid(row=0, column=0)
        b2.grid(row=9, column=0)


class Select_from_group_available(tk.Frame):
    def __init__(self, parent, controller,db, GID, TName,tterm):
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
        G_ID = GID
        T_Name = TName
        T_Term = tterm

        def getSelected():
            selected = []
            for i in range(len(boxVars)):
                for j in range(len(boxVars[i])):
                    if boxVars[i][j].get() == 1:
                        selected.append({'TaskDayOfWeek': j+1, 'TaskTime': i})
            query = """INSERT INTO GROUP_TASK(GroupID, TaskName, TaskDayOfWeek, TaskTime, TaskTerm)
            VALUES(%s,%s,%s,%s,%s)
            """
            for selected_dict in selected:
                self.db.execute(query,(G_ID, T_Name, selected_dict["TaskDayOfWeek"],
                                       selected_dict["TaskTime"],T_Term))
                print(G_ID, T_Name, selected_dict["TaskDayOfWeek"],
                                       selected_dict["TaskTime"],T_Term)
            showinfo("Success", "정상적으로 추가되었습니다.")
            controller.show_frame("MainPage")
        now_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
        end_date = (datetime.datetime.now() + datetime.timedelta(days=7*int(T_Term))).strftime("%Y-%m-%d")
        ExOfUnT = db.getGroupAvailableTime(G_ID, now_date, end_date)

        # ExOfUnT = [{'TaskDayOfWeek': 3, 'TaskTime': 12},
        #            {'TaskDayOfWeek': 3, 'TaskTime': 13},
        #            {'TaskDayOfWeek': 2, 'TaskTime': 18},
        #            {'TaskDayOfWeek': 1, 'TaskTime': 18},
        #            {'TaskDayOfWeek': 6, 'TaskTime': 18},
        #            {'TaskDayOfWeek': 0, 'TaskTime': 6},
        #            {'TaskDayOfWeek': 4, 'TaskTime': 10}]
        print(ExOfUnT)
        dayofweek = list("일 월 화 수 목 금 토".split(" "))
        for x in range(rows):  # times
            boxes.append([])
            for y in range(columns):  # dayofweek
                Label(self, text="%s" % (dayofweek[y])).grid(row=2, column=y + 1)
                Label(self, text="%s" % (x)).grid(row=x + 3, column=0)
                #print(y+1,x)
                if {'TaskDayOfWeek': y+1, 'TaskTime': x} in ExOfUnT:
                    #print("Disable!")
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
            #UserID = "2015147040"
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
                dayofweek = (convert_date.weekday()+2)%8
                print(dayofweek)
                sql = """INSERT INTO PERSONAL_SCHEDULE(UserID, ScheduleName, ScheduleDate, ScheduleDayOfWeek, ScheduleTime)
                values(%s,%s,%s,%s,%s)
                """

                for t in lst:
                    db.execute(sql,(UserID,name, date, str(dayofweek), t))
                showinfo("Success", "정상적으로 추가되었습니다.")
                controller.show_frame("MainPage")
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
        #UserID = "2015147040"
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
        b1.grid(row=0, column=0,columnspan=2)

        label = Label(self, text="그룹 이름을 검색하세요", width=40)
        label.grid(row=1,column=0,columnspan=2)

        SearchVar = StringVar()

        entry = Entry(self,  width=40, textvariable=SearchVar)
        entry.grid(row=2, column=0)

        def Search():
            sql ="""SELECT GroupID, GroupName FROM GR0UP WHERE GroupName LIKE %s and
            GroupID NOT IN(SELECT GroupID FROM PARTICIPANT WHERE UserID=%s)"""

            result = db.executeAll(sql, ("%"+SearchVar.get()+"%",UserID))
            frame = SelectGroup_forRequest(parent=parent, controller=controller, db=db,
                                                result = result)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()
        button = Button(self, text="검색" , command = Search)
        button.grid(row=2,column=1)
class SelectGroup_forRequest(tk.Frame):
    def __init__(self, parent, controller, db, result):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0,columnspan=3)
        label1 = Label(self, text="그룹번호", width=8)
        label1.grid(row=1, column=0)
        label2 = Label(self, text="그룹명", width=8)
        label2.grid(row=1, column=1)
        label3 = Label(self, text="신청하기", width=8)
        label3.grid(row=1, column=2)

        i = 2
        cnt = 0
        groups_implement = []

        def request(idx):
            gt = result[idx]
            sql1 = """Select * from REQUEST WHERE FromID = %s and GroupID = %s"""
            already = db.executeAll(sql1,(UserID, gt['GroupID']))
            if len(already)!=0:
                showinfo("Error", "이미 신청하셨습니다.")
            else:
                sqlforcaptainID = """Select GroupCaptain from NoClass WHERE GroupID = %s"""
                captainID = db.executeAll(sqlforcaptainID,(gt['GroupID']))[0]['GroupCaptain']

                sql2 = """INSERT INTO Request(FromID, ToID, GroupID,isInvite,GroupName) VALUES (%s,%s,%s,%s,%s)"""
                db.execute(sql2,(UserID, captainID, gt['GroupID'], 0, gt['GroupName']))
                showinfo("Success", "정상적으로 신청되었습니다.")

        for group in result:
            cnt += 1
            item = []
            grID = group["GroupID"]
            grName = group["GroupName"]

            item.append(Label(self, text=grID, width=8))
            item.append(Label(self, text=grName, width=8))

            self.button = Button(self, text="가입 신청하기", width=8)
            self.button['command'] = lambda idx=cnt - 1: request(idx)
            item.append(self.button)
            groups_implement.append(item)

        for kk in range(len(groups_implement)):
            groups_implement[kk][0].grid(row=i, column=0)
            groups_implement[kk][1].grid(row=i, column=1)
            groups_implement[kk][2].grid(row=i, column=2)

            i += 1
class SelectGroup_forDeleteTask(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        sql = """Select GroupID, GroupName From Gr0up
                Where GroupID IN (Select GroupId From Participant Where UserID=%s and IsCaptain=1)
                """
        my_groups = self.db.executeAll(sql, (UserID))

        my_groups_dict = {}
        for group in my_groups:
            my_groups_dict[(str(group["GroupID"]) + " : " + str(group["GroupName"]))] = group["GroupID"]
        options = ["그룹을 선택해주세요"]
        dict_key = list(my_groups_dict.keys())
        for i in dict_key:
            options.append(str(i))

        var1 = StringVar(self)
        var1.set(options[0])

        option_menu = OptionMenu(self, var1, *options)
        option_menu.grid(row=2, column=0)

        def Modify_Group_Task():
            selected_GroupID = my_groups_dict[var1.get()]

            frame = DeleteGroupTask(parent=parent, controller=controller, db=db,
                                                gid = selected_GroupID)

            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()
        button = Button(self, text="확인" , command = Modify_Group_Task)
        button.grid(row=3, column=0)

class DeleteGroupTask(tk.Frame):
    def __init__(self, parent, controller, db, gid):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.GroupID = gid
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("SelectGroup_forDeleteTask"), width=40,
                    height=2)
        b1.grid(row=0, column=0, columnspan=3)

        sql = """select GroupID, TaskName, TaskDayOfWeek, TaskTime From GROUP_TASK WHERE GroupID = %s
        """

        group_task = self.db.executeAll(sql, (self.GroupID))

        label1 = Label(self, text="과업명", width=8)
        label1.grid(row=1, column=0)
        label2 = Label(self, text="요일", width=8)
        label2.grid(row=1, column=1)
        label3 = Label(self, text="시간", width=8)
        label3.grid(row=1, column=2)
        label4 = Label(self, text="삭제하기", width=8)
        label4.grid(row=1, column=3)

        def delete(idx):
            gt = group_task[idx]
            sql = """Delete From GROUP_TASK WHERE GroupID=%s and TaskName=%s and TaskDayOfWeek=%s and TaskTime=%s"""
            db.execute(sql,(self.GroupID, gt['TaskName'],gt['TaskDayOfWeek'],gt['TaskTime']))


            for item in tasks_implement[idx]:
                item.destroy()

        i = 2
        cnt = 0
        tasks_implement = []

        # request = [{"RequestNo" : "1", "FromID": "2015147040", "ToID":"2015147001","GroupID":1,"isInvite":"1"},
        #            {"RequestNo" : "2", "FromID": "2015147032", "ToID":"2015147010","GroupID":2,"isInvite":"0"},
        #            {"RequestNo" : "3", "FromID": "2015147012", "ToID":"2015147012","GroupID":3,"isInvite":"1"}]
        # PersonName = ["황동영","김용우","조동규"]
        # GroupNames = ["와이빅타","산정관","야이"]

        for gt in group_task:
            cnt += 1
            item = []
            task_name = gt["TaskName"]
            # inviter_name = PersonName[cnt-1]
            dayofweek_dict_inttokor = {2 : '월', 3: '화', 4: '수', 5: '목', 6: '금', 7:'토', 1: '일'}
            dayofweek_dict_kortoint = {'월' : 2, '화' : 3, '수' : 4, '목' : 5, '금' : 6 , '토' : 7, '일' : 1}
            task_dayofweek = dayofweek_dict_inttokor[int(gt["TaskDayOfWeek"])]
            tasktime = gt["TaskTime"]
            # group_name = GroupNames[cnt-1]

            item.append(Label(self, text=task_name, width=8))
            item.append(Label(self, text=task_dayofweek, width=8))
            item.append(Label(self, text=tasktime, width=8))

            self.button = Button(self, text="삭제", width=8)
            self.button['command'] = lambda idx=cnt - 1: delete(idx)
            item.append(self.button)
            tasks_implement.append(item)

        for kk in range(len(tasks_implement)):
            tasks_implement[kk][0].grid(row=i, column=0)
            tasks_implement[kk][1].grid(row=i, column=1)
            tasks_implement[kk][2].grid(row=i, column=2)
            tasks_implement[kk][3].grid(row=i, column=3)

            i += 1

class SelectGroup_forDeleteTaskALL(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        sql = """Select GroupID, GroupName From Gr0up
                Where GroupID IN (Select GroupId From Participant Where UserID=%s and IsCaptain=1)
                """
        my_groups = self.db.executeAll(sql, (UserID))

        my_groups_dict = {}
        for group in my_groups:
            my_groups_dict[(str(group["GroupID"]) + " : " + str(group["GroupName"]))] = group["GroupID"]
        options = ["그룹을 선택해주세요"]
        dict_key = list(my_groups_dict.keys())
        for i in dict_key:
            options.append(str(i))

        var1 = StringVar(self)
        var1.set(options[0])

        option_menu = OptionMenu(self, var1, *options)
        option_menu.grid(row=2, column=0)

        def Modify_Group_Task():
            selected_GroupID = my_groups_dict[var1.get()]

            frame = DeleteGroupTaskALL(parent=parent, controller=controller, db=db,
                                                gid = selected_GroupID)

            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()
        button = Button(self, text="확인" , command = Modify_Group_Task)
        button.grid(row=3, column=0)

class DeleteGroupTaskALL(tk.Frame):
    def __init__(self, parent, controller, db, gid):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.GroupID = gid
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("SelectGroup_forDeleteTask"), width=40,
                    height=2)
        b1.grid(row=0, column=0, columnspan=3)

        sql = """select GroupID, TaskName, TaskDayOfWeek, TaskTime, TaskDate From GROUP_TASK_ALL WHERE GroupID = %s
        """

        group_task_all = self.db.executeAll(sql, (self.GroupID))

        label1 = Label(self, text="과업명", width=8)
        label1.grid(row=1, column=0)
        label5 = Label(self, text = "날짜", width = 8)
        label5.grid(row=1, column=1)
        label2 = Label(self, text="요일", width=8)
        label2.grid(row=1, column=2)
        label3 = Label(self, text="시간", width=8)
        label3.grid(row=1, column=3)
        label4 = Label(self, text="삭제하기", width=8)
        label4.grid(row=1, column=4)

        def delete(idx):
            gt = group_task_all[idx]
            sql = """Delete From GROUP_TASK_ALL WHERE GroupID=%s and TaskName=%s and TaskDayOfWeek=%s and TaskTime=%s and TaskDate = %s"""
            db.execute(sql,(self.GroupID, gt['TaskName'],gt['TaskDayOfWeek'],gt['TaskTime'], gt['TaskDate']))


            for item in task_all_implement[idx]:
                item.destroy()

        i = 2
        cnt = 0
        task_all_implement = []

        # request = [{"RequestNo" : "1", "FromID": "2015147040", "ToID":"2015147001","GroupID":1,"isInvite":"1"},
        #            {"RequestNo" : "2", "FromID": "2015147032", "ToID":"2015147010","GroupID":2,"isInvite":"0"},
        #            {"RequestNo" : "3", "FromID": "2015147012", "ToID":"2015147012","GroupID":3,"isInvite":"1"}]
        # PersonName = ["황동영","김용우","조동규"]
        # GroupNames = ["와이빅타","산정관","야이"]

        for gt in group_task_all:
            cnt += 1
            item = []
            task_name = gt["TaskName"]
            task_date = gt["TaskDate"]
            # inviter_name = PersonName[cnt-1]
            dayofweek_dict_inttokor = {2 : '월', 3: '화', 4: '수', 5: '목', 6: '금', 7:'토', 1: '일'}
            dayofweek_dict_kortoint = {'월' : 2, '화' : 3, '수' : 4, '목' : 5, '금' : 6 , '토' : 7, '일' : 1}
            task_dayofweek = dayofweek_dict_inttokor[int(gt["TaskDayOfWeek"])]
            tasktime = gt["TaskTime"]
            # group_name = GroupNames[cnt-1]

            item.append(Label(self, text=task_name, width=8))
            item.append(Label(self, text=task_date, width=8))
            item.append(Label(self, text=task_dayofweek, width=8))
            item.append(Label(self, text=tasktime, width=8))

            self.button = Button(self, text="삭제", width=8)
            self.button['command'] = lambda idx=cnt - 1: delete(idx)
            item.append(self.button)
            task_all_implement.append(item)

        for kk in range(len(task_all_implement)):
            task_all_implement[kk][0].grid(row=i, column=0)
            task_all_implement[kk][1].grid(row=i, column=1)
            task_all_implement[kk][2].grid(row=i, column=2)
            task_all_implement[kk][3].grid(row=i, column=3)
            task_all_implement[kk][4].grid(row=i, column=4)

            i += 1

# Create the entire GUI program

if __name__ == "__main__" :
    main_account_screen()
