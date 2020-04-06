import matplotlib.pyplot
import agentframework

def distance_between(agents_row_a, agents_row_b):
    '''
    Calculate Pythagorian distance between point 0 and point 1
    '''
    return (
            (agents_row_a.x - agents_row_b.x)**2 + 
            (agents_row_a.y - agents_row_b.y)**2 
    )**0.5

num_of_agents = 50
num_of_iterations = 100

agents = []


# Set up agents (y, x)
for i in range(num_of_agents):
    agents.append(agentframework.Agent())


# Move agent
for _ in range(num_of_iterations):
    for i in range(num_of_agents):
        agents[i].move()


matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)
for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i].x, agents[i].y, color='black')
matplotlib.pyplot.show()

distance = distance_between(agents[0], agents[1])
#distance = distance_between([0, 0], [3, 4])

for agents_row_a in agents:
    for agents_row_b in agents:
        distance = distance_between(agents_row_a, agents_row_b)
