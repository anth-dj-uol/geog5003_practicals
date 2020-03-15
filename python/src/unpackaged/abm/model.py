import matplotlib.pyplot
import operator    # Do this line at the top of the code.
import random

agents = []

# Set up agents (y, x)
agents.append([random.randint(0, 99), random.randint(0, 99)])
agents.append([random.randint(0, 99), random.randint(0, 99)])

print(agents)


# Move point 0

# Random walk one step
if random.random() < 0.5:
    agents[0][0] += 1
else:
    agents[0][0] -= 1

if random.random() < 0.5:
    agents[0][1] += 1
else:
    agents[0][1] -= 1

# Random walk one step
if random.random() < 0.5:
    agents[0][0] += 1
else:
    agents[0][0] -= 1

if random.random() < 0.5:
    agents[0][1] += 1
else:
    agents[0][1] -= 1

print(agents[0][0], agents[0][1])


# Move point 1

# Random walk one step
if random.random() < 0.5:
    agents[1][0] += 1
else:
    agents[1][0] -= 1

if random.random() < 0.5:
    agents[1][1] += 1
else:
    agents[1][1] -= 1

# Random walk one step
if random.random() < 0.5:
    agents[1][0] += 1
else:
    agents[1][0] -= 1

if random.random() < 0.5:
    agents[1][1] += 1
else:
    agents[1][1] -= 1

print(agents[1][0], agents[1][1])


# Calculate Pythagorian distance between point 0 and point 1
distance = (
        (agents[1][0] - agents[0][0])**2 + 
        (agents[1][1] - agents[0][1])**2 
)**0.5

print(distance)

eastern_point = max(agents, key=operator.itemgetter(1))
print(eastern_point)    # Do this line at the bottom.


matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)

matplotlib.pyplot.scatter(agents[0][1],agents[0][0], color='black')
matplotlib.pyplot.scatter(agents[1][1],agents[1][0], color='black')
matplotlib.pyplot.scatter(eastern_point[1],eastern_point[0], color='red')

matplotlib.pyplot.show()

