import pandas as pd
import pymysql

db= pymysql.connect(host='localhost', port= 3306, user='root',password='yourpasswd',charset='utf8')
cursor= db.cursor(pymysql.cursors.DictCursor)

#### 데이터베이스 새로 생성

# In[72]:


#sql_renew_db = 'Drop Database pro'
#cursor.execute(sql_renew_db)

# In[73]:


sql_create_Database = 'CREATE DATABASE pro'
cursor.execute(sql_create_Database)

# In[74]:


sql_use_Database = 'Use pro'

sql_create_table1 = '''
    create table USERS(
   UserID CHAR(10) Not null,
    PW varchar(20) Not null,
    Name VARCHAR(45) NOT NULL,
    Age int NOT NULL,
    Job varchar(20) not null,
    Major varchar(20) not null,
    Email_Address varCHAR(30) NOT NULL,
    CONSTRAINT USERS_PK PRIMARY KEY(UserID)
    );'''

sql_create_table2 = '''
create table LANGUAGE(
   UserID CHAR(10) NOT null,
    TestName varchar(20) NOT null,
    Score INT not null,
    IssueDate DATE null,
    Expiration DATE null,
    constraint Language_PK primary key(UserID, TestName),
   constraint Language_USER_FK Foreign Key(UserID)
      REFERENCES USERS(UserID)
         ON UPDATE CASCADE
            ON DELETE CASCADE
   );
'''

sql_create_table3 = '''
create table LICENSE(
   UserID CHAR(10) Not null,
    LicenseName varchar(20) Not null,
    Score INT null,
    IssueDate DATE null,
    Expiration DATE null,
    constraint License_PK primary key(UserID, LicenseName),
   constraint License_USER_FK Foreign Key(UserID)
      REFERENCES USERS(UserID)
         ON UPDATE CASCADE
            ON DELETE CASCADE
   );
'''

sql_create_table4 = '''
create table INTERNSHIP(
   UserID CHAR(10) Not null,
    CompanyName varchar(20) Not null,
    Position varchar(30) not null,
    HowLong INT null, 
    constraint INTERNSHIP_PK primary key(UserID, CompanyName),
   constraint INTERNSHIP_USER_FK Foreign Key(UserID)
      REFERENCES USERS(UserID)
         ON UPDATE CASCADE
            ON DELETE CASCADE
   );
'''

sql_create_table5 = '''
create table CIRCLE( -- 동아리, 학회
   UserID CHAR(10) Not null,
    CircleName varchar(20) Not null,
    Position varchar(30) null,
    HowLong INT null, 
    constraint Circle_PK primary key(UserID, CircleName),
   constraint Circle_USER_FK Foreign Key(UserID)
      REFERENCES USERS(UserID)
         ON UPDATE CASCADE
            ON DELETE CASCADE
   );
'''

sql_create_table6 = '''
create table PERSONAL_SCHEDULE(
   UserID CHAR(10) Not null,
    ScheduleID int Not null Auto_increment,
    ScheduleName Varchar(20) not null,
    ScheduleDate DATE Not null,
    ScheduleDayOfWeek int not null,
    ScheduleTime int not null,
    constraint INDI_EVENT_PK primary key(ScheduleID),
    constraint INDI_EVENT_USER_FK Foreign Key(UserID)
      REFERENCES USERS(UserID)
         ON UPDATE CASCADE
            ON DELETE CASCADE
   );
'''

sql_create_table7 = '''
create Table GR0UP( 
   GroupID INT NOT NULL Auto_increment, 
   GroupName char(20) not null,
    IsClass int not null,
    constraint RAW_GROUP_PK primary key(GroupID)
    );
'''

sql_create_table8 = '''
create Table PARTICIPANT(
   GroupID INT NOT null,
    UserID CHAR(10) Not null,
    IsCaptain int not null,
    Constraint Participant_PK primary key(GroupID, UserID),
    constraint Participant_USER_FK Foreign Key(UserID)
      REFERENCES USERS(UserID)
         ON UPDATE CASCADE
            ON DELETE CASCADE,
   constraint Participant_Group_FK foreign Key(GroupID)
      REFERENCES GR0UP(GroupID)
            ON DELETE CASCADE
   );
'''
sql_create_table9 = '''
create Table CLASS(
    GroupID INT NOT NULL,
    ClassName char(13) not null,
    Major varchar(20) Not null,
    ClassProfessor varchar(20) not null,
    Constraint Class_PK primary key(GroupID),
    constraint Class_RG_FK1 foreign Key(GroupID)
      REFERENCES GR0UP(GroupID)
            ON DELETE CASCADE
   );
'''

