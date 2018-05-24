import pygame.gfxdraw
import pygame.draw
from math import *
from vector2d import *

class Body():
    """
    Base shape class.
    Default parameters:
        name = ""
        color = (255,255,255)
        fill = False
        F = Vec2D(0,0)
        a = Vec2D(0,0)
        a_const = Vec2D(0,0)
        v = Vec2D(0,0)
        x = y = 0
        m = 1
        w = 0
        angle = 0
        restitution = 1
        staticfriction = 0
        dynamicfriction = 0
    """
    def __init__(self, engine, **attr):
        self.engine = engine
        self.name = ""
        self.color = (255,255,255)
        self.fill = False
        self.F = Vec2D(0,0)
        self.a = Vec2D(0,0)
        self.const_a = Vec2D(0,0) # Mingi konstantne kiirendus
        self.v = Vec2D(0,0)
        self.x = self.y = 0
        self.m = 1
        self.w = 0 # nurkkiirus
        self.angle = 0
        self.restitution = 1 # elastsus
        self.staticfriction = 0 # hoordetegur
        self.dynamicfriction = 0
        for key, value in attr.items():
            setattr(self, key, value)

        self.drag = 0
        self.N = Vec2D(0,0)
        self.path = list()
        self.contacts = set()

    def getNormalForce(self):
        # Kui keha kiirus on nullilähedane, viime ta nulli
        if abs(self.v[0]) < self.engine.vBoundary:
            self.engine.energyloss += self.v[0]**2 * self.m/2
            self.v = Vec2D(0, self.v[1])
        if abs(self.v[1]) < self.engine.vBoundary:
            self.engine.energyloss += self.v[1]**2 * self.m/2
            self.v = Vec2D(self.v[0], 0)

        N = Vec2D(0,0)
        g = self.engine.g + self.const_a
        for cx, cy in sorted(self.contacts, key=lambda x: dot2D(g, x)):
            distance_cp = dot2D(g, Vec2D(cx, cy))
            distance_self = dot2D(g, Vec2D(self.x, self.y))
            n = Vec2D(cx - self.x, cy - self.y)

            # Kui keha on pinna all või pole paigal, siis
            # siis ei rakenda toereaktsiooni
            if distance_cp < distance_self or dot2D(self.v, n):
                continue

            n = n.normalised()
            angle = degrees(acos(dot2D(n, g.normalised())))
            N -= g.rotate(angle)
            #N -= n*(dot2D(n, g))
        return N

    def getAcceleration(self, t=1):
        # Liidame kõik mõjuvad kiirendused
        self.N = self.getNormalForce()
        aSum = self.F / self.m + self.engine.g + self.const_a + self.N
        
##        if self.drag and any(self.v):
##            direction = self.v.normalised()
####            if (self.v.modulesq() * self.drag * t)**2 < self.v.modulesq():
####                aSum -= self.drag * abs(self.v) * self.v
####            elif aSum.modulesq() *t**2 < self.v.modulesq():
####                aSum -= self.v
##
##            if dot2D(self.drag * abs(self.v) * self.v * t, direction) <= dot2D(self.v + aSum*t, direction):
##                aSum -= self.drag * abs(self.v) * self.v

        if self in self.engine.gravityBodies and len(self.engine.gravityBodies) > 1:
            G = 6.674*10**-11
            for o in self.engine.gravityBodies - {self,}:
                r = Vec2D(o.x - self.x, o.y - self.y)
                aSum += G*o.m/r.modulesq() * r.normalised()
        return aSum

    def update_position(self, x=None):
        # Keha liigutamiseks
        pass
    def delta_position(self, x=None): return
    def getEnergy(self):
        if self.m == float("inf"):
            return 0
        return (abs(self.v*self.v)*self.m + self.w*self.w*self.I) / 2 + self.m*dot2D(
            self.engine.g, Vec2D(self.engine.width - self.x, self.engine.height - self.y))
    def move(self):
        # keha joonistamiseks
        pass


