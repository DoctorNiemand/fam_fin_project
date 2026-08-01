from fastapi import FastAPI
from models.user import User
from database import Session

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello Sergei!"}

@app.get("/users")
def root():
    return sers.to_dict()

sers = User(
    name = "Sergei",
    login = "sergei",
    password = "123456789",
    role = "Admin")

session = Session()
session.add(sers)
session.commit()
