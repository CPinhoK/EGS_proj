from fastapi import FastAPI , HTTPException, Request ,WebSocket
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import databases
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import random
import string

import os
import time

### Database configuration
#print(f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@db:3306/{os.getenv('DB_NAME')}")
DATABASE_URL = f"mysql+pymysql://test:test@paymentapi-db:3306/test"
#DATABASE_URL = "mysql+pymysql://test:test@dcbsdhvbcsecbuib:3306/test"

#DATABASE_URL = f"mysql+pymysql://test:test@zppinho:3306/test"
#DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@127.0.0.1:3306/{os.getenv('DB_NAME')}"
#DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

payment_details_t = sqlalchemy.Table(  ##payment_details table
    "payment_details_t",
    metadata,
    sqlalchemy.Column("paymentid", String(32), primary_key=True),
    sqlalchemy.Column("incoming_paymentid", String(32), unique=False),
    sqlalchemy.Column("totaltopay", Float),
    sqlalchemy.Column("metodo_de_pagamento", String(32)),
    sqlalchemy.Column("source", String(32)),
    sqlalchemy.Column("payment_desc", String(32)),
    sqlalchemy.Column("timestamp_recv", String(32)),
    sqlalchemy.Column("timestamp_processed", String(32)),
    sqlalchemy.Column("wallet_that_payed", String(32)),
)

wallet_t = sqlalchemy.Table(  ##wallet table
    "wallet_t",
    metadata,
    sqlalchemy.Column("wallet_id", String(32), primary_key=True,unique=True),
    sqlalchemy.Column("cash_assoc", Float),
    sqlalchemy.Column("niff", Integer,unique=True),
    sqlalchemy.Column("wallet_desc", String(32)),
    sqlalchemy.Column("user_id", String(32)),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)



##MODELS

class Payment_details(BaseModel):
    incoming_paymentid : str
    paymentid : str 
    totaltopay: float
    metodo_de_pagamento: str
    source: str | None = None
    payment_desc : str | None = None
    timestamp_recv : str | None = None
    timestamp_processed : str
    wallet_that_payed : str

class Payment_details_in(BaseModel):
    incoming_paymentid : str
    ##paymentid : str   generated by me
    totaltopay: float
    metodo_de_pagamento: str
    source: str | None = None
    payment_desc : str | None = None
    timestamp_recv : str | None = None
    #timestamp_processed : str | None = None generated by me
    #wallet_that_payed : str    #chosen by user in a header

class Wallet(BaseModel):
    wallet_id: str
    cash_assoc: float 
    niff: int 
    wallet_desc: str | None = None
    user_id: str
 
class Wallet_in(BaseModel):
    niff: int 
    wallet_desc: str | None = None
    #user_id: str        #user id comes from the header
    #wallet_id: str      #randomly generated by me
    #cash_assoc: float   #Wallet starts with gifted 2$
    
class Wallet_update(BaseModel):
    niff: int | None = None
    wallet_desc: str | None = None
    cash_assoc: float   #cash to be added to the wallet in a update



master_wallet_id="2tLgVHNHZxnsHPVev"

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup() -> None:
    database_ = database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = database
    if database_.is_connected:
        await database_.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello Payz"}

@app.get("/status")
async def get_status():
    return 0

@app.post("/payment")
async def payment_request(payment_details: Payment_details_in,request: Request,wallet_id :str):
    
    uid = await are_credentials_correct(request) #after this the payment should proceed
    
    
    
    ##make sure this wallet belongs to the user
    query_sel = sqlalchemy.select(wallet_t.c).where(wallet_t.c.user_id == uid, wallet_t.c.wallet_id==wallet_id)
    #print(query_sel)
    wallet_info = await database.fetch_all(query_sel)
    #print(wallet_info)
    if wallet_info==[]:
        raise HTTPException(status_code=406, detail="Invalid wallet ID")
    
    ##get current wallet cash
    query_sel = sqlalchemy.select(wallet_t.c.cash_assoc).where(wallet_t.c.user_id == uid, wallet_t.c.wallet_id==wallet_id)
    #print(query_sel)
    wallet_cash = await database.fetch_all(query_sel)
    cuurent_wallet_cash = wallet_cash[0][0]
    
    if cuurent_wallet_cash<payment_details.totaltopay:
        raise HTTPException(status_code=406, detail="Wallet does not have enough cash")
    
    
    ## proceed with the payment
    
    timeprocessed=time.time()
    paymentid=id_generator()
    
    final_totaltopay=payment_details.totaltopay+0.2 # flat tax
    if cuurent_wallet_cash<final_totaltopay:
        raise HTTPException(status_code=406, detail="Wallet does not have enough cash after payment service tax")
    
    ##deduct cash and add to master
    query_update = wallet_t.update().values(cash_assoc=(wallet_t.c.cash_assoc - final_totaltopay )).where(wallet_t.c.wallet_id==wallet_id)
    last_record_id = await database.execute(query_update)
    
    query_update = wallet_t.update().values(cash_assoc=(wallet_t.c.cash_assoc + final_totaltopay )).where(wallet_t.c.wallet_id==master_wallet_id)
    last_record_id = await database.execute(query_update)
    
    ##create a payment history
    query_in = payment_details_t.insert().values(incoming_paymentid=payment_details.incoming_paymentid ,paymentid=paymentid ,totaltopay=final_totaltopay ,metodo_de_pagamento=payment_details.metodo_de_pagamento ,source=payment_details.source, payment_desc=payment_details.payment_desc , timestamp_recv=payment_details.timestamp_recv , timestamp_processed=timeprocessed , wallet_that_payed=wallet_id)
    last_record_id = await database.execute(query_in)
    
    ##Tell webservice  that payment was ok???
    return {"id": last_record_id, "message": "Payment sucessfull"}

