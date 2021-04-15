from typing import ContextManager
from flask.globals import g
from flask.templating import render_template
from flask import Flask, render_template, redirect, url_for, request, flash, session, sessions
from app import app
from flask_mysqldb import MySQL
import hashlib
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail, Message
from pymysql import cursors
from werkzeug.utils import format_string
import DTO
import SQL
import alert
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from pymysql import cursors
from werkzeug.utils import format_string
from flask_mail import Mail, Message
import alert
import SQL
import constants
import configadmin
from datetime import date, datetime,timedelta
import pyautogui as pag

app.config.from_pyfile('MailConfig.cfg')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_DB'] = 'cts'
mysql = MySQL(app) 
mail = Mail(app)
s = URLSafeTimedSerializer('thisisascrect!')

@app.route('/')
def home():
    global image
    if 'idname' not in session:
        return render_template("login.html")
    elif session['idname']=="abc":
        
        return render_template('home.html')
    elif 'idname' in session: 
        email = session['idname']
        cursor = mysql.connection.cursor() 
        cursor.execute(SQL.SQLIMAGE,(email,))
        image = cursor.fetchone()
        cursor.execute(SQL.SQLHOMEUSER1,(email,))
        homeuser = cursor.fetchone()
        cursor.execute(SQL.SQLHOMEUSER2,(email,))
        homeuser1 = cursor.fetchone()
        return render_template('home.html',img=image[0],point=image[1],homeuser=homeuser[0],homeuser1=homeuser1[0])
    else:
        return render_template("login.html")

@app.route('/home')
def homeadmin():
    if 'idname' in session: 
        cursor = mysql.connection.cursor() 
        cursor.execute(SQL.SQLHOMECOUNTEMPL)
        countempl = cursor.fetchone()
        cursor.execute(SQL.SQLHOMECOUNTMISS)
        countmiss = cursor.fetchone()
        return render_template('home.html',countempl=countempl[0],countmiss=countmiss[0])
    else:
        return render_template("login.html")
# Logout account
@app.route('/logout')
def logout():
    session.pop('idname', None)
    return render_template("login.html")
    
# Login    
@app.route('/logi',methods=['GET','POST'])
def login():
    error = ""
    global image
   
    if request.method == 'POST':
        cursor = mysql.connection.cursor() 
        user = request.form['idname']
        psw = request.form['password']
        passhash = hashlib.md5(psw.encode()).hexdigest() 
        cursor.execute(SQL.SQLCHECKBLOCK, (user, passhash)) 
        checkblock = cursor.fetchone()
        cursor.execute(SQL.SQLCHECKPASS,(user,passhash,))
        check = cursor.fetchone()
        if configadmin.username==user and configadmin.password==psw:
            session['idname'] = request.form['idname']  
            return redirect(url_for('homeadmin'))
            # return render_template('home.html')

        elif checkblock:
            error = alert.LOGINSTATUS  
        elif check:
            session['idname'] = request.form['idname']  
            cursor.execute(SQL.SQLIMAGE,(user,))
            image = cursor.fetchone()
            return redirect(url_for('home'))       
        else :
             error = alert.LOGINACCOUNT
    return render_template("login.html",error=error)

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
        cursor.execute(SQL.SQLSELECTEMAIL,(email,))
        account = cursor.fetchone()
        if account:
            error = alert.REGISTERACCOUNT 
        else:
            mail.send(msg)
            return render_template('notification_register.html')
    return render_template("login.html", error = error)     

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
            error = alert.COMFIRMFAILPASSWORD
        else:
            passhash = hashlib.md5(password.encode()).hexdigest() 
            cur = mysql.connection.cursor()
            value =(email, passhash)
            cur.execute(SQL.SQLREGISTER,(value))
            mysql.connection.commit()
            session['idname'] = email
            return render_template('/home.html', email = email,img=image[0],point=image[1])
    return render_template("update_password.html", email =email,error = error)

# forgot password 
@app.route('/forgotpassword', methods=['GET','POST'])
def forgotpassword():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        token = s.dumps(email, salt='email-confirm')
        msg = Message('Confirm email',sender="ctsinternshipqnu@gmail.com", recipients=[email])
        link = url_for('forgot_email', token = token, _external = True)
        msg.html= render_template('form_forgot_pass.html',link = link)
        cursor = mysql.connection.cursor() 
        cursor.execute(SQL.SQLSELECTEMAIL,(email,))
        account = cursor.fetchone()
        if not(account):
            error = alert.FORGOTFAILEMAIL
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
            error = alert.COMFIRMFAILPASSWORD
        else:
            passhash = hashlib.md5(password.encode()).hexdigest() 
            cur = mysql.connection.cursor()
            value = (email, passhash)
            cur.execute(SQL.SQLUPDATEPSW,value)
            mysql.connection.commit()
            session['idname'] = email
            return render_template('/home.html', email = email,img=image[0],point=image[1])
    return render_template("update_password.html",email =email,error = error)




