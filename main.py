from users import User
from userInterface import Window

if __name__ == "__main__":
    #Handle user
    player = User()
    player.initFromDB("Josh2")
    if player.isInitialised():
        print(player)
        print(dict(player))
    else:
        raise(Exception("Player was not initialised!"))
    
    #Create window
    win = Window()
    win.renderFrame()
    win.run(fps=0.5)