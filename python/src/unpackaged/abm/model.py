import matplotlib.pyplot
import operator    # Do this line at the top of the code.
import random

num_of_agents = 10
num_of_iterations = 10

agents = []

# Set up agents (y, x)
for i in range(num_of_agents):
    agents.append([random.randint(0, 99), random.randint(0, 99)])

print(agents)


# Move agent
for _ in range(num_of_iterations):
    for i in range(num_of_agents):
        
        # Random walk one step
        if random.random() < 0.5:
            agents[i][0] = (agents[i][0] + 1) % 100
        else:
            agents[i][0] = (agents[i][0] - 1) % 100
                
        if random.random() < 0.5:
            agents[i][1] = (agents[i][1] + 1) % 100
        else:
            agents[i][1] = (agents[i][1] - 1) % 100

        print(agents[i][0], agents[i][1])



# Calculate Pythagorian distance between point 0 and point 1
#distance = (
#        (agents[1][0] - agents[0][0])**2 + 
#        (agents[1][1] - agents[0][1])**2 
#)**0.5
#
#print(distance)

eastern_point = max(agents, key=operator.itemgetter(1))
print(eastern_point)    # Do this line at the bottom.


matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)

for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i][1],agents[i][0], color='black')

matplotlib.pyplot.scatter(eastern_point[1],eastern_point[0], color='red')

matplotlib.pyplot.show()