@app.get("/payment")
async def display_all_payments(request: Request):
    
    uid = await are_credentials_correct(request) #after this the payment history can be displayed
    
    
    
    ##get all wallets_ids of the user
    query_sel = sqlalchemy.select(wallet_t.c).where(wallet_t.c.user_id == uid)
    #print(query_sel)
    wallets_info = await database.fetch_all(query_sel)
    if wallets_info==[]:
        raise HTTPException(status_code=400, detail="User does not have wallets")
    
    wallet_ids = [wallet_id[0] for wallet_id in wallets_info]
    print(wallet_ids)
    
    allpaymenets=[]
    
    for walletid in wallet_ids:
        ## user payemnts
        query_sel = sqlalchemy.select(payment_details_t.c).where(payment_details_t.c.wallet_that_payed == walletid)
        #print(query_sel)
        paymentinfo = await database.fetch_all(query_sel)
        if paymentinfo != []:
            allpaymenets.append(paymentinfo)
        
    if allpaymenets==[]:
        raise HTTPException(status_code=400, detail="User does not have payments")
    
    return {"Payments info": allpaymenets}
    


@app.get("/payment/{paympaymentid}")
async def display_payment(paympaymentid : str,request: Request):
    
    uid = await are_credentials_correct(request) #after this the payment spesific history can be displayed
    
    
    
    ##get all wallets_ids of the user
    query_sel = sqlalchemy.select(wallet_t.c).where(wallet_t.c.user_id == uid)
    #print(query_sel)
    wallets_info = await database.fetch_all(query_sel)
    if wallets_info==[]:
        raise HTTPException(status_code=400, detail="User does not have wallets")
    
    wallet_ids = [wallet_id[0] for wallet_id in wallets_info]
    print(wallet_ids)
    
    
    for walletid in wallet_ids:
        query_sel = sqlalchemy.select(payment_details_t.c).where(payment_details_t.c.wallet_that_payed == walletid,payment_details_t.c.paymentid==paympaymentid)
        #print(query_sel)
        paymentinfo = await database.fetch_all(query_sel)
        if paymentinfo!=[]:
            break
    if paymentinfo==[]:
         raise HTTPException(status_code=404, detail="Payments or Transfers not found")  
    return {"Payment info": paymentinfo}

    
@app.get("/authenticate")
async def authenticate(uid:str,token:str):
    #ask auth if credentials add up
    
    if(uid=="notvalid" or token=="notvalid"):
        return 1 
    return 0

@app.get("/wallet")
async def get_all_wallets(request: Request):
    
    uid = await are_credentials_correct(request) #after this wallets info can be displayed
    
    
    
    query_sel = sqlalchemy.select(wallet_t.c).where(wallet_t.c.user_id == uid)
    #print(query_sel)
    wallets_info = await database.fetch_all(query_sel)
    if wallets_info==[]:
        raise HTTPException(status_code=400, detail="User does not have wallets")
    
    return {"Wallets info": wallets_info}

@app.get("/wallet/{wallet_id}")
async def get_wallet(request: Request,wallet_id: str):

    uid = await are_credentials_correct(request) #after this wallet info can be displayed
    
    
    
    query_sel = sqlalchemy.select(wallet_t.c).where(wallet_t.c.user_id == uid, wallet_t.c.wallet_id==wallet_id)
    #print(query_sel)
    wallet_info = await database.fetch_all(query_sel)
    if wallet_info==[]:
        raise HTTPException(status_code=400, detail="Invalid wallet id")

    return {"Wallet info": wallet_info}

