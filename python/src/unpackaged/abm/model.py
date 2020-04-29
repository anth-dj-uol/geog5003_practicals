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
default_environment_filepath = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'in.txt'
default_start_positions_url = \
    'http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html'


def log(message):
    """
    Print the given message to standard output

    Parameters
    ----------
    message : str
        The message to print.

    Returns
    -------
    None.

    """

    print(message)


class Controller():
    def __init__(self, model, view_class):
        """
        Instantiate a Controller

        Parameters
        ----------
        model : Model
            The model to update and fetch data from.
        view_class : View
            The view in which the model should be rendered.

        Returns
        -------
        None.

        """

        # Initialize model properties
        self.model = model
        self.view = view_class(self)
        self.animation = None
        
        # Display initial model view
        self.update_view()
    
    def update_parameters(self):
        """
        Update the model parameters from values specified in the GUI

        Returns
        -------
        None.

        """

        # Update model parameters with GUI values
        self.model.set_parameters(
            int(self.view.num_of_agents_entry.get()),
            int(self.view.num_of_iterations_entry.get()),
            int(self.view.neighbourhood_size_entry.get())
        )
        
        # Intialize model with new parameters
        self.model.initialize()
    
    def iterate(self):
        """
        Iterate the current model and update the view.

        Returns
        -------
        None.

        """
        
        # Iterate model
        self.model.iterate()
        
        # Update the view
        self.update_view()
        
    def update_view(self):
        """
        Update the view with the current model state

        Returns
        -------
        None.

        """
        self.view.display(self.model)
    
    def run_model(self):
        """
        Run the currently configured model from the start.
        
        Returns
        -------
        None.

        """
        
        log("Running model...")
        
        # Reset current model
        self.reset()
        
        # Start animation
        self.animation = matplotlib.animation.FuncAnimation(
            self.view.fig, (lambda frame_number: self.iterate()), interval=10, repeat=False, frames=self.model.num_of_iterations)
        
        # Render animation
        self.view.canvas.draw()
    
    def stop_animation(self):
        """
        Stop a running animation.

        Returns
        -------
        None.

        """
        
        # Stop animation if one exists
        if self.animation is not None:
            self.animation.event_source.stop()
    
    def start_animation(self):
        """
        Continue an animation that has been stopped.

        Returns
        -------
        None.

        """
        
        # Start animation if one exists
        if self.animation is not None:
            self.animation.event_source.start()
    
    def reset(self):
        """
        Reset the model.
        
        This will stop any running animation and reset the model to
        it's initial configuration using the current parameters.

        Returns
        -------
        None.

        """
        
        # Stop any currently running animation
        self.stop_animation()
        
        # Update the model
        self.update_parameters()
        
        # Update the view
        self.update_view()
        self.view.canvas.draw()


class View():
    """
    The View class provides a GUI to view and interact with the model. It 
    handles the model rendering and user interaction events.
    
    Public Methods:
        
        display -        renders the given model
        
    """

    def __init__(self, controller):
        """
        Instantiate a View.

        Parameters
        ----------
        controller : Controller
            Controller class used to handle GUI events.

        Returns
        -------
        None.

        """

        # Set the controller back-reference
        self.controller = controller

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
        
        # Add canvas for rendering
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.fig, master=root)
        canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.canvas = canvas
    
    def display(self, model):
        """
        Display the current state of the given model

        Parameters
        ----------
        model : Model
            The model to be rendered in the GUI.

        Returns
        -------
        None.

        """
        
        # Fetch the required model properties to be displayed
        environment = model.environment
        agents = model.agents
        
        # Reset the current view data
        self.fig.clear()
        matplotlib.pyplot.ylim(0, 99)
        matplotlib.pyplot.xlim(0, 99)
        
        # Render the environment
        matplotlib.pyplot.imshow(environment)
        
        # Render each agent
        for agent in agents:
            matplotlib.pyplot.scatter(agent.x, agent.y, color='black')

    def on_run_model(self):
        """
        Trigger a model run event

        Returns
        -------
        None.

        """
        self.controller.run_model()

    def on_stop(self):
        """
        Trigger an animation stop event

        Returns
        -------
        None.

        """
        self.controller.stop_animation()

    def on_start(self):
        """
        Trigger an animation start event

        Returns
        -------
        None.

        """
        self.controller.start_animation()

    def on_reset(self):
        """
        Trigger a reset event

        Returns
        -------
        None.

        """
        self.controller.reset()


    def insert_labelled_entry(self, row, label, default_value):
        """
        Return an entry field widget with the given label and default value.

        Parameters
        ----------
        row : tkinter.Frame
            Frame widget to attach to.
        label : str
            Entry field text label.
        default_value : str
            Default value for the entry field.

        Returns
        -------
        entry : tkinter.Entry
            A GUI entry component.

        """

        # Create the label element
        label = tkinter.Label(row, text=label)
        label.grid(row=0)
        
        # Create the entry element
        entry = tkinter.Entry(row)
        entry.grid(row=0, column=1)
        
        # Set the default value
        entry.insert(0, str(default_value))
        
        # Add to the GUI
        row.pack(side=tkinter.TOP, fill=tkinter.X, padx=4, pady=8)
        return entry
        

