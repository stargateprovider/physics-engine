from math import *
from numpy import roots

from vector2d import *
from bodies import *


def quadrat(a, b, c):
    d = b*b - 4*a*c
    if d < 0 or not a:
        return None
    d = sqrt(d) if d else 0
    return ((-b + d) / (2*a), (-b - d) / (2*a))

def min_in_range(iterable, mini, maxi):
    if not hasattr(iterable, "__iter__"):
        return
    smallest = maxi
    found = False
    for i in iterable:
        if i == None or i.imag:
            continue
        if mini <= i.real <= smallest <= maxi:
            smallest = i.real
            found = True
    if found:
        return smallest
    return


def fix_intersections(engine):
    intersections = True
    while intersections:
        #engine.draw()
        intersections = False
        kontrollimata = set(engine.objects)

        for o1 in engine.movingBodies:
            kontrollimata.remove(o1)
            
##            if o1.x+o1.radius > engine.width:
##                o1.x -= o1.x + o1.radius - engine.width
##                intersections = True
##            elif o1.x-o1.radius < 0:
##                o1.x += o1.radius - o1.x
##                intersections = True
##            if o1.y+o1.radius > engine.height:
##                o1.y -= o1.y + o1.radius - engine.height
##                intersections = True
##            elif o1.y-o1.radius < 0:
##                o1.y += o1.radius - o1.y
##                intersections = True
                
            for o2 in kontrollimata:
                types = (type(o1), type(o2))

                if types == (Circle, Circle):
                    dx = o1.x - o2.x
                    dy = o1.y - o2.y
                    dist = dx**2 + dy**2 
                    penetration = (o1.radius + o2.radius)**2 - dist

                    # Ringid lõikuvad üle lubatud määra, tuleb eraldada
                    if penetration > 1e-10:
                        intersections = True
                        dist = sqrt(dist)
                        penetration = o1.radius + o2.radius - dist
                        dir1 = Vec2D(dx, dy) / dist
                        dir2 = -dir1
                        if dir1[0] == 0:
                            dir1 = Vec2D(1, dir1[1])
                            dir2 = Vec2D(-1, dir2[1])
                        if dir1[1] == 0:
                            dir1 = Vec2D(dir1[0], 1)
                            dir2 = Vec2D(dir2[0], -1)#dir1[1], -1)

                        mSum = penetration / (o1.m+o2.m)
                        o1.x, o1.y = o1.m * mSum * dir1 + (o1.x, o1.y)
                        o2.x, o2.y = o2.m * mSum * dir2 + (o2.x, o2.y)
                        if engine.debug:
                            print("fixedPenetration", o1.name, o2.name, penetration, o1.x, o1.y, o2.x, o2.y)

                elif types == (Circle, Wall) or types == (Wall, Circle):
                    c, w = (o1, o2) if types[0] == Circle else (o2, o1)
                    dist1 = cross2D(Vec2D(c.x - w.x1, c.y - w.y1) + w.normal * c.radius, w.lineVecDir)
                    dist2 = cross2D(Vec2D(c.x - w.x1, c.y - w.y1) - w.normal * c.radius, w.lineVecDir)

                    # Ring lõikub sirgega
                    if dist2 < 0 < dist1 or dist1 < 0 < dist2:

                        # Kontrollime, millisel pool joont ring asub ning
                        # lükkame ta tagasi selles suunas
                        if abs(dist1) < abs(dist2):
                            separateDir = -w.normal * dist1
                        elif abs(dist2) < abs(dist1):
                            separateDir = -w.normal * dist2
                        else:
                            separateDir = -c.getAcceleration().normalised()
                            
                        intersections = True
                        c.x, c.y = separateDir + (c.x, c.y)
                        if dot2D(separateDir, c.v) < 0:
                            # Kui ringil on veel pinnasuunaline kiirus,
                            # tekib koheselt põrge
                            for col in engine.collisions:
                                if (col.o1, col.o2) == (c,w) or (col.o1, col.o2) == (w,c):
                                    break
                            else:
                                col = Collision(engine, c, w)
                                col.normal = -separateDir.normalised()
                                col.time = 0
                                if col.time < engine.next_collision:
                                    engine.collisions = [col,]
                                    engine.next_collision = col.time
                                elif col.time == engine.next_collision:
                                    engine.collisions.append(col)
                        if engine.debug:
                            print("fixedPenetration", w.name, c.x, c.y, separateDir, dist1, dist2, w.normal)                    
                    

