from engine import *

width = 580
height = 300
engine = Engine(width, height, gravity=Vec2D(0,0), velBoundary=.00001, time_step=.1, bgcolor=(230,230,230), pathLimit=1000)
#engine.debug=True

engine.addCircle(radius=11, x=30, y=50, v=Vec2D(3,5), m=10, name="r9m10e13", color=(0,150,150))
engine.addCircle(radius=11, x=330, y=50, v=Vec2D(3,3), const_a=Vec2D(0,.1), m=5, name="r15m10e3", color=(150,150,0))
engine.addWall(width, height, 0, height, name="wallS")

##for x in range(20, width-18, 41):
##    engine.addCircle(radius=20, x=x, y=height-x, v=Vec2D(0,0), m=90, w=30, name="r19m9",color=(0,125,0))

engine.start()
