import json
from agent import Agent

class Data():
  
    def agents():
        with open("agents.json") as f:
            agents = []
            data = json.load(f)
            for entry in data:
                agent = Agent(agreeableness = entry['agreeableness'], location = entry['country_tld'], latitude = entry['latitude'], longitude = entry['longitude']) 
                agents.append(agent)
            return agents    
