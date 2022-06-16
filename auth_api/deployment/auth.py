import random
from flask import Flask, request, jsonify, Response, render_template, redirect, request
from flask_restful import Api
import json
# import threading
import time
import sqlite3
from flask_cors import CORS

# import mysql.connector
# from mysql.connector import Error

TEST = True

WAIT_TIME = 60
TOKEN_SIZE = 64

### Database

# def create_connection(host_name, user_name, user_password, db_name):
#     connection = False
#     try:
#         connection = mysql.connector.connect(
#             host = host_name,
#             user = user_name,
#             passwd = user_password,
#             auth_plugin = 'mysql_native_password',
#             database = db_name
#         )
#         print('Connection do MySQL DB Successfull')
#     except Error as e:
#         print(f"##### {e}")
#     return connection

# def execute(connection, query):
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#     except Error as e:
#         print(f"##### {e}")

# def retrieve(connection, query):
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         return cursor.fetchall()
#     except Error as e:
#         print(f"##### {e}")

# dbcon = create_connection('localhost', 'root', 'DBpassword99.', 'auth')

# execute(dbcon, '''CREATE TABLE IF NOT EXISTS USERS
#                 (username   text    NOT NULL,
#                 password    text    NOT NULL,
#                 website     text    NOT NULL,
#                 token       text,
#                 timestamp   text,
#                 PRIMARY KEY (username, website));''')

# execute(dbcon, '''INSERT INTO USERS(username, password, website)
#                  VALUES ('admin',  'admin', '')''')