sql_create_table10 = '''
create Table NoCLASS(
   GroupID INT NOT NULL,
    GroupCaptain varchar(20) not null,
    Constraint NoClass_PK primary key(GroupID),
    constraint NoClass_RG_FK foreign Key(GroupID)
      REFERENCES GR0UP(GroupID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
   );
'''

sql_create_table11 = '''
create Table GROUP_TASK(
   GroupID Int NOT NULL, 
    TaskName VARCHAR(20) NOT NULL,
    TaskDayOfWeek int NOT NULL, 
    TaskTime int NOT NULL,
    TaskTerm int NOT NULL,
    Constraint G_T_PK primary key(GroupID, TaskName, TaskDayOfWeek, TaskTime),
    Constraint G_T_FK1 foreign key(GroupID)
      REFERENCES GR0UP(GroupID)
            ON DELETE CASCADE
    );
'''

sql_create_table12 = '''
create Table GROUP_TASK_ALL(
   GroupID Int NOT NULL, 
    TaskName VARCHAR(20) NOT NULL,
    TaskDayOfWeek int NOT NULL, 
    TaskTime int NOT NULL,
    TaskDate DATE NOT NULL, 
    constraint G_T_W_PK primary key(GroupID, TaskName, TaskDayOfWeek, TaskTime, TaskDate),
    Constraint G_T_W_FK1 foreign key(GroupID, TaskName, TaskDayOfWeek, TaskTime)
      REFERENCES GROUP_TASK(GroupID, TaskName, TaskDayOfWeek, TaskTime)
         ON UPDATE CASCADE
            ON DELETE CASCADE
    );
'''

sql_create_table13 = '''
create Table GROUP_SCHEDULE(
   GroupID Int NOT NULL, 
    TaskName VARCHAR(20) NOT NULL,
    TaskDayOfWeek int NOT NULL, 
   TaskTime int NOT NULL,
    TaskDate DATE NOT NULL, 
    UserID char(10) NOT NULL,
    constraint G_E_PK primary key(GroupID, TaskName, TaskDayOfWeek, TaskTime, TaskDate, UserID),
    constraint G_E_FK1 Foreign Key(GroupID, TaskName, TaskDayOfWeek, TaskTime, TaskDate)
      REFERENCES GROUP_TASK_ALL(GroupID, TaskName, TaskDayOfWeek, TaskTime, TaskDate)
         ON UPDATE CASCADE
            ON DELETE CASCADE,
   Constraint G_E_FK2 foreign key(UserID)
      references participant(UserID)
         ON UPDATE CASCADE
            ON DELETE CASCADE
   );
'''

sql_create_table14 = '''
Create table REQUEST(
   RequestNo INT NOT Null auto_increment,
   FromID CHAR(10) Not null, -- 초대 하는 사람
    ToID CHAR(10) Not null, -- 초대 받는 사람
    GroupID int not null,
    isInvite int not null,
    GroupName char(20) not null,
   constraint REQUEST_PK primary key(RequestNo),
   constraint REQUEST_USER_FK Foreign Key(FromID)
      REFERENCES USERS(UserID)
         ON UPDATE CASCADE
            ON DELETE CASCADE,
   constraint REQUEST_USER_FK2 Foreign Key(ToID)
      REFERENCES USERS(UserID)
         ON UPDATE CASCADE
            ON DELETE CASCADE,
   constraint REQUEST_GROUP_FK Foreign Key(GroupID)
      REFERENCES GR0UP(GroupID)
            ON DELETE CASCADE
   );
'''

cursor.execute(sql_use_Database)
cursor.execute(sql_create_table1)
cursor.execute(sql_create_table2)
cursor.execute(sql_create_table3)
cursor.execute(sql_create_table4)
cursor.execute(sql_create_table5)
cursor.execute(sql_create_table6)
cursor.execute(sql_create_table7)
cursor.execute(sql_create_table8)
cursor.execute(sql_create_table9)
cursor.execute(sql_create_table10)
cursor.execute(sql_create_table11)
cursor.execute(sql_create_table12)
cursor.execute(sql_create_table13)
cursor.execute(sql_create_table14)

