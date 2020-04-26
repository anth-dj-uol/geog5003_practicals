import random

class Agent():
    
    def __init__(self, environment, agents, y, x):
        self.x = x if x != None else random.randint(0, 99)
        self.y = y if y != None else random.randint(0, 99)
        self.environment = environment
        self.store = 0
        self.agents = agents

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
    
    @x.deleter
    def x(self):
        del self._x
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
    
    @y.deleter
    def y(self):
        del self._y
    
    def move(self):
        if random.random() < 0.5:
            self.x = (self.x + 1) % 99
        else:
            self.x = (self.x - 1) % 99

        if random.random() < 0.5:
            self.y = (self.y + 1) % 99
        else:
            self.y = (self.y - 1) % 99

    def eat(self): # can you make it eat what is left?
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
    
    def distance_between(self, agent):
        '''
        Calculate Pythagorian distance between point 0 and point 1
        '''
        return (
                (self.x - agent.x)**2 + 
                (self.y - agent.y)**2 
        )**0.5

    def share_with_neighbours(self, neighbourhood):
        for agent in self.agents:
            if agent != self:
                distance = self.distance_between(agent)
                if distance <= neighbourhood:
                    average = (self.store + agent.store) / 2
                    self.store = average
                    agent.store = average
                
            
        
