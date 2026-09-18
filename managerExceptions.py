class ParamError(Exception):
    def __init__(self):
        self.message = "Loader/Version not provided"
        self.errorCode = 400

    def __str__(self):
        return f"{self.message} (Error Code: {self.errorCode})"

class NotFoundError(Exception):
    def __init__(self):
        self.message = "Could not find the mod. Check if url/id is correct"
        self.errorCode = 404

    def __str__(self):
        return f"{self.message} (Error Code: {self.errorCode})"

class ModNotProvided(Exception):
    def __init__(self):
        self.message = "No Mod Provided"
        self.errorCode = 404

    def __str__(self):
        return f"{self.message} (Error Code: {self.errorCode})"

class NoURL(Exception):
    def __init__(self):
        self.message = "No URL Provided"
        self.errorCode = 404

    def __str__(self):
        return f"{self.message} (Error Code: {self.errorCode})"