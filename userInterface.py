from time import sleep as wait
from os import name as platformName, system
import threading
from getkey import getkey, keys

class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Window:
    pass

class Shape:
    def __init__(self, shape: list, position: tuple=(0, 0)):
        self.position = Vector2(*position)
        self.shape = shape
        self.width = len(shape[0])
        self.height = len(shape)

    #Movement functions
    def moveUp(self, window: Window, amount: int=1):
        if self.position.y > 0:
            self.position.y -= 1
    def moveDown(self, window: Window, amount: int=1):
        if self.position.y + self.height < window.resolution.y:
            self.position.y += 1
    def moveLeft(self, window: Window, amount: int=1):
        if self.position.x > 0:
            self.position.x -= 1
    def moveRight(self, window: Window, amount: int=1):
        if self.position.x + self.width < window.resolution.x:
            self.position.x += 1

class Window:
    def __init__(self, resolution: tuple=(20, 20), corners: tuple=("┏", "┓", "┗", "┛"), top: str="━", sides: str="┃"):
        self.resolution = Vector2(*resolution)
        self.name = "┫TETRISPY┣"
        self.topLeft, self.topRight, self.bottomLeft, self.bottomRight = corners
        self.top = top
        self.sides = sides
        self.shapes = []
        self.currentlySelected = None

    def addShape(self, shapeToAdd: Shape):
        self.shapes.append(shapeToAdd)
        self.currentlySelected = self.shapes[-1]

    def renderFrame(self, lines: list=[]):
        lines.append(self.topLeft + self.top*(int(self.resolution.x/2)-int(len(self.name)/2)) + self.name + self.top*(int(self.resolution.x/2)-int(len(self.name)/2)) + self.topRight)
        rendery = 0
        for i in range(self.resolution.y):
            if i >=  self.shapes[0].position.y and i < self.shapes[0].height+self.shapes[0].position.y:
                middle = " "*self.shapes[0].position.x + self.shapes[0].shape[rendery] + " "*(self.resolution.x-self.shapes[0].width-self.shapes[0].position.x)
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
        print("Exiting renderThread")
    
    def stopRenderThread(self, *args) -> bool:
        try:
            self.renderThread.shouldRender.set()
            self.renderThread.join()
        except NameError:
            return False
        else:
            return True

    def run(self, fps: int=4, debug: bool=False):
        #Create threading for renderLoop and start it
        renderThread = threading.Thread(target=self.renderLoop, name="windowThread", kwargs={"fps": fps, "debug": debug})
        renderThread.start()

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
                    self.currentlySelected.moveUp(window=self)
                elif key == keys.DOWN:
                    self.currentlySelected.moveDown(window=self)
                elif key == keys.LEFT:
                    self.currentlySelected.moveLeft(window=self)
                elif key == keys.RIGHT:
                    self.currentlySelected.moveRight(window=self)

        print("Exiting Main")
