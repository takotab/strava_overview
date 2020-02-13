import json
import os

import stravalib
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class AuthToken:
    def __init__(self, path="auth_token.json"):
        self.path = path

    def set(self, dct: {}):
        json.dump(dct, open(self.path, "w"))

    def get(self, state=None):
        if state is None:
            return state
        return json.load(open(self.path, "r"))


def get_access_token(state: {} = None):
    auth = AuthToken()
    state = auth.get(state)
    client_id, secret = os.environ["client_id"], os.environ["secret"]
    client = stravalib.client.Client()
    if "refresh_token" in state:
        token = client.refresh_access_token(
            client_id=client_id,
            client_secret=secret,
            refresh_token=state["refresh_token"],
        )
    else:
        token = client.exchange_code_for_token(
            client_id=client_id, client_secret=secret, code=state["code"],
        )
    state["refresh_token"] = token["refresh_token"]
    state["access_token"] = token["acces_token"]
    auth.set(state)
    return state["access_token"]


@app.get("/authorized")
@app.post("/authorized")
def auth(code: str, scope: str):
    state = {"code": code, "scope": scope}
    get_access_token(state)
    return {"please return to the web page": ""}


if __name__ == "__main__":
    uvicorn.run("main:app", port=5555)
