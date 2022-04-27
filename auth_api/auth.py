import random
from flask import Flask, request, jsonify, Response, render_template, redirect, request
from flask_restful import Api
import json
import threading
import time
import sqlite3

WAIT_TIME = 60
TOKEN_SIZE = 64
TEST = True

### Database

dbcon = sqlite3.connect('auth.db', check_same_thread=False)

cursor = dbcon.cursor()

dbcon.execute  ('''CREATE TABLE IF NOT EXISTS USERS
                (username   text    NOT NULL,
                password    text    NOT NULL,
                website     text    NOT NULL,
                token       text,
                timestamp   text,
                PRIMARY KEY (username, website));''')
dbcon.commit()

dbcon.execute('''INSERT OR IGNORE INTO USERS(username, password, website)
                 VALUES ('admin',  'admin', 'test')''')

allData = cursor.execute('''SELECT * FROM USERS''')
allAccounts = cursor.fetchall()
for acc in allAccounts:
    print(acc)


### API

def runApi():
    app = Flask(__name__)
    api = Api(app)
    redirectUrl = ''

    @app.get('/signup')
    def signupPage():
        global redirectUrl
        redirectUrl = ''
        d = str(request.data.decode('utf-8'))
        try:
            data = json.loads(d)
            # print(data)
            redirectUrl = data['redirectUrl']
        except:
            # return Response(status=500)
            pass
        if redirectUrl == None or redirectUrl == '':
            redirectUrl = str(request.environ['REMOTE_ADDR'])
        return render_template('signup.html')

    @app.post('/signup')
    def signup():
        global redirectUrl
        try:
            token = generateRandom()
            username = ''
            password = ''
            timestamp = ''
            if (TEST): redirectUrl = ''
            try:
                for key, value in request.form.items():
                    # print("key: {0}, value: {1}".format(key, value))
                    if key == 'username': username = value
                    if key == 'password': password = value
            except:
                return Response(status=400)
            token = generateRandom()
            timestamp = str(time.asctime(time.localtime(time.time())))
            accData = cursor.execute('''SELECT * FROM USERS WHERE username = "%s" AND website = "%s"'''%(username, redirectUrl))
            accounts = cursor.fetchall()
            if len(accounts) > 0:
                return Response(status=409)
            dbcon.execute('''INSERT OR IGNORE INTO USERS(username, password, website, token, timestamp)
                                    VALUES ("%s", "%s", "%s", "%s", "%s")'''%(username, password, redirectUrl, token, timestamp))
            print('Username: ' + str(username))
            print('Pass: ' + str(password))
            # print('Token: ' + str(token))
            allData = cursor.execute('''SELECT * FROM USERS''')
            allAccounts = cursor.fetchall()
            for acc in allAccounts:
                print(acc)
            # response = {'token' : token }
            # r = Response(json.dumps(response), status=201, mimetype='application/json')
            return redirect(redirectUrl, 201, None)
        except:
            return Response(status=500)

    @app.get('/login')
    def loginPage():
        global redirectUrl
        redirectUrl = ''
        d = str(request.data.decode('utf-8'))
        try:
            data = json.loads(d)
            # print(data)
            redirectUrl = data['redirectUrl']
        except:
            # return Response(status=500)
            pass
        if redirectUrl == None or redirectUrl == '':
            redirectUrl = str(request.environ['REMOTE_ADDR'])
        return render_template('login.html')

    @app.post('/login')
    def login():
        global redirectUrl
        try:
            token = generateRandom()
            username = ''
            password = ''
            timestamp = ''
            if (TEST): redirectUrl = ''
            try:
                for key, value in request.form.items():
                    # print("key: {0}, value: {1}".format(key, value))
                    if key == 'username': username = value
                    if key == 'password': password = value
            except:
                return Response(status=400)
            token = generateRandom()
            timestamp = str(time.asctime(time.localtime(time.time())))
            accData = cursor.execute('''SELECT * FROM USERS WHERE username = "%s" AND password="%s" AND website = "%s"'''%(username, password, redirectUrl))
            accounts = cursor.fetchall()
            if len(accounts) < 1:
                return Response(status=401)
            dbcon.execute('''INSERT OR REPLACE INTO USERS(username, password, website, token, timestamp)
                                    VALUES ("%s", "%s", "%s", "%s", "%s")'''%(username, password, redirectUrl, token, timestamp))
            print('Username: ' + str(username))
            print('Pass: ' + str(password))
            # print('Token: ' + str(token))
            allData = cursor.execute('''SELECT * FROM USERS''')
            allAccounts = cursor.fetchall()
            for acc in allAccounts:
                print(acc)
            # response = {'token' : token }
            # r = Response(json.dumps(response), status=201, mimetype='application/json')
            return redirect(redirectUrl, 201, None)
        except:
            return Response(status=500)

    @app.post('/logout')
    def logout():
        try:
            data = ''
            token = ''
            username = ''
            password = ''
            redirectUrl = ''
            try:
                d = str(request.data.decode('utf-8'))
                data = json.loads(d)
                token = data['token']
                username = data['username']
                password = data['password']
                redirectUrl = data['redirectUrl']
                if (TEST): redirectUrl = ''
            except:
                return Response(status=400)
            timestamp = str(time.asctime(time.localtime(time.time())))
            accData = cursor.execute('''SELECT * FROM USERS WHERE username = "%s" AND password = "%s" AND website = "%s" AND token = "%s"'''%(username, password, redirectUrl, token))
            accounts = cursor.fetchall()
            if len(accounts) < 1:
                return Response(status=403)
            dbcon.execute('''INSERT OR REPLACE INTO USERS(username, password, website, token, timestamp)
                                    VALUES ("%s", "%s", "%s", "", "%s")'''%(username, password, redirectUrl, timestamp))
            # print('Username: ' + str(username))
            # print('Token: ' + str(token))
            allData = cursor.execute('''SELECT * FROM USERS''')
            allAccounts = cursor.fetchall()
            for acc in allAccounts:
                print(acc)
            # response = {'token' : token }
            # r = Response(json.dumps(response), status=201, mimetype='application/json')
            return redirect(redirectUrl, 201, None)
        except:
            return Response(status=500)

    @app.get('/status')
    def status():
        try:
            data = ''
            token = ''
            try:
                d = str(request.data.decode('utf-8'))
                data = json.loads(d)
                token = data['token']
            except:
                return Response(status=400)
            accData = cursor.execute('''SELECT * FROM USERS WHERE token = "%s"'''%(token))
            accounts = cursor.fetchall()
            if len(accounts) < 1:
                response = {'token' : '' }
                r = Response(json.dumps(response), status=201, mimetype='application/json')
                return r
            # print('Username: ' + str(username))
            # print('Token: ' + str(token))
            allData = cursor.execute('''SELECT * FROM USERS''')
            allAccounts = cursor.fetchall()
            for acc in allAccounts:
                print(acc)
            response = {'token' : token }
            r = Response(json.dumps(response), status=201, mimetype='application/json')
            return r
        except:
            return Response(status=500)
    
    @app.get('/token')
    def token():
        # try:
            data = ''
            username = ''
            redirectUrl = ''
            token = ''
            try:
                d = str(request.data.decode('utf-8'))
                data = json.loads(d)
                username = data['username']
                redirectUrl = data['redirectUrl']
            except:
                return Response(status=400)
            accData = cursor.execute('''SELECT * FROM USERS WHERE username = "%s" AND website = "%s"'''%(username, redirectUrl))
            accounts = cursor.fetchall()
            if len(accounts) < 1:
                # response = {'token' : '' }
                # r = Response(json.dumps(response), status=201, mimetype='application/json')
                # return r
                return Response(status=403)
            else:
                u, p, w, t, ts = accounts[0]
                token = t
            # print('Username: ' + str(username))
            # print('Token: ' + str(token))
            allData = cursor.execute('''SELECT * FROM USERS''')
            allAccounts = cursor.fetchall()
            for acc in allAccounts:
                print(acc)
            response = {'token' : token }
            r = Response(json.dumps(response), status=201, mimetype='application/json')
            return r
        # except:
        #     return Response(status=500)

    @app.put('/update')
    def update():
        try:
            data = ''
            token = ''
            username = ''
            password = ''
            redirectUrl = ''
            try:
                d = str(request.data.decode('utf-8'))
                data = json.loads(d)
                token = data['token']
                username = data['username']
                password = data['password']
                redirectUrl = data['redirectUrl']
                if (TEST): redirectUrl = ''
            except:
                return Response(status=400)
            accData = cursor.execute('''SELECT * FROM USERS WHERE token = "%s"'''%(token))
            accounts = cursor.fetchall()
            if len(accounts) < 1:
                return Response(status=403)
            timestamp = str(time.asctime(time.localtime(time.time())))
            dbcon.execute('''UPDATE USERS SET username = "%s", password = "%s", website = "%s", timestamp = "%s" WHERE token = "%s"'''%(username, password, redirectUrl, timestamp, token))
            # token = generateRandom()
            # dbcon.execute('''UPDATE USERS SET token = "%s" WHERE username = "%s" AND website = "%s"'''%(token, username, redirectUrl))
            allData = cursor.execute('''SELECT * FROM USERS''')
            allAccounts = cursor.fetchall()
            for acc in allAccounts:
                print(acc)
            # response = {'token' : token }
            # r = Response(json.dumps(response), status=201, mimetype='application/json')
            return redirect(redirectUrl, 201, None)
        except:
            return Response(status=500)

    @app.delete('/delete')
    def delete():
        try:
            data = ''
            token = ''
            username = ''
            password = ''
            redirectUrl = ''
            try:
                d = str(request.data.decode('utf-8'))
                data = json.loads(d)
                token = data['token']
                username = data['username']
                password = data['password']
                redirectUrl = data['redirectUrl']
                if (TEST): redirectUrl = ''
            except:
                return Response(status=400)
            timestamp = str(time.asctime(time.localtime(time.time())))
            accData = cursor.execute('''SELECT * FROM USERS WHERE username = "%s" AND password = "%s" AND website = "%s" AND token = "%s"'''%(username, password, redirectUrl, token))
            accounts = cursor.fetchall()
            if len(accounts) < 1:
                return Response(status=403)
            dbcon.execute('''DELETE FROM USERS WHERE username = "%s" AND password = "%s" AND website = "%s"'''%(username, password, redirectUrl, token))
            # print('Username: ' + str(username))
            # print('Token: ' + str(token))
            allData = cursor.execute('''SELECT * FROM USERS''')
            allAccounts = cursor.fetchall()
            for acc in allAccounts:
                print(acc)
            # response = {'token' : token }
            # r = Response(json.dumps(response), status=201, mimetype='application/json')
            return redirect(redirectUrl, 201, None)
        except:
            return Response(status=500)

    # def stop():
    #     time.sleep(WAIT_TIME)
    #     try:
    #         shutSignal = requests.get('http://0.0.0.0:5000/shutdown')
    #         print('Stoped listening')
    #     except Exception:
    #         print('Already shut')

    def run():
        if __name__ == '__main__':
            app.run(host='0.0.0.0', port=5000)

    # apiThread = threading.Thread(target=run)
    # stopThread = threading.Thread(target=stop)
    # apiThread.start()
    # stopThread.start()
    run()

def generateRandom():
    r = ''
    char = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(0,TOKEN_SIZE):
        index = random.randrange(0, len(char)-1)
        r += char[index]
    return r

runApi()