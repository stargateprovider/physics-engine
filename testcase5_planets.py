from engine import *

width = 650
height = 500
engine = Engine(width, height, gravity=Vec2D(0,0), velBoundary=.00001, time_step=.1, bgcolor=(0,0,0), pathLimit=100)
#engine.debug=True

engine.addCircle(radius=9, x=width//2, y=height//2, v=Vec2D(0,0), w=15, m=10e13, name="r9m10e13", color=(150,0,150))
engine.addCircle(radius=15, x=width//2-50, y=height//2, v=Vec2D(0,10), w=2, m=10e3, name="r15m10e3", color=(150,150,0))
engine.addCircle(radius=8, x=13, y=90, v=Vec2D(0,0), w=0, m=10e4, name="r8m10e4", color=(0,150,150))

engine.addWall(width, height, 0, height, name="wallS")

##for x in range(20, width-18, 41):
##    engine.addCircle(radius=20, x=x, y=height-x, v=Vec2D(0,0), m=90, w=30, name="r19m9",color=(0,125,0))

engine.start()