# In[75]:


sql_insert_trigger1 = '''
create TRIGGER DulpicateTask_all After insert on GROUP_TASK
FOR EACH ROW 
BEGIN
   DECLARE s int;
    DECLARE x INT DEFAULT 0;
    DECLARE gap int;
    DECLARE new_date date;
    SET s = NEW.taskterm;
   WHILE s > 0 DO
    set gap = (select if(NEW.TaskDayofWeek >=dayofweek(curdate()), NEW.TaskDayofWeek-dayofweek(curdate()),NEW.TaskDayofWeek-dayofweek(curdate())+7)+7*x);
    set new_date = (select date_add(curdate(), interval gap day));
    INSERT INTO GROUP_TASK_ALL(GroupID, TaskName,TaskDayofWeek,TaskTime,TaskDate)
    VALUES (NEW.GroupID, NEW.TaskName, NEW.TaskDayofWeek, NEW.TaskTime, new_date);
    Set s = (s -1);
    Set x = (x +1);
    END WHILE;
END;

'''
cursor.execute(sql_insert_trigger1)

sql_insert_trigger2 = '''
create TRIGGER Dulpicate_TASK_USER_all After insert on GROUP_TASK_ALL
FOR EACH ROW 
BEGIN
    INSERT INTO GROUP_SCHEDULE
    SELECT GROUP_TASK_ALL.GroupID, TaskName, TaskDayofWeek, TaskTime, TaskDate, participant.UserID
    From GROUP_TASK_ALL, PARTICIPANT
    WHERE participant.GROUPID = New.GROUPID and participant.GroupID = GROUP_TASK_ALL.GroupID
    on duplicate key update GroupID = VALUES(GroupID);
END;

'''
cursor.execute(sql_insert_trigger2)

sql_insert_trigger3 = '''
create TRIGGER reverse_cascade_Delete before delete on GROUP_SCHEDULE
FOR EACH ROW 
BEGIN
   Declare a int;
    SET a = (select Count(*) FROM GROUP_SCHEDULE
         WHERE GroupID = old.GROUPID and TaskName=old.TaskName and TaskDayofWeek = old.TaskDayofWeek and TaskTime = old.TaskTime and TaskDate = old.TaskDate);
    if a = 1 then delete FROM GROUP_TASK_ALL WHERE GroupID = old.GROUPID and TaskName=old.TaskName and TaskDayofWeek = old.TaskDayofWeek and TaskTime = old.TaskTime and TaskDate = old.TaskDate;
    end if ;
END;
'''
cursor.execute(sql_insert_trigger3)

sql_insert_trigger4 = '''
create TRIGGER reverse_cascade_Delete2 before delete on GROUP_TASK_ALL
FOR EACH ROW 
BEGIN
   Declare a int;
    SET a = (select Count(*) FROM GROUP_TASK_ALL
         WHERE GroupID = old.GROUPID and TaskName=old.TaskName and TaskDayofWeek = old.TaskDayofWeek and TaskTime = old.TaskTime);
    if a = 1 then delete FROM GROUP_TASK WHERE GroupID = old.GROUPID and TaskName=old.TaskName and TaskDayofWeek = old.TaskDayofWeek and TaskTime = old.TaskTime;
    end if ;
END;
'''
cursor.execute(sql_insert_trigger4)

sql_insert_trigger5 = '''
create TRIGGER new_participant_schedule after insert on participant
FOR EACH ROW 
BEGIN
    INSERT INTO GROUP_SCHEDULE 
    SELECT GROUP_TASK_ALL.GroupID, TaskName, TaskDayofWeek, TaskTime, TaskDate, New.UserID
    FROM GROUP_TASK_ALL, participant
    Where GROUP_TASK_ALL.GroupID = New.GroupID
    on duplicate key update GroupID = VALUES(GroupID);   
END;
'''
cursor.execute(sql_insert_trigger5)

sql_insert_procedure1 = '''
CREATE PROCEDURE GroupImport
      (GroupName1 char(20),
         USERID1 Char(10))
Begin
   Declare a int;
   INSERT INTO GR0UP(GroupName, IsClass) Values (GroupName1, 0);
    SET a = (select count(*) from gr0up);
    INSERT INTO noclass Values (a, USERID1);
    INSERT INTO Participant Values (a,USERID1, 1);
End;
'''

