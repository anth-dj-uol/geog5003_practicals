import random
import unittest

class Agent():
    """
    A basic implementation of an agent that can interact
    with its environment and other agents.
    """

    def __init__(self, environment, agents, y, x, store_size=0, bite_size=10):
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
        store_size : int
            Maximum capacity for the store. If < 0 is specified, there is no
            store limit

        Returns
        -------
        None.

        """

        # Set a reference to the environment
        self.environment = environment
        
        # Set a reference to model agents
        self.agents = agents
        
        # Initialize the store
        self.store = 0
        
        # Set the max store capacity
        self.store_size = store_size
        
        # Initialize bite size
        self.bite_size = bite_size

        # Set the start position
        self.x = x if x != None else random.randint(0, environment.x_length)
        self.y = y if y != None else random.randint(0, environment.y_length)
        

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
        self.x = (self.x + self._get_random_step_value()) % self.environment.x_length
        self.y = (self.y + self._get_random_step_value()) % self.environment.y_length

    
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
        if self.resources_available() and self.can_eat():
            
            # Eat a portion of the environment and store it locally
            self.environment.plane[self.y][self.x] -= self.bite_size
            self.store += self.bite_size
    

    def resources_available(self):
        """
        Check if resources are available

        Returns
        -------
        bool
            Returns True if resources are available to eat, otherwise False
            is returned.

        """
        
        return self.environment.plane[self.y][self.x] > self.bite_size
    

    def can_eat(self):
        """
        Check if the agent can eat any more resources.

        Returns
        -------
        bool
            Returns True if the agent can still each, otherwise False
            is returned.

        """
        
        return self.store_size <= 0 or \
            (self.store + self.bite_size) <= self.store_size
        
    
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
                distance = self._distance_between(agent)
                if distance <= neighbourhood_size:
                    
                    # Share store contents by having each agent take
                    # half of the average
                    average = (self.store + agent.store) / 2
                    self.store = average
                    agent.store = average


    def _distance_between(self, agent):
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



class Environment():
    """
    The Environment class represents the model environment. It consists of a
    2-dimensional array representing the plane and properties to get the plane
    x-axis length and y-axis length.
    
    """
    
    def __init__(self, environment_plane, x_lim=None, y_lim=None):
        """
        Instantiate an Environment.

        Parameters
        ----------
        environment_plane : list[list[int]]
            2-D environment plane with values representing the amount of
            resources available at that coordinate.
        x_lim : int, optional
            Limit for the x-axis. The default is None.
        y_lim : TYPE, optional
            Limit for the y-axis. The default is None.

        Returns
        -------
        None.

        """

        # Clear the current environment
        self._plane = environment_plane
        
        # Set the y-axis length
        self._y_length = len(self._plane)
        if y_lim is not None and y_lim < self._y_length:
            self._y_length = y_lim

        # Set the x-axis length
        if self._y_length > 0:
            self._x_length = len(self._plane[0])
            if x_lim is not None and x_lim < self._x_length:
                self._x_length = x_lim


    @property
    def plane(self):
        """
        Get the environment plane.
        """
        return self._plane


    @property
    def y_length(self):
        """
        Get the y-axis length.
        """
        return self._y_length

    @property
    def x_length(self):
        """
        Get the x-axis length.
        """
        return self._x_length



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
        
        # Setup test case
        environment = self.create_environment(8, 1, 1)
        agents = []
        y = 1
        x = 2
        agent = Agent(environment, agents, y, x)

        # Test initial agent property values
        self.assertEqual(agent.y, y)
        self.assertEqual(agent.x, x)
        self.assertEqual(len(agent.environment.plane), 1)
        self.assertEqual(len(agent.environment.plane[0]), 1)


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
            agent = Agent(self.create_environment(), [], y, x)
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
        
        # Setup test case
        environment = self.create_environment(11, 1, 1)
        agent = Agent(environment, [], 0, 0)
        agent.eat()
        
        # Verify effect of eat function
        self.assertEqual(agent.store, 10)
        self.assertEqual(environment.plane[0][0], 1)


    def test_no_eat_when_environment_depleted(self):
        """
        Test that the Agent does not eat from the environment when there
        are not enough resources.

        Returns
        -------
        None.

        """

        # Setup test case
        environment = self.create_environment(10, 1, 1)
        agent = Agent(environment, [], 0, 0)
        agent.eat()
        
        # Verify effect of eat function
        self.assertEqual(agent.store, 0)
        self.assertEqual(environment.plane[0][0], 10)


    def test_distance_between(self):
        """
        Test that the distance is calculated correctly.

        Returns
        -------
        None.

        """

        # Setup test case
        agent1 = Agent([[]], [], 0, 0)
        agent2 = Agent([[]], [], 4, 3)
        
        # Verify distance calculation
        self.assertEqual(agent1._distance_between(agent2), 5)

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
        
        # Create new environment plane using the given parameters
        environment = []
        for i in range(rows):
            environment.append([])
            for j in range(columns):
                environment[i].append(initial_value)
        
        # Create new environment from the initialized plane
        return Environment(environment)
                        

# Run unit tests when invoked as a script
if __name__ == '__main__':
    unittest.main()