import json
import os
import inspect
import shutil

import modrinthInterface

class DownloadManager:
    def __init__(self, gameVersion, loader, onlyServer = True, usingConnector = False):
        self.modrinth = modrinthInterface.ModrinthManager(gameVersion, loader, usingConnector)
        self.onlyServer = onlyServer
        self.usingConnector = usingConnector
        self.downloadedModIDs = []

    async def downloadMod(self, data = None, modVersion = None, filename = None):
        targetEntryPos = 0
        targetFilePos = 0

        if filename:
            for i in range(len(data)):
                for j in range(len(data[i]['files'])):
                    if data[i]['files'][j]['filename'] == filename:
                        targetEntryPos = i
                        targetFilePos = j

        if modVersion:
            for i in range(len(data)):
                if data[i]['version_number'] == modVersion:
                    targetEntryPos = i

                    break

        modID = data[targetEntryPos]['project_id']
        filename = data[targetEntryPos]['files'][targetFilePos]['filename']
        downloadUrl = data[targetEntryPos]['files'][targetFilePos]['url']

        for dependency in data[targetEntryPos]['dependencies']:
            if dependency['dependency_type'] == 'required':
                dependencyModVersion = dependency['version_id']
                dependencyModID = dependency['project_id']
                dependencyFilename = dependency['file_name']

                if dependencyModID == modID:
                    continue

                dependencyData = await self.modrinth.getVersionsInfo(dependencyModID)

                print(f"Downloading a dependency for {filename}")
                await self.downloadMod(dependencyData, dependencyModVersion, dependencyFilename)

        if modID in self.downloadedModIDs:
            print(f"{filename} (or another version) already downloaded. Skipping!")
            return

        success = await self.modrinth.downloadModFromModrinth(url=downloadUrl, dest=f"mods/{filename}")

        if success:
            print(f"Successfully downloaded {filename}")
            self.downloadedModIDs.append(modID)

        else:
            print(f"Failed at mod: {filename}")

            with open('mods/.unable.txt', 'a+') as f:
                f.write(f"{filename}")

            return

    async def parseFileAndDownload(self, file = None):
        #try:
            if os.path.exists('mods'):
                shutil.rmtree('mods')

            os.makedirs("mods", exist_ok=True)

            with open('mods/.able.txt', 'w'):
                pass

            with open('mods/.unable.txt', 'w'):
                pass

            with open(file, 'r') as f:
                mods = json.load(f)

            if self.onlyServer:
                print("Not downloading client side mods")

            if not self.usingConnector:
                print("Sinytra connector not being used. Only downloading mods that match given loader")

            for i in mods:
                if not i['filename'].split('.')[-1] in ('jar', 'disabled'):
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

                data = await self.modrinth.getVersionsInfo(modID=modID)

                modEnvironment = data[0]['environment']

                if self.onlyServer and modEnvironment in ("client_only"):
                    print(f"Skipping mod {filename}. (In server only and mod is client only)")

                    continue

                await self.downloadMod(data=data, modVersion=modVersion, filename=filename)

        #except Exception as e:
        #    print(f"ERROR: {e} in function {inspect.currentframe().f_code.co_name}")