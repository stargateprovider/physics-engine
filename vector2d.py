import math

# Kohandatud Pythoni turtle mooduli vektorklass
class Vec2D(tuple):
    """
    Provides (for a, b vectors, k number):
       a+b vector addition
       a-b vector subtraction
       a*b inner product
       k*a and a*k multiplication with scalar
       |a| absolute value of a
       a.rotate(angle) rotation
    """
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))
    def __bool__(self):
        return self[0] or self[1]
    def __add__(self, other):
        return Vec2D(self[0]+other[0], self[1]+other[1])
    def __mul__(self, other):
        #if isinstance(other, Vec2D):
        if hasattr(other, "__iter__") and len(other) >= 2:
            return self[0]*other[0] + self[1]*other[1] # Dotproduct
        return Vec2D(self[0]*other, self[1]*other)
    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2D(self[0]*other, self[1]*other)
    def __sub__(self, other):
        return Vec2D(self[0]-other[0], self[1]-other[1])
    def __neg__(self):
        return Vec2D(-self[0], -self[1])
    def __abs__(self):
        return math.sqrt(self[0]**2 + self[1]**2)
    def rotate(self, angle, c=None, s=None):
        """rotate self counterclockwise by angle
        """
        perp = Vec2D(-self[1], self[0])
        angle = angle * math.pi / 180.0
        if c == None: c = math.cos(angle)
        if s == None: s = math.sin(angle)
        return Vec2D(self[0]*c + perp[0]*s, self[1]*c + perp[1]*s)
    def perp(self, clockwise = True):
        """return perpendicular vector""" #Fixed
        return Vec2D(self[1], -self[0]) if clockwise else Vec2D(-self[1], self[0])
    def __getnewargs__(self):
        return (self[0], self[1])
##    def __repr__(self):
##        return "(%.2f,%.2f)" % self

    def __truediv__(self, other):
        #if isinstance(other, (Vec2D, tuple, list)):
        if hasattr(other, "__iter__") and len(other) >= 2:
            return Vec2D(self[0]/other[0] if other[0] else 0,
                                self[1]/other[1] if other[1] else 0)
        return Vec2D(self[0]/other, self[1]/other)

    def crossProduct(self, other):
        return self[0] * other[1] - self[1] * other[0]

    def dotProduct(self, other):
        return self[0] * other[0] + self[1] * other[1]

    def modulesq(self):
        return self[0]**2 + self[1]**2
    
    def normalised(self):
        length = self.__abs__()
        if length != 0:
            return self/length
        return Vec2D(0,0)

def dot2D(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]
def cross2D(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]


# Two crossed vectors return a scalar
def cross2D(a, b):
    if hasattr(a, "__iter__") and len(a) == 2:
        if hasattr(b, "__iter__") and len(b) == 2: 
            return a[0] * b[1] - a[1] * b[0]
        elif isinstance(b, (float, int)):
            return Vec2D(-b * a[1], b * a[0])
        
    elif isinstance(a, (float, int)):
        if hasattr(b, "__iter__") and len(b) == 2: 
            return Vec2D(-a * b[1], a * b[0])

    return a*b
