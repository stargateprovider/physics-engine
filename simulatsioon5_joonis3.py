from engine import *

width = 166*2
height = 100*2
engine = Engine(width, height, gravity=Vec2D(0,10), velBoundary=.001, time_step=.01, bgcolor=(230,230,230))
#engine.debug=True

engine.addWall(width, height, width, 0, name="wallE", restitution=.5)
engine.addWall(0, 0, 0, height, name="wallW", restitution=.5)

engine.addWall(width//2, 0, width//2, height, name="wallW")

engine.addWall(width, height, 0, height, name="wallS", restitution=.5)
engine.addWall(0, 0, width, 0, name="wallN")
#engine.addWall(0,0, width, height, name="wallDiagonal")

engine.addCircle(radius=10*2, x=3*width//4, y=55, v=Vec2D(0,0), m=15, w=12, name="r9m15",color=(200,0,0), restitution=.5)

for x in range(21*2, width//2-19, 41*2):
    engine.addCircle(radius=20*2, x=x, y=height-22*2, v=Vec2D(0,0), m=90, w=30, name="r19m9",color=(0,125,0), restitution=.5)
for x in range(width//2+21*2, width-18, 41*2):
    engine.addCircle(radius=20*2, x=x, y=height-21*2, v=Vec2D(0,0), m=90, w=30, name="r19m9",color=(0,125,0), restitution=.5)

engine.start()
