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
from datetime import timedelta
from tkinter.messagebox import askokcancel
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
                  AddEx, Lang, Licen, Intern, Cir, SelectGroup_forDeleteTask, SelectGroup_forDeleteTaskALL, ManageEx,AddClasses,MakeGroup):
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
        welcome = Label(self, text="{}님 환영합니다.".format(UserName),width=40)
        b1 = Button(self, text="내 시간표 보기", command = lambda :  controller.show_frame("TimeTable"),width=40,height=2)
        b2 = Button(self, text="일정보기(리스트)", command = lambda : controller.show_frame("ScheduleList"),width=40,height=2)
        b3 = Button(self, text="개인 일정 생성", command = lambda : controller.show_frame("MakePersonalSchedule"), width=40, height=2)
        b4 = Button(self, text="그룹 일정 생성", command = lambda : controller.show_frame("Select_GroupTask_Term"),width=40,height=2)
        b5 = Button(self, text="받은 초대 확인", command = lambda : controller.show_frame("ShowRequest"),width=40,height=2)
        b6 = Button(self, text="그룹원 찾기", command = lambda : controller.show_frame("FindUser"),width=40,height=2)
        b7 = Button(self, text="그룹 찾기", command = lambda : controller.show_frame("FindGroup"),width=40,height=2)
        b8 = Button(self, text="경력 추가하기", command = lambda : controller.show_frame("AddEx"),width=40,height=2)
        b9 = Button(self, text="경력 관리하기", command = lambda : controller.show_frame("ManageEx"),width=40,height=2)
        b10 = Button(self, text="과업 관리하기", command = lambda : controller.show_frame("SelectGroup_forDeleteTask"),width=40,height=2)
        b11 = Button(self, text="과업(날짜별) 관리하기", command = lambda : controller.show_frame("SelectGroup_forDeleteTaskALL"),width=40,height=2)
        b12 = Button(self, text="수업 추가하기", command = lambda : controller.show_frame("AddClasses"),width=40,height=2)
        b13 = Button(self, text="그룹 추가하기", command = lambda : controller.show_frame("MakeGroup"),width=40,height=2)
        welcome.grid(row=0,column=0)
        b1.grid(row=1, column=0)
        b2.grid(row=2, column=0)
        b3.grid(row=3, column=0)
        b4.grid(row=4, column=0)
        b5.grid(row=5, column=0)
        b6.grid(row=6, column=0)
        b7.grid(row=7, column=0)
        b8.grid(row=8, column=0)
        b9.grid(row=9, column=0)
        b10.grid(row=10,column=0)
        b11.grid(row=11,column=0)
        b12.grid(row=12,column=0)
        b13.grid(row=13,column=0)

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

            sql = """SELECT * FROM LANGUAGE WHERE UserID=%s and TestName =%s"""
            res = db.executeAll(sql,(UserID, name))
            if len(res)!=0:
                ask = askokcancel("Error","이미 해당 이름의 경력이 존재합니다. 정보를 업데이트 하시겠습니까?")
                if ask == 1:
                    if len(issue)!=0 and len(expir)!=0:
                        query = """UPDATE LANGUAGE SET Score = %s, IssueDate=%s, Expiration=%s WHERE UserID=%s and TestName=%s"""
                        try:
                            db.execute(query,(score, issue, expir, UserID, name))
                            showinfo("Success","정상적으로 갱신되었습니다.")
                            controller.show_frame("MainPage")
                        except pymysql.err.InternalError:
                            showinfo("Error", "올바른 형식으로 입력해주세요.")
                    elif len(issue)!=0:
                        query = """UPDATE LANGUAGE SET Score = %s, IssueDate=%s WHERE UserID=%s and TestName=%s"""
                        try:
                            db.execute(query, (score, issue, UserID, name))
                            showinfo("Success", "정상적으로 갱신되었습니다.")
                            controller.show_frame("MainPage")
                        except pymysql.err.InternalError:
                            showinfo("Error", "올바른 형식으로 입력해주세요.")
                    elif len(expir)!=0:
                        query = """UPDATE LANGUAGE SET Score = %s, Expiration=%s WHERE UserID=%s and TestName=%s"""
                        try:
                            db.execute(query, (score, expir, UserID, name))
                            showinfo("Success", "정상적으로 갱신되었습니다.")
                            controller.show_frame("MainPage")
                        except pymysql.err.InternalError:
                            showinfo("Error", "올바른 형식으로 입력해주세요.")
                    else:
                        query = """UPDATE LANGUAGE SET Score = %s WHERE UserID=%s and TestName=%s"""
                        try:
                            db.execute(query, (score, UserID, name))
                            showinfo("Success", "정상적으로 갱신되었습니다.")
                            controller.show_frame("MainPage")
                        except pymysql.err.InternalError:
                            showinfo("Error", "올바른 형식으로 입력해주세요.")

            else :
                if len(issue)!=0 and len(expir)!=0:
                    query = """INSERT INTO Language(UserID, TestName, Score, IssueDate, Expiration)
                    VALUES(%s,%s,%s,%s,%s)
                    """
                    try:
                        self.db.execute(query,(UserID, name, score, issue, expir))
                        showinfo("Success", "정상적으로 추가되었습니다.")
                        controller.show_frame("MainPage")
                    except pymysql.err.InternalError:
                        showinfo("Error", "올바른 형식으로 입력해주세요.")
                elif len(issue)!=0:
                    query = """INSERT INTO Language(UserID, TestName, Score, IssueDate)
                                    VALUES(%s,%s,%s,%s)
                                    """
                    try:
                        self.db.execute(query, (UserID, name, score, issue))
                        showinfo("Success", "정상적으로 추가되었습니다.")
                        controller.show_frame("MainPage")
                    except pymysql.err.InternalError:
                        showinfo("Error", "올바른 형식으로 입력해주세요.")
                elif len(expir)!=0:
                    query = """INSERT INTO Language(UserID, TestName, Score, Expiration)
                                                VALUES(%s,%s,%s,%s)
                                                """

                    try :
                        self.db.execute(query, (UserID, name, score, expir))
                        showinfo("Success", "정상적으로 추가되었습니다.")
                        controller.show_frame("MainPage")
                    except pymysql.err.InternalError:
                        showinfo("Error", "올바른 형식으로 입력해주세요.")
                else:
                    query = """INSERT INTO Language(UserID, TestName, Score)
                                                                    VALUES(%s,%s,%s)
                                                                """
                    try:
                        self.db.execute(query, (UserID, name, score))
                        showinfo("Success", "정상적으로 추가되었습니다.")
                        controller.show_frame("MainPage")
                    except pymysql.err.InternalError:
                        showinfo("Error", "올바른 형식으로 입력해주세요.")

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
                try:
                    self.db.execute(query,(UserID, name, score, issue, expir))
                    showinfo("Success", "정상적으로 추가되었습니다.")
                    controller.show_frame("MainPage")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")
            elif len(issue)!=0:
                query = """INSERT INTO License(UserID, LicenseName, Score, IssueDate)
                                VALUES(%s,%s,%s,%s)
                                """
                try :
                    self.db.execute(query, (UserID, name, score, issue))
                    showinfo("Success", "정상적으로 추가되었습니다.")
                    controller.show_frame("MainPage")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")
            elif len(expir)!=0:
                query = """INSERT INTO License(UserID, LicenseName, Score, Expiration)
                                                VALUES(%s,%s,%s,%s)
                                                """

                try:
                    self.db.execute(query, (UserID, name, score, expir))
                    showinfo("Success", "정상적으로 추가되었습니다.")
                    controller.show_frame("MainPage")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")

            else:
                query = """INSERT INTO License(UserID, LicenseName, Score)
                                                                VALUES(%s,%s,%s)
                                                                """
                try:
                    self.db.execute(query, (UserID, name, score))
                    showinfo("Success", "정상적으로 추가되었습니다.")
                    controller.show_frame("MainPage")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")


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
                try:
                    self.db.execute(query, (UserID, name, pos, long))
                    showinfo("Success", "정상적으로 추가되었습니다.")
                    controller.show_frame("MainPage")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")

            else:
                query = """INSERT INTO INTERNSHIP(UserID, CompanyName, Position)
                VALUES(%s,%s,%s)
                """
                try:
                    self.db.execute(query, (UserID, name, pos))
                    showinfo("Success", "정상적으로 추가되었습니다.")
                    controller.show_frame("MainPage")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")


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
                try:
                    self.db.execute(query, (UserID, name, pos, long))
                    showinfo("Success", "정상적으로 추가되었습니다.")
                    controller.show_frame("MainPage")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")
            elif len(long)!=0:
                query = """INSERT INTO Circle(UserID, CircleName, HowLong)
                                        VALUES(%s,%s,%s)
                                        """
                try:
                    self.db.execute(query, (UserID, name, long))
                    showinfo("Success", "정상적으로 추가되었습니다.")
                    controller.show_frame("MainPage")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")
            elif len(long)!=0:
                query = """INSERT INTO Circle(UserID, CircleName, Position)
                                        VALUES(%s,%s,%s)
                                        """
                try:
                    self.db.execute(query, (UserID, name, pos))
                    showinfo("Success", "정상적으로 추가되었습니다.")
                    controller.show_frame("MainPage")

                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")

            else:
                query = """INSERT INTO Circle(UserID, CircleName)
                        VALUES(%s,%s)
                        """
                try:
                    self.db.execute(query, (UserID, name))
                    showinfo("Success", "정상적으로 추가되었습니다.")
                    controller.show_frame("MainPage")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")


        b = Button(self, text="확인", command=confirm, width=10)
        b.grid(row=10, column=0)

