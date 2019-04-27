from pypresence import Presence
import time
import calendar
import json
import os
import requests


class ghrp():
    def __init__(self, discord_client_id: str, github_username: str, github_client_id: str = None, github_client_secret: str = None):
        """Init method for the GHRP class.

        Arguments:
            discord_client_id {str} -- Discord Client ID from the developer
            portal.
            github_username {str} -- GitHub username to monitor

        Keyword Arguments:
            github_client_id {str} -- GitHub OAuth application client id 
            (default: {None})
            github_client_secret {str} -- GitHub OAuth application client
            secret (default: {None})
        """
        self.dclient = discord_client_id
        self.gusername = github_username
        self.gclientid = github_client_id
        self.gclientsecret = github_client_secret
        self.show_status = False

        self.payload = None
        self.headers = {}
        self.events_url = "https://api.github.com/users/{}/events".format(
            config["github_username"])
        self.session = requests.Session()

        self.timestamp = 0

        # if github client id and secret are not provided we need to make sure
        # we don't go over the ratelimit.
        if self.gclientid and self.gclientsecret:
            self.interval = 30
            payload = {
                "client_id": config["github_client_id"],
                "client_secret": config["github_client_secret"]
            }
        else:
            self.interval = 60

        self.rpc = Presence(self.dclient)
        self.rpc.connect()

    def get_newest_push(self, events: dict) -> dict:
        """Helper method for getting the most recent commit.
        Returns the most recent event object that includes a commit
        (not new projects)

        Returns:
            dict -- Most recent event containing a commit.
        """
        for event in events:
            if event["type"] == "PushEvent":
                return event
        return None

    def update(self) -> None:
        """Method to update the rich presence instance.
        Every 30 or 60 seconds (see __init__) it queries the GitHub events API.
        If there is new info, it checks if it is a commit. If it is, it
        parses it and updates the rich presence. After 1 hour, it clears the
        rich presence.
        """
        events_rq = self.session.get(
            self.events_url, headers=self.headers, params=self.payload)
        if events_rq.status_code != 304:
            self.show_status = True
            self.headers["If-None-Match"] = events_rq.headers["ETag"]
            events = json.loads(events_rq.text)
            latest = self.get_newest_push(events)
            repo_name = latest["repo"]["name"].split("/")[1]
            commit_message = latest["payload"]["commits"][0]["message"].split("\n")[
                0]
            self.timestamp = calendar.timegm(time.strptime(
                latest["created_at"], "%Y-%m-%dT%H:%M:%SZ"))

            self.rpc.update(details=repo_name, state=commit_message,
                            large_image="github")
        else:
            if (time.time() - self.timestamp) > 60*60 and self.show_status:
                self.rpc.clear()
                self.show_status = False

if __name__ == "__main__":
    config = {
        "discord_client_id": None,
        "github_username": None,
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

    instance = ghrp(config["discord_client_id"], config["github_username"],
                    config["github_client_id"], config["github_client_secret"])

    while True:
        instance.update()
        time.sleep(instance.interval)
