import math

class Zone():

    @classmethod
    def calculate_height(self, y1, y2):
        return (y1 - y2)*40000/360
 
    @classmethod
    def calculate_width(self, x1, x2, y1, y2):
        # see here: http://stackoverflow.com/questions/24617013/convert-latitude-and-longitude-to-x-and-y-grid-system-using-python
        return (x2 - x1)*40000*math.cos((y1+y2)*math.pi/360)/360
    
    def __init__(self, x1, x2, y1, y2, inhabitants):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.height = Zone.calculate_height(y1, y2)
        self.width = Zone.calculate_width(x1, x2, y1, y2)
        self.inhabitants = inhabitants

    @property
    def latitude(self):
        return (self.x1, self.x2)

    @property
    def longitude(self):
        return (self.y1, self.y2)

    @property
    def sqkm(self):
        return self.height * self.width

    @property
    def pop_density(self):
        return self.inhabitants / self.sqkm

    
# DEBUG #
#zone = Zone(170, 171, -39, -40, 4000)
#print(zone.pop_density)
#print("latitude: ", zone.latitude)
#print("longitude: ", zone.longitude)
#print("width: ", zone.width)
#print("height: ", zone.height)
#print("sqkm:", zone.sqkm)