@app.post("/wallet")
async def create_wallet(request: Request,wallet: Wallet_in):
    print(wallet)
    uid=await are_credentials_correct(request) #wallet can now be created
    
    

    ##search database for a wallet with the same niff
    query_sel = sqlalchemy.select(wallet_t.c.niff)
    #print(query_sel)
    niffs = await database.fetch_all(query_sel)
    niffs = [niff[0] for niff in niffs]
    if wallet.niff in niffs:
        #print("A wallet with that niff already exists")
        raise HTTPException(status_code=406, detail="A wallet with that niff already exists")
    
    ##generate a wallet id/test if that id already exists
    query_sel = sqlalchemy.select(wallet_t.c.wallet_id)
    wallet_ids = await database.fetch_all(query_sel)
    wallet_ids = [wallet_id[0] for wallet_id in wallet_ids]
    new_walletid=id_generator()
    while(new_walletid in wallet_ids):
        new_walletid=id_generator()
    
    ##create the wallet
    query_in = wallet_t.insert().values(wallet_id=new_walletid, cash_assoc=2 ,niff=wallet.niff ,wallet_desc=wallet. wallet_desc,user_id=uid)
    last_record_id = await database.execute(query_in)
    return {"Message":"Wallet created"}#{**wallet.dict(), "id": last_record_id}


@app.put("/wallet/{wallet_id}")
async def update_wallet(wallet_id: str,wallet: Wallet_update,request: Request):
    
    uid=await are_credentials_correct(request) #wallet can now be updated
    
    
    
    ##make sure this wallet belongs to the user
    query_sel = sqlalchemy.select(wallet_t.c).where(wallet_t.c.user_id == uid, wallet_t.c.wallet_id==wallet_id)
    #print(query_sel)
    wallet_info = await database.fetch_all(query_sel)
    #print(wallet_info)
    if wallet_info==[]:
        raise HTTPException(status_code=406, detail="Invalid wallet ID")
    
    ##get current wallet cash
    query_sel = sqlalchemy.select(wallet_t.c.cash_assoc).where(wallet_t.c.user_id == uid, wallet_t.c.wallet_id==wallet_id)
    #print(query_sel)
    wallet_cash = await database.fetch_all(query_sel)
    cuurent_wallet_cash = wallet_cash[0][0]
    print(cuurent_wallet_cash)
    newcash=cuurent_wallet_cash+abs(wallet.cash_assoc)
    
    ##Make sure you want to change the niff
    if wallet.niff != None:
        
        ##search database for a wallets with the same niff
        query_sel = sqlalchemy.select(wallet_t.c.niff)
        #print(query_sel)
        niffs = await database.fetch_all(query_sel)
        niffs = [niff[0] for niff in niffs]
        if wallet.niff in niffs:
            #print("A wallet with that niff already exists")
            raise HTTPException(status_code=406, detail="A wallet with that niff already exists")
        
        query_update = wallet_t.update().values(niff=wallet.niff,wallet_desc=wallet.wallet_desc,cash_assoc=newcash).where(wallet_t.c.wallet_id==wallet_id)
    else:
        query_update = wallet_t.update().values(wallet_desc=wallet.wallet_desc,cash_assoc=newcash).where(wallet_t.c.wallet_id==wallet_id)
    
    ##Update wallet
    last_record_id = await database.execute(query_update)
    
    return {"detail":"Wallet with id "+wallet_id+" updated"}
    
@app.delete("/wallet/{wallet_id}")
async def delete_wallet(wallet_id: str,request: Request):
    
    uid=await are_credentials_correct(request) #wallet can now be destroyed
    
    
    
    ##make sure this wallet belongs to the user
    query_sel = sqlalchemy.select(wallet_t.c).where(wallet_t.c.user_id == uid, wallet_t.c.wallet_id==wallet_id)
    #print(query_sel)
    wallet_info = await database.fetch_all(query_sel)
    #print(wallet_info)
    if wallet_info==[]:
        raise HTTPException(status_code=406, detail="Invalid wallet ID")
    
    ##Delete wallet
    query_del = wallet_t.delete().where(wallet_t.c.wallet_id==wallet_id)
    last_record_id = await database.execute(query_del)

    return {"detail":"Wallet with id "+wallet_id+" deleted"}


