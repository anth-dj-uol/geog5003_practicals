import tkinter
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
import matplotlib.animation 
import agentframework
import csv
import random


num_of_agents = 50
num_of_iterations = 200
neighbourhood = 20
filename = 'in.txt'

agents = []
environment = []

# Prepare model plot
matplotlib.pyplot.ioff()
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_autoscale_on(False)

# Read environment data from file
with open(filename, newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        rowlist = []
        for value in row:
            rowlist.append(value)
        environment.append(rowlist)

# Set up agents
for i in range(num_of_agents):
    agents.append(agentframework.Agent(environment, agents))


def update(frame_number):
    fig.clear()
    random.shuffle(agents)
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
    matplotlib.pyplot.ylim(0, 99)
    matplotlib.pyplot.xlim(0, 99)
    matplotlib.pyplot.imshow(environment)
    for agent in agents:
        matplotlib.pyplot.scatter(agent.x, agent.y, color='black')


def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, interval=50, repeat=False, frames=num_of_iterations)
    canvas.draw()

# Create GUI window
root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# Create menu
menubar = tkinter.Menu(root)
root.config(menu=menubar)
model_menu = tkinter.Menu(menubar)
menubar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)

#root.mainloop()