from datetime import datetime
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename
from utilities.Logger import App_Logger

class HumanFaceDetection:
    def __init__(self,imagefile):
        self.imagefile=imagefile
        self.IsHumanFaceDetected=False
        self.file_object = open("LogFolder/Log_"+str(datetime.now().date())+".txt", 'a+')
        self.log_writer = App_Logger()
    def VerifyDetection(self):
        try:
           self.log_writer.log(self.file_object, 'Image Detection Started')
           img = cv2.imdecode(np.fromstring(self.imagefile.read(), np.uint8), cv2.IMREAD_UNCHANGED)
           self.log_writer.log(self.file_object, 'Model Haarcascade Initialized')
           face_cascade = cv2.CascadeClassifier('utilities/haarcascade_frontalface_default.xml')
           gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
           self.log_writer.log(self.file_object, 'Converted to Gray Scale')
           face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
           self.log_writer.log(self.file_object, 'Detection completed')
           self.IsHumanFaceDetected=len(face)==1
           self.log_writer.log(self.file_object, 'Returing the detection')
           return self.IsHumanFaceDetected
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured:'+str(e))
            return self.IsHumanFaceDetected
    def SaveProfileImage(self,email):
        try:
            self.log_writer.log(self.file_object, 'Profile Image Save started')
            imagefilename = secure_filename(self.imagefile.filename)
            self.imagefile.save(os.path.join('images', email + '.' + imagefilename.split('.')[1]))
            self.log_writer.log(self.file_object, 'Image Saved')
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured:'+str(e))
            raise e