cursor.execute(sql_insert_procedure1)

sql_insert_function0 = '''SET GLOBAL log_bin_trust_function_creators = 1;
'''
cursor.execute(sql_insert_function0)
db.commit()

sql_insert_function1 = '''
create function career_check(
            UserID1 char(10),
            TestName1 varchar(20),
                LicenseName1 varchar(20),
            CompanyName1 varchar(20),
                circle1 varchar(20))
Returns varchar(1000) 
Begin
   Declare a int;
    Declare b int;
    Declare c int;
    Declare d int;
    Declare e varchar(20);
    Declare f varchar(20);
    Declare result varchar(1000) DEFAULT '1';
   SET a = (SELECT Score from language, USERS where TestName = TestName1 and LANGUAGE.UserID = USERS.UserID and USERS.UserID = UserID1 );
    SET b = (SELECT Score from License, USERS where LicenseName = LicenseName1 and License.UserID = USERS.UserID and USERS.UserID = UserID1);
    SET c = (SELECT Howlong from INTERNSHIP, USERS where CompanyName = CompanyName1 and INTERNSHIP.UserID = USERS.UserID and USERS.UserID = UserID1);
    SET d = (SELECT Howlong from Circle,USERS Where CircleName = Circle1 and Circle.UserID = USERS.UserID and USERS.UserID = UserID1);
    SET e = (SELECT CompanyName from INTERNSHIP, USERS where CompanyName = CompanyName1 and INTERNSHIP.UserID = USERS.UserID and USERS.UserID = UserID1);
    SET f = (SELECT CircleName from Circle,USERS Where CircleName = Circle1 and Circle.UserID = USERS.UserID and USERS.UserID = UserID1);
    SET result = (SELECT concat(IFNULL(concat(TestName1,' : ',a),''),' / ',IFNULL(concat(LicenseName1,' : ',b),''),' / ',IFNULL(e,''),IFNULL(concat(' ',c,'주'),''),' / ',IFNULL(f,''),IFNULL(concat(' ',d,'주'),'')));
return result;
end;
'''
cursor.execute(sql_insert_function1)

# # 기본 데이터 주입

# ## User
#

# In[76]:


cursor.execute(sql_use_Database)
sql_insert_user = '''INSERT INTO users VALUES('ew5224','123','김용우',961011,'학생','정보산업공학','ew5224@naver.com')'''
cursor.execute(sql_insert_user)
sql_insert_user = '''INSERT INTO users VALUES('ab123','123','하현진',101,'대학원생','경영학','hehe@gmail.com');'''
cursor.execute(sql_insert_user)
sql_insert_user = '''INSERT INTO users VALUES('abc123','123','황동영',961013,'학생','컴퓨터과학','y0ng@gmail.com');'''
cursor.execute(sql_insert_user)
sql_insert_user = '''INSERT INTO users VALUES('sakura','123','사쿠라',980319,'아이즈원','비올레타','sakura@gmail.com');'''
cursor.execute(sql_insert_user)
sql_insert_user = '''INSERT INTO users VALUES('jodongkyu','123','조동규',960505,'학생','건축공학','yadong@naver.com');'''
cursor.execute(sql_insert_user)
sql_insert_user = '''INSERT INTO users VALUES('qqqq','123','안규남',940911,'교수','산업공학','qqq@naver.com');'''
cursor.execute(sql_insert_user)
sql_insert_user = '''INSERT INTO users VALUES('a','123','정원찬',701101,'다크나이트','뭐하지','a@gmail.com');'''
cursor.execute(sql_insert_user)
sql_insert_user = '''INSERT INTO users VALUES('b','123','강동인',961013,'학생','컴퓨터공학','y0ng@gmail.com');'''
cursor.execute(sql_insert_user)
sql_insert_user = '''INSERT INTO users VALUES('c','123','최예나',991219,'아이즈원','라비앙로즈','yena@gmail.com');'''
cursor.execute(sql_insert_user)
sql_insert_user = '''INSERT INTO users VALUES('yumyum','123','염정운',960110,'유진남친','유진학박사','yumbyung@gmail.com');'''
cursor.execute(sql_insert_user)
db.commit()

# ## Group

