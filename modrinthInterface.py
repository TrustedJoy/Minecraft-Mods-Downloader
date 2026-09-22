import inspect
import managerExceptions
import requests
import json

class ModrinthManager:
    def __init__(self, gameVersion, loader, usingConnector = False):
        self.gameVersion = gameVersion
        self.loader = loader
        self.usingConnector = usingConnector
        pass

    async def getVersionsInfo(self, modID = None):
        try:
            if not modID:
                raise managerExceptions.ModNotProvided

            if self.gameVersion and self.loader:
                gameVersion = str(json.dumps([self.gameVersion]))
                loader = str(json.dumps([self.loader]))

                url = f'https://api.modrinth.com/v2/project/{modID}/version'

                params = {'game_versions' : gameVersion, 'loaders' : loader}
                r = requests.get(url, params=params)

                if not len(r.json()):
                    if self.usingConnector:
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