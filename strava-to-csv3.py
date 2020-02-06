#!/usr/bin/python
# -*- coding: utf-8 -*-
import stravalib
import http.server
import urllib.parse
import webbrowser
import pandas as pd
import datetime

# Global Variables - put your data in the file 'client.secret' and separate the fields with a comma!
client_id, secret = open("client.secret").read().strip().split(",")
port = 5000
url = "http://localhost:%d/authorized" % port
allDone = False
types = [
    "time",
    "distance",
    "latlng",
    "altitude",
    "velocity_smooth",
    "moving",
    "grade_smooth",
    "temp",
    "watts",
    "cadence",
    "heartrate",
]
limit = 3

# Create the strava client, and open the web browser for authentication
client = stravalib.client.Client()
authorize_url = client.authorization_url(client_id=client_id, redirect_uri=url)
print("Opening: %s" % authorize_url)
webbrowser.open(authorize_url)

# Define the web functions to call from the strava API
def UseCode(code):
    # Retrieve the login code from the Strava server
    print(client_id.__repr__(), secret.__repr__(), code.__repr__())
    access_token = client.exchange_code_for_token(
        client_id=client_id, client_secret=secret, code=code
    )
    # Now store that access token somewhere (for now, it's just a local variable)
    print(access_token)
    client.access_token = access_token["access_token"]
    athlete = client.get_athlete()
    print(
        (
            "For %(id)s, I now have an access token %(token)s"
            % {"id": athlete.id, "token": access_token}
        )
    )
    return client


def GetActivities(client, limit):
    # Returns a list of Strava activity objects, up to the number specified by limit
    activities = client.get_activities(limit=limit)
    assert len(list(activities)) == limit
    for item in activities:
        print(item)
    return activities


def GetStreams(client, activity, types):
    # Returns a Strava 'stream', which is timeseries data from an activity
    streams = client.get_activity_streams(activity, types=types, series_type="time")
    return streams


def DataFrame(dict, types):
    # Converts a Stream into a dataframe, and returns the dataframe
    print(dict, types)
    df = pd.DataFrame()
    for item in types:
        if item in list(dict.keys()):
            df.append(item.data)
    df.fillna("", inplace=True)
    return df


def ParseActivity(act, types):
    act_id = act.id
    name = act.name
    print(str(act_id), str(act.name), act.start_date)
    streams = GetStreams(client, act_id, types)
    df = pd.DataFrame()

    # Write each row to a dataframe
    for item in types:
        if item in list(streams.keys()):
            df[item] = pd.Series(streams[item].data, index=None)
        df["act_id"] = act.id
        df["act_startDate"] = pd.to_datetime(act.start_date)
        df["act_name"] = name
    return df


def calctime(time_sec, startdate):
    try:
        timestamp = startdate + datetime.timedelta(seconds=int(time_sec))
    except:
        print("time processing error : " + str(time_sec))
        timestamp = startdate
    return timestamp


def split_lat(series):
    lat = series[0]
    return lat


def split_long(series):
    long = series[1]
    return int


def concatdf(df_lst):
    return pd.concat(df_lst, ignore_index=False)


class MyHandler(http.server.BaseHTTPRequestHandler):
    # Handle the web data sent from the strava API

    def do_HEAD(self):
        return self.do_GET()

    def do_GET(self):
        # Get the API code for Strava
        # self.wfile.write("<script>window.close();</script>")
        state = {o.split("=")[0]: o.split("=")[1] for o in self.path.split("&")}
        code = state["code"]
        print(code)
        # Login to the API
        client = UseCode(code)

        # Retrieve the last limit activities
        activities = GetActivities(client, limit)

        # Loop through the activities, and create a dict of the dataframe stream data of each activity
        print("looping through activities...")
        df_lst = {}
        for act in activities:
            print(act.name)
            df_lst[act.start_date] = ParseActivity(act, types)

        # create the concatenated df and fill null values
        df_total = concatdf(df_lst)
        df_total.fillna("", inplace=True)

        # Calculate the timestamp column
        df_total = df_total.reset_index(level=0)
        df_total["timestamp"] = pd.to_datetime(
            list(map(calctime, df_total["time"], df_total["level_0"]))
        ).to_pydatetime()

        # Split out lat and long columns
        df_total.to_csv("activ.csv")
        df_total["lat"] = list(map(split_lat, (df_total["latlng"])))
        df_total["long"] = list(map(split_long, (df_total["latlng"])))

        # Index by startdate and timestamp, and drop arbitrary columns
        df_total = df_total.set_index(["act_startDate", "timestamp"])
        df_total.drop(["latlng", "level_0"], axis=1, inplace=True)

        # Write the file to a CSV - this will end up in your working directory
        now = datetime.datetime.now()
        df_total.to_csv("RideData_" + str(now.strftime("%Y%m%d%H%M%S")) + ".csv")
        print("script complete!")


if __name__ == "__main__":
    ###Run the program to login and grab data###
    try:
        httpd = http.server.HTTPServer(("localhost", port), MyHandler)
        httpd.handle_request()
    except KeyboardInterrupt:
        # Allow ^C to interrupt from any thread.
        sys.stdout.write("\033[0m")
        sys.stdout.write("User Interupt\n")
