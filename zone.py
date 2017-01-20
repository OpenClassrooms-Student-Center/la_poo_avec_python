import math

class Zone():

    inhabitants = 0
    avg_agreeableness = 0

    @classmethod
    def calculate_height(cls, y1, y2):
        # I think this is wrong because I need to add a minus sign before to get a positive result.
        return - (y1 - y2)*40000/360
 
    @classmethod
    def calculate_width(cls, x1, x2, y1, y2):
        # see here: http://stackoverflow.com/questions/24617013/convert-latitude-and-longitude-to-x-and-y-grid-system-using-python
        return (x2 - x1)*40000*math.cos((y1+y2)*math.pi/360)/360
    
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.height = Zone.calculate_height(y1, y2)
        self.width = Zone.calculate_width(x1, x2, y1, y2)

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

    def register_new_inhabitants(self, agents):
        x_range = range(int(self.latitude[0]), int(self.latitude[1]))
        y_range = range(int(self.longitude[0]), int(self.longitude[1]))

        in_zone = []
        for agent in agents:
            #print("FOUND AGENT! latitude", agent.latitude)
            if int(agent.latitude) in x_range:
                in_zone.append(agent)
                self.inhabitants += 1

            if int(agent.longitude) in y_range:
                if agent not in in_zone:
                    in_zone.append(agent)
                    self.inhabitants +=1

        self.avg_agreeableness = self.calc_avg_agreeableness(in_zone)

    @classmethod
    def average(self, l):
        if len(l) > 0:
            return sum(l) / float(len(l))
        else:
            return 0

    def calc_avg_agreeableness(self, people):    
        agreeableness_list = [agent.agreeableness for agent in people]
        return Zone.average(agreeableness_list)


