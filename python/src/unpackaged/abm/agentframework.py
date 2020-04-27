import random

class Agent():
    """
    A basic implementation of an agent that can interact
    with its environment and other agents.
    """

    def __init__(self, environment, agents, y, x):
        """
        Return a new Agent instance.

        The Agent must be given a reference to its `environment`, the `agents` in its
        environment, and its initial `y`-axis and `x`-axis position.
        """
        self.x = x if x != None else random.randint(0, 99)
        self.y = y if y != None else random.randint(0, 99)
        self.environment = environment
        self.store = 0
        self.agents = agents

    @property
    def x(self):
        """
        The agent's current x-axis position in its environment.
        """
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
    
    @x.deleter
    def x(self):
        del self._x
    
    @property
    def y(self):
        """
        The agent's current y-axis position in its environment.
        """
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
    
    @y.deleter
    def y(self):
        del self._y
    
    def move(self):
        """
        Move the agent at most one step in a random direction along
        the x-axis and y-axis of its environment.

        The agent has an equal chance to move forward, backward or nowhere.
        """
        x_rand = random.random()
        new_x = self.x
        if x_rand < 0.33:
            new_x = self.x + 1
        elif x_rand < 0.66:
            new_x = self.x - 1
        self.x = new_x % 99

        y_rand = random.random()
        new_y = self.y
        if y_rand < 0.33:
            new_y = self.y + 1
        elif y_rand < 0.66:
            new_y = self.y - 1
        self.y = new_y % 99

    def eat(self):
        """
        Eat a portion of the environment.
        """
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
    
    def distance_between(self, agent):
        """
        Return the Pythagorian distance to the given `agent`.
        """
        return (
                (self.x - agent.x)**2 + 
                (self.y - agent.y)**2 
        )**0.5

    def share_with_neighbours(self, neighbourhood):
        """
        Share the store contents with nearby agents.

        If an agent is within a threshold distance, the sum of
        their store contents will be equally divided among them.
        """
        for agent in self.agents:
            if agent != self:
                distance = self.distance_between(agent)
                if distance <= neighbourhood:
                    average = (self.store + agent.store) / 2
                    self.store = average
                    agent.store = average
                
            
        