# In[77]:


sql_insert_group = '''INSERT INTO GR0UP (GroupName, IsClass)
                        VALUES('SQL스터디',0),('산정관기말고사대비',0),('구글취준스터디',0),('산업공학과학생회',0),('정산15학번모여라',0),('Hadoop스터디',0)'''
cursor.execute(sql_insert_group)
sql_insert_group = '''INSERT INTO GR0UP (GroupName, IsClass)
                        VALUES('아이즈원',0)'''
cursor.execute(sql_insert_group)
sql_insert_group = '''INSERT INTO GR0UP (GroupName, IsClass)
                        VALUES('다낭여행',0)'''
cursor.execute(sql_insert_group)
sql_insert_group = '''INSERT INTO GR0UP (GroupName, IsClass)
                        VALUES('산정관조모임',0),('지정시예습스터디',0)'''
cursor.execute(sql_insert_group)
db.commit()

# ## Participant
sql_insert_noclass = '''
INSERT INTO noclass Values(1,'ew5224'),(2,'c'),(3,'qqqq'),(4,'jodongkyu');
'''
cursor.execute(sql_insert_noclass)
db.commit()
# In[78]:


sql_insert_participant = '''INSERT INTO participant(GroupID,UserID,IsCaptain) VALUES(1, 'ew5224', 1),(1, 'ab123',0),(1, 'b' , 0);'''
cursor.execute(sql_insert_participant)
sql_insert_participant = '''INSERT INTO participant(GroupID, UserID,IsCaptain) VALUES(2, 'c',1),(2,'sakura',0);'''
cursor.execute(sql_insert_participant)
sql_insert_participant = '''INSERT INTO participant(GroupID, UserID, IsCaptain) VALUES(3, 'qqqq',1),(3,'ew5224',0),(3,'abc123',0),(3,'yumyum',0);'''
cursor.execute(sql_insert_participant)
sql_insert_participant = '''INSERT INTO participant(GroupID, UserID, IsCaptain) VALUES(4, 'jodongkyu',1),(4,'ew5224',0),(4,'abc123',0),(4,'a',0);'''
cursor.execute(sql_insert_participant)
db.commit()

# ## Class

# In[79]:


lll = pd.read_csv('lecture.csv')

# 수업 - 그룹
for i in range(len(lll)):
    sql_insert_class = '''INSERT INTO GR0UP(GroupName, IsClass) VALUES('{GroupName}',1)'''.format(
        GroupName=lll.iloc[i][3])
    cursor.execute(sql_insert_class)
    db.commit()

# 수업 - 클래스
for i in range(len(lll)):
    sql_call_groupID = '''SELECT GroupID FROM GR0UP WHERE GroupName= '{GroupName}';'''.format(GroupName=lll.iloc[i][3])
    cursor.execute(sql_call_groupID)
    GroupID = cursor.fetchall()
    sql_insert_class2 = '''INSERT INTO Class(GroupID,ClassName,Major,ClassProfessor) VALUES({ID},'{ClassName}','산업공학전공','{ClassProfessor}')'''.format(
        ClassName=lll.iloc[i][3], ClassProfessor=lll.iloc[i][4], ID=GroupID[0]['GroupID'])
    cursor.execute(sql_insert_class2)
    db.commit()

# 수업 - 유저
for i in range(len(lll)):
    sql_insert_class_users = '''INSERT INTO USERS VALUES('{Professor}',123,'{Professor}',999,'교수','Nan','Nan')
                            on duplicate key update UserID = VALUES(UserID)'''.format(Professor=lll.iloc[i][4])
    cursor.execute(sql_insert_class_users)
    db.commit()

# 수업 - 파티시펀트
for i in range(len(lll)):
    sql_call_groupID = '''SELECT GroupID FROM GR0UP WHERE GroupName= '{GroupName}';'''.format(GroupName=lll.iloc[i][3])
    cursor.execute(sql_call_groupID)
    GroupID = cursor.fetchall()
    GroupID = int(GroupID[0]['GroupID'])
    sql_insert_participant_prof = '''INSERT INTO PARTICIPANT(GroupID, UserID,IsCaptain) VALUES({ID},'{Professor}',1)'''.format(
        ID=GroupID, Professor=lll.iloc[i][4])
    print(sql_insert_participant_prof)
    cursor.execute(sql_insert_participant_prof)
    db.commit()

