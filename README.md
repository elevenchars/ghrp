# discordghrp
### discord rich presence tool

Discordghrp will show your most recent GitHub commit for up to one hour after it is made in your rich presence.

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