class Collision():
    collisionTable = {
        (Circle, Circle): "predict_circles",
        (Circle, Wall): "predict_circle_wall"
    }
    resolutionTable = {
        (Circle, Circle): "response_circles",
        (Circle, Wall): "response_circle_wall"
    }
    def __init__(self, engine, o1, o2, **attr):
        self.engine = engine
        self.o1 = o1
        self.o2 = o2
        self.to1 = type(o1)
        self.to2 = type(o2)

        #Porkeinfo
        self.time = float("inf")
        self.normal = None
        self.detection()

    def detection(self):
        collider12 = self.collisionTable.get((self.to1, self.to2))
        collider21 = self.collisionTable.get((self.to2, self.to1))
        col = None
        if collider12:
            col = getattr(self, collider12)(self.o1, self.o2)
        elif collider21:
            col = getattr(self, collider21)(self.o2, self.o1)

        if col != None:
            self.time, self.normal = col
    def response(self):
        resolver12 = self.resolutionTable.get((self.to1, self.to2))
        resolver21 = self.resolutionTable.get((self.to2, self.to1))

        if self.engine.debug:
            print("preCol", self.o1.name, self.o2.name, self.o1.v, self.o2.v,
                  self.o1.w, self.o2.w)
            
        if resolver12:
            getattr(self, resolver12)(self.o1, self.o2)
        elif resolver21:
            getattr(self, resolver21)(self.o2, self.o1)

        if self.engine.debug:
            print("postCol", self.o1.v, self.o2.v, self.o1.w, self.o2.w)
    
    def predict_circles(self, obj1, obj2):
        D_POS = Vec2D(obj1.x, obj1.y) - Vec2D(obj2.x, obj2.y)
        D_ACC = obj1.getAcceleration() - obj2.getAcceleration()
        D_VEL = obj1.v - obj2.v
        distance = D_POS.modulesq() - (obj1.radius + obj2.radius)**2
        step = self.engine.step
        if distance <= 0 and dot2D(D_POS, D_VEL) < 0:
            if self.engine.debug: print("CCINSTANT nc", self.engine.next_collision, obj1.name, obj2.name, distance, D_POS, D_VEL, dot2D(D_POS, D_VEL))
            return (0, D_POS)
        elif any(D_ACC) and self.engine.next_collision > 0:
            a = (D_ACC.modulesq() / 4) * step**4
            b = D_ACC.dotProduct(D_VEL) * step**3
            c = (D_VEL.modulesq() + D_ACC.dotProduct(D_POS)) * step**2
            d = 2 * D_VEL.dotProduct(D_POS) * step
            t = roots([a, b, c, d, distance])
        elif any(D_VEL) and self.engine.next_collision > 0:
            a = D_VEL
            b = 2 * D_POS
            b = b.dotProduct(a) * step
            a = a.modulesq() * step**2
            t = quadrat(a, b, distance)
        else:
            return None

        t = min_in_range(t, 0, self.engine.next_collision)
        if t == None or t == []:
            return

        ddp = obj1.delta_position(t) - obj2.delta_position(t) if t else (0,0)
        D_POS2 = D_POS + ddp
        confirmation = D_POS2.modulesq() - (obj1.radius + obj2.radius)**2
        dotProduct = D_POS2.dotProduct(D_VEL + D_ACC * t * step)
        if confirmation < .1 and dotProduct < 0:
            return (t, D_POS2)

    def predict_circle_wall(self, c, w):
        a = cross2D(c.getAcceleration() / 2, w.lineVecDir) * self.engine.step**2
        b = cross2D(c.v, w.lineVecDir) * self.engine.step
        
        bestT = self.engine.next_collision # Varaseim põrge mille leiame
        bestN = None # Varaseimale ajale vastav põrge
        for n in (w.normal, -w.normal):
            dist = cross2D(Vec2D(c.x - w.x1, c.y - w.y1) + n * c.radius, w.lineVecDir)
            dist2 = cross2D(Vec2D(c.x - w.x1, c.y - w.y1) - n * c.radius, w.lineVecDir)

            if dist == 0 or dist < 0 < dist2:
                dot_nv = dot2D(n, c.v)
                if dot_nv > 0 or dot2D(n, c.getAcceleration()) > 0:
                    c.contacts.add(n * c.radius + (c.x, c.y))
                    if dot_nv > 0:
                        return (0, n)
            elif bestT == 0:
                return None
            
            if a:
                t = min_in_range(quadrat(a,b,dist), 0, bestT)
                if t != None:
                    bestT = t
                    bestN = n
            elif b:
                t = -dist / b
                if 0 <= t <= bestT:
                    bestT = t
                    bestN = n

        # Kui leiti aeg ja ring liigub seina poole
        if bestN != None and dot2D(bestN, c.v + c.getAcceleration()*c.engine.step*bestT) > 0:
            return (bestT, bestN)
        
    def response_circles(self, obj1, obj2):
        D_VEL = obj1.v - obj2.v
        n = self.normal
        dotP = dot2D(n, D_VEL)
        n_norm = n.normalised()
        r1 = -n_norm*obj1.radius
        r2 =  n_norm*obj2.radius
        if dotP < 0:
            # Põrkenormaalisuunaline impulss
            e = (obj1.restitution + obj2.restitution) / 2
            jn = (-(1+e)*dotP) / (dot2D(n,n) * (1/obj1.m + 1/obj2.m))

            obj1.v += jn * n / obj1.m
            obj2.v -= jn * n / obj2.m

            # Põrketeljesuunaline impulss
