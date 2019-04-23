from pypresence import Presence
import time
import json
import os
import requests

config = {
	"github_username": None,
	"discord_client_id": None
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

# rpc.update(join="fffffff")
while True:
	event_rq = sess.get("https://api.github.com/users/elevenchars/events", headers=headers)
	if event_rq.status_code != 304:
		headers["If-None-Match"] = event_rq.headers["ETag"]
		event = json.loads(event_rq.text)
		print(event[0])
	else:
		print("No change")
	time.sleep(60) # can be changed, this is just so that ratelimit doesn't get roasted