@app.put("/transaction")
async def transfer_cash(request: Request,from_wallet_id :str,to_wallet_id :str,ammount: float):
    
    uid = await are_credentials_correct(request) #after this the payment should proceed
    
    
    
    ##make sure this wallet belongs to the user
    query_sel = sqlalchemy.select(wallet_t.c).where(wallet_t.c.user_id == uid, wallet_t.c.wallet_id==from_wallet_id)
    #print(query_sel)
    wallet_info = await database.fetch_all(query_sel)
    #print(wallet_info)
    if wallet_info==[]:
        raise HTTPException(status_code=406, detail="Invalid wallet ID")
    
    ##make sure the to_wallet exists
    query_sel = sqlalchemy.select(wallet_t.c).where(wallet_t.c.wallet_id==to_wallet_id)
    #print(query_sel)
    wallet_info = await database.fetch_all(query_sel)
    if wallet_info==[]:
        raise HTTPException(status_code=400, detail="Invalid wallet id")
    
    ##get current wallet cash
    query_sel = sqlalchemy.select(wallet_t.c.cash_assoc).where(wallet_t.c.user_id == uid, wallet_t.c.wallet_id==from_wallet_id)
    #print(query_sel)
    wallet_cash = await database.fetch_all(query_sel)
    cuurent_wallet_cash = wallet_cash[0][0]
    
    if cuurent_wallet_cash<ammount:
        raise HTTPException(status_code=406, detail="Wallet does not have enough cash")
    
    pd=Payment_details

    ## proceed with the transfer
    
    timeprocessed=time.time()
    paymentid=id_generator()
    
    pd.incoming_paymentid=paymentid
    pd.paymentid=paymentid
    pd.totaltopay=ammount
    pd.metodo_de_pagamento="Direct transfer"
    pd.source=from_wallet_id
    pd.payment_desc="Tranfer to wallet "+to_wallet_id
    pd.timestamp_recv=timeprocessed
    pd.timestamp_processed=timeprocessed
    pd.wallet_that_payed=from_wallet_id
    
    
    ##deduct cash and add to master
    query_update = wallet_t.update().values(cash_assoc=(wallet_t.c.cash_assoc - ammount )).where(wallet_t.c.wallet_id==from_wallet_id)
    last_record_id = await database.execute(query_update)
    
    query_update = wallet_t.update().values(cash_assoc=(wallet_t.c.cash_assoc + ammount )).where(wallet_t.c.wallet_id==to_wallet_id)
    last_record_id = await database.execute(query_update)
    
    ##create a payment history
    query_in = payment_details_t.insert().values(incoming_paymentid=pd.incoming_paymentid ,paymentid=pd.paymentid ,totaltopay=pd.totaltopay ,metodo_de_pagamento=pd.metodo_de_pagamento ,source=pd.source, payment_desc=pd.payment_desc , timestamp_recv=pd.timestamp_recv , timestamp_processed=pd.timestamp_processed , wallet_that_payed=pd.wallet_that_payed)
    last_record_id = await database.execute(query_in)
    return {"id": last_record_id, "message": "Transfer sucessfull"}


##oldauth for tests

@app.get("/oldauth")
async def oldauth(request: Request):
    #print(request.headers.items())
    uid,token=None,None
    if(good_auth_header(request)):
        uid,token=split_header(request)
        #print("UID:"+uid+"\nToken:"+token)
    else:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    return {"Accept header": (uid,token) }



""" @app.websocket("/ws_cw")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Accepted")
    while True:
        try:
            data = await websocket.receive_json()
            print(data)
            ret= await create_wallet(data)
            print(ret)
        except:
            pass
 """





async def are_credentials_correct(request: Request,hd='auth'):
    if(good_auth_header(request,hd)):
        uid,token=split_header(request,hd)
        print("UID:"+uid+"\nToken:"+token)
    else:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    value=await authenticate(uid,token)
    #print({"Accept header": (uid,token) ,"Value":value})
    if value!=0:
        raise HTTPException(status_code=401, detail="Unauthorized acesss")
    return uid


def good_auth_header(request: Request,hd='auth'):
    header = request.headers.get(hd)
    print("auth:",header)
    if header is None:  #empty
        return False
    header=' '.join(header.split()) #convert multiple spaces in 1
    header=header.split(" ")
    if(len(header) != 2): # more than uid and tok
        return False
    return True 

def split_header(request: Request,hd='auth'):
    header = request.headers.get(hd)
    header=' '.join(header.split())  #convert multiple spaces in 1
    header=header.split(" ")
    uid = header[0]
    token= header[1]
    return(uid,token)

def id_generator(size=17, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for a in range(size))
