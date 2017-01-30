#! /usr/bin/env python
# https://docs.python.org/3/library/argparse.html
import argparse
from collections import defaultdict # for income graph
import json
import math

import matplotlib as mil
mil.use('TkAgg') # add it before launching matplotlib
import matplotlib.pyplot as plt
# static method



class Agent:

    def __init__(self, position, **properties):
        self.position = position
        for property_name, property_value in properties.items():
            setattr(self, property_name, property_value)


class Position:

    def __init__(self, longitude_degrees, latitude_degrees):
        # We store the degree values, but we will be mostly using radians
        # because they are much more convenient for computation purposes.

        # assert : Lève une exception si renvoie False
        assert -180 <= longitude_degrees <= 180
        self.longitude_degrees = longitude_degrees

        assert -90 <= latitude_degrees <= 90
        self.latitude_degrees = latitude_degrees

    @property
    def longitude(self):
        """Longitude in radians"""
        return self.longitude_degrees * math.pi / 180

    @property
    def latitude(self):
        """Latitude in radians"""
        return self.latitude_degrees * math.pi / 180


class Zone:
    """
    A rectangular geographic area bounded by two corners. The corners can
    be top-left and bottom right, or top-right and bottom-left so you should be
    careful when computing the distances between them.
    """

    ZONES = []
    # The width and height of the zones that will be added to ZONES. Here, we
    # choose square zones but we could just as well use rectangular shapes.

    # Attributs de classe (constante si hors de la classe) car on fait 
    # cls.WIDTH_DEGREES
    MIN_LONGITUDE_DEGREES = -180
    MAX_LONGITUDE_DEGREES = 180
    MIN_LATITUDE_DEGREES = -90
    MAX_LATITUDE_DEGREES = 90
    WIDTH_DEGREES = 1 # degrees of longitude
    HEIGHT_DEGREES = 1 # degrees of latitude

    # S'il y a un attribut d'instance, il va dans __init__

    EARTH_RADIUS_KILOMETERS = 6371

    def __init__(self, corner1, corner2):
        self.corner1 = corner1
        self.corner2 = corner2
        self.inhabitants = []

    @property
    def population(self):
        """Number of inhabitants in the zone"""
        return len(self.inhabitants)

    @property
    def width(self):
        """Zone width, in kilometers"""
        # Note that here we access the class attribute via "self" and it
        # doesn't make any difference
        return abs(self.corner1.longitude - self.corner2.longitude) * self.EARTH_RADIUS_KILOMETERS

    @property
    def height(self):
        """Zone height, in kilometers"""
        # Note that here we access the class attribute via "self" and it
        # doesn't make any difference
        return abs(self.corner1.latitude - self.corner2.latitude) * self.EARTH_RADIUS_KILOMETERS

    def add_inhabitant(self, inhabitant):
        self.inhabitants.append(inhabitant)

    def population_density(self):
        """Population density of the zone, (people/km²)"""
        # Note that this will crash with a ZeroDivisionError if the zone has 0
        # area, but it should really not happen
        return self.population / self.area()

    def area(self):
        """Compute the zone area, in square kilometers"""
        return self.height * self.width

    def average_agreeableness(self):
        if not self.inhabitants:
            return 0
        return sum([inhabitant.agreeableness for inhabitant in self.inhabitants]) / self.population

    def contains(self, position):
        """Return True if the zone contains this position"""
        return position.longitude >= min(self.corner1.longitude, self.corner2.longitude) and \
            position.longitude < max(self.corner1.longitude, self.corner2.longitude) and \
            position.latitude >= min(self.corner1.latitude, self.corner2.latitude) and \
            position.latitude < max(self.corner1.latitude, self.corner2.latitude)

    @classmethod
    def find_zone_that_contains(cls, position):
        if not cls.ZONES:
            # Initialize zones automatically if necessary
            cls._initialize_zones()

        # Compute the index in the ZONES array that contains the given position
        longitude_index = int((position.longitude_degrees - cls.MIN_LONGITUDE_DEGREES)/ cls.WIDTH_DEGREES)
        latitude_index = int((position.latitude_degrees - cls.MIN_LATITUDE_DEGREES)/ cls.HEIGHT_DEGREES)
        longitude_bins = int((cls.MAX_LONGITUDE_DEGREES - cls.MIN_LONGITUDE_DEGREES) / cls.WIDTH_DEGREES) # 180-(-180) / 1
        zone_index = latitude_index * longitude_bins + longitude_index

        # Just checking that the index is correct
        zone = cls.ZONES[zone_index]
        assert zone.contains(position)

        return zone

    @classmethod
    def _initialize_zones(cls):
        # Note that this method is "private": we prefix the method name with "_".
        cls.ZONES = []
        for latitude in range(cls.MIN_LATITUDE_DEGREES, cls.MAX_LATITUDE_DEGREES, cls.HEIGHT_DEGREES):
            for longitude in range(cls.MIN_LONGITUDE_DEGREES, cls.MAX_LONGITUDE_DEGREES, cls.WIDTH_DEGREES):
                bottom_left_corner = Position(longitude, latitude)
                top_right_corner = Position(longitude + cls.WIDTH_DEGREES, latitude + cls.HEIGHT_DEGREES)
                zone = Zone(bottom_left_corner, top_right_corner)
                cls.ZONES.append(zone)

