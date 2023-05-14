from database.db import DB
from Model.User import User
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename, send_file
from utilities.Submit import FormSubmit
from Model.Employee import Employee
from MLRepository.ImageDetection import HumanFaceDetection
import nltk

app = Flask(__name__)
app.secret_key = 'my_secret_key'


@app.route('/', methods=['GET'])
@cross_origin()
def LoginPage():
    nltk.download('punkt')
    nltk.download('stopwords')
    return render_template("login.html")

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('LoginPage'))

@app.route('/home', methods=['POST', 'GET'])
@cross_origin()
def HomePage():
    try:
        db = DB()
        db.InitTables()
        if('user_id' in session):
            return render_template('home.html')
        username = request.form['username']
        password = request.form['password']
        user=User()
        if (user.AuthenticateUser(db.instance, username, password)):
            session['user_id'] = username
            return render_template('home.html')
        else:
            flash("User Does Not Exists")
            return render_template('login.html')
    except Exception as e:
        return render_template('login.html')
    finally:
        db.Close()

@app.route('/registration', methods=['POST', 'GET'])
@cross_origin()
def Registration():
    try:
        id = request.args.get('id')
        isedit = False
        if (id == None):
            id = 0
        else:
            isedit = True
        db = DB()
        employee=Employee()
        emp = employee.read_employee(db.instance, id)
        addresses = employee.get_all_addresses(db.instance, id)
        return render_template('registration.html', employee=emp, isEdit=isedit, addresses=enumerate(addresses))
    except Exception as e:
        return render_template('registration.html', employee=None, isEdit=None, addresses=[])
    finally:
        db.Close()

@app.route('/createuser', methods=['POST', 'GET'])
@cross_origin()
def CreateUser():
    return  render_template('createuser.html')

@app.route('/saveuser', methods=['POST', 'GET'])
@cross_origin()
def SaveUser():
    try:
        db = DB()
        name = request.form['name']
        lname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        confpassword = request.form['confirmpassword']
        if (password == confpassword):
            user = User(name, lname, username, password)
            if (user.create_user(db.instance)):
                return render_template('login.html')
            else:
                flash("Username already in Use")
                return render_template('createuser.html')
        else:
            flash("Password does not match")
            return render_template('createuser.html')
    except Exception as e:
        return render_template('createuser.html')
    finally:
        db.Close()

@app.route('/get_all_employees')
@cross_origin()
def GetAllEmployee():
    try:
        db = DB()
        emp=Employee()
        employees = emp.get_all_employees(db.instance)
        datalist = []
        for emp in employees:
            data = {
                "name": emp.name,
                "email": emp.email,
                "country": emp.country,
                "city": emp.city,
                "zipcode": emp.zip_code,
                "phone": emp.phone,
                "department": emp.department,
                "skillpercent":emp.skillpercent,
                "id": emp.id,
                "edit": "edit",
                "delete": "delete"
            }
            datalist.append(data)
        data = jsonify({'data': datalist})
        return data
    except Exception as e:
        return jsonify({'data': []})
    finally:
        db.Close()

@app.route('/delete-employee/<int:id>', methods=['DELETE'])
@cross_origin()
def DeleteEmployee(id):
    try:
        db=DB()
        emp=Employee()
        emp.delete_employee(db.instance,id)
        return jsonify({'message': 'Employee deleted successfully.'})
    except:
        return jsonify({'error': 'Error deleting employee.'}), 500
    finally:
        db.Close()

@app.route('/view_pdf/<filename>')
def ViewResume(filename):
    return send_file('Resume/' + filename+'.pdf', mimetype='application/pdf',environ=request.environ)

@app.route('/submit', methods=['POST', 'GET'])
@cross_origin()
def Submit():
    try:
        if request.method == 'POST':
            db = DB()
            name = request.form['name']
            email = request.form['email']
            country = request.form['country']
            city = request.form['city']
            zip_code = request.form['zip']
            address = request.form['address']
            phone = request.form['phone']
            department = request.form['department']
            emp = ['', name, email, country, city, zip_code, address, phone, department]
            isUpdate = eval(request.form['update'])
            addressList = request.form.getlist('address')
            employee = Employee(name, email, country, city, zip_code, address, phone, department, '')
            imagefile = request.files['photo']
            resumefile = request.files['resume']
            jobDescription = request.form['skill']
            formSubmit=FormSubmit()
            if (not isUpdate and employee.IsDuplicateEmail(db.instance)):
                flash("Email ID Provided is Already Exists!")
                return render_template('registration.html', employee=emp)
            if imagefile and formSubmit.Allowed_file_image(imagefile.filename):
                detect = HumanFaceDetection(imagefile)
                if (detect.VerifyDetection()):
                    detect.SaveProfileImage(email)
                else:
                    flash("Please Upload Valid Profile Picture")
                    return render_template('registration.html', employee=emp, isEdit=isUpdate)
            else:
                flash("Please Upload Picture with Valid format")
                return render_template('registration.html', employee=emp, isEdit=isUpdate)
            if resumefile and formSubmit.Allowed_file_resume(resumefile.filename):
                formSubmit.SaveForm(resumefile, email, jobDescription, employee, isUpdate, addressList, db.instance)
            else:
                flash("Please Upload Resume with Valid format")
                return render_template('registration.html', employee=emp, isEdit=isUpdate)
            return render_template('home.html')
    except Exception as e:
        flash("Exception Occured: "+str(e))
        return render_template('registration.html', employee=emp, isEdit=isUpdate)
    finally:
        db.Close()



if __name__ == "__main__":
    app.run(port=4080)
    #app.run(host='127.0.0.1', port=5016, debug=True)
   # app.run(debug=True)