# # with dbcon.cursor() as cursor:
# #      cursor.execute('''SELECT * FROM USERS''')
# #      result = cursor.fetchall()
# result = retrieve(dbcon, '''SELECT * FROM USERS''')
# if result != None:
#     for row in result:
#         print(row)

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
                 VALUES ('admin',  'admin', '')''')
dbcon.execute('''INSERT OR IGNORE INTO USERS(username, password, website)
                 VALUES ('admin',  'admin', 'test.url')''')

allData = cursor.execute('''SELECT * FROM USERS''')
allAccounts = cursor.fetchall()
for acc in allAccounts:
    print(acc)


global redir

redir=[]


### API

def runApi():
    app = Flask(__name__)
    CORS(app, resource={
                        r"/*":{
                            "origins":"*"
                        }
                       })
    api = Api(app)

    @app.get('/signup')
    def signupPage():
        print('################################################')
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
        if TEST: redirectUrl = 'test.url'
        return render_template('signup.html', result = redirectUrl)

    @app.post('/signup')
    def signup():
        try:
            token = generateRandom()
            username = ''
            password = ''
            timestamp = ''
            try:
                for key, value in request.form.items():
                    print("key: {0}, value: {1}".format(key, value))
                    if key == 'username': username = value
                    if key == 'password': password = value
                    if key == 'redirectUrl': redirectUrl = value
            except:
                response = redirect('/signup', 400)
                return response
            token = generateRandom()
            timestamp = str(time.asctime(time.localtime(time.time())))
            accData = cursor.execute('''SELECT * FROM USERS WHERE username = "%s" AND website = "%s"'''%(username, redirectUrl))
            accounts = cursor.fetchall()
            if len(accounts) > 0:
                response = redirect('/signup', 409)
                return response
                # return Response(status=409)
            dbcon.execute('''INSERT OR IGNORE INTO USERS(username, password, website, token, timestamp)
                                    VALUES ("%s", "%s", "%s", "%s", "%s")'''%(username, password, redirectUrl, token, timestamp))
            print('Username: ' + str(username))
            print('Pass: ' + str(password))
            print('redirectUrl: ' + str(redirectUrl))
            # print('Token: ' + str(token))
            allData = cursor.execute('''SELECT * FROM USERS''')
            allAccounts = cursor.fetchall()
            for acc in allAccounts:
                print(acc)
            # response = {'token' : token }
            # r = Response(json.dumps(response), status=201, mimetype='application/json')
            # return redirect(redirectUrl, 201, None)
            redirectUrl = 'https://'+redirectUrl+'/'
            response = redirect(redirectUrl, 201, None)
            response.headers = {'token' : token}
            return response
        except:
            response = redirect('/signup', 500)
            return response
            # return Response(status=500)

    @app.get('/login')
    def loginPage():
        redirectUrl = ''
        #print(request.headers)
        redirectUrl=request.headers.get('Referer')
        d = str(request.data.decode('utf-8'))
        try:
            data = json.loads(d)
            #print("\n\n",data,"\n\n")
            #redirectUrl = data['redirectUrl']
            #redirectUrl=request.headers.get('Referer')
        except:
            # return Response(status=500)
            pass
        if redirectUrl == None or redirectUrl == '':
            redirectUrl = str(request.environ['REMOTE_ADDR'])
        if TEST: redirectUrl = 'test.url'
        # redir.append(redirectUrl)
        # print("Redirect to:"+redir[0])
        return render_template('login.html', result = redirectUrl)

    @app.post('/login')
    def login():
        try:
            token = generateRandom()
            username = ''
            password = ''
            timestamp = ''
            try:
                for key, value in request.form.items():
                    print("key: {0}, value: {1}".format(key, value))
                    if key == 'username': username = value
                    if key == 'password': password = value
                    if key == 'redirectUrl': redirectUrl = value
            except:
                response = redirect('/login', 400)
                return response
                # return Response(status=400)
            token = generateRandom()
            timestamp = str(time.asctime(time.localtime(time.time())))
            accData = cursor.execute('''SELECT * FROM USERS WHERE username = "%s" AND password="%s" AND website = "%s"'''%(username, password, redirectUrl))
            accounts = cursor.fetchall()
            if len(accounts) < 1:
                response = redirect('/login', 401)
                return response
                # return Response(status=401)
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
            # return redirect(redirectUrl, 201, None)
            # redirectUrl=redir.pop(0)
            # print("Redirect to:"+redirectUrl)
            #response = redirect(redirectUrl, code=302)
            #headers = {'token' : token}
            headers = 'token_' + token + '_user_'+username
            #print(response.headers)
            redirectUrl = 'https://'+redirectUrl+'/'
            return test(redirectUrl,headers)
        except:
            response = redirect('/login', 500)
            return response
            # return Response(status=500)

    @app.route('/test')
    def test(redirectUrl,headers):
        print(redirectUrl+'params/'+headers)
        return redirect(redirectUrl+'params/'+headers)
        response.headers=headers
        return response
    
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
                if TEST: redirectUrl = 'test.url'
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
    
    # @app.get('/token')
    # def token():
    #     # try:
    #         data = ''
    #         username = ''
    #         redirectUrl = ''
    #         token = ''
    #         try:
    #             d = str(request.data.decode('utf-8'))
    #             data = json.loads(d)
    #             username = data['username']
    #             redirectUrl = data['redirectUrl']
    #         except:
    #             return Response(status=400)
    #         accData = cursor.execute('''SELECT * FROM USERS WHERE username = "%s" AND website = "%s"'''%(username, redirectUrl))
    #         accounts = cursor.fetchall()
    #         if len(accounts) < 1:
    #             # response = {'token' : '' }
    #             # r = Response(json.dumps(response), status=201, mimetype='application/json')
    #             # return r
    #             return Response(status=403)
    #         else:
    #             u, p, w, t, ts = accounts[0]
    #             token = t
    #         # print('Username: ' + str(username))
    #         # print('Token: ' + str(token))
    #         allData = cursor.execute('''SELECT * FROM USERS''')
    #         allAccounts = cursor.fetchall()
    #         for acc in allAccounts:
    #             print(acc)
    #         response = {'token' : token }
    #         r = Response(json.dumps(response), status=201, mimetype='application/json')
    #         return r
    #     # except:
    #     #     return Response(status=500)

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
                if TEST: redirectUrl = 'test.url'
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
                if TEST: redirectUrl = 'test.url'
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
            print('################################################')
            app.run(host='0.0.0.0', port=5001)

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
