"""An example flask application demonstrating server-sent events."""

from hashlib import sha1
import re
from shutil import rmtree
from stat import S_ISREG, ST_CTIME, ST_MODE
import json
import io
import os,xlwt
import time
from werkzeug.utils import secure_filename
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
import mysql.connector
DATA_DIR = 'app/static/css'
KEEP_ALIVE_DELAY = 25
MAX_IMAGE_SIZE = 800, 600
MAX_IMAGES = 100
MAX_DURATION = 100


BROADCAST_QUEUE = Queue()
UPLOAD_FOLDER = 'app/static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 120 * 1024 * 1024 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "123456",
    database="cts"
    )


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Admin management user
@app.route('/usermanagement')
def usermanagement():
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(SQL.SQLUSERMANA)
    data1 = mycursor.fetchall()
    return render_template("usermanagement.html",data1 = data1)

# Admin Block Account
@app.route("/blockuser/<string:id_user>", methods=["GET"])
def blockuser(id_user):
    cursor = mydb.cursor()
    cursor.execute(SQL.SQLUNLOCKACC, ("0",id_user,))
    mydb.commit()
    return redirect(url_for('usermanagement'))

# Admin Unlock Account
@app.route("/unlockuser/<string:id_user>", methods=["GET"])
def unlockuser(id_user):
    cursor = mydb.cursor()
    cursor.execute(SQL.SQLUNLOCKACC, ("1",id_user,))
    mydb.commit()
    return redirect(url_for('usermanagement'))


@app.route('/', methods=['POST'])
def upload_image():

	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename
		return redirect(url_for('profile', filename = filename))
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/profile')
def profile():
    filename = request.args.get("filename", None)
    mycursor = mydb.cursor(buffered=True)
    id = CTS.session['idname']
    mycursor.execute(SQL.SQLSHOWPROFILE,(id,))
    myresult = mycursor.fetchall()
    return render_template("userprofile.html",data = myresult,img=CTS.image[0],point=CTS.image[1], filename = filename)
 

@app.route('/updateprofile',methods=['GET','POST'])
def updateprofile():
    if request.method=='POST':
        filename = request.args.get("filename", None)
        name = request.form['edithoten']
        mycursor = mydb.cursor()
        email = CTS.session['idname']
        val = (name,filename,email,)
        mycursor.execute(SQL.SQLUPDATEPROFILE,val)
        mydb.commit()
        flash(alert.UPDATESUCC)
        return redirect(url_for('profile'))

    
# Export Excel
@app.route('/download/report/excel')
def download_report():
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


@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
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
        
    