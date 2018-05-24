from math import sqrt
from engine import *

space_v1 = sqrt((6.674e-11*10e13)/abs(Vec2D(0, -100))) * Vec2D(1,0)
space_v2 = sqrt((6.674e-11*10e13)/abs(Vec2D(0, -200))) * Vec2D(1,0)

list_N1 = []
list_N2 = []
list_balance = []

for x in range(42, 332//2-19, 82):
    list_N1.append({"type":Circle, "radius":20*2, "x":x, "y":200-44, "v":Vec2D(0,0), "m":90, "name":"r19m9", "color":(0,125,0), "restitution":.5})
for x in range(332//2+42, 332-18, 82):
    list_N1.append({"type":Circle, "radius":20*2, "x":x, "y":200-42, "v":Vec2D(0,0), "m":90, "name":"r19m9", "color":(0,125,0), "restitution":.5})
list_N1.extend([
    {"type":Wall, "x1":332, "y1":200, "x2":332, "y2":0, "name":"wallE", "restitution":.5},
    {"type":Wall, "x1":0, "y1":0, "x2":0, "y2":200, "name":"wallW", "restitution":.5},
    {"type":Wall, "x1":332//2, "y1":0, "x2":332//2, "y2":200, "name":"Separator", "color":(0,0,0)},
    {"type":Wall, "x1":332, "y1":200, "x2":0, "y2":200, "name":"wallS", "restitution":.5},
    {"type":Wall, "x1":0, "y1":0, "x2":332, "y2":0, "name":"wallN"},
    {"type":Circle, "radius":10*2, "x":3*332//4, "y":55, "v":Vec2D(0,0), "m":15, "w":12, "name":"r9m15", "color":(200,0,0), "restitution":.5}
])

for x in range(20, 224-18, 41):
    list_N2.append({"type":Circle, "radius":20, "x":x, "y":380, "v":Vec2D(0,0), "m":90, "name":"r19m9","color":(0,125,0), "restitution":.75})
list_N2.extend([
    {"type":Wall, "x1":224, "y1":400, "x2":224, "y2":0, "name":"wallE"},
    {"type":Wall, "x1":0, "y1":0, "x2":0, "y2":400, "name":"wallW"},
    {"type":Wall, "x1":224, "y1":400, "x2":0, "y2":400, "name":"wallS"},
    {"type":Wall, "x1":0, "y1":0, "x2":224, "y2":0, "name":"wallN"},
    {"type":Circle, "radius":9, "x":69, "y":400-65, "v":Vec2D(0,2), "m":15, "name":"r9m15", "color":(0,125,0), "restitution":.75}
])

for x in range(20, 90-18, 41):
    list_balance.append({"type":Circle, "radius":20, "x":x, "y":100-21, "v":Vec2D(0,0), "m":90, "name":"r19m9","color":(0,125,0), "restitution":.5})
list_balance.extend([
    {"type":Wall, "x1":90, "y1":100, "x2":90, "y2":0, "name":"wallE"},
    {"type":Wall, "x1":0, "y1":0, "x2":0, "y2":100, "name":"wallW"},
    {"type":Wall, "x1":90, "y1":100, "x2":0, "y2":100, "name":"wallS"},
    {"type":Wall, "x1":0, "y1":0, "x2":90, "y2":0, "name":"wallN"},
])

#Tõmbejõud 2 jaoks:
up = Vec2D(0, -1).normalised()
var = 6.674e-11*20e15
v = sqrt(var/abs(Vec2D(148, 0))) * up - sqrt((6.674e-11*10e6)/abs(Vec2D(15, 0))) * up


demoBodies = {
    "Kiirus": (
{"type":Circle, "radius":1, "x":600//2-1/sqrt(2), "y":450//2+1/sqrt(2), "v":Vec2D(1,-1), "w":15, "m":7, "name":"r1m7", "color":(150,0,150), "fill":True},
{"type":Circle, "radius":9, "x":600//2, "y":450//2-30, "v":Vec2D(19,0), "w":15, "m":10, "name":"r9m10", "color":(150,0,150), "fill":True},
{"type":Circle, "radius":20, "x":600//2-150, "y":450//2+150, "v":Vec2D(-1.11,3.33), "w":2, "m":19, "name":"r20m19", "color":(0,150,150), "fill":True},
{"type":Circle, "radius":8, "x":13, "y":90, "v":Vec2D(6,4), "w":-55, "m":4, "name":"r20m19", "color":(0,150,150), "fill":True},
{"type":Wall, "x1":600, "y1":450, "x2":600, "y2":0, "name":"wallE"},
{"type":Wall, "x1":0, "y1":0, "x2":0, "y2":450, "name":"wallW", "color":(0,0,0)},
{"type":Wall, "x1":600, "y1":450, "x2":0, "y2":450, "name":"wallS"},
{"type":Wall, "x1":0, "y1":0, "x2":600, "y2":0, "name":"wallN", "color":(0,0,0)},
{"type":Circle, "radius":4, "x":600-8, "y":450-8, "v":Vec2D(.5,.5), "a":Vec2D(3,4), "m":3, "color":(0,255,0),"name":"sa", "fill":True},
{"type":Circle, "radius":4, "x":20, "y":20, "v":-Vec2D(.5,.5), "m":3, "a":Vec2D(-3.33,2), "name":"sb", "fill":True},
{"type":Circle, "radius":4, "x":36, "y":450-36, "v":Vec2D(-1,1), "m":3, "name":"sc", "fill":True},
{"type":Circle, "radius":9, "x":600//2, "y":50, "v":Vec2D(0,5), "m":10, "w":33.3, "name":"r9m10","color":(0,125,125), "fill":True},
{"type":Circle, "radius":9, "x":600//2, "y":150, "v":Vec2D(0,-5), "m":10, "name":"r9m1","color":(125,125,0), "fill":True},
{"type":Circle, "radius":9, "x":600//2-50, "y":100, "v":Vec2D(5,0), "m":.5, "name":"r9m.5","color":(125,0,125), "fill":True},
{"type":Circle, "radius":9, "x":600//2+50, "y":100, "v":Vec2D(-5,0), "m":9, "name":"r9m9","color":(0,125,0), "fill":True},
{"type":Circle, "radius":20, "x":600//2, "y":100, "v":Vec2D(0,0), "m":3, "w":99, "name":"r20m3", "fill":True},
{"type":Circle, "radius":10, "x":600//2, "y":22, "v":Vec2D(0,-1), "m":10, "name":"r10m10", "fill":True},
{"type":Circle, "radius":10, "x":600//2-9, "y":32, "v":Vec2D(0,-1), "w":9, "m":10, "name":"r10m10a", "fill":True},
{"type":Circle, "radius":19, "x":46, "y":450-19, "v":Vec2D(5,0), "m":9, "w":30,"name":"r19m9","color":(0,125,0), "fill":True},
{"type":Circle, "radius":9, "x":69, "y":450-50, "v":Vec2D(0,2), "m":15, "w":12, "name":"r9m15","color":(0,125,0), "fill":True}
),
    "Toereaktsioon 1": list_N1,
    "Toereaktsioon 2": list_N2,
    "Tasakaal": list_balance,
    "Tõmbejõud": (
{"type":Circle, "radius":9, "x":1024//2, "y":768//2, "v":Vec2D(0,0), "w":15, "m":10e13, "name":"r9m10e13", "color":(150,0,150), "fill":True},
{"type":Circle, "radius":15, "x":1024//2-50, "y":768//2, "v":Vec2D(0,10), "w":2, "m":10e3, "name":"r15m10e3", "color":(150,150,0)},
{"type":Circle, "radius":8, "x":13*17.5, "y":90*2.7, "v":Vec2D(0,0), "w":0, "m":10e4, "name":"r8m10e4", "color":(0,150,150)},
{"type":Circle, "radius":8, "x":1024//2, "y":768//2+100, "v":space_v1, "m":10e4, "name":"r8m10e4", "color":(150,150,150)},
{"type":Circle, "radius":5, "x":1024//2, "y":768//2+200, "v":space_v2, "m":10e3, "name":"r8m10e4", "color":(150,150,150)}
),
    "Tõmbejõud 2": (
{"type":Circle,"radius":11, "x":900//2, "y":660//2, "v":Vec2D(0,0), "m":20e15},
{"type":Circle,"radius":4, "x":900//2-50, "y":660//2, "v":sqrt(var/abs(Vec2D(50, 0))) * up, "m":10e4, "color":(150,150,0)},
{"type":Circle,"radius":5, "x":900//2-100, "y":660//2, "v":sqrt(var/abs(Vec2D(100, 0))) * up, "m":10e6,"color":(0,150,0)},
{"type":Circle,"radius":3, "x":900//2-200, "y":660//2, "v":sqrt(var/abs(Vec2D(200, 0))) * up, "m":10e6,"color":(0,150,150)},
{"type":Circle,"radius":3, "x":900//2-133, "y":660//2, "v":sqrt(var/abs(Vec2D(133, 0))) * up, "m":10e6},
{"type":Circle,"radius":3, "x":900//2-148, "y":660//2, "v":v, "m":10e1, "color":(150,0,150)}
),
    "Õhutakistus": (
{"type":Circle, "radius":8, "x":13, "y":90, "v":Vec2D(.9,4), "w":-55, "m":.4, "name":"r20m19", "restitution":.5, "fill":True},
{"type":Wall, "x1":224, "y1":400, "x2":224, "y2":0, "name":"wallE"},
{"type":Wall, "x1":0, "y1":0, "x2":0, "y2":400, "name":"wallW"},
{"type":Wall, "x1":224, "y1":400, "x2":0, "y2":400, "name":"wallS"},
{"type":Wall, "x1":0, "y1":0, "x2":224, "y2":0, "name":"wallN"}
),
}


demoSettings = {
    "Kiirus":
    {
        "width":        600,
        "height":       450,
        "g":            Vec2D(0,0),
        "vBoundary":    .00001,
        "step":         .5,
        "fpsLimit":     120,
        "bgcolor":      (0,0,0),
    },
    "Toereaktsioon 1":
    {
        "width":        332,
        "height":       200,
        "g":            Vec2D(0,10),
        "vBoundary":    .001,
        "step":         .01,
        "bgcolor":      (230,230,230)
    },
    "Toereaktsioon 2":
    {
        "width":        224,
        "height":       400,
        "g":            Vec2D(0,10),
        "vBoundary":    .00001,
        "step":         .1,
        "bgcolor":      (0,0,0)
    },
    "Tasakaal":
    {
        "width":        90,
        "height":       100,
        "g":            Vec2D(0,10),
        "vBoundary":    .0001,
        "step":         .1,
        "bgcolor":      (0,0,0)
    },
    "Tõmbejõud":
    {
        "width":        1024,
        "height":       768,
        "g":            Vec2D(0,0),
        "vBoundary":    .00001,
        "step":         .1,
        "bgcolor":      (0,0,0),
        "pathLimit":    100
    },
    "Tõmbejõud 2":
    {
        "width":        900,
        "height":       660,
        "g":            Vec2D(0,0),
        "vBoundary":    .00001,
        "step":         .1,
        "bgcolor":      (0,0,0),
        "pathLimit":    200
    },
    "Õhutakistus":
    {
        "width":        224,
        "height":       400,
        "g":            Vec2D(0,10),
        "vBoundary":    .0001,
        "step":         .01,
        "coef_drag":    0.00027,
        "bgcolor":      (0,0,0)
    },
}

demoBodies["Kiirendus"] = demoBodies["Kiirus"]
demoSettings["Kiirendus"] = dict(demoSettings["Kiirus"])
demoSettings["Kiirendus"]["g"] = Vec2D(0, 9.8)


def demo(engine, key):
    for k, v in demoSettings[key].items():
        setattr(engine, k, v)
    engine.screen = pygame.display.set_mode(
            (demoSettings[key]["width"], demoSettings[key]["height"]), RESIZABLE)
    for body in demoBodies[key]:
        attr = dict(body)
        typ = attr.pop("type")
        if typ == Circle:
            pos = (attr.pop("radius"), attr.pop("x"), attr.pop("y"))
            engine.addCircle(*pos, **attr)
        elif typ == Wall:
            pos = (attr.pop("x1"), attr.pop("y1"), attr.pop("x2"), attr.pop("y2"))
            engine.addWall(*pos, **attr)
