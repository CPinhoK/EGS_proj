from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
import random

class cashtowallet(BaseModel):
    card_id: int
    cashtoadd: int
    
class payment_details(BaseModel):
    totaltopay: float
    metodo_de_pagamento: str
    source: str | None = None
    paymentid : str | None = None
    payment_dec : str | None = None

class wallet(BaseModel):
    card_id: int
    cash_assoc: float 
    niff: int | None = None
    wallet_desc: str | None = None

class user(BaseModel):
    client_id: int
    authtoken: str
    wallet_id: int | None
 



x=wallet(card_id=-1,cash_assoc=11111,wallet_desc="payment manger wallet",niff=1111)
y=wallet(card_id=22,cash_assoc=200,wallet_desc="random guy  wallet",niff=2222)
z=wallet(card_id=33,cash_assoc=10,wallet_desc="other guy  wallet",niff=3333)

walletdatabase={x.card_id:x,y.card_id:y,z.card_id:z}

user0=user(client_id=0,authtoken="x",wallet_id=-1)
user1=user(client_id=1,authtoken="y",wallet_id=22)
user2=user(client_id=2,authtoken="z",wallet_id=33)
user3=user(client_id=3,authtoken="bbb")

userdatabase = {user0.authtoken:user0,  user1.authtoken:user1,  user2.authtoken:user2,  user3.authtoken:user3 }#authtoken:user


current_token=None
currentdata=[current_token]


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Payz"}

@app.get("/status")
async def get_status():
    return 0

@app.post("/payment")
async def pay(payment_details: payment_details):
    
    #is user autheticated?
    #if not redirect
    #does the user have a wallet?
    #if not redirect
    current_token=currentdata[0]
    if current_token==None:
        raise HTTPException(status_code=403, detail="User not autheticated")
    current_user=userdatabase.get(current_token)
    if current_user.wallet_id == None:
        raise HTTPException(status_code=403, detail="User does not have a wallet associated")
    currentwallet=walletdatabase.get(current_user.wallet_id)
    masterwallet=walletdatabase.get(-1)
    totaltopay=payment_details.totaltopay + 0.05 #0.05 money taken for the service
    if currentwallet.cash_assoc<totaltopay:
        raise HTTPException(status_code=403, detail="Wallet does not have enough cash")
    currentwallet.cash_assoc-=totaltopay
    masterwallet.cash_assoc+=0.05
    walletdatabase.update({currentwallet.card_id:currentwallet})
    walletdatabase.update({masterwallet.card_id:masterwallet})
    
    return {"message": ("Payment sucessfull",totaltopay)}


@app.get("/wallet")
async def get_wallets():
    return {"walletdatabase ": walletdatabase}

@app.get("/wallet/{card_id}")
async def get_wallet(card_id: int):
    return {"wallet ": walletdatabase.get(card_id)}

@app.post("/wallet/create")
async def create_wallet(wallet: wallet):
    if wallet.card_id not in walletdatabase.keys():
        walletdatabase.update({wallet.card_id:wallet})
        return {"wallet ": wallet}
    else:
        raise HTTPException(status_code=403, detail="Wallet already exists")
    
    
@app.delete("/wallet/delete")
async def delete_wallet(walletid: int):
    if walletid in walletdatabase.keys():
        walletdatabase.pop(walletid)
        associatedcards=list(userdatabase.values())
        associatedcards=getwalletids(associatedcards)
        if walletid in associatedcards:
            userofwallet=getuserwithcard(walletid,list(userdatabase.values()))
            currentuser=userdatabase.get(userofwallet)
            currentuser.wallet_id = None
            userdatabase.update({userofwallet:currentuser})
        
        return {"Wallet deleted"}
    else:
        raise HTTPException(status_code=404, detail="Wallet does not exist")

@app.put("/wallet/update")
async def update_wallet(wallet: wallet):
    if wallet.card_id in walletdatabase.keys():
        walletdatabase.update({wallet.card_id:wallet})
        return {"wallet ": wallet}
    else:
        raise HTTPException(status_code=404, detail="Wallet does not exist")
    

@app.post("/wallet/add_cash/")
async def add_cash_to_wallet(cashtowallet: cashtowallet):
    if cashtowallet.card_id in walletdatabase.keys():
        this_wallet = walletdatabase.get(cashtowallet.card_id)
        this_wallet.cash_assoc+=abs(cashtowallet.cashtoadd)
        walletdatabase.update({cashtowallet.card_id:this_wallet})
        return {"Cash added "}
    else:
        raise HTTPException(status_code=404, detail="Wallet does not exist")
    
@app.put("/wallet/associate/{card_id}")
async def associate_wallet(card_id: int):
    currentusertoken=current_token
    #currentusertoken=something     grab current user token
    if card_id in walletdatabase.keys():
        associatedcards=list(userdatabase.values())
        associatedcards=getwalletids(associatedcards)
        #print(associatedcards)
        if card_id not in associatedcards:
            thisuser=userdatabase.get(currentusertoken)
            thisuser.wallet_id=card_id
            userdatabase.update({currentusertoken:thisuser})
            return {"Card associated"}
        else: 
            raise HTTPException(status_code=403, detail="Wallet already associated")
    else:
        raise HTTPException(status_code=404, detail="Wallet does not exist")

@app.get("/authentication")
async def auth(token: str):
    currentdata.clear()
    currentdata.extend(token)
    return {"token ": currentdata[0]}

@app.get("/user")
async def get_users():
    return {"userdatabase ": userdatabase}



def getwalletids(userlist):
    walletid=[]
    for user in userlist:
        walletid.append(user.wallet_id)
    return walletid

def getuserwithcard(walletid,userlist):
    for user in userlist:
        if user.wallet_id==walletid:
            return user.authtoken
        