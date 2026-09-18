import json
import modrinthInterface

class DownloadManager:
    def __init__(self):
        self.modrinth = modrinthInterface.ModrinthManager()
        pass

    async def downloadMod(self, modID = None, gameVersion = None, loader = None, modVersion = None, usingConnector = False):

        data = await self.modrinth.getVersionsInfo(modID, gameVersion, loader, usingConnector)

        modName = None
        downloadUrl = None
        filename = None

        if not modVersion:
            modName = data[0]['name']
            filename = data[0]['files'][0]['filename']
            downloadUrl = data[0]['files'][0]['url']

        else:
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

        success = await self.modrinth.downloadMod(url=downloadUrl, dest=f"testing/{filename}")

        if success:
            print(f"Successfuly downloaded {filename}")

        else:
            print(f"Failed at mod with ID: {modID}")
            exit()


    async def parseFileAndDownload(self, file = None, gameVersion = None, loader = None, onlyServer = True, usingConnector = False):

        try:
            with open(file, 'r') as f:
                mods = json.load(f)

            if onlyServer:
                print("Not downloading client side testing")

            if not usingConnector:
                print("Sinytra connector not being used. Only downloading testing that match given loader")

            for i in mods:
                if not i['filename'].split('.')[-1] in ('jar', 'disabled'):
                    continue

                if not i['url'].split('/')[2] == "modrinth.com":
                    continue

                modID = i['url'].split('/')[-1]
                modVersion = i['version']

                modEnvironment = await self.modrinth.getEnvironment(modID=modID, gameVersion=gameVersion, loader=loader, usingConnector=usingConnector)

                if onlyServer:
                    if modEnvironment in ('client_only'):

                        print(f"Skpping mod with ID {modID}. (In server only and mod is client only)")

                        continue

                await self.downloadMod(modID=modID, gameVersion=gameVersion, loader=loader, modVersion=modVersion, usingConnector=usingConnector)

        except Exception as e:
            print(f"ERROR: {e}")