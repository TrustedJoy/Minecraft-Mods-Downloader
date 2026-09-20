import inspect
import managerExceptions
import requests
import json

class ModrinthManager:
    def __init__(self):
        pass

    async def getVersionsInfo(self, modID = None, gameVersion = None, loader = None, usingConnector = False):
        try:
            if not modID:
                raise managerExceptions.ModNotProvided

            if gameVersion and loader:
                gameVersion = str(json.dumps([gameVersion]))
                loader = str(json.dumps([loader]))

                url = f'https://api.modrinth.com/v2/project/{modID}/version'

                params = {'game_versions' : gameVersion, 'loaders' : loader}
                r = requests.get(url, params=params)

                if not len(r.json()):
                    if usingConnector:
                        loader = '["forge", "fabric", "neoforge]'

                        params = {'game_versions': gameVersion, 'loaders': loader}
                        r = requests.get(url, params=params)

                    else:
                        raise managerExceptions.EmptyResponse

                if r.status_code == 404:
                    raise managerExceptions.NotFoundError

                return r.json()

            else:
                raise managerExceptions.ParamError

        except Exception as e:
            print(f"ERROR: {e} at mod with ID {modID} in function {inspect.currentframe().f_code.co_name}")


    async def getEnvironment(self, modID = None, gameVersion = None, loader = None, usingConnector = False):

        data = await self.getVersionsInfo(modID, gameVersion, loader, usingConnector)

        return data[0]['environment']

    async def downloadModFromModrinth(self, url = None, dest = None):
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