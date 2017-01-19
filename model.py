from agent import Agent
from data import Data

class Model():
    """Class used to manipulate data"
    Will store people's agreebleness and density in a zone.
    """

    def initialize_people():
        return Data.agents() 

    @classmethod
    def average(self, l):
        return sum(l) / float(len(l))

people = Model.initialize_people()
agreeableness_list = []
for agent in people:
    agreeableness_list.append(agent.agreeableness)
average = Model.average(agreeableness_list)
print(average)
