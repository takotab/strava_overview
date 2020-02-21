import os
import time
from collections import defaultdict

import numpy as np
import pandas as pd
import streamlit as st

from strava_overview.models import *

dagen_van_week = {
    0: "Maandag",
    1: "Dinsdag",
    2: "Woensdag",
    3: "Donderdag",
    4: "Vrijdag",
    5: "Zaterdag",
    6: "Zondag",
}
import SessionState


def main():
    st.header("Motion Review")
    st.subheader("Een overview van jou trainingsweek")
    ath = None
    state = SessionState.get(trys=0)
    if ath == None:
        auth = st.button("Authenticate strava")
        st.subheader("Of login:")
        email = st.text_input("Email")
        ww = st.text_input("Wachtword", type="password")

        if auth:
            ath = Athlete.authenticate()
            st.balloons()
            st.write("Authenticated")
            return ath
        if email and ww:
            state.trys += 1
            try:
                ath = Athlete.login(email, ww, state.trys)
                st.balloons()
                return ath
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
    main()
