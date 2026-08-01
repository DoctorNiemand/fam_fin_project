from fastapi import FastAPI
from models.user import User

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello Sergei!"}

@app.get("/users")
def root():
    return sers.to_dict()

sers = User(1,
    "Sergei",
    "sergei",
    "123456789",
    "Admin")
dad = User(2,
    "Dad",
    "dad",
    "987654321",
    "Member")

print(sers.__tablename__)