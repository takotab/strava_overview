import os
import time
from collections import defaultdict

import numpy as np
import pandas as pd
import streamlit as st

import SessionState
from strava_overview.models import *
from strava_overview.ti import *


@st.cache
def make_df(acts):
    # return pd.DataFrame([act.row(make_ti) for act in acts[::-1]])
    return pd.DataFrame([act.row() for act in acts[::-1]])


def weekly(state, locs):
    locs[0].text(f"hello {state.ath.firstname} {state.ath.lastname}")
    days = 7
    h = Handel(str(state.ath.id))
    acts = h.get_activities(start_date=None, days=7)
    acts[0].get_max_heartrate()
    locs[1].text(f"Hieronder de activiteiten van de laatste {days} dagen:")
    df = make_df(acts)
    df = emoji_name(df)
    del df["Type"]
    locs[1].dataframe(df)
    s = df.Duur.sum()
    locs[3].text(f"Totale inspannings tijd: {s}")
    # if os.path.isfile("auth_token.json"):
    #     non_hr = st.checkbox("Inclusief activteiten zonder hartslag.")
    #     h.start()
    #     st.write(f"Welcome {h.athlete.firstname} {h.athlete.lastname}")

    #     st.write(f"Hieronder de activiteiten van de laatste {days} dagen:")
    #     acts = h.get_activities(days=days)
    #     df = {}
    #     for k, act in acts.items():
    #         if act.has_heartrate or non_hr:
    #             df[k] = {
    #                 # "dag": pd.Timestamp(act.start_date).weekday_name,
    #                 "Dag": dagen_van_week[pd.Timestamp(act.start_date).weekday()],
    #                 "duur": act.elapsed_time,
    #             }
    #             if act.has_heartrate:
    #                 df[k]["gemiddelde hartslag"] = act.average_heartrate
    #             else:
    #                 df[k]["gemiddelde hartslag"] = ""
    #             act_lst.append(act)
    #     df = pd.DataFrame(df).T
    #     st.write(df.iloc[::-1])

    # fs = []
    # if act_lst:
    #     my_bar = st.progress(0)
    #     p = lambda x: my_bar.progress(x)
    #     fs = h.parse_activitys(act_lst, streamlit_progress=p)

    # if fs:
    #     acts = {}
    #     dates = [pd.Timestamp(o.start_date).date() for o in act_lst]
    #     dates = {
    #         k.date(): 0.0 for k in list(pd.date_range(min(dates), pd.Timestamp.now()))
    #     }
    #     del my_bar
    #     max_hr = st.number_input("Wat is uw maximale hartslag:", 0, 300, 200)
    #     my_bar = st.progress(0)
    #     t_tri = 0
    #     for i, (f, act) in enumerate(zip(fs, act_lst)):
    #         my_bar.progress((i + 1) / len(fs))
    #         df = pd.read_csv(f)
    #         tri = training_impulse_hr(df.heartrate, max_hr)
    #         t_tri += tri
    #         acts[act.name] = {
    #             "Trainings impuls": tri,
    #             "date": pd.Timestamp(act.start_date).date(),
    #         }
    #         dates[pd.Timestamp(act.start_date).date()] += tri
    #     del my_bar
    #     df = pd.DataFrame(
    #         {k: {"Trainings impuls": np.round(v, 0)} for k, v in dates.items()}
    #     ).T
    #     st.write(df)
    #     st.bar_chart(df)
    #     st.markdown("---")
    #     st.subheader(f"Je totale trainings impuls voor de laatste 7 days was: ")
    #     st.header(f"{np.round(t_tri, 0)}")


if __name__ == "__main__":
    ath = Athlete.get_athlete("5058582")
    state = SessionState.get(trys=0, ath=ath)
    locations = [st.empty() for _ in range(4)]
    print(locations[0])
    weekly(state, locations)
