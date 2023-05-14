from datetime import datetime
import docx2txt
import PyPDF2
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utilities.Logger import App_Logger

class ResumeParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.resume_text = ""
        self.file_object = open("LogFolder/Log_"+str(datetime.now().date())+".txt", 'a+')
        self.log_writer = App_Logger()

        if (filepath.endswith('.docx')):
            with open(filepath, 'rb') as f:
                self.resume_text = docx2txt.process(f)
                self.log_writer.log(self.file_object, 'Resume converted to text from docx')
        elif (filepath.endswith('.pdf')):
            with open(filepath, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)
                for pgno in range(num_pages):
                    pgtext = pdf_reader.pages[pgno].extract_text()
                    self.resume_text += pgtext
                self.log_writer.log(self.file_object, 'Resume Converted to text from pdf')
    def DataCleaning(self,dataset):
        try:
            self.log_writer.log(self.file_object, 'Data Cleaning Started')
            tokens = word_tokenize(dataset)
            self.log_writer.log(self.file_object, 'Tokenizing completed')
            stop_words = set(stopwords.words('english'))
            filtered_tokens = []
            for token in tokens:
                if token.lower() not in stop_words and token.isalpha():
                    filtered_tokens.append(token.lower())
            self.log_writer.log(self.file_object, 'Filtered Tokens Generated')
            return filtered_tokens
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured:'+str(e))
            raise e
    def GetSkillSets(self,jobDescriptions):
        try:
            self.log_writer.log(self.file_object, 'Getting skills values started')
            resumeFiltered = self.DataCleaning(self.resume_text)
            jobDescrpFiltered = self.DataCleaning(jobDescriptions)
            skills = []
            for token in resumeFiltered:
                if token in jobDescrpFiltered:
                    skills.append(token)
            skills = list(set(skills))
            self.log_writer.log(self.file_object, 'All skills extracted')
            bags = [' '.join(jobDescrpFiltered), ' '.join(skills)]
            vectorizer = CountVectorizer()
            self.log_writer.log(self.file_object, 'Creating bag of words with Vectors')
            vectors = vectorizer.fit_transform(bags).toarray()
            v1 = vectors[0].reshape(1, -1)
            v2 = vectors[1].reshape(1, -1)
            self.log_writer.log(self.file_object, 'Started cosine similarity check')
            cosine_sim = cosine_similarity(v1, v2)[0][0]
            similarity_percent = cosine_sim * 100
            self.log_writer.log(self.file_object, 'Similarity Check completed ')
            return round(similarity_percent, 1)
        except Exception as e:
            self.log_writer.log(self.file_object, 'Exception Occured:'+str(e))
            raise e


