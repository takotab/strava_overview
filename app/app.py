import streamlit as st
from strava_overview.to_csv import *
import pandas as pd


def main():
    st.title("Motion Review")
    st.write("Een overview van jou trainingsweek")
    client_id, secret = open("client.secret").read().strip().split(",")
    h = Handel(client_id, secret)
    h.start()
    st.write(f"Welcome {h.athlete.firstname} {h.athlete.lastname}")
    acts = h.get_activities()
    # fs = h.parse_activitys(acts)
    st.write(acts)


if __name__ == "__main__":
    main()
