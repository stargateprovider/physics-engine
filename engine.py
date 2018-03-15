import pygame
from pygame.locals import *
import pygame.gfxdraw
import pygame.draw

from vector2d import *
from bodies import *
from collision import *


class Engine():
    def __init__(self, width, height, time_step=1,
                 velBoundary=1e-5, gravity=Vec2D(0,0),
                 coef_drag=0, bgcolor=(0,0,0), fpsLimit=None,
                 title="Physics", pathLimit=0):
        self.width = width
        self.height = height
        self.step = time_step
        self.g = gravity
        self.coef_drag = coef_drag
        self.vBoundary = velBoundary
        self.energyloss = 0
        
        self.time = 0 # Töötamise aeg
        self.next_collision = 1 # aja protsent
        self.collisions = []
        self.objects = set()
        self.gravityBodies = set()
        self.pathLimit = pathLimit
        
        self.fps = fpsLimit
        self.pause = False
        self.debug = False
        self.accumulator = 0

        self.bgcolor = bgcolor
        pygame.init()
        self.screen = pygame.display.set_mode([width,height])
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

    def addCircle(self, radius, x, y, **attr):
        self.objects.add(Circle(radius=radius, x=x, y=y, engine=self, **attr))
    def addWall(self, x1, y1, x2, y2, **attr):
        self.objects.add(Wall(x1=x1, y1=y1, x2=x2, y2=y2, engine=self, **attr))
    def removeBody(self, body):
        self.objects.discard(body)
    
    def start(self, endcondition = None):
        self.running = True
        self.endCondition = endcondition

        self.movingBodies = set()
        for o in self.objects:
            if type(o) != Wall:
                self.movingBodies.add(o)
                
        for o1 in self.movingBodies:
            for o2 in self.movingBodies:
                if o1.m * o2.m > 10e6 and o1 != o2:
                    self.gravityBodies.add(o1)
                    self.gravityBodies.add(o2)
        
        self.mainloop()
    def stop(self):
        self.running = False
        self.endCondition = True
    def togglePause(self):
        self.pause = not self.pause
        
    def draw(self):
        """Draws everything on screen."""
        self.screen.fill(self.bgcolor)
        for o in self.objects:
            o.move()
        pygame.display.flip()
        if self.fps != None:
            self.clock.tick(self.fps)
        else:
            self.clock.tick()
        
    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    self.togglePause()
                elif event.key == K_d:
                    self.debug = not self.debug
        pressed = pygame.key.get_pressed()

    def updateScene(self):
        self.time_left = 1 # Protsent, mis kaadrist jarel on
        self.collisions = [0] # Siia kogutakse leitud põrkuvate kehade paarid

        while self.collisions and self.time_left:
            self.next_collision = self.time_left
            self.collisions = []
            kontrollimata = set(self.objects)
            for o1 in self.objects:
                kontrollimata.remove(o1)
                for o2 in kontrollimata:
                    col = Collision(self, o1, o2)
                    if col.time < self.next_collision:
                        self.collisions = [col,]
                        self.next_collision = col.time
                    elif col.time == self.next_collision:
                        self.collisions.append(col)
                if self.debug:
                    self.errorCheck(o1, 0.1)

            fix_intersections(self)

            if self.collisions:
                for o in self.movingBodies:
                    o.a = o.getAcceleration()

                for o in self.movingBodies:
                    o.update_position(self.next_collision)
                self.time_left -= self.next_collision
                
                for col in self.collisions:
                    if self.debug:
                        print("col", col.time, col.normal)
                    col.response()

            self.time += self.next_collision
            self.processEvents()

        self.energy = 0
        for o in self.movingBodies:
            o.a = o.getAcceleration()
        for o in self.movingBodies:
            if self.time_left:
                o.update_position(self.time_left)
            o.path.append((o.x, o.y))
            self.energy += o.getEnergy()
        
    def mainloop(self):
        while not self.endCondition:
            self.processEvents()
            if not self.pause:
##                if self.debug:
##                        print(self.energy)
                self.updateScene()
                self.draw()

    def errorCheck(self, o, allow=0):
        # Funktsioon vigade kontrollimiseks
        if type(o) != Circle:
            return
        if o.x-o.radius < -allow or o.x+o.radius > self.width+allow or o.y-o.radius < -allow or o.y+o.radius > self.height+allow:
            if hasattr(o, "name"): print("\n",o.name, o.v, o.delta_position(self.next_collision))
            print("BAD LOCATION>", self.time, self.time_left, o.x, o.y, o.radius)
            print(self.next_collision, self.collisions, end="\n\n")
            #self.draw()
            #pygame.draw.circle(self.screen, (200,22,23), (int(o.x), int(o.y)), 2)
            input()

        for o2 in self.objects:
            if type(o2) == Circle and (o.x-o2.x)**2 + (o.y-o2.y)**2 < (o.radius+o2.radius-allow)**2 and o!=o2:
                penetration = o.radius + o2.radius - sqrt((o.x-o2.x)**2 + (o.y-o2.y)**2)
                print("\nCIRCLES INTERSECT t:{} nc:{} depth:{}".format(self.time, self.next_collision, penetration))
                print(o.name, o.radius, o.x, o.y, o.v, o.a, o.N, "\n", o2.name, o2.radius, o2.x, o2.y, o2.v, o2.a, o2.N)
                #self.draw()
                pygame.draw.circle(self.screen, (200,22,23), (int(o.x), int(o.y)), 2)
                pygame.draw.circle(self.screen, (200,22,23), (int(o2.x), int(o2.y)), 2)
                input()

