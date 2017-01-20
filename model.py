import json
from grid import Grid
from agent import Agent

class Model():
    """Class used to manipulate data
    Will store people's agreebleness and density in a zone.
    """

    def __init__(self):
        # new grid
        grid = Grid()
        # new zones
        zones = grid.zones
        # agents in this grid
        people = self.create_agents_from_json()

        # place agents on grid
        for zone in grid.zones:
            zone.register_new_inhabitants(people)
            print("inhabitants:", zone.inhabitants, "pop density:", zone.pop_density, "agree:", zone.avg_agreeableness)


        # make graph on browser
      
    # Create agents from a JSON file
    def create_agents_from_json(self):
        with open("agents.json") as f:
            agents = []
            data = json.load(f)
            for entry in data:
                agent = Agent(agreeableness = entry['agreeableness'], location = entry['country_tld'], latitude = entry['latitude'], longitude = entry['longitude']) 
                agents.append(agent)
            return agents



Model()

