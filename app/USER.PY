"""An example flask application demonstrating server-sent events."""

from hashlib import sha1
from shutil import rmtree
from stat import S_ISREG, ST_CTIME, ST_MODE
import json
import io
import os,xlwt
import time
import hashlib
from app import app
from PIL import Image, ImageFile
from gevent.event import AsyncResult
from gevent.queue import Empty, Queue
from gevent.timeout import Timeout
import flask 
from flask import Flask, render_template, redirect, url_for, request, flash, session, sessions,Response
from flask.templating import render_template 
from flask_mysqldb import MySQL 
import MySQLdb.cursors
import alert
from app import CTS
import SQL
import configpass
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime,timedelta
from werkzeug.utils import secure_filename
DATA_DIR = 'app/static/css'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
BROADCAST_QUEUE = Queue()
app.config['MAX_CONTENT_LENGTH'] =  64 * 1280 * 1280
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password = configpass.passwordmysql,
    database="cts"
    )


def allowed_file(filename):
    	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Admin Block Account
@app.route("/blockuser/<string:id_user>", methods=["GET"])
def blockuser(id_user):
    try:
        cursor = mydb.cursor()
        cursor.execute(SQL.SQLUNLOCKACC, ("0",id_user,))
        mydb.commit()
        flash(alert.BLOCKEMPLOYEE)
        return redirect(url_for('usermanagement'))
    except:
        return redirect(url_for('errorpage'))

# Admin Unlock Account
@app.route("/unlockuser/<string:id_user>", methods=["GET"])
def unlockuser(id_user):
    try:
        cursor = mydb.cursor()
        cursor.execute(SQL.SQLUNLOCKACC, ("1",id_user,))
        mydb.commit()
        flash(alert.UNBLOCKEMPLOYEE)
        return redirect(url_for('usermanagement'))
    except:
        return redirect(url_for('errorpage'))

@app.route('/', methods=['POST'])
def upload_image():
    
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(DATA_DIR, filename))
		if request.method == 'POST':
			mycursor = mydb.cursor()
			mycursor.execute('UPDATE employee SET Image = %s WHERE Email = %s',(filename, CTS.session['idname'],))
			mydb.commit()
		flash(alert.UPDATEIMAGESUCC)
		return redirect(url_for('profile',filename = filename))
	else:
    		flash(alert.UPDATEIMAGEFAIL)
	return redirect(url_for('profile'))

@app.route('/display/<filename>')
def display_image(filename):
    try:
	#print('display_image filename: ' + filename)
	    redirect(url_for('static', filename='uploads/'+ filename), code=301)
    except:
        return redirect(url_for('errorpage')) 

@app.route('/profile')
def profile():
    try:
        filename = request.args.get('filename', None)
        mycursor = mydb.cursor(buffered=True)
        id = CTS.session['idname']
        mycursor.execute(SQL.SQLSHOWPROFILE,(id,))
        myresult = mycursor.fetchall()
        mycursor.execute(SQL.SQLIMAGE,(id,))
        image = mycursor.fetchone()
        return render_template("userprofile.html",data = myresult,img=image[0],point=CTS.image[1],filename = filename)
    except:
        return redirect(url_for('errorpage'))     

@app.route('/updateprofile',methods=['GET','POST'])
def updateprofile():
    try:
        if request.method=='POST':
            name = request.form['edithoten']
            mycursor = mydb.cursor()
            email = CTS.session['idname']
            val = (name,email)
            mycursor.execute(SQL.SQLUPDATEPROFILE,val)
            mydb.commit()
            flash(alert.UPDATESUCC)
            return redirect(url_for('profile'))
    except:
        return redirect(url_for('errorpage'))

    
# Export Excel
@app.route('/download/report/excel')
def download_report():
    try:
        cursor = mydb.cursor()
        cursor.execute(SQL.SQLEXPORTEXCEL)
        result = cursor.fetchall()
        #output in bytes
        output = io.BytesIO()
        #create WorkBook object
        workbook = xlwt.Workbook()
        #add a sheet
        sh = workbook.add_sheet('Employee Report')
        #add headers
        sh.write(0, 0, 'ID nhân viên')
        sh.write(0, 1, 'Email nhân viên')
        sh.write(0, 2, 'Họ tên nhân viên')
        sh.write(0, 3, 'Điểm')
        sh.write(0, 4, 'Trạng thái tài khoản')
        
        idx = 0
        for row in result:
            sh.write(idx+1, 0, str(row[0]))
            sh.write(idx+1, 1, row[1])
            sh.write(idx+1, 2, row[2])
            sh.write(idx+1, 3, row[3])
            if row[4] == 1:
                sh.write(idx+1, 4, "Hoạt động")
            else: 
                sh.write(idx+1, 4, "Đã bị khóa")
            idx += 1
        
        workbook.save(output)
        output.seek(0)
        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=employee_report.xls"})
    except:
        return redirect(url_for('errorpage'))
def loopschedule():
    mycursor = mydb.cursor()
    mycursor.execute(SQL.SQLLOOP)
    loopall = mycursor.fetchall()
    now = datetime.now()
    state = 1
    for mission in loopall:
        Idmission = mission[0]
        mycursor.execute(SQL.SQLCURRENTDATE,(Idmission,))
        mydb.commit()
        totaldate = mission[1]
        currentdate = mission[2]
        if currentdate % totaldate == 0 and currentdate!=0:
            startdate = now
            peroid = mission[1]
            enddate = startdate + timedelta(peroid)             
            valloop = (startdate,enddate,state,Idmission)
            mycursor.execute(SQL.SQLUPDATETLOOPMIS,valloop)
            mydb.commit()
            print("Mission", Idmission, " đã được reset thành công" )
loopschedule()
sched = BackgroundScheduler(daemon=True)
sched.add_job(loopschedule,'cron',day_of_week='mon-sun', hour=0, 
                    minute=0)
sched.start()



@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    try:
        error = ""
        if request.method == "POST":
            email = CTS.session['idname']
            old = request.form['oldpassword']
            oldmd5 =  hashlib.md5(old.encode()).hexdigest()
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            mycursor = mydb.cursor()
            mycursor.execute(SQL.SQLPASSWORD, (email,))
            user = mycursor.fetchone()
            if oldmd5 != user[0]:
                flash('{}'.format(alert.PASSWORDOLD))
            elif password != confirm_password:
                flash('{}'.format(alert.PASSWORD))
            else:
                passhash = hashlib.md5(password.encode()).hexdigest()
                mycursor.execute(SQL.SQLUPDATEPASSWORD, (passhash, email))
                mydb.commit()
                flash('{}'.format(alert.UPDATEPASSWORD))
                return redirect(url_for('profile'))
        return redirect(url_for('profile'))
    except:
        return redirect(url_for('errorpage'))