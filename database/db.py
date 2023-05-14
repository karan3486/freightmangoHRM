import sqlite3
from datetime import datetime

from Model.Employee import Employee
from Model.User import User
from utilities.Logger import App_Logger


class DB():
    def __init__(self):
        self.instance=sqlite3.connect('database/dbHRManagement.db')
        self.file_object = open("LogFolder/Log_"+str(datetime.now().date())+".txt", 'a+')
        self.log_writer = App_Logger()
        self.log_writer.log(self.file_object, 'Database Connection started')
    def InitTables(self):
        try:
            self.log_writer.log(self.file_object, 'Table creation started')
            User.create_table_user(self.instance)
            Employee.create_table(self.instance)
            Employee.create_table_address(self.instance)
            self.log_writer.log(self.file_object, 'Table created')
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured:'+str(e))
            raise e
    def Close(self):
        self.instance.close()
        self.log_writer.log(self.file_object, 'DataBase Connection Closed')

