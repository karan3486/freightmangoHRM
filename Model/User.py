from datetime import datetime

from utilities.Logger import App_Logger

class User:
    def __init__(self, fname='', lname='', username='', password=''):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.password = password
        self.file_object = open("LogFolder/Log_"+str(datetime.now().date())+".txt", 'a+')
        self.log_writer = App_Logger()
    def create_table_user(conn1):
        c1 = conn1.cursor()
        c1.execute('''CREATE TABLE IF NOT EXISTS TaUser
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      firstname TEXT NOT NULL,
                      lastname TEXT NOT NULL,
                      username TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL
                      )''')
        conn1.commit()
    def create_user(self,conn1):
        c1 = conn1.cursor()
        c1.execute("""SELECT count(*) FROM TaUser WHERE username=?""", (self.username,))
        row = c1.fetchone()
        if (row[0] > 0):
            return False
        else:
            c1.execute("""INSERT INTO TaUser (firstname, lastname, username, password)
                              VALUES (?, ?, ?, ?)""",
                       (self.fname, self.lname, self.username, self.password))
            conn1.commit()
            return True
        #return row[0]
    def AuthenticateUser(self,conn1,username,password):
        try:
            c1 = conn1.cursor()
            self.log_writer.log(self.file_object, 'User Authentication Started')
            c1.execute("""SELECT count(*) FROM TaUser WHERE username=? AND password=?""", (username, password))
            row = c1.fetchone()
            self.log_writer.log(self.file_object, 'User Fetched')
            if (row[0] == 1):
                self.log_writer.log(self.file_object, 'User Successfully Verified')
                return True
            else:
                self.log_writer.log(self.file_object, 'Unauthorized User not verified')
                return False
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured:'+str(e))
            raise e
