import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

roam_port = os.environ.get("ROAM_PORT")
roam_token = os.environ.get("ROAM_TOKEN")
roam_graph = os.environ.get("ROAM_GRAPH")

def call_roam_api(action, args):
    url = f"http://127.0.0.1:{roam_port}/api/{roam_graph}"
    headers = {
        "Authorization": f"Bearer {roam_token}",
    }
    body = {
        "action": action,
        "args": args,
        "expectedApiVersion": "1.1.0",
    }
    response = requests.post(url, headers=headers,json=body)
    return response.json()

def get_page(uid=None, title=None):
    result_dict = call_roam_api(
        "data.ai.getPage", 
        [{"uid": uid}]if uid is not None  else [{"title": title}]
    )
    return result_dict["result"]

def search(query, scope="all"):
    result_dict = call_roam_api(
        "data.ai.search",
        [{"query": query, "scope": scope}]
    )
    return result_dict["result"]


def get_today_uid():
    dt = datetime.now()
    today_uid = f"{dt.month:02d}-{dt.day:02d}-{dt.year}"
    return today_uid
