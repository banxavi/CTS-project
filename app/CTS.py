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
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from pymysql import cursors
from werkzeug.utils import format_string
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import alert
from datetime import *
import pyautogui as pag


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
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
@app.route('/mission',methods=['GET','POST'])
def mission():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from mission')
    task = cursor.fetchall()
    return render_template('missionsystemadmin.html',task=task)


@app.route('/viewmission', methods=['GET','POST'])
def viewmission():
    if request.method == 'POST':
        id = request.form['id']
        cursor = mysql.connection.cursor()
        sqlview = 'select employee.Name from process,employee \
        where  process.Employee_Id=employee.Employee_Id  and Mission_Id = %s'
        cursor.execute(sqlview,id)
        view = cursor.fetchall()
        for a in view:
            flash("{}".format(a[0]))
        return redirect(url_for('mission'))

# Admin add mission
@app.route('/addmission',methods=["GET","POST"])
def addmission():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        descr = request.form['descr']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        point = request.form['point']
        limit = request.form['limit']
        start = datetime.strptime(startdate,"%Y-%m-%d" )
        end = datetime.strptime(enddate,"%Y-%m-%d")
        if start >= end  :
            # flash("{}".format(alert.errordate))
            pag.alert(text=alert.errordate, title="Thông báo:")
            return redirect(url_for('mission'))
        else :
            sqlinsert = 'INSERT INTO `cts`.`mission` (`Title`, `Description`, `StartDate`, `EndDate`, `Limit`, `Point`)  VALUES (%s, %s, %s,%s,%s,%s)'
            val = (name,descr,startdate,enddate,limit,point)
            cursor.execute(sqlinsert,val)
            mysql.connection.commit()
            flash("{}".format(alert.addmissonsucc))
            return redirect(url_for('mission'))
        
# Admin edit mission
@app.route('/editmission',methods=["GET","POST"])
def editmission():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        descr = request.form['descr']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        point = request.form['point']
        limit = request.form['limit']
        state1 = 1
        state0 = 0
        start = datetime.strptime(startdate,"%Y-%m-%d" )
        end = datetime.strptime(enddate,"%Y-%m-%d")
        if start >= end:
            # flash("{}".format(alert.errordate))
            pag.alert(text=alert.errordate, title="Thông báo:")
            return redirect(url_for('mission'))
        elif int(limit) >=1:
            sqlupdate = 'UPDATE `cts`.`mission` SET State =%s, `Title` = %s, `Description` = %s, `StartDate` = %s, `EndDate` = %s, `Limit` = %s, `Point` = %s \
                WHERE (`Mission_Id` = %s)'
            val = (state1,name,descr,startdate,enddate,limit,point,id,)
            cursor.execute(sqlupdate,val)
            mysql.connection.commit()
            flash("{}".format(alert.editmissionsucc))
            return redirect(url_for('mission'))
        elif int(limit)<=0 :
            sqlupdate = 'UPDATE `cts`.`mission` SET State = %s, `Title` = %s, `Description` = %s, `StartDate` = %s, `EndDate` = %s, `Limit` = %s, `Point` = %s \
                WHERE (`Mission_Id` = %s)'    
            val = (state0,name,descr,startdate,enddate,limit,point,id,)
            cursor.execute(sqlupdate,val)      
            mysql.connection.commit()
            flash("{}".format(alert.editmissionsucc))
            return redirect(url_for('mission'))

# Admin edit mission
@app.route('/deletemission/<id>/',methods=["GET","POST"])
def deletemission(id):
    cursor = mysql.connection.cursor()
    sqldelete = 'DELETE from mission WHERE Mission_Id=%s'
    val = id
    cursor.execute(sqldelete,(val,))
    mysql.connection.commit()
    flash("{}".format(alert.deletemissionsucc))
    return redirect(url_for('mission'))

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