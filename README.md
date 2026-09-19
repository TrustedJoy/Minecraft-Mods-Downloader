
# Minecraft-Mods-Downloader

I made this cause I was bored in class. Takes a json file exported from Prism and downloads all the mods. Mainly made it so I could automatically download mods for a server.

Currently downloads only from modrinth

Adds curseforge mods to a file called .unable.txt under the mods folder


## How To Use

Download this repo either as a zip or clone it

Export the mods as json. Make sure to include the filename, url and version

Downloads the mods in a folder called mods in the same directory as the repo

After extracting the repo and getting the json file run in cmd
```bash
pip install -r requirements.txt
python main.py [modlist] [version] [loader] [onlyServer] [usingConnector]
```
| Field            | Description                                                                                     | Required | Default | Accepted Values           |
|:-----------------|:------------------------------------------------------------------------------------------------|:---------|:--------|---------------------------|
| `modlist`        | Path to json file containing mods                                                               | `yes`    |         | `path.json`               |
| `version`        | The minecraft version you are running                                                           | `yes`    |         | `any minecraft version`   |
| `loader`         | Loader you are using. If usingConnector is true it downloads irrespective of loader provided    | `yes`    |         | `forge, fabric, neoforge` |
| `onlyServer`     | If 1, doesn't download only client side mods                                                    | `no`     | `1`     | `1, 0`                    |
| `usingConnector` | Specifies if you are using sinytra connector (see below) (1 if you are using sinytra. 0 if not) | `no`     | `0`     | `1, 0`                    |


The program won't download mods which are not for the loader provided if sinytra is not being used.\
If you are using sinytra make sure to pass 0/1 for onlyServer and 1 for usingConnector (otherwise it'll take 1 for onlyServer)



## EPILOGUE
I just made this for fun when I was bored in class. I do plan to add support for curseforge and also have it be able to use text files with just the mod names. Though I don't know when that will happen