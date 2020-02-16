import streamlit as st
import pandas as pd
import numpy as np
import os
from collections import defaultdict


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
    auth = st.button("Authenticate strava")
    st.subheader('Of login:')
    email = st.text_input('Email')
    ww = st.text_input('Wachtword',type='password')

    if auth:
        st.balloons()
    if email and ww:
        st.write('hello there')



if __name__ == "__main__":
    main()