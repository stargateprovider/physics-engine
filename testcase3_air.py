from engine import *

width = 224
height = 400
engine = Engine(width, height, gravity=Vec2D(0,10), velBoundary=.00001, time_step=.01, coef_drag = 0.00027, bgcolor=(0,0,0))
#engine.debug=True

##engine.addCircle(radius=1, x=width//2-1/sqrt(2), y=height//2+1/sqrt(2), v=Vec2D(1,-1), w=15, m=7, name="r1m7", color=(150,0,150))
##engine.addCircle(radius=9, x=width//2, y=height//2-30, v=Vec2D(19,0), w=15, m=10, name="r9m10", color=(150,0,150))
engine.addCircle(radius=20, x=width//2, y=0, v=Vec2D(-1.11,3.33), w=2, m=19, name="r20m19", restitution=1)
engine.addCircle(radius=8, x=13, y=90, v=Vec2D(.9,4), w=-55, m=.4, name="r20m19", restitution=1)

engine.addWall(width, height, width, 0, name="wallE")
engine.addWall(0, 0, 0, height, name="wallW")
engine.addWall(width, height, 0, height, name="wallS")
engine.addWall(0, 0, width, 0, name="wallN")
#engine.addWall(0,0, width, height, name="wallDiagonal")
#engine.addWall(0, height-2, width, height-20, name="wallDiagonal")

engine.start()
