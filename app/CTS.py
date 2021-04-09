from typing import ContextManager
from flask.globals import g
from flask.templating import render_template
from flask import Flask, render_template, redirect, url_for, request, flash, session, sessions,jsonify
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
import configadmin
from datetime import date, datetime,timedelta


app.config.from_pyfile('MailConfig.cfg')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'cts'


mysql = MySQL(app) 
mail = Mail(app)
s = URLSafeTimedSerializer('thisisascrect!')

# Function LOGOUT
@app.route('/')
def home():
    global idplo
    if 'idname' in session:
        email = session['idname']
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT Employee_Id FROM employee WHERE Email = %s', (email,))
        table = cursor.fetchone()
        idplo = table[0]
    else:
        return render_template('login.html')
    return render_template('home.html', idname = email)
   

# Logout account
@app.route('/logout')
def logout():
    session.pop('idname', None)
    return render_template("login.html")
    
# Login    
@app.route('/logi',methods=['GET','POST'])
def login():
    error = ""
    if request.method == 'POST':
        cursor = mysql.connection.cursor() 
        user = request.form['idname']
        psw = request.form['password']
        passhash = hashlib.md5(psw.encode()).hexdigest()
        cursor.execute(SQL.SQLCHECKPASS,(user,passhash,))
        check = cursor.fetchone()
        cursor.execute(SQL.SQLCHECKBLOCK, (user, passhash))
        checkblock = cursor.fetchone()
        
        if configadmin.username==user and configadmin.password==psw:
            session['idname'] = request.form['idname']  
            return render_template('home.html')
        elif checkblock:
            error = "Tài khoản đã bị khóa"
        elif check:
            Employee_Id = check[0]
            session['idname'] = request.form['idname']  
            return render_template('home.html')          
        else :
            error = 'Tài khoản hoặc mật khẩu sai' 
    return render_template("login.html",loi=error)

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
            error = alert.COMFIRMFAILPASSWORD
        else:
            passhash = hashlib.md5(password.encode()).hexdigest() 
            cur = mysql.connection.cursor()
            value =(email,passhash)
            cur.execute(SQL.SQLREGISTER,(value))
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
            cur.execute(SQL.SQLUPDATEPSW,(value))
            mysql.connection.commit()
            session['idname'] = email
            return render_template('/home.html', email = email)
    return render_template("update_password.html",email =email,error = error)


#Admin Block Account
@app.route("/blockuser/<string:id_user>", methods=["GET"])
def blockuser(id_user):
    # cursor = mysql.connection.cursor()
    # cursor.execute("UPDATE employee SET Status = '0' WHERE Employee_Id = (%s)",(id_user,))
    # mysql.connection.commit()
    return redirect(url_for('usermanagement'))

#Admin Unlock Account 
@app.route("/unlockuser/<string:id_user>", methods=["GET"])
def unlockuser(id_user):
    # cursor = mysql.connection.cursor()
    # cursor.execute("UPDATE employee SET Status = '1' WHERE Employee_Id = (%s)",(id_user,))
    # mysql.connection.commit()
    return redirect(url_for('usermanagement'))

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

        cursor.execute(SQL.SQLVIEWMISS,id)
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
    return render_template("usermission.html")
 # Mission avaiable
@app.route('/usermissionavaiable')
def usermissionavaiable():
    cursor = mysql.connection.cursor()
    cursor.execute(SQL.SQLVIEWMISSUSER)
    MissionAvaiable = cursor.fetchall()
    return render_template("usermissionavaiable.html",MissionAvaiable=MissionAvaiable)
#Take Mission
@app.route('/takemission/<id>/',methods=['GET','POST'])
def takemission(id):
    cursor = mysql.connection.cursor()
    Employee_mail = session['idname']
    cursor.execute(SQL.SQLGETEMP_ID,(Employee_mail,))
    Employee_Id =cursor.fetchone()
    cursor.execute(SQL.SQLVALIDATE,(Employee_Id[0],id))
    Validate = cursor.fetchone()
    if request.method == "GET":
        if Validate:
            flash(alert.TAKEMISSIONFAIL)
            return redirect(url_for('usermissionavaiable'))
        else:
            cursor.execute(SQL.SQLTAKEMISSION,(Employee_Id[0],id,1,))
            cursor.execute(SQL.SQLUPDATEMISSION,(id,))
            mysql.connection.commit()
            flash(alert.TAKEMISSION)
            return redirect(url_for('usermissionavaiable'))
    
