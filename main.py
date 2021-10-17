# Nama  : Handy Zulkarnain
# NIM   : 18219060

from os import name
from fastapi import FastAPI
import json

from fastapi.exceptions import HTTPException

with open("menu.json", "r") as read_file:
    data = json.load(read_file)

app = FastAPI()

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