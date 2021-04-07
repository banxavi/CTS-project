"""An example flask application demonstrating server-sent events."""

from hashlib import sha1
from shutil import rmtree
from stat import S_ISREG, ST_CTIME, ST_MODE
import json
 
import os
import time
from app import app
from PIL import Image, ImageFile
from gevent.event import AsyncResult
from gevent.queue import Empty, Queue
from gevent.timeout import Timeout
import flask 
from flask import Flask, render_template, redirect, url_for, request, flash, session, sessions
from flask.templating import render_template 
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector
DATA_DIR = 'dataimage'
KEEP_ALIVE_DELAY = 25
MAX_IMAGE_SIZE = 800, 600
MAX_IMAGES = 100
MAX_DURATION = 100


BROADCAST_QUEUE = Queue()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="cts"
    )


try:  # Reset saved files on each start
    rmtree(DATA_DIR, True)
    os.mkdir(DATA_DIR)
except OSError:
    pass


def broadcast(message):
    """Notify all waiting waiting gthreads of message."""
    waiting = []
    try:
        while True:
            waiting.append(BROADCAST_QUEUE.get(block=False))
    except Empty:
        pass
    print('Broadcasting {} messages'.format(len(waiting)))
    for item in waiting:
        item.set(message)


def receive():
    """Generator that yields a message at least every KEEP_ALIVE_DELAY seconds.

    yields messages sent by `broadcast`.

    """
    now = time.time()
    end = now + MAX_DURATION
    tmp = None
    # Heroku doesn't notify when clients disconnect so we have to impose a
    # maximum connection duration.
    while now < end:
        if not tmp:
            tmp = AsyncResult()
            BROADCAST_QUEUE.put(tmp)
        try:
            yield tmp.get(timeout=KEEP_ALIVE_DELAY)
            tmp = None
        except Timeout:
            yield ''
        now = time.time()


def safe_addr(ip_addr):
    """Strip off the trailing two octets of the IP address."""
    return '.'.join(ip_addr.split('.')[:2] + ['xxx', 'xxx'])


def save_normalized_image(path, data):
    """Generate an RGB thumbnail of the provided image."""
    image_parser = ImageFile.Parser()
    try:
        image_parser.feed(data)
        image = image_parser.close()
    except IOError:
        return False
    image.thumbnail(MAX_IMAGE_SIZE, Image.ANTIALIAS)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(path)
    return True


def event_stream(client):
    """Yield messages as they come in."""
    force_disconnect = False
    try:
        for message in receive():
            yield 'data: {}\n\n'.format(message)
        print('{} force closing stream'.format(client))
        force_disconnect = True
    finally:
        if not force_disconnect:
            print('{} disconnected from stream'.format(client))



@app.route('/usermanagement')
def usermanagement():
 

    mycursor = mydb.cursor(buffered=True)
    sql = "Select Employee_Id, Name, Email,Image,Status,Point from cts.employee "
    mycursor.execute(sql)
    data1 = mycursor.fetchall()

    sql1 = "select Image from employee"
    mycursor.execute(sql1)
    img = mycursor.fetchone()
    return render_template("usermanagement.html",data1 = data1,img=img[0])

@app.route('/post', methods=['POST'])
def post():
    """Handle image uploads."""
    sha1sum = sha1(flask.request.data).hexdigest()
    target = os.path.join(DATA_DIR, '{}.jpg'.format(sha1sum))
    convert = '{}.jpg'.format(sha1sum)
    message = json.dumps({'src': target,
                          'ip_addr': safe_addr(flask.request.access_route[0])})

    mycursor = mydb.cursor()

    sql = 'UPDATE employee SET Image = %s WHERE Employee_Id = %s'
    a=1
    val = (convert,a)
    mycursor.execute(sql,val)
    mydb.commit()

    try:
        if save_normalized_image(target, flask.request.data):
            broadcast(message)  # Notify subscribers of completion
    except Exception as exception:  # Output errors
        return '{}'.format(exception)
    return redirect(url_for('profile'))


@app.route('/stream')
def stream():
    """Handle long-lived SSE streams."""
    return flask.Response(event_stream(flask.request.access_route[0]),
                          mimetype='text/event-stream')


@app.route('/profile')
def profile():
    """Provide the primary view along with its javascript."""
    image_infos = []
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        file_stat = os.stat(filepath)
        if S_ISREG(file_stat[ST_MODE]):
            image_infos.append((file_stat[ST_CTIME], filepath))

    images = []
    for i, (_, path) in enumerate(sorted(image_infos, reverse=True)):
        if i >= MAX_IMAGES:
            os.unlink(path)
            continue
        images.append('<div><img alt="User uploaded image" src="{}" /></div>'
                      .format(path))

    mycursor = mydb.cursor(buffered=True)
    sql = 'select Image from employee'
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    return render_template("profile.html",img=myresult[0])
 

