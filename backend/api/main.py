from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import users, workspaces, transactions, accounts


app = FastAPI(
    title="Family Finance API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(workspaces.router)
app.include_router(transactions.router)
app.include_router(accounts.router)


@app.get("/")
def root():
    return {"message": "Family Finance API"}