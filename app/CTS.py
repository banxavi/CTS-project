from typing import List
from flask.templating import render_template
from flask import Flask, render_template, redirect,url_for,request,flash,session,sessions
from app import app
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import pymysql
import re
import hashlib
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail, Message
from pymysql import cursors
from werkzeug.utils import format_string
import DTO
import alert
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config.from_pyfile('MailConfig.cfg')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'cts'

mysql = MySQL(app) 
mail = Mail(app)
s = URLSafeTimedSerializer('thisisascrect!')

# Function LOGOUT
@app.route('/')
def home():
    return render_template("home.html")

# Logout account
@app.route('/logout')
def logout():
    return render_template("login.html")
    
# Login    
@app.route('/logi',methods=['GET','POST'])
def login():
    loi = ""
    if request.method == 'POST':
        user = request.form['idname']
        psw = request.form['password']
        if user=="abc" and psw=="123":
            session['idname'] = request.form['idname']  
            return render_template('home.html')
        if user=="abcd" and psw =="123":
            session['idname'] = request.form['idname']     
            return render_template('home.html')
        else:
                loi = 'Tài khoản hoặc mật khẩu sai'
    return render_template("login.html",loi=loi)

# Notification register
@app.route('/notiregister',methods=['GET','POST'])
def register():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        token = s.dumps(email, salt='email-confirm')
        msg = Message('Confirm email',sender="ctsinternshipqnu@gmail.com", recipients=[email])
        link = url_for('confirm_email', token = token, _external = True)
        msg.html= render_template('form_mail.html',link = link)
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT * FROM Employee WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            error = "Tài khoản này đã tồn tại"
        else:
            mail.send(msg)
            return render_template('notification_register.html')
    return render_template("login.html", errorres = error)     

#Accept link gmail
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=36000)
        return redirect(url_for('updatepass', email = email))
    except SignatureExpired:
        return render_template('overtime_mail.html')


# Update password when verify link gmail
@app.route('/updatepass',methods=['GET','POST'])
def updatepass():
    error = ""
    email = request.args.get('email', None)
    if request.method == 'POST':
        password = request.form['password']
        pass_confirm = request.form['pass_confirm']
        if password != pass_confirm:
            error = alert.loginfailpassword
        else:
            passhash = hashlib.md5(password.encode()).hexdigest() 
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO employee (Email,Password) VALUES (%s,%s)", (email,passhash,))
            mysql.connection.commit()
            session['idname'] = email
            return render_template('/home.html', email = email)
    return render_template("update_password.html",email =email,error = error)

# forgot password 
@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        token = s.dumps(email, salt='email-confirm')
        msg = Message('Confirm email',sender="ctsinternshipqnu@gmail.com", recipients=[email])
        link = url_for('forgot_email', token = token, _external = True)
        msg.html= render_template('form_forgot_pass.html',link = link)
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT * FROM Employee WHERE email = %s', (email,))
        account = cursor.fetchone()
        if not(account):
            error = alert.forgotfailemail
        else:
            mail.send(msg)
            return render_template('notification_register.html')
    return render_template("forgot_password.html",error = error)

#Accept link mail forgot password
@app.route('/forgot_email/<token>')
def forgot_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=36000)
        return redirect(url_for('updatepassforgot', email = email))
    except SignatureExpired:
        return render_template('overtime_mail.html')

#Update Password forgot
@app.route('/updatepassforgot',methods=['GET','POST'])
def updatepassforgot():
    error = ""
    email = request.args.get('email', None)
    if request.method == 'POST':
        password = request.form['password']
        pass_confirm = request.form['pass_confirm']
        if password != pass_confirm:
            error = alert.loginfailpassword
        else:
            passhash = hashlib.md5(password.encode()).hexdigest() 
            cur = mysql.connection.cursor()
            cur.execute("UPDATE employee SET password=%s WHERE email=%s",
                        (passhash, email))
            mysql.connection.commit()
            session['idname'] = email
            return render_template('/home.html', email = email)
    return render_template("update_password.html",email =email,error = error)

# #Forgot password user
# @app.route('/forgotpsw')
# def forgotpsw():
#     return render_template('forgot_password.html')


#Form forgot password when verify link Gmail
# @app.route('/verifyforgot')
# def verifyforgot():
#     return render_template('verifyforgot.html')

# Admin Management Mission
@app.route('/mission')
def mission():
    # with open("dummydataTask.json", "r",encoding="utf8") as fin:
    #     data = json.load(fin)
    # Task = data 
    # print(Task[1])
    # print(type(Task))
    Task = DTO.Myreq
    return render_template("missionsystemadmin.html",Task1=Task)

# User Management
@app.route('/usermanagement')
def usermanagement():
    return render_template("usermanagement.html")
# Management ward admin
@app.route('/managementward')
def managementward():
    return render_template("managementward.html")


 # Fuction User
 # User's mission
@app.route('/usermission')
def usermission():
    return render_template("usermission.html")
 # Mission avaiable
@app.route('/usermissionavaiable')
def usermissionavaiable():
    return render_template("usermissionavaiable.html")
# User profile
# @app.route('/userprofile')
# def userprofile():
#     return render_template("userprofile.html")