def clamp(lower_clamp, value, higher_clamp):
    if value <= lower_clamp :
        return lower_clamp
    if value >= higher_clamp :
        return higher_clamp
    return value

class Color:
    
    def int_clamp(self,value):
        return int(clamp(self.lower_clamp,value,self.higher_clamp))
    
    def __init__(self,_r,_g,_b):
        self.lower_clamp = 0
        self.higher_clamp = 255
        self.r = _r
        self.g = _g
        self.b = _b
    
    def scale(self, factor):
        return Color(
            self.int_clamp(self.r*factor),
            self.int_clamp(self.g*factor),
            self.int_clamp(self.b*factor),
            )
    
    def as_tuple(self):
        return (self.r,self.g,self.b)
    
def from_hsv(h,s,v):
    '''
    h angle in degrees
    s saturation of color
    v value of intensity
    '''
    c = v * s
    x = c * (1- abs(((h/60)%2)-1))
    m = v - c
    h = h % 360
    if 0 <= h and h < 60:
        (r2,g2,b2) = (c,x,0)
    if 60 <= h and h < 120:
        (r2,g2,b2) = (x,c,0)
    if 120 <= h and h < 180:
        (r2,g2,b2) = (0,c,x)
    if 180 <= h and h < 240:
        (r2,g2,b2) = (0,x,c)
    if 240 <= h and h < 300:
        (r2,g2,b2) = (x,0,c)
    if 300 <= h and h < 360:
        (r2,g2,b2) = (c,0,x)
    (r,g,b) = ((r2+m)*255,(g2+m)*255,(b2+m)*255)
    return Color(int(r),int(g),int(b))
