from datetime import datetime
from utilities.Logger import App_Logger
class Employee:
    def __init__(self, name='', email='', country='', city='', zip_code='', address='', phone='', department='',skillpercent='',id=None, profile_photo=None, resume=None):
        self.name = name
        self.email = email
        self.country = country
        self.city = city
        self.zip_code = zip_code
        self.address = address
        self.phone = phone
        self.department = department
        self.profile_photo = profile_photo
        self.resume = resume
        self.id=id
        self.skillpercent=skillpercent
        self.file_object = open("LogFolder/Log_" + str(datetime.now().date()) + ".txt", 'a+')
        self.log_writer = App_Logger()

    def create_employee(self,conn1):
        try:
            c1 = conn1.cursor()
            self.log_writer.log(self.file_object, 'Inserting to Table TaEmployee started')
            c1.execute("""INSERT INTO TaEmployee (name, email, country, city, zip, address, phone, department,skillpercent)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)""",
                       (self.name, self.email, self.country, self.city, self.zip_code, self.address, self.phone,
                        self.department, self.skillpercent))

            c1.execute("""SELECT id FROM TaEmployee WHERE email=?""", (self.email,))
            row = c1.fetchone()
            conn1.commit()
            self.log_writer.log(self.file_object, 'Record Successfully created and Saved in TaEmployee table')
            return row[0]
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured: '+str(e))
            raise e

    def update_employee(self,conn1):
        try:
            c1 = conn1.cursor()
            self.log_writer.log(self.file_object, 'Updating TaEmployee table started')
            c1.execute(
                "UPDATE  TaEmployee SET name=?, country=?, city=?, zip=?, address=?, phone=?, department=?,skillpercent=? WHERE email=?",
                (self.name, self.country, self.city, self.zip_code, self.address, self.phone, self.department,
                 self.skillpercent, self.email))
            c1.execute("""SELECT id FROM TaEmployee WHERE email=?""", (self.email,))
            row = c1.fetchone()
            conn1.commit()
            self.log_writer.log(self.file_object, 'Update table completed successfully')
            return row[0]
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured:'+str(e))
            raise e

    def IsDuplicateEmail(self,conn1):
        try:
            c1 = conn1.cursor()
            self.log_writer.log(self.file_object, 'Checking the Duplicate email values')
            c1.execute("""SELECT COUNT(*) FROM TaEmployee WHERE email=?""", (self.email,))
            row = c1.fetchone()
            if (row[0] > 0):
                self.log_writer.log(self.file_object, 'Duplicate emails Found')
                return True
            else:
                self.log_writer.log(self.file_object, 'No Duplicate emails found')
                return False
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured:'+str(e))
            raise e

    def SaveAddresses(self,conn1,data):
        try:
            c1 = conn1.cursor()
            self.log_writer.log(self.file_object, 'Saving Address Started')
            self.log_writer.log(self.file_object, 'Inserting addresses to TaAddress table initiated')
            query = 'INSERT INTO TaAddress (id, address) VALUES (?, ?)'
            c1.executemany(query, data)
            conn1.commit()
            self.log_writer.log(self.file_object, 'Data Saved successfully')
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured:'+str(e))
            raise e

    def UpdateAddresses(self,conn1,data,id):
        try:
            c1 = conn1.cursor()
            c1.execute("""DELETE FROM TaAddress WHERE id=?""", (id,))
            conn1.commit()
            query = 'INSERT INTO TaAddress (id, address) VALUES (?, ?)'
            c1.executemany(query, data)
            conn1.commit()
        except Exception as e:
            raise e

    def get_all_addresses(self,conn1,id):
        try:
            cursor = conn1.cursor()
            cursor.execute("""SELECT * FROM TaAddress WHERE id=?""", (id,))
            rows = cursor.fetchall()
            return rows
        except Exception as e:

            raise e

    def get_all_employees(self,conn1):
        try:
            cursor = conn1.cursor()
            self.log_writer.log(self.file_object, 'Getting All records of Employee')
            cursor.execute("SELECT * FROM TaEmployee")
            rows = cursor.fetchall()
            self.log_writer.log(self.file_object, 'Successfully fetched all the record')
            employees = []
            for row in rows:
                employee = Employee(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[0])
                employees.append(employee)
            return employees
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured: ' + str(e))
            raise e

    def delete_employee(self,conn,id):
        try:
            cursor = conn.cursor()
            self.log_writer.log(self.file_object, 'Deleting employee '+str(id))
            cursor.execute("""DELETE FROM TaEmployee WHERE id=?""", (id,))
            conn.commit()
            self.log_writer.log(self.file_object, 'Employee successfully deleted')
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured: ' + str(e))
            raise e

    def read_employee(self,conn,id):
        try:
            cursor = conn.cursor()
            self.log_writer.log(self.file_object, 'Getting all details of employee of:'+str(id))
            cursor.execute("""SELECT * FROM TaEmployee WHERE id=?""", (id,))
            row = cursor.fetchone()
            self.log_writer.log(self.file_object, 'Successfully fetched')
            return row
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured: '+str(e))
            raise e

    @staticmethod
    def create_table(conn1):
        c1 = conn1.cursor()
        c1.execute('''CREATE TABLE IF NOT EXISTS TaEmployee
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          email TEXT NOT NULL,
                          country TEXT NOT NULL,
                          city TEXT NOT NULL,
                          zip TEXT NOT NULL,
                          address TEXT NOT NULL,
                          phone TEXT NOT NULL,
                          department TEXT NOT NULL,
                          skillpercent TEXT
                          )''')
        conn1.commit()

    @staticmethod
    def create_table_address(conn1):
        c1 = conn1.cursor()
        c1.execute('''CREATE TABLE IF NOT EXISTS TaAddress
                             (id TEXT,
                              address TEXT
                              )''')
        conn1.commit()

