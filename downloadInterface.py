import json
import os
import inspect
from typing import Any

import modrinthInterface

class DownloadManager:
    def __init__(self):
        self.modrinth = modrinthInterface.ModrinthManager()
        pass

    async def downloadMod(self, modID = None, gameVersion = None, loader = None, modVersion = None, filename = None, usingConnector = False):

        data = await self.modrinth.getVersionsInfo(modID, gameVersion, loader, usingConnector)

        downloadUrl, filename, modName = await self.getDownloadUrl(data, filename, modVersion)

        if not os.path.exists("mods"):
            os.makedirs("mods")

        success = await self.modrinth.downloadModFromModrinth(url=downloadUrl, dest=f"mods/{filename}")

        if success:
            print(f"Successfuly downloaded {filename}")

        else:
            print(f"Failed at mod with ID: {modID}")

            with open('mods/.unable.txt', 'a+') as f:
                f.write(f"{modName}")

            exit()

    async def getDownloadUrl(self, data, filename, modVersion) -> tuple[Any, Any, Any]:

        downloadUrl = None
        modName = None

        if filename:
            for i in range(len(data)):
                for j in data[i]['files']:
                    if j['filename'] == filename:
                        modName = data[i]['name']
                        downloadUrl = j['url']

        if modVersion:
            for i in range(len(data)):
                if data[i]['version_number'] == modVersion:
                    modName = data[i]['name']
                    filename = data[i]['files'][0]['filename']
                    downloadUrl = data[i]['files'][0]['url']

                    break

        if not downloadUrl:
            modName = data[0]['name']
            filename = data[0]['files'][0]['filename']
            downloadUrl = data[0]['files'][0]['url']

        return downloadUrl, filename, modName

    async def parseFileAndDownload(self, file = None, gameVersion = None, loader = None, onlyServer = True, usingConnector = False):

        try:
            os.makedirs("mods", exist_ok=True)

            with open('mods/.able.txt', 'w'):
                pass

            with open('mods/.unable.txt', 'w'):
                pass

            with open(file, 'r') as f:
                mods = json.load(f)

            if onlyServer:
                print("Not downloading client side mods")

            if not usingConnector:
                print("Sinytra connector not being used. Only downloading mods that match given loader")

            downloadedMods = [f for f in os.listdir('mods') if os.path.isfile(f"mods/{f}")]

            for i in mods:
                if not i['filename'].split('.')[-1] in ('jar', 'disabled'):
                    continue

                if i['filename'] in downloadedMods:
                    print(f"Mod {i['filename']} already downloaded. Skipping")
                    continue

                if not i['url'].split('/')[2] == "modrinth.com":
                    print("Curseforge Mod. Not able to download")
                    with open('mods/.unable.txt', 'a+') as f:
                        f.write(f"{i['url']}\n")
                    continue

                else:
                    with open('mods/.able.txt', 'a+') as f:
                        f.write(f"{i['url']}\n")

                    #continue

                modID = i['url'].split('/')[-1]
                modVersion = i['version']
                filename = i['filename']

                modEnvironment = await self.modrinth.getEnvironment(modID=modID, gameVersion=gameVersion, loader=loader, usingConnector=usingConnector)

                if onlyServer:
                    if modEnvironment in ('client_only'):

                        print(f"Skpping mod with ID {modID}. (In server only and mod is client only)")

                        continue

                await self.downloadMod(modID=modID, gameVersion=gameVersion, loader=loader, modVersion=modVersion, filename=filename, usingConnector=usingConnector)

        except Exception as e:
            print(f"ERROR: {e} in function {inspect.currentframe().f_code.co_name}")