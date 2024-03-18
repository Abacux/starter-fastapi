#API Functions
#--------------------------------------
#Imports
import pymongo
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
from bson import ObjectId
from typing import Optional

app = FastAPI()

#-------------usersDataBase------------#

#Conexion
client = pymongo.MongoClient('mongodb+srv://issaiase64:abacux64@cluster0.calbbx3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
basedD = client['Gym']
collection = basedD['usuarios']
#Esquema


class User(BaseModel):
   id: Optional[str] = "Opcional"
   user: str
   password: str
   name: str
   lastName: Optional[str] = "undefined"
   phoneNumber: Optional[str]
   shoppingHistory: dict
   

"""{
  "id": "opcional",
  "user": "userName",
  "password": "password",
  "name": "userName",
  "lastName": "opcional",
  "phoneNumber": "userName",
  "shoppingHistory": {}
}"""

def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
        "user": user["user"],
        "password": user["password"],
        "name": user["name"],
        "lastName": user["lastName"],
        "phoneNumber": user["telefono"],
        "shoppingHistory": user["shoppingHistory"]
        }


def users_schema(users) -> list:
    return [user_schema(user) for user in users]

#Funciones
#find
@app.get("/")
async def read_root():
   return {"API": "usersGym"}

@app.get("/users/", response_model=list[User])
async def getUsers():
      return users_schema(collection.find())

@app.get("/one-user/{itemId}", response_model=User)
async def getOneUser(itemId:str):
      return search_user("_id", ObjectId(itemId))

@app.post("/post-user/", response_model=User, status_code=status.HTTP_201_CREATED)
async def postUser(modelo:User):
    if type(search_user("user",modelo.user)) == User:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="La tarea ya existe")
    user_dict = dict(modelo)
    del user_dict["id"]
    id = collection.insert_one(user_dict).inserted_id
    new_user = user_schema(collection.find_one({"_id":id}))
    return User(**new_user)

@app.put("/put-user/{itemId}", response_model=User)
async def putUser(itemId:str, modelo:User):
    dict_modelo = dict(modelo)
    del dict_modelo["id"]
    try:
        collection.find_one_and_replace({"_id":ObjectId(modelo.id)},dict_modelo)
    except:
        return {"Error":"No se ha actualizado la tarea"}
    return search_user("_id", ObjectId(modelo.id))

@app.delete("/delete-user/{itemId}", status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def deleteUser(itemId:str):
  
  found = collection.delete_one({"_id":ObjectId(itemId)})

  if not found:
      return {"Error":"No se ha encontrado el usuario"}

@app.delete("/delete-all/", status_code=status.HTTP_205_RESET_CONTENT)
async def deleteAllUser():
  
  found = collection.delete_many({})

  if not found:
      return {"Error":"No se han encontrado usuarios"}


def search_user(field: str, key):
    try:
        user = collection.find_one({field:key})
        return User(user_schema(user))
    except:
        return {"Error":"No se ha encontrado el usuario"}

