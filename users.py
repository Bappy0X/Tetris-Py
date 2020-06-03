from json import load

class User:
    def __init__(self, username: str=None, highScore: int=None):
        self.username = username
        self.highScore = highScore
    
    def __repr__(self):
        return f"<User:\"{self.username}\">"

    def __iter__(self):
        yield "username", self.username
        yield "highScore", self.highScore

    def isInitialised(self) -> bool:
        return((self.username != None) and (self.highScore != None))

    def initFromDB(self, username: str):
        #Open file and look for the user's data, if it cant be found then create a new JSON user object
        with open("userDatabase.json", "r") as file:
            data = load(file)
        if not data:
            raise(Exception("Data couldn't be read!"))
            return
        userData = data.get(username, {"highScore": 0})

        #Sanitise this data and return it
        self.__init__(username, userData["highScore"])
        return self