class Model():
    """
    The Model class represents an Agent-Based Model (ABM). It consists of a
    collection of agents and an environment for the agents to interact with.
    
    Public Methods:
        
        initialize -        initializes the model properties using the 
                            configured model parameters
        
        iterate -           runs a single iteration of the model
        
        set_parameters -    sets the model parameters  
    """
    
    def __init__(self):
        """
        Instantiate a Model.

        Returns
        -------
        None.

        """
        # Initialize model properties
        self.agents = []
        self.environment = []
        self.start_positions = self._fetch_start_positions(default_start_positions_url)

        # Set default parameters        
        self.set_parameters(default_num_of_agents, default_num_of_iterations, default_neighbourhood_size)
        
        # Initialize model properties
        self.initialize()
        
    def initialize(self):
        """
        Initialize the model properties.

        Returns
        -------
        None.

        """
        
        # Create a new model environment
        self._create_environment(default_environment_filepath)
        
        # Create a new set of agents
        self._create_agents()

    def iterate(self):
        """
        Run a single iteration of the model.
        
        This will cause each agent to move one step, attempt to eat a portion
        of their environment and share with any neighbouring agents.

        Returns
        -------
        None.

        """
        
        # Simulate an interaction step for each agent in the model
        agents = self.agents
        random.shuffle(agents)
        for i in range(len(agents)):
            agents[i].move()
            agents[i].eat()
            agents[i].share_with_neighbours(self.neighbourhood_size)
    
    def set_parameters(self, num_of_agents, num_of_iterations, neighbourhood_size):
        """
        Set new model parameters

        Parameters
        ----------
        num_of_agents : int
            number of agents.
        num_of_iterations : int
            number of iterations.
        neighbourhood_size : int
            neighbourhood size within which agents can interact with
            each other.

        Returns
        -------
        None.

        """
        self.num_of_agents = num_of_agents
        self.num_of_iterations = num_of_iterations
        self.neighbourhood_size = neighbourhood_size

    
    def _fetch_start_positions(self, url):
        """
        Return agent start positions from the provided URL.
        
        Parameters
        ----------
        url : str
            URL from which start positions will be obtained

        Returns
        -------
        td_xs : list[str]
            list of x-axis coordinate values.
        td_ys : list[str]
            list of y-axis coordinate values.

        """

        # Fetch text content from the given URL
        r = requests.get(url)
        content = r.text

        # Parse the given HTML to obtain the x-axis and y-axis positions
        soup = bs4.BeautifulSoup(content, 'html.parser')
        td_xs = soup.find_all(attrs={"class" : "x"})
        td_ys = soup.find_all(attrs={"class" : "y"})
        return (td_xs, td_ys)

    def _create_agents(self):
        """
        Generate new set of agents using the current model parameters

        Returns
        -------
        None.

        """
        
        # Reset the current agents list
        self.agents = []
        
        # Calculate the environment size
        environment_size = len(self.environment)
        
        # Get the initial start positions
        start_xs, start_ys = self.start_positions
        
        # Create all agents
        for i in range(self.num_of_agents):
            
            # Get the initial start position
            y = int(start_ys[i].text if len(start_ys) > i else random.randint(0, environment_size - 1))
            x = int(start_xs[i].text if len(start_xs) > i else random.randint(0, environment_size - 1))
            
            # Add new Agent to the model
            self.agents.append(agentframework.Agent(self.environment, self.agents, y, x))

    def _create_environment(self, filename):
        """
        Set the model environment using data from the provided file path.

        Parameters
        ----------
        filename : str
            File path to the environment data in CSV format.

        Returns
        -------
        None.

        """

        # Clear the current environment
        self.environment.clear()

        # Open the given file
        with open(filename, newline='') as f:
            
            # Create a CSV reader
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            
            # Read in each row and column to obtain the 2-D environment data
            for row in reader:
                rowlist = []
                for value in row:
                    rowlist.append(value)
                self.environment.append(rowlist)


def main():
    log("Starting the Agent-Based Model GUI...")
    #root.mainloop()
    Controller(Model(), View)

if __name__ == '__main__':
    main()