# () ne se fait pas trop.
# Ceci est un mixin ?
class BaseGraph:

    def __init__(self):
        self.show_grid = True

        self.title = "Your graph title"
        self.x_label = "X-axis label"
        self.y_label = "X-axis label"

    def show(self, zones):
        x_values, y_values = self.xy_values(zones)
        self.plot(x_values, y_values)

        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.grid(self.show_grid)
        plt.show()

    def plot(self, x_values, y_values):
        """Override this method to create different kinds of graphs, such as histograms"""
        # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot
        plt.plot(x_values, y_values, '.')

    def xy_values(self, zones):
        """
        Returns:
            x_values
            y_values
        """
        # You should implement this method in your children classes
        raise NotImplementedError


class AgreeablenessGraph(BaseGraph):
    # Inheritance, yay!

    def __init__(self):
        # Call base constructor
        super(AgreeablenessGraph, self).__init__()

        self.title = "Nice people live in the countryside"
        self.x_label = "population density"
        self.y_label = "agreeableness"

    def xy_values(self, zones):
        x_values = [zone.population_density() for zone in zones]
        y_values = [zone.average_agreeableness() for zone in zones]
        return x_values, y_values

class IncomeGraph(BaseGraph):
    # Inheritance, yay!

    def __init__(self):
        # Call base constructor
        super(IncomeGraph, self).__init__()

        self.title = "Older people have more money"
        self.x_label = "age"
        self.y_label = "income"

    def xy_values(self, zones):
        income_by_age = defaultdict(float)
        population_by_age = defaultdict(int)
        for zone in zones:
            for inhabitant in zone.inhabitants:
                income_by_age[inhabitant.age] += inhabitant.income
                population_by_age[inhabitant.age] += 1

        x_values = range(0, 100)
        # list comprehension (listcomps)
        y_values = [income_by_age[age] / (population_by_age[age] or 1) for age in range(0, 100)]
        return x_values, y_values


def main():
    # Si on avait mis tout ça en bas, on aurait eu beaucoup de variables globales.
    parser = argparse.ArgumentParser("Display population stats")
    parser.add_argument("src", help="Path to source json agents file")
    args = parser.parse_args()

    # Load agents
    for agent_properties in json.load(open(args.src)):
        longitude = agent_properties.pop('longitude')
        latitude = agent_properties.pop('latitude')
        # store agent position in radians
        position = Position(longitude, latitude)

        zone = Zone.find_zone_that_contains(position)
        agent = Agent(position, **agent_properties)
        zone.add_inhabitant(agent)

    agreeableness_graph = AgreeablenessGraph()
    agreeableness_graph.show(Zone.ZONES)

    income_graph = IncomeGraph()
    income_graph.show(Zone.ZONES)

if __name__ == "__main__":
    main()
