from engine import *

width = 600
height = 450
engine = Engine(width, height, gravity=Vec2D(0,10), velBoundary=.00001, time_step=.1, bgcolor=(0,0,0))
#engine.debug=True

engine.addCircle(radius=1, x=width//2-1/sqrt(2), y=height//2+1/sqrt(2), v=Vec2D(1,-1), w=15, m=7, name="r1m7", color=(150,0,150))
engine.addCircle(radius=9, x=width//2, y=height//2-30, v=Vec2D(19,0), w=15, m=10, name="r9m10", color=(150,0,150))
engine.addCircle(radius=20, x=width//2-150, y=height//2+150, v=Vec2D(-1.11,3.33), w=2, m=19, name="r20m19", color=(0,150,150))
engine.addCircle(radius=8, x=13, y=90, v=Vec2D(6,4), w=-55, m=4, name="r20m19", color=(0,150,150))

engine.addWall(width, height, width, 0, name="wallE")
engine.addWall(0, 0, 0, height, name="wallW")
engine.addWall(width, height, 0, height, name="wallS")
engine.addWall(0, 0, width, 0, name="wallN")
#engine.addWall(0,0, width, height, name="wallDiagonal")
#engine.addWall(0, height-2, width, height-20, name="wallDiagonal")


# # # # Tunneling objects: # # # #
##engine.addCircle(radius=9, x=33, y=100, v=Vec2D(21.20,0), m=30, name="r9m30")
##engine.addCircle(radius=8, x=255, y=90, v=Vec2D(-33,0), m=11, name="r8m11")
##engine.addCircle(radius=7, x=255, y=120, v=Vec2D(-33,0), m=11, name="r7m11")

##engine.addCircle(radius=11, x=35, y=90, v=Vec2D(10000,0), m=5, name="r11")
##engine.addCircle(radius=4, x=35, y=180, v=Vec2D(10000,0), m=5, name="r4")

##smallA=engine.addCircle(radius=4, x=width-8, y=height-8, v=Vec2D(.5,.5), a=Vec2D(3,4), m=3, color=(0,255,0),name="sa")
##smallB=engine.addCircle(radius=4, x=20, y=20, v=-Vec2D(.5,.5), m=3, a=Vec2D(-3.33,2), name="sb")
##smallC=engine.addCircle(radius=4, x=36, y=height-36, v=Vec2D(-1,1), m=3, name="sc")

##bigA=engine.addCircle(radius=9, x=width, y=height-55.5, v=Vec2D(0,5), m=3, name="ba")
##bigB=engine.addCircle(radius=9, x=0, y=90, v=Vec2D(0,.5), m=3, name="bb",color=(125,125,125))
##bigC=engine.addCircle(radius=9, x=155, y=60, v=Vec2D(9,0), m=3, color=(0,0,255),name="bc") ###Sinine
##
##smalld=engine.addCircle(radius=4, x=width-8-2/3, y=height//2-4.5, v=Vec2D(.5,0), m=3, color=(0,125,125),name="sd")
##smalle=engine.addCircle(radius=4, x=width-8-2/3, y=height//2+3.5, v=Vec2D(.5,0), m=3, color=(125,125,0),name="se")
##smallf=engine.addCircle(radius=4, x=width-8-2/3, y=height//2-16.5, v=Vec2D(.5,.5), m=3, color=(125,0,125),name="sf")
##smallg=engine.addCircle(radius=4, x=width-8-2/3, y=height//2+15, v=Vec2D(.5,-.5), m=3, color=(0,125,0),name="sg")
##bigd=engine.addCircle(radius=9, x=width-55.5, y=height/2, v=Vec2D(5,0), m=3, name="bd")

##simultanious:
engine.addCircle(radius=9, x=width//2, y=50, v=Vec2D(0,5), m=10, w=33.3, name="r9m10",color=(0,125,125))
engine.addCircle(radius=9, x=width//2, y=150, v=Vec2D(0,-5), m=10, name="r9m1",color=(125,125,0))
engine.addCircle(radius=9, x=width//2-50, y=100, v=Vec2D(5,0), m=.5, name="r9m.5",color=(125,0,125))
engine.addCircle(radius=9, x=width//2+50, y=100, v=Vec2D(-5,0), m=9, name="r9m9",color=(0,125,0))
engine.addCircle(radius=20, x=width//2, y=100, v=Vec2D(0,0), m=3, w=99, name="r20m3")
engine.addCircle(radius=10, x=width//2, y=22, v=Vec2D(0,-1), m=10, name="r10m10")
engine.addCircle(radius=10, x=width//2-9, y=32, v=Vec2D(0,-1), w=9, m=10, name="r10m10a")
engine.addCircle(radius=19, x=46, y=height-19, v=Vec2D(5,0), m=9, w=30,name="r19m9",color=(0,125,0))
engine.addCircle(radius=9, x=69, y=height-50, v=Vec2D(0,2), m=15, w=12, name="r9m15",color=(0,125,0))

##for x in range(20, width-18, 41):
##    engine.addCircle(radius=20, x=x, y=height-x, v=Vec2D(0,0), m=90, w=30, name="r19m9",color=(0,125,0))
##engine.addCircle(radius=15, x=105, y=height-80, v=Vec2D(-1.11,0), w=0, m=19, name="r20m19", color=(0,150,150))

engine.start()
