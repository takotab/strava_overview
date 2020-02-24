import uvicorn
from fastapi import FastAPI

from strava_overview.backend import save_code_to_token

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authorized")
@app.post("/authorized")
def auth(code: str, scope: str):
    state = {"code": code, "scope": scope}
    token = save_code_to_token(state)
    return {"please return to the web page\nAnd fill in the code": token}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)
