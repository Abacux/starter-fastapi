#API Functions
#--------------------------------------
#Imports
import pymongo
from typing import Union, List
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://127.0.0.1:5500",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#-------------usersDataBase------------#

#Conexion
client = pymongo.MongoClient('mongodb+srv://issaiase64:abacux64@cluster0.calbbx3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
basedD = client['Gym']
collection = basedD['usuarios']
#Esquema
class User(BaseModel):
   id: str
   userName: str
   password: str
   name: str
   lastName: str
   genere: str
   inscription: str
   membership: str
   remainingDays: str

"""{
  "_id": "id",
  "userName": "userName",
  "password": "password",
  "name": "name",
  "lastName": "lastName",
  "genere": "genere",
  "inscription": "inscription",
  "membership": "membership",
  "remainingDays": "remainingDays"
}"""

def userSchema(user):
   return {"_id": str(user["id"]),
            "userName": user["userName"],
            "password": user["password"],
            "name": user["name"],
            "lastName": user["lastName"],
            "genere": user["genere"],
            "inscription": user["inscription"],
            "membership": user["membership"],
            "remainingDays": user["remainingDays"]}

#Funciones
#find
@app.get("/")
async def read_root():
   return {"Hello": "World"}

@app.get("/users/")
async def getUsers():
      data ={}
      for u in collection.find({}):
          data[str(u["_id"])] = u
      return data



@app.post("/new-user/")
async def postData(modelo:User):
   dict_modelo = dict(modelo)
   idValue= dict_modelo["id"]
   dict_modelo.pop("id")
   dict_modelo["_id"]=idValue

   collection.insert_one(dict_modelo)
