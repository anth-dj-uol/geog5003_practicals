import matplotlib.pyplot
import operator    # Do this line at the top of the code.
import random
import time

def distance_between(agents_row_a, agents_row_b):
    '''
    Calculate Pythagorian distance between point 0 and point 1
    '''
    return (
            (agents_row_a[0] - agents_row_b[0])**2 + 
            (agents_row_a[1] - agents_row_b[1])**2 
    )**0.5

num_of_agents = 1000
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


eastern_point = max(agents, key=operator.itemgetter(1))
print(eastern_point)    # Do this line at the bottom.


matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)

for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i][1],agents[i][0], color='black')

matplotlib.pyplot.scatter(eastern_point[1],eastern_point[0], color='red')

matplotlib.pyplot.show()

distance = distance_between(agents[0], agents[1])
#distance = distance_between([0, 0], [3, 4])

start = time.clock()
for i in range(num_of_agents):
    for j in range(num_of_agents):
        distance = distance_between(agents[i], agents[j])
end = time.clock()
print("time = " + str(end-start))
