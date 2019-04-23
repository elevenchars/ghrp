from pypresence import Presence
import time
import json
import os
import requests


def get_newest_push(events: dict):
    for event in events:
        if event["type"] == "PushEvent":
            return event
    return None

config = {
    "github_username": None,
    "discord_client_id": None,
    "github_client_id": None,
    "github_client_secret": None,
}

config_location = "config.json"
if os.path.isfile(config_location):
    with open(config_location, "r") as config_file:
        config.update(json.load(config_file))

# We do this so that when(if) the config format is updated it will auto populate new fields.
with open(config_location, "w") as config_file:
    json.dump(config, config_file, indent=2, separators=(",", ":"))

for key in config:
    if not config[key]:
        print("{} not specified in {}.".format(key, config_location))

rpc = Presence(config["discord_client_id"])
rpc.connect()

sess = requests.Session()
headers = {}
payload = None
if config["github_client_id" and "github_client_secret"]:
    payload = {
        "client_id": config["github_client_id"],
        "client_secret": config["github_client_secret"]
    }
else:
    print("Proceeding without GitHub OAuth (60 rq/hr)")

events_url = "https://api.github.com/users/{}/events".format(config["github_username"])
# rpc.update(join="fffffff")
while True:
    # this crashes :( don't know why
    events_rq = sess.get(events_url, headers=headers, params=payload)
    if events_rq.status_code != 304:
        headers["If-None-Match"] = events_rq.headers["ETag"]
        events = json.loads(events_rq.text)
        latest = get_newest_push(events)
        print(latest)
    else:
        print("No change")

    repo_name = latest["repo"]["name"]
    # the split is so that we only get the tagline (?) of the repo
    commit_message = latest["payload"]["commits"][0]["message"].split("\n")[0]
    print("Presence Updated\nRepo: {}\nMessage: {}".format(repo_name, commit_message))
    rpc.update(details=repo_name, state=commit_message, large_image="github")
    time.sleep(60)  # can be changed, this is just so that ratelimit doesn't
    # get roasted