##            t = (D_VEL - dotP * n).normalised()
##            df = dynamicFriction = (obj1.dynamicfriction + obj2.dynamicfriction) / 2
##
####            da = obj1.getAcceleration() - obj2.getAcceleration()
####            if dot2D(n, da.normalised()) < 1e-4:
####                return
##
##            v_ab = (obj1.v + cross2D(obj1.w, r1)) - (obj2.v + cross2D(obj2.w, r2))
##            j_angular = cross2D(r1, t)**2 / obj1.I + cross2D(r2, t)**2 / obj2.I
##            jt = (-dot2D(v_ab, t)) / (1/obj1.m + 1/obj2.m + j_angular)
##
##            mu = (obj1.staticfriction + obj2.staticfriction) / 2
##            # Clamp magnitude of friction and create impulse vector
##            if abs(jt) < jn * mu:
##                frictionImpulse = jt * t
##            else:
##                frictionImpulse = -jn * t * dynamicFriction
##
##            obj1.v += frictionImpulse / obj1.m
##            obj2.v -= frictionImpulse / obj2.m
##            obj1.w += cross2D(r1, frictionImpulse) / obj1.I #.perp()
##            obj2.w -= cross2D(r2, frictionImpulse) / obj2.I #.perp()
            
        elif self.engine.debug:
            print("False collision found {} {} {} {}".format(self.time, dotP, obj1.name, obj2.name))

        if dotP < 0 or dot2D(n, (obj1.getAcceleration() - obj2.getAcceleration())) <= 0:
            obj1.contacts.add(r1 + (obj1.x, obj1.y))
            obj2.contacts.add(r2 + (obj2.x, obj2.y))


    def response_circle_wall(self, c, w):
        dotP = dot2D(self.normal, c.v)
        r = self.normal*c.radius
        if dotP > 0:
            # Põrkenormaalisuunaline impulss
            e = (c.restitution + w.restitution) / 2
            j = -(1+e) * dotP * c.m

            c.v += j * self.normal / c.m

            # Põrketeljesuunaline impulss
##            t = (c.v - dotP * self.normal).normalised()
##            v_ab = c.v + cross2D(c.w, r)
##            j_angular = cross2D(r, t)**2 / c.I
##            jt = (- dot2D(v_ab, t)) / (1/c.m + j_angular)
##
##            df = dynamicFriction = (c.dynamicfriction + w.dynamicfriction) / 2
##            mu = (c.staticfriction + w.staticfriction) / 2
##            # Clamp magnitude of friction and create impulse vector
##            if abs(jt) < j * mu:
##                frictionImpulse = jt * t
##            else:
##                frictionImpulse = -j * t * dynamicFriction
##            
##            c.v -= frictionImpulse / c.m
##            c.w += cross2D(r, frictionImpulse) / c.I #.perp()            

        elif self.engine.debug:
            print("False collision found {} {} {} {}".format(self.time, dotP, obj1.name, obj2.name))
        if dotP > 0 or dot2D(self.normal, c.getAcceleration()) > 0:
            c.contacts.add(r + (c.x, c.y))
