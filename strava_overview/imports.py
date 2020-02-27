import stravalib
import urllib.parse
import webbrowser
import os
import pandas as pd
import sys
from fastcore.utils import *
import time
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
host = os.getenv("host")
client_id = os.getenv("client_id")
secret = os.getenv("secret")

from git import Repo
from nbdev.export import Config as nb_Config
from nbdev.export import *

def git_add(fname, commit_msg='.'):
    repo = Repo(nb_Config().nbs_path.parent)
    notebook2script(fname)
    nb = read_nb(fname)
    default = find_default_export(nb['cells'])
    py = [os.path.join(nb_Config().lib_path,*default.split('.'))+'.py',
          os.path.join(nb_Config().nbs_path,fname)
         ]
    repo.index.add(py)
    repo.index.commit(commit_msg)
    return py
