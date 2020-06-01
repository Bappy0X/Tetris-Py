from time import sleep as wait
from os import name, system
import threading
#from signal import signal, SIGTERM, SIGINT
from getkey import getkey, keys

class Shape:
    def __init__(self, shape: list, position: tuple=(0, 0)):
        self.posx, self.posy = position
        self.shape = shape

triangle = Shape([
    "    **",
    "    **",
    "******",
    "******"
])

class Resolution:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Window:
    def __init__(self, resolution: tuple=(20, 10), corners: tuple=("┏", "┓", "┗", "┛"), top: str="━", sides: str="┃"):
        x, y = resolution
        self.resolution = Resolution(x, y)
        self.name = "┫TETRISPY┣"
        self.topLeft, self.topRight, self.bottomLeft, self.bottomRight = corners
        self.top = top
        self.sides = sides

    def renderFrame(self):
        print(f"{self.topLeft}{self.top*(int(self.resolution.x/2)-int(len(self.name)/2))}{self.name}{self.top*(int(self.resolution.x/2)-int(len(self.name)/2))}{self.topRight}")
        for i in range(self.resolution.y):
            if i >= triangle.posy and i < len(triangle.shape) + triangle.posy:
                middle = " "*triangle.posx + triangle.shape[i] + " "*(self.resolution.x-len(triangle.shape[i])-triangle.posx)
            else:
                middle = " "*self.resolution.x
            print(f"{self.sides}{middle}{self.sides}")
        print(f"{self.bottomLeft}{self.top*self.resolution.x}{self.bottomRight}")

    def renderLoop(self, fps: int=2):
        thisThread = threading.currentThread()
        while not thisThread.shouldRender.is_set():#getattr(thisThread, "shouldRun", False):
            print("Press \"q\" or \"CTRL+Z\" to exit.")
            print(f"{' '*(self.resolution.x+2-len(f'Rendering at {fps}fps'))}Rendering at {fps}fps")
            self.renderFrame()
            wait((60/fps)/60)
            system("cls" if name == "nt" else "clear")
        print("Exiting renderLoop")
    
    def stopRenderThread(self, *args):
        self.renderThread.shouldRender.set()
        self.renderThread.join()

    def run(self, fps: int=2):
        #Create threading for renderLoop
        self.renderThread = threading.Thread(target=self.renderLoop, name="windowThread", kwargs={"fps": fps})
        self.renderThread.shouldRender = threading.Event()

        #Start thread
        self.renderThread.start()

        #While loop for key presses
        while self.renderThread.is_alive():
            try:
                key = getkey()
            except KeyboardInterrupt as e:
                self.stopRenderThread()
            else:
                if key == "q":
                    self.stopRenderThread()
                elif key == keys.UP:
                    print("UP")
                    triangle.posy += 1
                elif key == keys.DOWN:
                    print("DOWN")
                    triangle.posy -= 1
                elif key == keys.LEFT:
                    print("LEFT")
                    triangle.posx -= 1
                elif key == keys.RIGHT:
                    print("RIGHT")
                    triangle.posx += 1

        print("Exiting Main")