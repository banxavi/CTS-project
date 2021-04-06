from typing import ContextManager
from flask.globals import g
from flask.templating import render_template
from flask import Flask, render_template, redirect, url_for, request, flash, session, sessions
from app import app
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pymysql
import re
import smtplib
import ssl
import configadmin
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from pymysql import cursors
from werkzeug.utils import format_string
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib,uuid

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'cts'
mysql = MySQL(app) 


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
    loi = None
    global tmaname
    global tma
    global idempl
    # try:
    if request.method == 'POST':
        tma = request.form['idname']
        password = request.form['password']
        passhash = hashlib.md5(password.encode()).hexdigest()
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT Email, Password FROM employee WHERE email = %s AND password = %s', (tma,  passhash,))
        account = cursor.fetchone()

        if tma==configadmin.username and password==configadmin.password:
            session['idname'] = request.form['idname']  
            return render_template('/home.html' )

        if account:
            session['idname'] = request.form['idname']      
            return render_template('/home.html')

        else:
            loi = 'Tài khoản hoặc mật khẩu sai'
    return render_template("login.html",loi=loi)

# Notification register
@app.route('/notiregister',methods=['GET','POST'])
def register():
    return render_template("notification_register.html")

# Update password when verify link gmail
@app.route('/updatepass',methods=['GET','POST'])
def updatepass():
    return render_template("update_password.html")
    # forgot password 
@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():
    return render_template("forgot_password.html")

#Forgot password user
@app.route('/forgotpsw')
def forgotpsw():
    return render_template('forgot_password.html')


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