# 수업 - 그룹 태스크
for i in range(len(lll)):
    sql_call_groupID = '''SELECT GroupID FROM GR0UP WHERE GroupName= '{GroupName}';'''.format(GroupName=lll.iloc[i][3])
    cursor.execute(sql_call_groupID)
    GroupID = cursor.fetchall()
    for j in range(len(lll.iloc[i][5].split(','))):
        if len(lll.iloc[i][5].split(',')[j]) > 1:
            a = int(lll.iloc[i][5].split(',')[j][0].replace('월', '2').replace('화', '3').replace('수', '4').replace('목',
                                                                                                                  '5').replace(
                '금', '6').replace('토', '7').replace('일', '1'))
            b = int(lll.iloc[i][5].split(',')[j][1]) + 8
        else:
            a = int(
                lll.iloc[i][5].split(',')[j - 1][0].replace('월', '2').replace('화', '3').replace('수', '4').replace('목',
                                                                                                                  '5').replace(
                    '금', '6').replace('토', '7').replace('일', '1'))
            b = int(lll.iloc[i][5].split(',')[j][0]) + 8
        sql_insert_class_task = '''INSERT INTO GROUP_TASK(GroupID,TaskName,TaskDayofWeek,TaskTime,TaskTerm) VALUES({ID},'{TaskName}',{TaskDayofWeek},{TaskTime},3)'''.format(
            ID=GroupID[0]['GroupID'], TaskName=lll.iloc[i][3], TaskDayofWeek=a, TaskTime=b)
        print(sql_insert_class_task)
        cursor.execute(sql_insert_class_task)
        db.commit()

# ## GroupTask

# In[80]:


sql_insert_grouptask = '''
INSERT INTO Group_Task Values(1, 'SQL스터디',3,12,5),(1,'SQL스터디',3,13,5),(2,'산정관기말고사팀',2,17,3),(2,'산정관기말고사팀',2,18,3)
,(2,'산정관기말고사팀',2,19,3),(3,'구글코딩테스트스터디',6,10,2),(3,'구글코딩테스트스터디',6,11,2),(3,'구글면접스터디',6,12,2),
(4,'23대학생회 종강총회',5,20,1)'''

cursor.execute(sql_insert_grouptask)
db.commit()

# ## Career

# In[81]:


sql_insert_language = '''
INSERT INTO Language Values('a','TOEFL',120,'2019-03-31', '2019-04-01'), ('a','JLPT',2,null,null),('ew5224','TOEFL',99,'2017-12-13','2019-12-31'),('c','TOEFL',45,'2010-10-01','2012-10-01'),('jodongkyu','TOEFL',120,null ,null ),('jodongkyu','TOEIC',990,null,null);
'''
cursor.execute(sql_insert_language)

sql_insert_license = '''
INSERT INTO license Values('a','SQLD',1,'2018-06-30', '2019-04-01'), ('a','운전면허',2,null,null),('ew5224','정보처리기사',1,'2017-12-13','2019-12-31'),('sakura','정보처리기사',1,'2010-10-01','2012-10-01'),('jodongkyu','SQLD',1,null ,null ),('jodongkyu','정보처리기사',1,null,null);
'''
cursor.execute(sql_insert_license)

sql_insert_circle = '''
INSERT INTO circle Values('a','ybigta','일반',Null), ('b','ybigta','일반',null),('ew5224','ybigta','부회장',52),('sakura','아이즈원','멤버',520),('jodongkyu','yii','조동규',null),('jodongkyu','ybigta','하고싶다',null);
'''
cursor.execute(sql_insert_circle)

sql_insert_internship = '''
INSERT INTO internship Values('a','삼성전자','인턴',Null), ('b','삼성전자','채용형',null),('ew5224','구글','부회장',52),('sakura','구글','인턴',26),('jodongkyu','구글','인턴',null),('jodongkyu','LG CNS','인턴',null);
'''
cursor.execute(sql_insert_internship)

db.commit()

# ## Class Participant

# In[82]:


sql_insert_class_participant = '''
INSERT INTO participant Values(25,'ew5224',0),(25,'jodongkyu',0),(25,'sakura',0),(25,'yumyum',0),(25,'c',0)
'''
cursor.execute(sql_insert_class_participant)
db.commit()