class Circle(Body):
    def __init__(self, radius, **attr):
        super().__init__(**attr)
        self.radius = radius
        self.I = self.m * radius**2
        self.drag = self.engine.coef_drag * pi * radius / (2*self.m)
        if self.engine.width <= 2 * radius or self.engine.height <= 2 * radius:
            raise ValueError("{} body {} is too large. radius = {}".format(type(self), self.name, self.radius))
        
    def update_position(self, time_percent=1):
        time_step = time_percent * self.engine.step
        self.F = Vec2D(0,0)
        if self.engine.debug:
            print("acceleration", self.name, self.a, self.N, self.contacts)
        
        self.angle += self.w * time_step
        while self.angle >= 2 * pi:
            self.angle -= 2 * pi
        while self.angle < 0:
            self.angle += 2 * pi

##        for cx, cy in self.contacts:
##            r = Vec2D(cx, cy) - (self.x, self.y)
##            #self.v += r.perp() * self.w * time_step
##            #self.w = self.v.modulesq() / self.radius

        # Suurema täpsusega Euleri integreerimine
        self.x += self.v[0] * time_step + (self.a[0] / 2) * time_step**2
        self.y += self.v[1] * time_step + (self.a[1] / 2) * time_step**2
        self.v += self.a * time_step
        self.a = Vec2D(0,0)
        
        todiscard = set()
        for cx, cy in self.contacts:
            n = Vec2D(cx - self.x, cy - self.y).normalised()
            # Kui keha ei asu enam kontaktpunktis voi on
            # olemas punktisuunaline kiirus, unustame punkti
            if Vec2D(self.x, self.y) + n*self.radius != Vec2D(cx, cy) or dot2D(n, self.v):
                todiscard.add((cx, cy))
        self.contacts -= todiscard

    def delta_position(self, time_percent = 1):
        time_step = time_percent * self.engine.step
##        v = self.v
##        for cx, cy in self.contacts:
##            r = Vec2D(cx, cy) - (self.x, self.y)
##            v += r.rotate(-90) * self.w * time_step
        return self.v * time_step + (self.getAcceleration() / 2) * time_step**2

    def move(self):
        scr = self.engine.screen
        suund = self.v.normalised() * self.radius + (self.x, self.y)
        a = self.angle
        r = self.radius * Vec2D(cos(a), sin(a)) + (self.x, self.y)
                
        if self.fill:
            pygame.gfxdraw.filled_circle(scr, int(self.x), int(self.y), self.radius, self.color)
        else:
            pygame.gfxdraw.circle(scr, int(self.x), int(self.y), self.radius, self.color)
        #Kiiruse suund:
        pygame.draw.line(scr, (120,120,120), (int(self.x), int(self.y)), (int(suund[0]), int(suund[1])))
        #Pöördenurk:
        pygame.draw.line(scr, self.color, (int(self.x), int(self.y)), (int(r[0]), int(r[1])))
        for cx, cy in self.contacts:
            assert -1 < cx < self.engine.width+1 and -1 < cy < self.engine.height+1, "contact point out of range {} {} {}".format(self.name, cx, cy)
            pygame.draw.circle(scr, (22,200,23), (int(cx), int(cy)), 3)
            
        if self.engine.pathLimit == 0:
            return
        #Trajektoor:
        for i in range(1, len(self.path)):
            p = tuple(map(int, self.path[i]))
            pygame.gfxdraw.pixel(scr, p[0], p[1], self.color)
            pygame.draw.line(scr, self.color, (int(self.path[i-1][0]), int(self.path[i-1][1])), p)
        if len(self.path) > self.engine.pathLimit:
            self.path = self.path[-self.engine.pathLimit:]

class Wall(Body):
    def __init__(self, x1, y1, x2, y2, **attr):
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2
        #Rnormal = Lnormal = True
        super().__init__(**attr)
        self.I = self.m = float("inf")
        self.v = Vec2D(0,0)
        self.lineVec = Vec2D(self.x2 - self.x1, self.y2 - self.y1)
        self.lineVecDir = self.lineVec.normalised()
        # Sirge normaal
        self.normal = self.lineVec.perp().normalised()
    def getAcceleration(self):
        return Vec2D(0,0)
    def move(self):
        pygame.draw.line(self.engine.screen, self.color, (int(self.x1), int(self.y1)), (int(self.x2), int(self.y2)))
