# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_models.ipynb (unless otherwise specified).

__all__ = ['Athlete', 'types', 'Activity', 'types', 'Handel', 'datetime_fix', 'get_activities', 'save_activities']

# Cell
import json

# Cell
import stravalib
import urllib.parse
import webbrowser
import os
import pandas as pd
import sys
from fastcore.utils import *
import time

# Cell
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, BooleanAttribute, MapAttribute, ListAttribute,
)

# Cell
from .s3 import *

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

class Athlete(Model):
    class Meta:
        table_name = "motionreview-athlete"
        region = 'eu-central-1'
    id = NumberAttribute(hash_key=True)
    firstname = UnicodeAttribute()
    lastname = UnicodeAttribute()
    profile = UnicodeAttribute()
    sex = UnicodeAttribute()
    max_heartrate = NumberAttribute(null=True)
    ftp = NumberAttribute(null=True)
    weight = NumberAttribute(null=True)
    zones = ListAttribute(null=True)
    password = UnicodeAttribute(null=True)
    email = UnicodeAttribute(null=True)
    access_token = UnicodeAttribute(null=True)
    refresh_token = UnicodeAttribute(null=True)

    @classmethod
    def from_stravalib(cls, athlete:stravalib.model.Athlete, **kwargs):
        dct = {k:athlete.__getattribute__(k) for k in 'firstname,lastname,profile,sex,max_heartrate,weight,ftp'.split(',') if (athlete.__getattribute__(k) is not None)}
        dct.update(kwargs)
        ath = cls(athlete.id,**dct)
        ath.save()
        return ath

    @classmethod
    def authenticate(cls, sleep_time = 60):
        client = stravalib.client.Client()
        go_strava_auth(client)
        tokens = Tokens()
        i = 0
        while i < sleep_time:
            i+=1
            time.sleep(1)
            id = tokens.is_new()
            if id:
                return get_athlete(id = id)
        raise FileNotFoundError

    @classmethod
    def from_id(cls, id =None, **kwargs):
        if id is None:
            return cls.authenticate(**kwargs)
        return get_athlete(id = id)

    @staticmethod
    def get_athlete(id = None, ath:stravalib.model.Athlete = None):
        if id is None:
            assert type(ath) == stravalib.model.Athlete
            id = ath.id

        aths =list(Athlete.query(int(id)))
        if len(aths) == 1:
            return aths[0]
        elif len(aths) == 0 and ath is not None:
            return Athlete.from_stravalib(ath)
        else:
            raise IndexError(f"to many athlets with id {ath.id}:{aths}")

# Cell
from .s3 import *

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

class Activity(Model):
    class Meta:
        table_name = "motionreview-activity"
        region = 'eu-central-1'

    id = UnicodeAttribute(hash_key=True)
    athlete_id = UnicodeAttribute()
    start_date_local = UTCDateTimeAttribute()
    name = UnicodeAttribute()
    act_type = UnicodeAttribute()
    device_watts = BooleanAttribute(default=False)
    has_heartrate = BooleanAttribute(default=False)
    on_s3 = BooleanAttribute(default=False)
    ti = NumberAttribute(null=True)
    ti_w = NumberAttribute(null=True)
    ti_hr = NumberAttribute(null=True)

    @classmethod
    def from_stravalib(cls, act):
        Athlete.get_athlete(ath = act.athlete)
        device = act.device_watts if act.device_watts else False
        act = cls(id = str(act.id), name = act.name, athlete_id = str(act.athlete.id), act_type = act.type,
                        device_watts=device, start_date_local = act.start_date_local, has_heartrate = act.has_heartrate,
                        )
        return act

    @classmethod
    def from_id(cls, id):
        return get_activity(id = id)

    @staticmethod
    def get_activity(id = None, act:stravalib.model.Activity = None):
        if id is None:
            assert type(act) == stravalib.model.Activity
            id = act.id

        acts =list(Activity.query(int(id)))
        if len(acts) == 1:
            return aths[0]
        elif len(acts) == 0:
            return Activity.from_stravalib(ath)
        else:
            raise IndexError(f"to many activitys with id {act.id}:{acts}")

    def save_stream(self, h):
        if not self.on_s3:
            streams = h.client.get_activity_streams(self.id, types=types, series_type="time")
            self.download_save(streams)

    def filename(self):
        if not os.path.isdir(self.athlete_id):
            os.mkdir(self.athlete_id)
        return self.athlete_id +'/'+ self.id + '.csv'

    def download_save(self, streams):
        df = pd.DataFrame()
        f = self.filename()
        # Write each row to a dataframe
        for item in types:
            if item in list(streams.keys()):
                df[item] = pd.Series(streams[item].data, index=None)
            df["act_id"] = self.id
            df["act_name"] = self.name
        df.to_csv(f, index=False)
        upload_file(f)
        self.on_s3 = True
        self.save()

    def get_df(self) -> pd.DataFrame:
        f = self.filename()
        download_file(f)
        return pd.read_csv(f)

# Cell
class Handel:
    def __init__(self, ath_id=None):
        self.client = stravalib.client.Client()
        self.athlete = Athlete.get_athlete(ath_id)
        self.set_access_token()
        self.strava_athlete = self.client.get_athlete()

    def set_access_token(self):
        self.client.access_token = self.athlete.access_token
        try:
            self.strava_athlete = self.client.get_athlete()
            return
        except:
            self.client.access_token = self.client.refresh_access_token(
                client_id=client_id,
                client_secret=secret,
                refresh_token=self.athlete.refresh_token,
            )
        self.strava_athlete = self.client.get_athlete()


# Cell
def datetime_fix(start_date, days):
    before = pd.Timestamp(start_date)
    before = pd.Timestamp(before.year,before.month,before.day,23,59)
    before.tz_localize('utc')
    after = before - pd.Timedelta(days=days)
    return before, after

# Cell
def get_activities(self, start_date = None, days = 7):
    start_date = ifnone(start_date, pd.Timestamp.now())
    before, after = datetime_fix(start_date, days)
    # Returns a list of Strava activity objects, up to the number specified by limit
    activities = self.client.get_activities(before = before, after=after)
    return [Activity.from_stravalib(item) for item in activities]

Handel.get_activities = get_activities


# Cell
def save_activities(self, activities:[]):
    for i, act in enumerate(activities):
        act.save_stream(self)
    return activities
Handel.save_activities = save_activities