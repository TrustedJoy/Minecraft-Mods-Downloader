import json
import inspect
import os
import managerExceptions
import requests
from dotenv import load_dotenv

class curseforgeManager:
    def __init__(self, gameVersion=None, loader=None, usingConnector=0):
        load_dotenv()
        self.gameVersion = gameVersion
        self.loader = loader
        self.usingConnector = usingConnector
        self.APIKey = os.environ.get("CURSEFORGE_API")

    async def getModFileData(self, modID = None):
        try:
            if not  modID:
                raise managerExceptions.ModNotProvided

            if self.gameVersion and self.loader:
                headers = {'x-api-key': self.APIKey}
                params = {'gameVersion': self.gameVersion, 'modLoaderType': self.loader}
                url = f'https://api.curseforge.com/v1/mods/{modID}/files'

                r = requests.get(url=url, headers=headers, params=params)
                data = r.json()['data']

                if not len(data):
                    if self.usingConnector:
                        params = {'gameVersion': self.gameVersion}

                        r = requests.get(url=url, headers=headers, params=params)
                        data = r.json()['data']

                        if not len(data):
                            raise managerExceptions.EmptyResponse

                    else:
                        raise managerExceptions.EmptyResponse

                if r.status_code == 404:
                    raise managerExceptions.NotFoundError

                return data

            else:
                raise managerExceptions.ParamError

        except managerExceptions.EmptyResponse:
            print(f"ERROR: No mod data found. Skipping!")

            return None

        except Exception as e:
            print(f"ERROR: {e} in function {inspect.currentframe().f_code.co_name}")