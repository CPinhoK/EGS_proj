import random
from flask import Flask, request, jsonify, Response, render_template, redirect, request
from flask_restful import Api
import json
import time
import sqlite3
from flask_cors import CORS

from pydantic import BaseModel
import databases
from pymysql import Timestamp
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import asyncio

TEST = True
TOKEN_SIZE = 64
TOKEN_TEST = 'DAiQRA9tuKJzVq3AsR69g8KvBokaU6XrRIMMXP45KUS3jJSMUKFYsByHMo6NOQ8X'


### Database

##DATABASE_URL = "sqlite:///./test.db"

DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@auth-db:3306/{os.getenv('MYSQL_DATABASE')}"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

accounts_t = sqlalchemy.Table(  ##account_details table
    "accounts_t",
    metadata,
    sqlalchemy.Column("username", String(128), primary_key=True),
    sqlalchemy.Column("password", String(128)),
    sqlalchemy.Column("website", String(128), primary_key=True),
    sqlalchemy.Column("token", String(128)),
    sqlalchemy.Column("timestamp", String(128)),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)


global redirectUrl

## Models

class Account(BaseModel):
    username : str
    password : str
    website : str
    token : str
    timestamp : str


### API

def runApi():
    app = Flask(__name__)
    CORS(app, resource={
                        r"/*":{
                            "origins":"*"
                        }
                       })
    api = Api(app)

    @app.get('/')
    async def return_all():
        await database.connect()
        allAccounts = accounts_t.select()
        accounts = await database.fetch_all(allAccounts)
        await database.disconnect()
        return str(accounts)

    @app.get('/signup')
    def signupPage():
        redirectUrl = ''
        try:
            d = str(request.data.decode('utf-8'))
            data = json.loads(d)
            redirectUrl = data['redirectUrl']
            #redirectUrl=request.headers.get('Referer')
        except:
            # return Response(status=500)
            pass
        if redirectUrl == None or redirectUrl == '':
            redirectUrl = str(request.environ['REMOTE_ADDR'])
        if TEST: redirectUrl = 'test.url'
        return render_template('signup.html', result = redirectUrl)

    @app.post('/signup')
    async def signup():
        try:
            u = p = redirectUrl = ''
            try:
                for key, value in request.form.items():
                    print("key: {0}, value: {1}".format(key, value))
                    if key == 'username': u = value
                    if key == 'password': p = value
                    if key == 'redirectUrl': redirectUrl = value
            except:
                response = redirect('/signup', 400)
                return response
            t = generateRandom()
            ts = str(time.asctime(time.localtime(time.time())))
            await database.connect()
            select_query = accounts_t.select().where(accounts_t.c.username == u, accounts_t.c.website == redirectUrl)
            select_response = await database.fetch_all(select_query)
            if len(select_response) > 0:
                await database.disconnect()
                response = redirect('/signup', 409)
                return response
                # return render_template('signup.html', result = redirectUrl)
            insert_query = accounts_t.insert().values(username=u, password=p, website=redirectUrl, token = t, timestamp = ts)
            await database.execute(insert_query)
            await database.disconnect()
            redirectUrl = 'https://'+redirectUrl
            response = redirect(redirectUrl, 201)
            response.headers['token'] = t
            response.headers['username'] = u
            return response
        except:
            response = redirect('/signup', 500)
            try:
                await database.disconnect()
            except:
                pass
            return response

    @app.get('/login')
    def loginPage():
        global redirectUrl
        redirectUrl = 'https://'+str(request.args.get('redirectUrl'))
        print(redirectUrl)
        try:
            d = str(request.data.decode('utf-8'))
            data = json.loads(d)
            redirectUrl = data['redirectUrl']
            #redirectUrl=request.headers.get('Referer')
        except:
            # return Response(status=500)
            pass
        if redirectUrl == None or redirectUrl == '':
            redirectUrl = str(request.environ['REMOTE_ADDR'])
        #if TEST: redirectUrl = 'test.url'
        return render_template('login.html', result = redirectUrl)

    @app.post('/login')
    async def login():
        try:
            u = p = ''
            try:
                for key, value in request.form.items():
                    print("key: {0}, value: {1}".format(key, value))
                    if key == 'username': u = value
                    if key == 'password': p = value
                    #if key == 'redirectUrl': redirectUrl = value
            except:
                response = redirect('/login', 400)
                return response
            await database.connect()
            select_query = accounts_t.select().where(accounts_t.c.username == u, accounts_t.c.password == p)
            select_response = await database.fetch_all(select_query)
            if len(select_response) < 1:
                await database.disconnect()
                response = redirect('/login', 401)
                return response
            t = generateRandom()
            ts = str(time.asctime(time.localtime(time.time())))
            update_query = accounts_t.update().where(accounts_t.c.username == u, accounts_t.c.password == p).values(token = t, timestamp = ts)
            await database.execute(update_query)
            #await database.disconnect()
            global redirectUrl
            print(redirectUrl)
            redirectUrl = redirectUrl+t+'_'+u
            print(redirectUrl)
            response = redirect(redirectUrl, 302)
            response.headers['token'] = t
            response.headers['username'] = u
            # headers = 'token_' + t + '_user_'+u
            return response
        except:
            response = redirect('/login', 303)
            try:
                await database.disconnect()
            except:
                pass
            return response
    
    @app.post('/logout')
    async def logout():
        try:
            u = w = ''    
            try:
                d = str(request.data.decode('utf-8'))
                data = json.loads(d)
                u = data['username']
                w = data['website']
                if w == None or w == '':
                    w = str(request.environ['REMOTE_ADDR'])
                if TEST: w = 'test.url'
            except:
                # return Response(status=400)
                pass
            ts = str(time.asctime(time.localtime(time.time())))
            await database.connect()
            try:
                update_query = accounts_t.update().where(accounts_t.c.username == u, accounts_t.c.website == w).values(token = '', timestamp = ts)
                await database.execute(update_query)
            except:
                await database.disconnect()
                w = 'https://'+w
                # return redirect(w, 403)
                return Response(status = 403)
            await database.disconnect()
            # return redirect(w, 201)
            return Response(status = 201)
        except:
            # response = redirect(w, 500)
            response = Response(status = 500)
            try:
                await database.disconnect()
            except:
                pass
            return response

    @app.get('/status')
    async def status():
        print("\n\n"+str( request.get_data() ))
        print("\n\n"+str(request.json))
        try:
            t = ''
            try:
                d = str(request.data.decode('utf-8'))
                data = json.loads(d)
                t = data['token']
                print(str(data))
                print(t)
            except:
                return Response(status = 400)
            await database.connect()
            select_query = accounts_t.select().where(accounts_t.c.token == t)
            select_response = await database.fetch_all(select_query)
            print(select_response)
            print(t)
            if len(select_response) < 1:
                response = {'token' : ''}
                await database.disconnect()
                return Response(json.dumps(response), 201)
            response = {'token' : t}
            await database.disconnect()
            return Response(json.dumps(response), 201)
        except:
            # response = redirect(w, 500)
            response = Response(status = 500)
            try:
                await database.disconnect()
            except:
                pass
            return response

    @app.get('/update')
    async def updatePage():
        redirectUrl = t = u = p = ''
        try:
            d = str(request.data.decode('utf-8'))
            data = json.loads(d)
            redirectUrl = data['redirectUrl']
            t = data['token']
            #redirectUrl=request.headers.get('Referer')
        except:
            # return Response(status=500)
            pass
        if redirectUrl == None or redirectUrl == '':
            redirectUrl = str(request.environ['REMOTE_ADDR'])
        if TEST: 
            redirectUrl = 'test.url'
            t = TOKEN_TEST
        await database.connect()
        # try:
        select_query = accounts_t.select().where(accounts_t.c.token == t)
        select_response = await database.fetch_all(select_query)
        if len(select_response) == 1:
            u = select_response[0][0]
            p = select_response[0][1]
        else:
            await database.disconnect()
            redirectUrl = 'https://'+redirectUrl
            return redirect(redirectUrl, 402)
        # except:
        #     await database.disconnect()
        #     redirectUrl = 'https://'+redirectUrl
        #     return redirect(redirectUrl, 403)
        await database.disconnect()
        return render_template('edit.html', url = redirectUrl, username = u, password = p)

    @app.post('/update')
    async def update():
        try:
            u = p = nu = np = redirectUrl = ''
            try:
                for key, value in request.form.items():
                    if key == 'username': u = value
                    if key == 'password': p = value
                    if key == 'redirectUrl': redirectUrl = value
                    if key == 'newUsername': nu = value
                    if key == 'newPassword': np = value
            except:
                return Response(status = 400)
            await database.connect()
            try:
                ts = str(time.asctime(time.localtime(time.time())))
                if not (np == None or np == ''):
                    update_query = accounts_t.update().where(accounts_t.c.username == u, accounts_t.c.password == p, accounts_t.c.website == redirectUrl).values(password = np, timestamp = ts)
                    await database.execute(update_query)
                if not (nu == None or nu == ''):
                    update_query = accounts_t.update().where(accounts_t.c.username == u, accounts_t.c.password == p, accounts_t.c.website == redirectUrl).values(username = nu, timestamp = ts)
                    await database.execute(update_query)
            except:
                await database.disconnect()
                return Response(status = 403)
            await database.disconnect()
            redirectUrl = 'https://'+redirectUrl
            response = redirect(redirectUrl, 201)
            # headers = 'token_' + t + '_user_'+u
            return response
        except:
            # response = redirect(w, 500)
            response = Response(status = 500)
            try:
                await database.disconnect()
            except:
                pass
            return response
    
    # @app.put('/update')
    # async def update():
    #     try:
    #         u = p = w = nu = np = ''
    #         try:
    #             d = str(request.data.decode('utf-8'))
    #             data = json.loads(d)
    #             w = data['website']
    #             u = data['username']
    #             p = data['password']
    #             nu = data['newUsername']
    #             np = data['newPassword']
    #         except:
    #             return Response(status = 400)
    #         await database.connect()
    #         try:
    #             ts = str(time.asctime(time.localtime(time.time())))
    #             update_query = accounts_t.update().where(accounts_t.c.username == u, accounts_t.c.password == p, accounts_t.c.website == w).values(username = nu, password = np, timestamp = ts)
    #             await database.execute(update_query)
    #         except:
    #             await database.disconnect()
    #             return Response(status = 403)
    #         await database.disconnect()
    #         response = {'token' : t}
    #         return Response(json.dumps(response), 201)
    #     except:
    #         # response = redirect(w, 500)
    #         response = Response(status = 500)
    #         try:
    #             await database.disconnect()
    #         except:
    #             pass
    #         return response

    @app.delete('/delete')
    async def delete():
        try:
            u = w = ''
            try:
                d = str(request.data.decode('utf-8'))
                data = json.loads(d)
                u = data['username']
                w = data['website']
            except:
                return Response(status = 400)
            ts = str(time.asctime(time.localtime(time.time())))
            await database.connect()
            try:
                delete_query = accounts_t.delete().where(accounts_t.c.username == u, accounts_t.c.website == w)
                await database.execute(delete_query)
            except:
                await database.disconnect()
                return Response(status = 403)
            await database.disconnect()
            return Response(status = 201)
        except:
            # response = redirect(w, 500)
            response = Response(status = 500)
            try:
                await database.disconnect()
            except:
                pass
            return response

    if __name__ == '__main__':
        context = ('server.crt', 'server.key')#certificate and key file
        #app.run(host='0.0.0.0', port=8006,ssl_context=context)
        app.run(host='0.0.0.0', port=8006)


def generateRandom():
    r = ''
    char = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(0,TOKEN_SIZE):
        index = random.randrange(0, len(char)-1)
        r += char[index]
    return r

runApi()