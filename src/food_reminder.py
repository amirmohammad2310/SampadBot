import schedule
import json
from datetime import datetime
import threading


def read_weekly_dic():
    with open("../data/weeklyschedule.json", "r") as file:
        return json.load(file)

def delete_weekly(id):
    with open("./data/weeklyschedule.json", "r") as file:
        dict_weekly = json.load(file)


    dict_weekly.pop(str(id))
    str_weekly = json.dumps(dict_weekly)

    with open("./data/weeklyschedule.json", "w") as file1:
        file1.write(str_weekly)
    




