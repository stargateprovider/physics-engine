from engine import *

width = 90
height = 100
engine = Engine(width, height, gravity=Vec2D(0,10), velBoundary=.0001, time_step=.1, bgcolor=(0,0,0))
#engine.debug=True

##engine.addCircle(radius=1, x=width//2-1/sqrt(2), y=height//2+1/sqrt(2), v=Vec2D(1,-1), w=15, m=7, name="r1m7", color=(150,0,150))
##engine.addCircle(radius=9, x=width//2, y=height//2-30, v=Vec2D(19,0), w=15, m=10, name="r9m10", color=(150,0,150))
##engine.addCircle(radius=20, x=width//2-150, y=height//2+150, v=Vec2D(-1.11,3.33), w=2, m=19, name="r20m19", color=(0,150,150))
##engine.addCircle(radius=8, x=13, y=90, v=Vec2D(6,4), w=-55, m=4, name="r20m19", color=(0,150,150))

engine.addWall(width, height, width, 0, name="wallE")
engine.addWall(0, 0, 0, height, name="wallW")
engine.addWall(width, height, 0, height, name="wallS")
engine.addWall(0, 0, width, 0, name="wallN")
#engine.addWall(0,0, width, height, name="wallDiagonal")
#engine.addWall(0, height-2, width, height-20, name="wallDiagonal")

##engine.addCircle(radius=19, x=46, y=height-19, v=Vec2D(5,0), m=9, w=30,name="r19m9",color=(0,125,0))
##engine.addCircle(radius=9, x=width//2, y=110, v=Vec2D(0,2), m=15, w=12, name="r9m15",color=(0,125,0))

for x in range(20, width-18, 41):
    engine.addCircle(radius=20, x=x, y=height, v=Vec2D(0,0), m=90, w=.1, name="r19m9",color=(0,125,0))
#engine.addCircle(radius=15, x=105, y=height-80, v=Vec2D(-1.11,0), w=0, m=19, name="r20m19", color=(0,150,150))

engine.start()
