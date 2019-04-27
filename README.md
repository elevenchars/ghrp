# discordghrp
###### Discord Rich Presence Tool

GHRP will show your most recent GitHub commit for up to one hour after it is made in your rich presence.

## Prerequisites

 - Create a new Discord application [here](https://discordapp.com/developers/applications/).
 - Upload a rich presence asset with the key `github` to the application.
 - Create a [GitHub OAuth Application](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/).

## Running

```
pip install -r requirements.txt
```

```
python ghrp.py
```

This will fail, but generate a file called `config.json`. Add your information.

You can then run `ghrp.py` in the background and have your rich presence automatically update

A GitHub OAuth application is not specifically required to use this, but in order to refresh the presence often (> once/min) we need to increase the ratelimit.

## Known Flaws

Currently, GHRP is not smart enough to determine if it needs to update your presence on a non-commit event.


For example, if a `WatchEvent` is pushed to the events API and no commit is made in the past hour it will show the most recent commit for `self.interval` seconds. This will be fixed shortly after a small refactor of the `ghrp.update()`.