class ManageEx(tk.Frame):
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        def show_lang():
            sql = """SELECT * FROM LANGUAGE WHERE UserID = %s"""
            result = db.executeAll(sql,(UserID))
            frame = ManageLang(parent=parent, controller=controller, db=db, result=result)

            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()

        def show_licen():
            sql = """SELECT * FROM LICENSE WHERE UserID = %s"""
            result = db.executeAll(sql, (UserID))
            frame = ManageLicen(parent=parent, controller=controller, db=db, result=result)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()

        def show_intern():
            sql = """SELECT * FROM INTERNSHIP WHERE UserID = %s"""
            result = db.executeAll(sql, (UserID))
            frame = ManageIntern(parent=parent, controller=controller, db=db, result=result)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()

        def show_cir():
            sql = """SELECT * FROM CIRCLE WHERE UserID = %s"""
            result = db.executeAll(sql, (UserID))
            frame = ManageCir(parent=parent, controller=controller, db=db, result=result)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()

        label = Label(self, text="경력 종류를 선택해주세요", width=40, height=2)
        label.grid(row=1, column=0)
        b2 = Button(self, text="어학", command=show_lang, width=40, height=2)
        b2.grid(row=2, column=0)
        b3 = Button(self, text="자격증", command=show_licen, width=40, height=2)
        b3.grid(row=3, column=0)
        b4 = Button(self, text="인턴십", command=show_intern, width=40, height=2)
        b4.grid(row=4, column=0)
        b5 = Button(self, text="동아리/학회", command=show_cir, width=40, height=2)
        b5.grid(row=5, column=0)





