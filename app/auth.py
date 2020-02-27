import os
import time
from collections import defaultdict

import numpy as np
import pandas as pd
import streamlit as st
import stravalib

import stravalib
from strava_overview.models import *
from strava_overview.auth import Tokens, InvalidToken, go_strava_auth


def auth(state, locations):
    ath = None
    if ath == None:
        auth = locations[0].button("Authenticate Strava")
        token = locations[1].text_input("Wat is uw strava code?", value="")
        locations[2].subheader("Of login:")
        email = locations[3].text_input("Email")
        ww = locations[4].text_input("Wachtword", type="password")
        if auth:
            client = stravalib.client.Client()
            go_strava_auth(client)

        if token != "":
            print("code:", token)
            try:
                id = Tokens.done(token)
                state.ath = Athlete.get_athlete(id)
                st.balloons()
                return state
            except InvalidToken:
                st.warning("De code in niet geldig.")

        if email and ww:
            state.trys += 1
            try:
                state.ath = Athlete.login(email, ww, state.trys)
                st.balloons()
                state.trys = -1
                return state
            except IncorrectPassword:
                st.warning("Het wachtwoord is incorrect.")

                if state.trys > 3:
                    sleep_time = state.trys * 10
                    st.warning(f"Te veel pogingen, wacht {sleep_time} seconden")
                    time.sleep(sleep_time)
                ww = "Wachtwoord"
            except LockedAccount:
                st.warning(
                    "Je account is geblokkeerd omdat er te veel fout wachtwoord poginingen zijn geweest."
                    + " Stuur een email naar motionnetai@gmail.com."
                )


if __name__ == "__main__":
    state = SessionState.get(trys=0)
    locations = [st.empty() for _ in range(10)]
    auth(state, locations)
