"""
Agent-Based Model Simulation
============================

A basic ABM that simulates agents traversing an environment
and eating a portion of it. Agents can share what they have
eaten with other agents if they are nearby.
"""

import tkinter
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot
import matplotlib.animation 
import csv
import random
import requests
import bs4
import os
import agentframework

# Define default parameter values
default_num_of_agents = 50
num_of_iterations = 200
neighbourhood = 20
dir_path = os.path.dirname(os.path.realpath(__file__))
default_filename = dir_path + os.sep + 'in.txt'
default_start_positions_url = \
    'http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html'

# Prepare the model visualization
matplotlib.pyplot.ioff()
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_autoscale_on(False)

# Initialize variables
agents = []
environment = []

def fetch_start_positions(url):
    """
    Return the start positions from the provided URL.
    """
    # Fetch start positions
    r = requests.get(url)
    content = r.text
    soup = bs4.BeautifulSoup(content, 'html.parser')
    td_xs = soup.find_all(attrs={"class" : "x"})
    td_ys = soup.find_all(attrs={"class" : "y"})
    return (td_xs, td_ys)

def populate_environment(filename, environment):
    """
    Return environment data from the given file path.
    """
    environment = [] if environment is None else environment
    with open(filename, newline='') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            rowlist = []
            for value in row:
                rowlist.append(value)
            environment.append(rowlist)
    return environment

def setup_agents(num_of_agents, environment, agents, start_positions):
    """
    Instatiate all agents, given the total number, their environment and
    a reference to the total list of agents.
    """
    start_xs, start_ys = start_positions
    for i in range(num_of_agents):
        y = int(start_ys[i].text)
        x = int(start_xs[i].text)
        agents.append(agentframework.Agent(environment, agents, y, x))


def update(frame_number, move=True):
    """
    Run a single iteration of the model simulation.

    Each agent in the model will move one step, eat a portion of the
    environment and share its store with any neighbouring agents. An
    updated plot will be rendered showing the current position of each
    agent and the current environment data.
    """
    fig.clear()
    random.shuffle(agents)
    for i in range(len(agents)):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
    matplotlib.pyplot.ylim(0, 99)
    matplotlib.pyplot.xlim(0, 99)
    matplotlib.pyplot.imshow(environment)
    for agent in agents:
        matplotlib.pyplot.scatter(agent.x, agent.y, color='black')


def run(canvas):
    """
    Start the simulation in an animated figure.
    """
    animation = matplotlib.animation.FuncAnimation(fig, update, interval=10, repeat=False, frames=num_of_iterations)
    canvas.draw()


def main():

    # Setup model
    populate_environment(default_filename, environment)
    start_positions = fetch_start_positions(default_start_positions_url)
    setup_agents(default_num_of_agents, environment, agents, start_positions)

    # Create GUI window
    root = tkinter.Tk()
    root.wm_title("Agent-Based Model")
    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
    canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    # Create menu
    menubar = tkinter.Menu(root)
    root.config(menu=menubar)
    model_menu = tkinter.Menu(menubar)
    menubar.add_cascade(label="Model", menu=model_menu)
    model_menu.add_command(label="Run model", command= lambda: run(canvas))

    # Display initial model
    update(0, False)

    #root.mainloop()


if __name__ == '__main__':
    main()