class ManageLang(tk.Frame):
    def __init__(self, parent, controller, db, result):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        controller.frames["ManageLang"] = self
        print(controller.frames)
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("ManageEx"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        label1 = Label(self, text="시험명", width=8)
        label1.grid(row=1, column=0)
        label2 = Label(self, text="점수", width=8)
        label2.grid(row=1, column=1)
        label3 = Label(self, text="취득일", width=8)
        label3.grid(row=1, column=2)
        label4 = Label(self, text="만료일", width=8)
        label4.grid(row=1, column=3)
        label5 = Label(self, text="수정하기", width=8)
        label5.grid(row=1, column=4)
        label6 = Label(self, text="삭제하기", width=8)
        label6.grid(row=1, column=5)

        def edit(idx):
            ex = result[idx]
            frame1 = NewInfo4EditLang(parent=parent, controller=controller, db=db, result=ex, prev = self)
            frame1.grid(row=0, column=0, sticky="nsew")
            frame1.tkraise()

        def delete(idx):
            ex = result[idx]
            sql = """Delete From Language WHERE UserID=%s and TestName = %s"""
            db.execute(sql,(UserID, ex['TestName']))


            for item in implement[idx]:
                item.destroy()

        i = 2
        cnt = 0
        implement = []

        # request = [{"RequestNo" : "1", "FromID": "2015147040", "ToID":"2015147001","GroupID":1,"isInvite":"1"},
        #            {"RequestNo" : "2", "FromID": "2015147032", "ToID":"2015147010","GroupID":2,"isInvite":"0"},
        #            {"RequestNo" : "3", "FromID": "2015147012", "ToID":"2015147012","GroupID":3,"isInvite":"1"}]
        # PersonName = ["황동영","김용우","조동규"]
        # GroupNames = ["와이빅타","산정관","야이"]

        for ex in result:
            cnt += 1
            item = []
            name = ex["TestName"]
            score = ex["Score"]
            issue = ex["IssueDate"]
            expir = ex["Expiration"]

            item.append(Label(self, text=name, width=8))
            item.append(Label(self, text=score, width=8))
            item.append(Label(self, text=issue, width=8))
            item.append(Label(self, text=expir, width=8))
            self.button1 = Button(self, text="수정", width=8)
            self.button1['command'] = lambda idx=cnt-1 : edit(idx)
            self.button2 = Button(self, text="삭제", width=8)
            self.button2['command'] = lambda idx=cnt - 1: delete(idx)
            item.append(self.button1)
            item.append(self.button2)
            implement.append(item)

        for kk in range(len(implement)):
            implement[kk][0].grid(row=i, column=0)
            implement[kk][1].grid(row=i, column=1)
            implement[kk][2].grid(row=i, column=2)
            implement[kk][3].grid(row=i, column=3)
            implement[kk][4].grid(row=i, column=4)
            implement[kk][5].grid(row=i, column=5)


            i += 1

class NewInfo4EditLang(tk.Frame):
    def __init__(self, parent, controller, db, result, prev):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        def back():
            prev.tkraise()
        b1 = Button(self, text="뒤로가기", command = back, width=40, height=2)
        b1.grid(row=0, column=0)
        Label01 = Label(self, text="시험명", width= 40, height=2)
        Label01.grid(row=1,column=0)
        Label02 = Label(self, text=result["TestName"],width=40, height=2)
        Label02.grid(row=2,column=0)
        Label1 = Label(self, text="점수", width=40, height=2)
        Label1.grid(row=3, column=0)

        ScoreVar = StringVar()

        Score_Entry = Entry(self, width=40, textvariable=ScoreVar)
        Score_Entry.insert(END, "시험 점수를 입력해주세요")
        Score_Entry.grid(row=4, column=0)

        Label2 = Label(self, text="취득일(YYYY-MM-DD, 공란가능)", width=40, height=2)
        Label2.grid(row=5, column=0)

        IssueVar = StringVar()

        Issue_Entry = Entry(self, width=40, textvariable=IssueVar)
        Issue_Entry.grid(row=6, column=0)

        Label3 = Label(self, text="만료일(YYYY-MM-DD, 공란가능)", width=40, height=2)
        Label3.grid(row=7, column=0)

        ExpirationVar = StringVar()

        Expiration_Entry = Entry(self, width=40, textvariable=ExpirationVar)
        Expiration_Entry.grid(row=8, column=0)

        def confirm():
            score = ScoreVar.get()
            issue = IssueVar.get()
            expir = ExpirationVar.get()

            if len(issue) != 0 and len(expir) != 0:
                query = """UPDATE LANGUAGE SET Score = %s, IssueDate=%s, Expiration=%s WHERE UserID=%s and TestName=%s"""
                try :
                    db.execute(query, (score, issue, expir, UserID, result['TestName']))
                    showinfo("Success", "정상적으로 갱신되었습니다.")
                    controller.show_frame("ManageEx")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")
            elif len(issue) != 0:
                query = """UPDATE LANGUAGE SET Score = %s, IssueDate=%s WHERE UserID=%s and TestName=%s"""
                try:
                    db.execute(query, (score, issue, UserID, result['TestName']))
                    showinfo("Success", "정상적으로 갱신되었습니다.")
                    controller.show_frame("ManageEx")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")
            elif len(expir) != 0:
                query = """UPDATE LANGUAGE SET Score = %s, Expiration=%s WHERE UserID=%s and TestName=%s"""
                try:
                    db.execute(query, (score, expir, UserID, result['TestName']))
                    showinfo("Success", "정상적으로 갱신되었습니다.")
                    controller.show_frame("ManageEx")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")
            else:
                query = """UPDATE LANGUAGE SET Score = %s WHERE UserID=%s and TestName=%s"""
                try :
                    db.execute(query, (score, UserID, result['TestName']))
                    showinfo("Success", "정상적으로 갱신되었습니다.")
                    controller.show_frame("ManageEx")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")



        b = Button(self, text="확인", command=confirm, width=10)
        b.grid(row=9, column=0)


class ManageLicen(tk.Frame):
    def __init__(self, parent, controller, db, result):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("ManageEx"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        label1 = Label(self, text="시험명", width=8)
        label1.grid(row=1, column=0)
        label2 = Label(self, text="점수", width=8)
        label2.grid(row=1, column=1)
        label3 = Label(self, text="취득일", width=8)
        label3.grid(row=1, column=2)
        label4 = Label(self, text="만료일", width=8)
        label4.grid(row=1, column=3)
        label5 = Label(self, text="수정하기", width=8)
        label5.grid(row=1, column=4)
        label6 = Label(self, text="삭제하기", width=8)
        label6.grid(row=1, column=5)

        def edit(idx):
            ex = result[idx]
            frame1 = NewInfo4EditLicen(parent=parent, controller=controller, db=db, result=ex, prev = self)
            frame1.grid(row=0, column=0, sticky="nsew")
            frame1.tkraise()

        def delete(idx):
            ex = result[idx]
            sql = """Delete From License WHERE UserID=%s and LicenseName = %s"""
            db.execute(sql, (UserID, ex['LicenseName']))

            for item in implement[idx]:
                item.destroy()

        i = 2
        cnt = 0
        implement = []

        # request = [{"RequestNo" : "1", "FromID": "2015147040", "ToID":"2015147001","GroupID":1,"isInvite":"1"},
        #            {"RequestNo" : "2", "FromID": "2015147032", "ToID":"2015147010","GroupID":2,"isInvite":"0"},
        #            {"RequestNo" : "3", "FromID": "2015147012", "ToID":"2015147012","GroupID":3,"isInvite":"1"}]
        # PersonName = ["황동영","김용우","조동규"]
        # GroupNames = ["와이빅타","산정관","야이"]

        for ex in result:
            cnt += 1
            item = []
            name = ex["LicenseName"]
            score = ex["Score"]
            issue = ex["IssueDate"]
            expir = ex["Expiration"]

            item.append(Label(self, text=name, width=8))
            item.append(Label(self, text=score, width=8))
            item.append(Label(self, text=issue, width=8))
            item.append(Label(self, text=expir, width=8))
            self.button1 = Button(self, text="수정", width=8)
            self.button1['command'] = lambda idx=cnt - 1: edit(idx)
            self.button2 = Button(self, text="삭제", width=8)
            self.button2['command'] = lambda idx=cnt - 1: delete(idx)
            item.append(self.button1)
            item.append(self.button2)
            implement.append(item)

        for kk in range(len(implement)):
            implement[kk][0].grid(row=i, column=0)
            implement[kk][1].grid(row=i, column=1)
            implement[kk][2].grid(row=i, column=2)
            implement[kk][3].grid(row=i, column=3)
            implement[kk][4].grid(row=i, column=4)
            implement[kk][5].grid(row=i, column=5)

            i += 1


class NewInfo4EditLicen(tk.Frame):
    def __init__(self, parent, controller, db, result, prev):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        def back():
            prev.tkraise()

        b1 = Button(self, text="뒤로가기", command = back, width=40, height=2)
        b1.grid(row=0, column=0)
        Label01 = Label(self, text="자격증 명", width= 40, height=2)
        Label01.grid(row=1,column=0)
        Label02 = Label(self, text=result["LicenseName"],width=40, height=2)
        Label02.grid(row=2,column=0)
        Label1 = Label(self, text="점수(등급)", width=40, height=2)
        Label1.grid(row=3, column=0)

        ScoreVar = StringVar()

        Score_Entry = Entry(self, width=40, textvariable=ScoreVar)
        Score_Entry.insert(END, "자격증 점수(등급) 입력해주세요")
        Score_Entry.grid(row=4, column=0)

        Label2 = Label(self, text="취득일(YYYY-MM-DD, 공란가능)", width=40, height=2)
        Label2.grid(row=5, column=0)

        IssueVar = StringVar()

        Issue_Entry = Entry(self, width=40, textvariable=IssueVar)
        Issue_Entry.grid(row=6, column=0)

        Label3 = Label(self, text="만료일(YYYY-MM-DD, 공란가능)", width=40, height=2)
        Label3.grid(row=7, column=0)

        ExpirationVar = StringVar()

        Expiration_Entry = Entry(self, width=40, textvariable=ExpirationVar)
        Expiration_Entry.grid(row=8, column=0)

        def confirm():
            score = ScoreVar.get()
            issue = IssueVar.get()
            expir = ExpirationVar.get()

            if len(issue) != 0 and len(expir) != 0:
                query = """UPDATE LICENSE SET Score = %s, IssueDate=%s, Expiration=%s WHERE UserID=%s and LicenseName=%s"""
                try:
                    db.execute(query, (score, issue, expir, UserID, result['LicenseName']))
                    showinfo("Success", "정상적으로 갱신되었습니다.")
                    controller.show_frame("ManageEx")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")
            elif len(issue) != 0:
                query = """UPDATE LICENSE SET Score = %s, IssueDate=%s WHERE UserID=%s and LicenseName=%s"""
                try:
                    db.execute(query, (score, issue, UserID, result['LicenseName']))
                    showinfo("Success", "정상적으로 갱신되었습니다.")
                    controller.show_frame("ManageEx")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")
            elif len(expir) != 0:
                query = """UPDATE LICENSE SET Score = %s, Expiration=%s WHERE UserID=%s and LicenseName=%s"""
                try:
                    db.execute(query, (score, expir, UserID, result['LicenseName']))
                    showinfo("Success", "정상적으로 갱신되었습니다.")
                    controller.show_frame("ManageEx")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")
            else:
                query = """UPDATE LICENSE SET Score = %s WHERE UserID=%s and LicenseName=%s"""
                try:
                    db.execute(query, (score, UserID, result['LicenseName']))
                    showinfo("Success", "정상적으로 갱신되었습니다.")
                    controller.show_frame("ManageEx")
                except pymysql.err.InternalError:
                    showinfo("Error", "올바른 형식으로 입력해주세요.")



        b = Button(self, text="확인", command=confirm, width=10)
        b.grid(row=9, column=0)

class ManageIntern(tk.Frame):
    def __init__(self, parent, controller, db, result):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("ManageEx"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        label1 = Label(self, text="회사명", width=8)
        label1.grid(row=1, column=0)
        label2 = Label(self, text="직무", width=8)
        label2.grid(row=1, column=1)
        label3 = Label(self, text="재직기간", width=8)
        label3.grid(row=1, column=2)
        label4 = Label(self, text="삭제하기", width=8)
        label4.grid(row=1, column=3)

        def delete(idx):
            ex = result[idx]
            sql = """Delete From Internship WHERE UserID=%s and CompanyName = %s"""
            db.execute(sql, (UserID, ex['CompanyName']))

            for item in implement[idx]:
                item.destroy()

        i = 2
        cnt = 0
        implement = []

        for ex in result:
            cnt += 1
            item = []
            name = ex["CompanyName"]
            pos = ex["Position"]
            long = ex["HowLong"]

            item.append(Label(self, text=name, width=8))
            item.append(Label(self, text=pos, width=8))
            item.append(Label(self, text=long, width=8))

            self.button2 = Button(self, text="삭제", width=8)
            self.button2['command'] = lambda idx=cnt - 1: delete(idx)

            item.append(self.button2)
            implement.append(item)

        for kk in range(len(implement)):
            implement[kk][0].grid(row=i, column=0)
            implement[kk][1].grid(row=i, column=1)
            implement[kk][2].grid(row=i, column=2)
            implement[kk][3].grid(row=i, column=3)

            i += 1

class ManageCir(tk.Frame):
    def __init__(self, parent, controller, db, result):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("ManageEx"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        label1 = Label(self, text="회사명", width=8)
        label1.grid(row=1, column=0)
        label2 = Label(self, text="직무", width=8)
        label2.grid(row=1, column=1)
        label3 = Label(self, text="재직기간", width=8)
        label3.grid(row=1, column=2)
        label4 = Label(self, text="삭제하기", width=8)
        label4.grid(row=1, column=3)

        def delete(idx):
            ex = result[idx]
            sql = """Delete From Internship WHERE UserID=%s and CircleName = %s"""
            db.execute(sql, (UserID, ex['CircleName']))

            for item in implement[idx]:
                item.destroy()

        i = 2
        cnt = 0
        implement = []

        for ex in result:
            cnt += 1
            item = []
            name = ex["CircleName"]
            pos = ex["Position"]
            long = ex["HowLong"]

            item.append(Label(self, text=name, width=8))
            item.append(Label(self, text=pos, width=8))
            item.append(Label(self, text=long, width=8))

            self.button = Button(self, text="삭제", width=8)
            self.button['command'] = lambda idx=cnt - 1: delete(idx)
            item.append(self.button)
            implement.append(item)

        for kk in range(len(implement)):
            implement[kk][0].grid(row=i, column=0)
            implement[kk][1].grid(row=i, column=1)
            implement[kk][2].grid(row=i, column=2)
            implement[kk][3].grid(row=i, column=3)

            i += 1
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

        current_date = datetime.datetime.today()
        week = current_date.isocalendar()[1]

        a = timedelta(days=1)
        b = current_date.weekday()
        date = datetime.datetime(current_date.year, current_date.month, current_date.day)

        startdate = date - a * b
        enddate = date + a * (6 - b)

        start = startdate.strftime("%Y-%m-%d")
        end = enddate.strftime("%Y-%m-%d")
        # DB
        sql = """select *
        From Personal_Schedule
        WHERE UserID = %s AND ScheduleDate >= %s AND ScheduleDate <= %s
        """

        personal_fetch = db.executeAll(sql, (UserID, start, end))

        sql = """select *
        From group_Schedule
        WHERE UserID = %s AND TaskDate >= %s AND TaskDate <= %s
        """

        group_fetch = db.executeAll(sql, (UserID, start, end))

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

        mpl.rc('font', family='DejaVu Sans')  # Mac의 경우는 AppleGothic, 윈도우의 경우는 Malgun Gothic을 사용하면 됩니다 :)
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
        ax.set_ylim(24, -1)
        ax.set_yticks(range(24, -1, -1))
        ax.set_yticklabels(range(24, -1, -1))

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

            p = j % 5

            start = row["ScheduleTime"]
            ax.fill_between([weekday - 0.4, weekday + 0.4], [start, start], [start + 1, start + 1], color=colors[p],
                            edgecolor='k', linewidth=0.5)
            nlen = len(name)
            ax.text(weekday-nlen*0.03,start+0.25, name, va="top", fontsize = 10)

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
                sql = """Delete From Request WHERE RequestNo =%s"""
                db.execute(sql, (req["RequestNo"]))
            else:
                db.execute(sql,(req["GroupID"],req["FromID"]))
                sql = """Delete From Request WHERE RequestNo =%s"""
                db.execute(sql, (req["RequestNo"]))

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
    def __init__(self, parent, controller, db):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("MainPage"), width=40,
                    height=2)
        b1.grid(row=0, column=0)

        label = Label(self, text = "그룹 선택")
        label.grid(row=1, column=0)

        sql = """Select GroupID, GroupName From Gr0up
                Where GroupID IN (Select GroupId From Participant Where UserID=%s and IsCaptain=1)
                """
        my_groups = self.db.executeAll(sql, (UserID))

        my_groups_dict = {}
        for group in my_groups:
            my_groups_dict[(str(group["GroupID"]) + " : " + str(group["GroupName"]))] = (group["GroupID"],group["GroupName"])
        options = ["그룹을 선택해주세요"]
        dict_key = list(my_groups_dict.keys())
        for i in dict_key:
            options.append(str(i))

        var1 = StringVar(self)
        var1.set(options[0])

        option_menu = OptionMenu(self, var1, *options)
        option_menu.grid(row=2, column=0)

        def go_on():
            group = var1.get()
            selected_GroupID = my_groups_dict[group][0]
            selected_GroupName = my_groups_dict[group][1]

            frame = SearchExperience(parent=parent, controller=controller, db=db,
                                                gid = selected_GroupID, gname = selected_GroupName)

            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()
        button = Button(self, text="확인" , command = go_on)
        button.grid(row=3, column=0)

class SearchExperience(tk.Frame):
    def __init__(self, parent, controller, db, gid, gname):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db
        self.GroupID = gid
        b1 = Button(self, text="뒤로가기", command=lambda: controller.show_frame("FindUser"), width=40,
                    height=2)
        b1.grid(row=0, column=0, columnspan=3)

        label1 = Label(self, text="어학시험명(공란가능)")
        label1.grid(row=1, column=0)

        Var1 = StringVar()

        Entry1 = Entry(self, width=40, textvariable=Var1)
        Entry1.grid(row=2, column=0)

        label2 = Label(self, text="자격증 명(공란가능)")
        label2.grid(row=3, column=0)

        Var2 = StringVar()

        Entry2 = Entry(self, width=40, textvariable=Var2)
        Entry2.grid(row=4, column=0)

        label3 = Label(self, text="인턴회사 명(공란가능)")
        label3.grid(row=5, column=0)

        Var3 = StringVar()
        Entry3 = Entry(self, width=40, textvariable=Var3)
        Entry3.grid(row=6, column=0)

        label4 = Label(self, text="동아리/학회 명(공란가능)")
        label4.grid(row=7, column=0)

        Var4 = StringVar()
        Entry4 = Entry(self, width=40, textvariable=Var4)
        Entry4.grid(row=8, column=0)

        def Search():
            search_object = [Var1.get(), Var2.get(), Var3.get(), Var4.get()]

            frame = SearchMemberResult(parent = parent, controller=controller, db=db, result=search_object, prev=self, group_id = self.GroupID,
                                       gname = gname)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()

        button = Button(self, text="검색", command=Search)
        button.grid(row=9, column=0)

class SearchMemberResult(tk.Frame):
    def __init__(self, parent, controller, db, result, prev, group_id, gname):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db = db

        def back():
            prev.tkraise()
        b1 = Button(self, text="뒤로가기", command = back, width=40, height=2)
        b1.grid(row=0, column=0,columnspan=3)

        label1 = Label(self, text="아이디", width=8)
        label1.grid(row=1, column=0)
        label2 = Label(self, text="이름", width=8)
        label2.grid(row=1, column=1)
        label3 = Label(self, text="경력", width=30)
        label3.grid(row=1, column=2)
        label4 = Label(self, text="초대하기", width=8)
        label4.grid(row=1, column=3)
        print(result)
        sql = """SELECT USERS.UserID, Name, career_check(USERS.UserID,%s,%s,%s,%s) AS Experience
        FROM USERS WHERE USERS.UserID Not in(SELECT UserID From Participant WHERE GroupID = %s)
        and USERS.UserID <> %s and career_check(USERS.UserID,%s,%s,%s,%s) <> ' /  /  / ';"""

        res = db.executeAll(sql,(result[0],result[1],result[2],result[3],group_id, UserID,result[0],result[1],result[2],result[3]))

        i = 2
        cnt = 0
        users_implement = []

        def request(idx):
            member = res[idx]
            sql1 = """Select * from REQUEST WHERE FromID = %s and GroupID = %s"""
            already = db.executeAll(sql1, (UserID, group_id))
            if len(already) != 0:
                showinfo("Error", "이미 초대하셨습니다.")
            else:
                sql2 = """INSERT INTO Request(FromID, ToID, GroupID,isInvite,GroupName) VALUES (%s,%s,%s,%s,%s)"""
                db.execute(sql2, (UserID, member['UserID'], group_id, 0, gname))
                showinfo("Success", "정상적으로 초대되었습니다.")

        for member in res:
            cnt += 1
            item = []
            userID = member["UserID"]
            userName = member["Name"]
            userExperience = member["Experience"]
            item.append(Label(self, text=userID, width=8))
            item.append(Label(self, text=userName, width=8))
            item.append(Label(self, text=userExperience, width=30))

            self.button = Button(self, text="초대하기", width=8)
            self.button['command'] = lambda idx=cnt - 1: request(idx)
            item.append(self.button)
            users_implement.append(item)

        for kk in range(len(users_implement)):
            users_implement[kk][0].grid(row=i, column=0)
            users_implement[kk][1].grid(row=i, column=1)
            users_implement[kk][2].grid(row=i, column=2)
            users_implement[kk][3].grid(row=i, column=3)

            i += 1

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
            sql ="""SELECT GroupID, GroupName FROM GR0UP WHERE IsClass =0 and GroupName LIKE %s and
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

                captainID = db.executeAll(sqlforcaptainID,(gt['GroupID']))
                print(captainID)
                captainID = captainID[0]['GroupCaptain']

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

        label5 = Label(self, text="삭제하기", width=8)
        label5.grid(row=1, column=3)

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

        def exe_selection():
            sql = """Call GroupImport(%s,%s)
            """
            # print(groupid, UserID)
            gname = ScheduleNameVar.get()

            self.db.execute(sql, (gname, UserID))
            showinfo("Success","성공적으로 생성하셨습니다.")
            controller.show_frame("MainPage")
            #self.db.commit()

            #self.db.executeAll(sql, (self.groupname))

        b2 = Button(self, text="추가", command=exe_selection)
        b2.grid(row=9, column=0)


# Create the entire GUI program

if __name__ == "__main__" :
    main_account_screen()
