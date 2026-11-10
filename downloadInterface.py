import json
import os
import inspect
import shutil
import requests
import modLogging
import managerExceptions
import modrinthInterface
import curseforgeInterface

class DownloadManager:
    def __init__(self, gameVersion, loader, onlyServer = True, usingConnector = False):
        self.modrinth = modrinthInterface.ModrinthManager(gameVersion, loader, usingConnector)
        self.curseforge = curseforgeInterface.curseforgeManager(gameVersion, loader, usingConnector)
        self.onlyServer = onlyServer
        self.usingConnector = usingConnector
        self.downloadedModIDsModrinth = []
        self.downloadedModIDsCurseforge = []

    async def downloadMod(self, url = None, dest = None):
        try:
            if not url:
                raise managerExceptions.NoURL

            with requests.get(url, stream=True) as response:
                with open(dest, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

        except Exception as e:

            print(f"ERROR: {e} in function: {inspect.currentframe().f_code.co_name}")
            return 0

        return  1

    async def downloadCurseforgeMod(self, data = None, filename = None):
        targetFilePos = 0

        if filename:
            for i in range(len(data)):
                if data[i]['fileName'] == filename:
                    targetFilePos = i

        modID = data[targetFilePos]['modId']
        filename = data[targetFilePos]['fileName']
        downloadUrl = data[targetFilePos]['downloadUrl']

        for i in data[targetFilePos]['dependencies']:
            if i['relationType'] == 3:
                dependencyModID = i['modId']

                if dependencyModID == modID:
                    continue

                dependencyData = await self.curseforge.getModFileData(modID=dependencyModID)

                if dependencyData is None:
                    dependencyUrl = f"https://www.curseforge.com/projects/{modID}"
                    modLogging.logUnable(reason="Dependency data not found", mod=dependencyUrl)

                    continue

                print(f"Downloading a dependency for {filename}")
                await self.downloadCurseforgeMod(data=dependencyData)

        if modID in self.downloadedModIDsCurseforge:
            print(f"{filename} (or another version) already downloaded. Skipping!")
            return

        success = await self.downloadMod(url=downloadUrl, dest=f"mods/{filename}")

        if success:
            print(f"Successfully downloaded {filename}")
            self.downloadedModIDsCurseforge.append(modID)

        else:
            modUrl = f"https://www.curseforge.com/projects/{modID}"

            print(f"Failed at mod: {modUrl}")

            modLogging.logUnable(reason="Failed during download", mod=modUrl)

            return


    async def downloadModrinthMod(self, data = None, modVersion = None, filename = None):
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

                if dependencyData is None:
                    dependencyModUrl = f"https://modrinth.com/mod/{dependencyModID}"
                    modLogging.logUnable(reason="Dependency failed", mod=dependencyModUrl)

                    continue

                print(f"Downloading a dependency for {filename}")
                await self.downloadModrinthMod(dependencyData, dependencyModVersion, dependencyFilename)

        if modID in self.downloadedModIDsModrinth:
            print(f"{filename} (or another version) already downloaded. Skipping!")
            return

        success = await self.downloadMod(url=downloadUrl, dest=f"mods/{filename}")

        if success:
            print(f"Successfully downloaded {filename}")
            self.downloadedModIDsModrinth.append(modID)

        else:
            modUrl = f"https://modrinth.com/mod/{modID}"

            print(f"Failed at mod: {modUrl}")

            modLogging.logUnable(reason="Failed during download", mod=modUrl)

            return

    async def parseFileAndDownload(self, file = None):
        try:
            #create files and directories
            if os.path.exists('mods'):
                shutil.rmtree('mods')

            os.makedirs("mods", exist_ok=True)

            #region Prechecks
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
            #endregion

            for i in mods:
                if not i['filename'].split('.')[-1] in ('jar', 'disabled'):
                    continue

                if i['url'].split('/')[2] == "modrinth.com":
                    modLogging.logAble(mod=i['url'])

                    modID = i['url'].split('/')[-1]
                    modVersion = i['version']
                    filename = i['filename']

                    data = await self.modrinth.getVersionsInfo(modID=modID)

                    if data is None:
                        modLogging.logUnable(reason="No data found", mod=i['url'])

                        continue

                    modEnvironment = data[0]['environment']

                    if self.onlyServer and modEnvironment in ("client_only"):
                        print(f"Skipping mod {filename}. (In server only and mod is client only)")
                        continue

                    await self.downloadModrinthMod(data=data, modVersion=modVersion, filename=filename)

                elif i['url'].split('/')[-3] == "www.curseforge.com":
                    modLogging.logAble(mod=i['url'])

                    modID = i['url'].split('/')[-1]
                    filename = i['filename']

                    data = await self.curseforge.getModFileData(modID=modID)

                    if data is None:
                        modLogging.logUnable(reason="No data found", mod=i['url'])

                        continue

                    await self.downloadCurseforgeMod(data=data, filename=filename)

                else:
                    print("Invalid Mod. Not able to download")

                    modLogging.logUnable(reason="Invalid Mod", mod=i['url'])

                    continue

        except Exception as e:
            print(f"ERROR: {e} in function {inspect.currentframe().f_code.co_name}")