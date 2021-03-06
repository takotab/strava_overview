import streamlit as st
import pandas as pd
import numpy as np
import os
from collections import defaultdict
from strava_overview.models import *
from auth import auth
from SessionState import get
from weekly import weekly

# def sidebar():
#     st.sidebar.input_text()

dagen_van_week = {
    0: "Maandag",
    1: "Dinsdag",
    2: "Woensdag",
    3: "Donderdag",
    4: "Vrijdag",
    5: "Zaterdag",
    6: "Zondag",
}


def main():
    st.header("Motion Review")
    st.subheader("Een overview van jou trainingsweek")
    state = get(ath="", trys=0, logged_in=False)
    locations = [st.empty() for _ in range(10)]
    if not state.logged_in:
        auth(state, locations)
    if state.ath is not "":
        for i in range(10):
            locations[i].empty()
        locations[0].text(f"Welkom {state.ath.firstname} {state.ath.lastname} ")
        weekly(state, locations[1:])


if __name__ == "__main__":
    main()
