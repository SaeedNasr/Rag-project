from fastapi import FastAPI

app = FastAPI()

@app.get("/welcome")
def welcome():
    return {"Massage":"Hello, welcome to Rag-APP!"}