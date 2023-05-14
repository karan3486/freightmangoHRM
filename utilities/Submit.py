from datetime import datetime
import os
from utilities.Logger import App_Logger
from werkzeug.utils import secure_filename
from MLRepository.ResumeParser import ResumeParser


class FormSubmit:
    def __init__(self):
        self.file_object = open("LogFolder/Log_"+str(datetime.now().date())+".txt", 'a+')
        self.log_writer = App_Logger()

    @staticmethod
    def Allowed_file_image(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}
    @staticmethod
    def Allowed_file_resume(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'docx', 'pdf','doc'}

    def SaveForm(self,resumefile,email,jobDescription,employee,isUpdate,addressList,conn):
        try:
            self.log_writer.log(self.file_object, 'Resume parsing started')
            filename = secure_filename(resumefile.filename)
            path = os.path.join('Resume', email + '.' + filename.split('.')[1])
            self.log_writer.log(self.file_object, 'Resume Saving....')
            resumefile.save(path)
            self.log_writer.log(self.file_object, 'Resume Saved')
            resumeParser = ResumeParser(path)
            self.log_writer.log(self.file_object, 'Resume parsed')
            skills_percent = resumeParser.GetSkillSets(jobDescription)
            self.log_writer.log(self.file_object, 'Skill percentage fetched')
            employee.skillpercent = skills_percent
            self.log_writer.log(self.file_object, 'Employee Saving Started')
            if (isUpdate):
                self.log_writer.log(self.file_object, 'Employee Update Started')
                id = employee.update_employee(conn)
                self.log_writer.log(self.file_object, 'Employee Updated')
                data = []
                if (len(addressList) > 1):
                    for addr in addressList[1:]:
                        data.append((id, addr))
                        employee.UpdateAddresses(conn, data, id)
                        self.log_writer.log(self.file_object, 'Employee Address Saved')
            else:
                id = employee.create_employee(conn)
                self.log_writer.log(self.file_object, 'Employee Saved')
                data = []
                if (len(addressList) > 1):
                    for addr in addressList[1:]:
                        data.append((id, addr))
                        employee.SaveAddresses(conn, data)
                        self.log_writer.log(self.file_object, 'Employee Address Saved')

        except Exception as e:
            self.log_writer.log(self.file_object,'Exception Occured: '+ str(e))
            raise e

