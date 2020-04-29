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
default_num_of_iterations = 200
default_neighbourhood_size = 20
default_filename = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'in.txt'
default_start_positions_url = \
    'http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html'


def log(message):
    """
    Print the message to standard output
    """
    print(message)
 

class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self
        self.animation = None
        
        # Display initial model view
        self.update_view()
    
    def update_parameters(self):
        self.model.update_parameters(
            int(self.view.num_of_agents_entry.get()),
            int(self.view.num_of_iterations_entry.get()),
            int(self.view.neighbourhood_size_entry.get())
        )
        self.model.initialize()
    
    def iterate(self):
        self.model.iterate()
        self.update_view()
        
    def update_view(self):
        self.view.display(self.model.environment, self.model.agents)
        self.view.canvas.draw()
    
    def run_model(self):
        log("Running model...")
        self.reset()
        self.animation = matplotlib.animation.FuncAnimation(
            self.view.fig, (lambda frame_number: self.iterate()), interval=10, repeat=False, frames=self.model.num_of_iterations)
        self.view.canvas.draw()
    
    def stop_animation(self):
        if self.animation is not None:
            self.animation.event_source.stop()
    
    def start_animation(self):
        if self.animation is not None:
            self.animation.event_source.start()
    
    def reset(self):
        self.stop_animation()
        self.update_parameters()
        self.update_view()
        self.view.canvas.draw()


class View():
    def __init__(self):

        # Prepare the visualization figure
        matplotlib.pyplot.ioff()
        self.fig = matplotlib.pyplot.figure(figsize=(7, 7))
        ax = self.fig.add_axes([0, 0, 1, 1])
        ax.set_autoscale_on(False)

        # Create GUI window
        root = tkinter.Tk()
        root.wm_title("Agent-Based Model")
        
        # Create menu
        menubar = tkinter.Menu(root)
        root.config(menu=menubar)
        model_menu = tkinter.Menu(menubar)
        menubar.add_cascade(label="Model", menu=model_menu)
        model_menu.add_command(label="Run model", command=self.on_run_model)
        model_menu.add_command(label="Stop animation", command=self.on_stop)
        model_menu.add_command(label="Start animation", command=self.on_start)
        model_menu.add_command(label="Reset", command=self.on_reset)
        
        # Add parameter inputs    
        self.num_of_agents_entry = self.insert_labelled_entry(
            tkinter.Frame(root), 'Number of Agents:', default_num_of_agents)
        self.num_of_iterations_entry = self.insert_labelled_entry(
            tkinter.Frame(root), 'Number of Iterations:', default_num_of_iterations)
        self.neighbourhood_size_entry = self.insert_labelled_entry(
            tkinter.Frame(root), 'Neighbourhood Size:', default_neighbourhood_size)
    
        self.root = root
        
        # Add canvas
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.fig, master=root)
        canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.canvas = canvas
    
    def on_run_model(self):
        self.controller.run_model()

    def on_stop(self):
        self.controller.stop_animation()

    def on_start(self):
        self.controller.start_animation()

    def on_reset(self):
        self.controller.reset()

    def display(self, environment, agents):
        """
        Run a single iteration of the model simulation.
    
        Each agent in the model will move one step, eat a portion of the
        environment and share its store with any neighbouring agents. An
        updated plot will be rendered showing the current position of each
        agent and the current environment data.
        """
        self.fig.clear()
        matplotlib.pyplot.ylim(0, 99)
        matplotlib.pyplot.xlim(0, 99)
        matplotlib.pyplot.imshow(environment)
        for agent in agents:
            matplotlib.pyplot.scatter(agent.x, agent.y, color='black')
        self.canvas.draw()


    def insert_labelled_entry(self, row, label, default_value):
        """
        Return entry with the given label and default value.
        """
        label = tkinter.Label(row, text=label)
        label.grid(row=0)
        entry = tkinter.Entry(row)
        entry.grid(row=0, column=1)
        entry.insert(0, str(default_value))
        row.pack(side=tkinter.TOP, fill=tkinter.X, padx=4, pady=8)
        return entry
        

class Model():
    def __init__(self):
        self.agents = []
        self.environment = []
        self.num_of_agents = default_num_of_agents
        self.num_of_iterations = default_num_of_iterations
        self.neighbourhood_size = default_neighbourhood_size
        self.start_positions = self.fetch_start_positions(default_start_positions_url)
        self.initialize()
        
    def initialize(self):
        self.populate_environment(default_filename)
        self.setup_agents()

    def iterate(self):
        agents = self.agents
        random.shuffle(agents)
        for i in range(len(agents)):
            agents[i].move()
            agents[i].eat()
            agents[i].share_with_neighbours(self.neighbourhood_size)
    
    def update_parameters(self, num_of_agents, num_of_iterations, neighbourhood_size):
        self.num_of_agents = num_of_agents
        self.num_of_iterations = num_of_iterations
        self.neighbourhood_size = neighbourhood_size
        self.setup_agents()

    
    def fetch_start_positions(self, url):
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

    def setup_agents(self):
        """
        Instatiate all agents, given the total number, their environment and
        a reference to the total list of agents.
        """
        self.agents = []
        environment_size = len(self.environment)
        start_xs, start_ys = self.start_positions
        for i in range(self.num_of_agents):
            y = int(start_ys[i].text if len(start_ys) > i else random.randint(0, environment_size - 1))
            x = int(start_xs[i].text if len(start_xs) > i else random.randint(0, environment_size - 1))
            self.agents.append(agentframework.Agent(self.environment, self.agents, y, x))

    def populate_environment(self, filename):
        """
        Return environment data from the given file path.
        """
        self.environment.clear()
        with open(filename, newline='') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                rowlist = []
                for value in row:
                    rowlist.append(value)
                self.environment.append(rowlist)


def main():
    log("Starting the Agent-Based Model GUI...")
    #root.mainloop()
    Controller(Model(), View())

if __name__ == '__main__':
    main()