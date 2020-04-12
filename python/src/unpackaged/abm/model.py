import matplotlib.pyplot
import agentframework
import csv
import random

num_of_agents = 50
num_of_iterations = 100
neighbourhood = 20

filename = 'in.txt'

agents = []
environment = []

with open(filename, newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        rowlist = []
        for value in row:
            rowlist.append(value)
        environment.append(rowlist)

# Set up agents (y, x)
for i in range(num_of_agents):
    agents.append(agentframework.Agent(environment, agents))


# Move agent
for _ in range(num_of_iterations):
    for i in range(num_of_agents):
        random.shuffle(agents)
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)


matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)
matplotlib.pyplot.imshow(environment)
for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i].x, agents[i].y, color='black')
matplotlib.pyplot.show()
