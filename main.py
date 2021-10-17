# Nama  : Handy Zulkarnain
# NIM   : 18219060

############ IMPORTS AND INITIAL CONFIGURE ############
from fastapi import FastAPI
import json

from fastapi.exceptions import HTTPException

import time
from typing import Dict
import jwt
from decouple import config

with open("menu.json", "r") as read_file:
    data = json.load(read_file)
with open("users.json", "r") as read_users_file:
    data_users = json.load(read_users_file)

app = FastAPI()


############ AUTHENTICATIONS ############
JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def res_access_token(token: str):
    return {
        "access_token": token
    }

def createJWT(user_id: str) -> Dict[str, str]:
    body = {
        "user_id": user_id,
        "expiry_time": time.time() + 1200
    }
    token = jwt.encode(body, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return res_access_token(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if (decoded_token["expiry_time"] >= time.time()):
            return decoded_token
        else:
            None
    except:
        return {}


############ HANDLE USERS ############
def check_user(username: str):
    for user in data_users['users']:
        if username == user['username']:
            return True
    return False

def check_password(password: str):
    for user in data_users['users']:
        if password == user['password']:
            return True
    return False

@app.post("/user/login")
def login_user(username: str, password: str):
    for user in data_users['users']:
        if (check_user(username)) and (check_password(password)):
            return createJWT(user['username'])
    raise HTTPException (
        status_code=500, detail="Wrong credentials!"
    )

@app.post("/user/register")
def create_user(username: str, password: str):
    if check_user(username):
        raise HTTPException(
            status_code=500, detail="Username has taken! Please proceed to login!"
        )
    else: 
        new_data = {"username":username, "password":password}
        data_users['users'].append(dict(new_data))
        read_users_file.close()
        with open("users.json", "w") as write_file:
            json.dump(data_users, write_file, indent=4)
        write_file.close()
        return createJWT(new_data['username'])


############ CRUD OPERATIONS ############
@app.get("/")
def root():
    return "Anda sedang berada di halaman awal. Silahkan tambahkan /docs pada akhir url."

@app.get("/menu")
def read_all_menu():
    return data['menu']

@app.get("/menu/{item_id}")
def read_menu(item_id: int):
    for item_menu in data['menu']:
        if (item_menu['id'] == item_id):
            return item_menu
    raise HTTPException(
        status_code=404, detail="Item menu not found!"
    )

@app.post("/menu")
def create_menu(name: str):
    id = 1
    if (len(data['menu']) > 0):
        # biar efisien kita perlu langsung nambahin ke element terakhir aja
        idLastMember = data['menu'][len(data['menu'])-1]['id']
        id = idLastMember + 1
    new_data = {"id":id, "name":name}        
    data['menu'].append(dict(new_data))
    read_file.close()
    with open("menu.json", "w") as write_file:
        json.dump(data, write_file, indent=4)
    write_file.close()
    return new_data

@app.delete('/menu/{item_id}')
def delete_menu(item_id: int):
    index = 0
    for item_menu in data['menu']:
        index+=1
        if (item_menu['id'] == item_id):
            data['menu'].pop(index-1)
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data, write_file, indent=4)
            write_file.close()
            return {}
    raise HTTPException(
        status_code=404, detail="Item menu not found!"
    )

@app.put("/menu/{item_id}")
def update_menu(item_id: int, item_name):
    for item_menu in data['menu']:
        if (item_menu['id'] == item_id):
            item_menu['name'] = item_name
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data, write_file, indent=4)
            write_file.close()
            return f'Updated menu for id:{item_id}'
    raise HTTPException(
        status_code=404, detail="Item menu not found!"
    )