#Form forgot password when verify link Gmail
# @app.route('/verifyforgot')
# def verifyforgot():
#     return render_template('verifyforgot.html')


# Admin Management Mission
@app.route('/mission',methods=['GET','POST'])
def mission():
    cursor = mysql.connection.cursor()
    cursor.execute(SQL.SQLMISSION)
    task = cursor.fetchall()
    min = datetime.now()
    max = min + timedelta(1)
    return render_template('missionsystemadmin.html',task=task,min=min,max=max)

# Show users take mission
@app.route('/viewmission', methods=['GET','POST'])
def viewmission():
    if request.method == 'POST':
        id = request.form['id']
        cursor = mysql.connection.cursor()
        cursor.execute(SQL.SQLVIEWMISS,id)
        view = cursor.fetchall()
        Title = alert.NOTTAKEMISSION
        for a in view:
            Title = a[5]
        return render_template("userstakemission.html",view=view,Title=Title)


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
        if start >= end:
            flash("{}".format(alert.ERRORDATE))
            return redirect(url_for('mission'))
        else :
            val = (name,descr,startdate,enddate,limit,point)
            cursor.execute(SQL.SQLINSERTMISSION,val)
            mysql.connection.commit()
            flash("{}".format(alert.ADDMISSONSUCC))
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

        cursor.execute(SQL.SQLVIEWMISS,(id,))
        view = cursor.fetchall()
        if view :
            flash("{}".format(alert.USERTAKEMISSION))
            return redirect(url_for('mission'))
        elif start >= end:
            flash("{}".format(alert.ERRORDATE))
            return redirect(url_for('mission'))
        elif int(limit) >=1:
            val = (state1,name,descr,startdate,enddate,limit,point,id,)
            cursor.execute(SQL.SQLUPDATEMISS1,val)
            mysql.connection.commit()
            flash("{}".format(alert.EDITMISSIONSUCC))
            return redirect(url_for('mission'))
        elif int(limit)<=0 :   
            val = (state0,name,descr,startdate,enddate,limit,point,id,)
            cursor.execute(SQL.SQLUPDATEMISS0,val)      
            mysql.connection.commit()
            flash("{}".format(alert.EDITMISSIONSUCC))
            return redirect(url_for('mission'))

# Admin edit mission
@app.route('/deletemission/<id>/',methods=["GET","POST"])
def deletemission(id):
    cursor = mysql.connection.cursor()
    val = id
    cursor.execute(SQL.SQLVIEWMISS,(val,))
    view = cursor.fetchall()
    if view :
        flash("{}".format(alert.DELETEUSERMISSION))
        return redirect(url_for('mission'))
    else :
        cursor.execute(SQL.SQLDELETEMISS,(val,))
        mysql.connection.commit()
        flash("{}".format(alert.DELETEMISSIONSUCC))
        return redirect(url_for('mission'))

# Management ward admin
@app.route('/managementward')
def managementward():
    return render_template("managementward.html")


 # Fuction User
 # User's mission
@app.route('/usermission')
def usermission():
    if 'idname' in session: 
        email = session['idname']
        cursor = mysql.connection.cursor()
        cursor.execute(SQL.SQLMISSIONUSER,(email,))
        missionuser = cursor.fetchall()
        return render_template("usermission.html",missionuser=missionuser,img=image[0],point=image[1])
 # Mission avaiable
@app.route('/usermissionavaiable')
def usermissionavaiable():
    cursor = mysql.connection.cursor()
    cursor.execute(SQL.SQLMISSION1)
    mission = cursor.fetchall()
    return render_template("usermissionavaiable.html",mission=mission,img=image[0],point=image[1])
    
#Research MissionofUser
@app.route('/missionsearch/<id>',methods=['GET','POST'])
def missionsearch(id):
   
        cursor = mysql.connection.cursor()
        cursor.execute(SQL.SQLSHOWUSERMISSION,(id,))
        listEmployee = cursor.fetchall()
        cursor.execute(SQL.SQLSHOWNAMEOFUSER,(id,))
        NameEmployee = cursor.fetchall()
        constants_list  = constants
        return render_template('missionsearch.html',listEmployee=listEmployee,NameEmployee=NameEmployee,constants_list=constants_list)
# User profile
# @app.route('/userprofile')
# def userprofile():
#     return render_template("userprofile.html")
