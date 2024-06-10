from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#Entidad user
class User(BaseModel):
    id:int
    name:str
    surname:str
    url:str
    age:int

users_list=[ 
       User(id=1, name="Ceci",surname="Mendez", url="http:galicia.ar",age=30),
       User(id=2, name="Cheito",surname="Carvallo",url="xx",age=42),
       User(id=3, name="Marianito",surname="Rodriguez",url="XX",age=55)]


@app.get("/userjson")
async def usersJson():
    return [{"name":"Gabriel", "surname":"Guerra", "url":"http://www.lanacion.com","age":55},
            {"name":"Ceci", "surname":"xx", "url":"http://www.ceci.com","age":32},
            {"name":"Cheito", "surname":"c", "url":"http://www.cheo.com","age":42},
            {"name":"Marianin", "surname":"rr", "url":"http://www.mr.com","age":55}
            ]


@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)

#"""
@app.get("/user/")
async def user(id: int):
    return search_user(id)    
#"""

@app.get("/userquery/")
async def userquery(id: int):
    return search_user(id)
"""
async def userquery():
    return users_list
    """

@app.get("/users")
async def users():
    return users_list

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error:","No se encontró resultado"}