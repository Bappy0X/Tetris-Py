from time import sleep as wait
from os import name as platformName, system
import threading
from getkey import getkey, keys

class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Shape:
    def __init__(self, shape: list, position: tuple=(0, 0)):
        self.position = Vector2(*position)
        self.shape = shape
        self.width = len(shape[0])
        self.height = len(shape)

sample = Shape([
    "########",
    "#      #",
    "#      #",
    "########"
])

shapes = []

class Window:
    def __init__(self, resolution: tuple=(20, 20), corners: tuple=("┏", "┓", "┗", "┛"), top: str="━", sides: str="┃"):
        self.resolution = Vector2(*resolution)
        self.name = "┫TETRISPY┣"
        self.topLeft, self.topRight, self.bottomLeft, self.bottomRight = corners
        self.top = top
        self.sides = sides

    def renderFrame(self, lines: list=[]):
        lines.append(self.topLeft + self.top*(int(self.resolution.x/2)-int(len(self.name)/2)) + self.name + self.top*(int(self.resolution.x/2)-int(len(self.name)/2)) + self.topRight)
        #for i in shapes:
        rendery = 0
        for i in range(self.resolution.y):
            if i >=  sample.position.y and i < sample.height+sample.position.y:
                middle = " "*sample.position.x + sample.shape[rendery] + " "*(self.resolution.x-sample.width-sample.position.x)
                rendery += 1
            else:
                middle = " "*self.resolution.x
            lines.append(self.sides + middle + self.sides)
        lines.append(self.bottomLeft + self.top*self.resolution.x + self.bottomRight)
        print("\n".join(lines))

    def renderLoop(self, fps: int=4, debug: bool=False):
        self.renderThread = threading.currentThread()
        self.renderThread.shouldRender = threading.Event()
        while not self.renderThread.shouldRender.is_set():
            self.renderFrame(lines=[
                "Press \"q\" or \"CTRL+Z\" to exit.",
                f"{' '*(self.resolution.x+2-len(f'Rendering at {fps}fps'))}Rendering at {fps}fps"
            ])
            wait((60/fps)/60)
            if not debug:
                system("cls" if platformName == "nt" else "clear")
        print("Exiting renderLoop")
    
    def stopRenderThread(self, *args) -> bool:
        try:
            self.renderThread.shouldRender.set()
            self.renderThread.join()
        except NameError:
            return False
        else:
            return True

    def run(self, fps: int=4, debug: bool=False):
        #Create threading for renderLoop
        threading.Thread(target=self.renderLoop, name="windowThread", kwargs={"fps": fps, "debug": debug})

        #Start thread
        self.renderThread.start()

        #While loop for key presses
        while self.renderThread.is_alive():
            try:
                key = getkey()
            except KeyboardInterrupt:
                self.stopRenderThread()
            else:
                if key == "q":
                    self.stopRenderThread()
                elif key == keys.UP:
                    if sample.position.y > 0:
                        sample.position.y -= 1
                elif key == keys.DOWN:
                    if sample.position.y + sample.height < self.resolution.y:
                        sample.position.y += 1
                elif key == keys.LEFT:
                    if sample.position.x > 0:
                        sample.position.x -= 1
                elif key == keys.RIGHT:
                    if sample.position.x + sample.width < self.resolution.x:
                        sample.position.x += 1

        print("Exiting Main")