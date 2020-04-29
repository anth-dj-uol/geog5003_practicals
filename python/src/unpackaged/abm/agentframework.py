import random
import unittest

class Agent():
    """
    A basic implementation of an agent that can interact
    with its environment and other agents.
    """

    def __init__(self, environment, agents, y, x):
        """
        Instantiate an Agent.
        
        Parameters
        ----------
        environment : list[list[int]]
            A 2-D array of number values representing the environment.
        agents : list[Agent]
            A list of agents used for interaction.
        y : int
            Initial y-axis position.
        x : int
            Initial x-axis position.

        Returns
        -------
        None.

        """

        # Set the start position
        self.x = x if x != None else random.randint(0, 99)
        self.y = y if y != None else random.randint(0, 99)
        
        # Set a reference to the environment
        self.environment = environment
        
        # Set a reference to model agents
        self.agents = agents
        
        # Initialize the store
        self.store = 0


    @property
    def x(self):
        """
        Get the current x-axis position in the environment.
        """
        return self._x
    
    
    @x.setter
    def x(self, value):
        """
        Set the current x-axis position in the environment.
        """
        self._x = value
    
    
    @x.deleter
    def x(self):
        del self._x
    
    
    @property
    def y(self):
        """
        Get the current y-axis position in the environment.
        """
        return self._y
    
    
    @y.setter
    def y(self, value):
        """
        Set the current y-axis position in the environment.
        """
        self._y = value
    
    
    @y.deleter
    def y(self):
        del self._y
    
    
    def move(self):
        """
        Move the agent a single step.

        The agent will move at most one step in a random direction along
        the x-axis and y-axis of its environment. The agent has an equal chance
        to move forward, backward or nowhere for each axis.
        
        Returns
        -------
        None.

        """

        # Walk a random step on each axis
        self.x = (self.x + self._get_random_step_value()) % 99
        self.y = (self.y + self._get_random_step_value()) % 99

    
    def _get_random_step_value(self):
        """
        Get a random step value of -1, 0 or 1.
        
        There is an equal chance of receiving any of the three possible
        step values.

        Returns
        -------
        int
            A random step value.

        """

        # Generate random chance value
        step_chance = random.random()
        
        # Decide on step value
        if step_chance < 0.33:
            return 1
        elif step_chance < 0.66:
            return -1
        return 0


    def eat(self):
        """
        Eat a portion of the environment.

        Returns
        -------
        None.

        """

        # Check that the current location has enough resources
        if self.environment[self.y][self.x] > 10:
            
            # Eat a portion of the environment and store it locally
            self.environment[self.y][self.x] -= 10
            self.store += 10
    
    
    def distance_between(self, agent):
        """
        Return the Pythagorian distance to the given `agent`.

        Parameters
        ----------
        agent : Agent
            The agent to calculate distance between.

        Returns
        -------
        float
            The distance between the specified agent.

        """

        return (
                (self.x - agent.x)**2 + 
                (self.y - agent.y)**2 
        )**0.5


    def share_with_neighbours(self, neighbourhood_size):
        """
        Share the store contents with nearby agents.

        If an agent is within the specified threshold distance, the sum of
        their store contents will be equally divided among them.

        Parameters
        ----------
        neighbourhood_size : int
            Size of the neighbourhood to search for other agents.

        Returns
        -------
        None.

        """

        # Check all agents that are not this agent
        for agent in self.agents:
            if agent != self:
                
                # Check if within the distance threshold
                distance = self.distance_between(agent)
                if distance <= neighbourhood_size:
                    
                    # Share store contents by having each agent take
                    # half of the average
                    average = (self.store + agent.store) / 2
                    self.store = average
                    agent.store = average



class AgentTestCase(unittest.TestCase):
    """
    The AgentTestCase class provides a collection of unit tests for
    the Agent class.
    """

    def test_init(self):
        """
        Test the initial Agent property values.

        Returns
        -------
        None.

        """
        environment = [[8]]
        agents = []
        y = 1
        x = 2
        agent = Agent(environment, agents, y, x)

        # Test initial agent property values
        self.assertEqual(agent.y, y)
        self.assertEqual(agent.x, x)
        self.assertEqual(len(agent.environment), 1)
        self.assertEqual(len(agent.environment[0]), 1)


    def test_move_limit(self):
        """
        Test that the Agent does not move more than a single per iteration.
        
        Since random values are generated to determine the step direction,
        a large number of iterations is used to ensure that a step of more
        than one is highly unlikely.

        Returns
        -------
        None.

        """
        # Unlikely to move past limit when high number of iterations used
        for _ in range(1000):
            y = 50
            x = 50
            agent = Agent([], [], y, x)
            agent.move()
            self.assertGreaterEqual(agent.x, x - 1)
            self.assertLessEqual(agent.x, x + 1)
            self.assertGreaterEqual(agent.y, y - 1)
            self.assertLessEqual(agent.y, y + 1)


    def test_eat(self):
        """
        Test that the Agent eats the correct amount from its environment.

        Returns
        -------
        None.

        """
        environment = [[11]]
        agent = Agent(environment, [], 0, 0)
        agent.eat()
        self.assertEqual(agent.store, 10)
        self.assertEqual(environment[0][0], 1)


    def test_no_eat_when_environment_depleted(self):
        """
        Test that the Agent does not eat from the environment when there
        are not enough resources.

        Returns
        -------
        None.

        """

        environment = [[10]]
        agent = Agent(environment, [], 0, 0)
        agent.eat()
        self.assertEqual(agent.store, 0)
        self.assertEqual(environment[0][0], 10)


    def test_distance_between(self):
        """
        Test that the distance is calculated correctly.

        Returns
        -------
        None.

        """

        agent1 = Agent([[]], [], 0, 0)
        agent2 = Agent([[]], [], 4, 3)
        self.assertEqual(agent1.distance_between(agent2), 5)

    def test_share_with_neighbours(self):
        """
        Test that agents share their resources correctly.

        Returns
        -------
        None.

        """

        # Set up test case
        environment = self.create_environment()
        agents = []
        agent1 = Agent(environment, agents, 0, 0)
        agent1.store = 10
        agents.append(agent1)
        agent2 = Agent(environment, agents, 0, 10)
        agent2.store = 0
        agents.append(agent2)

        # Check nothing is shared when too far
        agent1.share_with_neighbours(1)
        self.assertEqual(agent1.store, 10)
        self.assertEqual(agent2.store, 0)

        # Check store is shared with nearby
        agent1.share_with_neighbours(10)
        self.assertEqual(agent1.store, 5)
        self.assertEqual(agent2.store, 5)


    def create_environment(self, initial_value=0, rows=100, columns=100):
        """
        Create a 2-D environment.

        Parameters
        ----------
        initial_value : int, optional
            Initial resource value. The default is 0.
        rows : int, optional
            Number of rows. The default is 100.
        columns : int, optional
            Number of columns. The default is 100.

        Returns
        -------
        environment : list[list[int]]
            An initialized environment.

        """
        
        environment = []
        for i in range(rows):
            environment.append([])
            for j in range(columns):
                environment[i].append(initial_value)
        return environment
                        

if __name__ == '__main__':
    unittest.main()