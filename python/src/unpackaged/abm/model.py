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
default_num_of_iterations = 5000
default_neighbourhood_size = 5
default_agent_store_size = 5000
default_environment_filepath = os.path.dirname(os.path.realpath(__file__)) + \
    os.sep + 'in.txt'
default_start_positions_url = \
    'http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html'
default_environment_limit = 100
default_agent_bite_size = 100
default_animation_interval = 50
agent_color_active = "black"
agent_color_inactive = "grey"


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
    """
    The Controller class coordinates communication between the given Model
    and View. It handles events that are triggered from the View and also
    propagates changes that occur in the Model.
    
    Public Methods:
        
        update_parameters - updates the model parameters from the view values
                        
        run_model - start a model simulation
        
        stop_animation - stop a running animation
        
        start_animation - start a stopped animation
        
        reset - reset the model with its current parameters
        
        load_parameters - load the model parameters from the view
    """
    
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
        self.model = model              # Store a reference to the model
        self.view = view_class(self)    # Initialize the View
        self.animation = None           # Used to track the animation
        self.iteration_count = 0        # Used to track the iteration count
        self.has_been_reset = False     # Track when a reset has occurred
        
        log("Initialized controller with current model:")
        log(self.model)
        
        # Display initial model view
        self._update_view()
        self._update_parameters_view();
        self.view.root.mainloop()
        
    
    def update_parameters(self):
        """
        Update the model parameters from values specified in the GUI.
        
        Will raise an exception when a parameter cannot be updated correctly.

        Returns
        -------
        None.

        """
        
        log("Updating model parameters.")
        
        # Stop any running animation
        self.stop_animation()
        
        # Validate and get number of agents
        num_of_agents = None
        num_of_agents_text = self.view.num_of_agents_entry.get()
        if len(num_of_agents_text) > 0:
            try:
                num_of_agents = int(num_of_agents_text)
            except:
                raise Exception("Number of agents must be an integer")

        # Validate and get number of iterations
        num_of_iterations = None
        num_of_iterations_text = self.view.num_of_iterations_entry.get()
        if len(num_of_iterations_text) > 0:
            try:
                num_of_iterations = int(num_of_iterations_text)
            except:
                raise Exception("Number of iterations must be an integer")

        # Validate and get neighbourhood size
        neighbourhood_size = None
        neighbourhood_size_text = self.view.neighbourhood_size_entry.get()
        if len(neighbourhood_size_text) > 0:
            try:
                neighbourhood_size = int(neighbourhood_size_text)
            except:
                raise Exception("Neighbourhood size must be an integer")

        # Validate and get agent store size
        agent_store_size = None
        agent_store_size_text = self.view.agent_store_size_entry.get()
        if len(agent_store_size_text) > 0:
            try:
                agent_store_size = int(agent_store_size_text)
            except:
                raise Exception("Agent store size must be an integer")

        # Get start positions URL
        start_positions_url = self.view.start_positions_url_entry.get()

        # Get environment filepath
        environment_filepath = self.view.environment_filepath_entry.get()

        # Validate and get environment limit values
        environment_limit_text = self.view.environment_limit_entry.get()
        x_lim = None
        y_lim = None
        if len(environment_limit_text) > 0:
            try:
                x_lim, y_lim = environment_limit_text.split(",")
                x_lim = int(x_lim)
                y_lim = int(y_lim)
            except:
                raise Exception("Environment limit must be of the form X,Y, where X and Y are integers")

        # Validate and get agent bite size
        agent_bite_size = None
        agent_bite_size_text = self.view.agent_bite_size_entry.get()
        if len(agent_bite_size_text) > 0:
            try:
                agent_bite_size = int(agent_bite_size_text)
            except:
                raise Exception("Agent store size must be an integer")

        # Update model parameters
        self.model.set_parameters(num_of_agents, num_of_iterations,
                                  neighbourhood_size, agent_store_size,
                                  start_positions_url, environment_filepath, 
                                  x_lim, y_lim, agent_bite_size)
        
        # Update view parameters
        self._update_parameters_view()
        

    def _iterate(self):
        """
        Iterate the current model and update the view.

        Returns
        -------
        None.

        """
        
        # Iterate model
        is_done = self.model.iterate()
        self.iteration_count += 1
        
        if is_done:
            self.stop_animation()
            log("Model simulation complete.")

        # Update the view
        self._update_view()


    def _update_view(self):
        """
        Update the view with the current model state

        Returns
        -------
        None.

        """
        self.view.display(self.model)
    
    
    def _update_parameters_view(self):
        """
        Update the parameter entry fields in the View from values in the Model.

        Returns
        -------
        None.

        """

        log("Updating view entry fields")     
        
        # Update all entry field values
        self._set_entry_field_value(self.view.num_of_agents_entry,
                                   self.model.num_of_agents)
        self._set_entry_field_value(self.view.num_of_iterations_entry,
                                   self.model.num_of_iterations)
        self._set_entry_field_value(self.view.neighbourhood_size_entry,
                                   self.model.neighbourhood_size)
        self._set_entry_field_value(self.view.agent_store_size_entry,
                                   self.model.agent_store_size)
        self._set_entry_field_value(self.view.start_positions_url_entry,
                                   self.model.start_positions_url)
        self._set_entry_field_value(self.view.environment_filepath_entry,
                                   self.model.environment_filepath)
        self._set_entry_field_value(self.view.agent_bite_size_entry,
                                   self.model.agent_bite_size)
        
        # Update the environment limit field
        environment_limit_text = ""
        if self.model.x_lim is not None and self.model.x_lim is not None:
            # If environment limit is set, format the display text
            environment_limit_text = "{},{}".format(self.model.x_lim,
                                                  self.model.y_lim)
        self._set_entry_field_value(self.view.environment_limit_entry,
                                   environment_limit_text)


    def _set_entry_field_value(self, entry_field, value):
        """
        Set the entry field text to the given value

        Parameters
        ----------
        entry_field : tkinter.Entry
            The entry field to modify.
        value : str
            The value to set in the entry field.

        Returns
        -------
        None.

        """
        
        entry_field.delete(0, tkinter.END)
        entry_field.insert(0, value)


    def run_model(self):
        """
        Run the currently configured model from the start.
        
        Returns
        -------
        None.

        """
        
        log("Running model.")
                
        # Attempt to reset the current model
        if not self.has_been_reset:
            self.reset()

        # Start animation
        self.animation = matplotlib.animation.FuncAnimation(
            self.view.fig,
            (lambda frame_number: self._iterate()),
            interval=default_animation_interval,
            repeat=False,
            frames=self.model.num_of_iterations)
        
        # Track
        self.has_been_reset = False
        
        # Render animation
        self.view.canvas.draw()


    def stop_animation(self):
        """
        Stop a running animation.

        Returns
        -------
        None.

        """
        
        log("Stopping animation.")

        # Stop animation if one exists
        if self.animation is not None:
            self.animation.event_source.stop()
            log("Stopped after {} iterations".format(self.iteration_count))


    def start_animation(self):
        """
        Continue a running animation.

        Returns
        -------
        None.

        """
        
        log("Starting animation.")

        # Stop animation if one exists
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
        
        log("Resetting model.")
        
        # Cancel any currently running animation
        self.stop_animation()
        self.animation = None
        self.iteration_count = 0
   
        # Attempt model initialization
        try:
            self.model.initialize()
        except Exception as e:
            # Abort initialization on error
            self.view.show_error(e)
            return
             
        # Update the view
        self._update_view()
        self.view.canvas.draw()
        
        # Track that a reset has occurred
        self.has_been_reset = True

        log("Model has been reset.")
        log(self.model)


    def load_parameters(self):
        """
        Load the parameters specified in the View.

        Returns
        -------
        None.

        """
        
        try:
            # Update the model
            self.update_parameters()
            
            # Reset current model
            self.reset();
            
        except Exception as e:
            self.view.show_error(e)




class View():
    """
    The View class provides a GUI to view and interact with the model. It 
    handles the model rendering and user interaction events.
    
    Public Methods:
        
        display -        renders the given model
        show_error -     displays an error popup
        
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

        log("Instantiating a View.")
        
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
        root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Create menu
        menubar = tkinter.Menu(root)
        root.config(menu=menubar)
        model_menu = tkinter.Menu(menubar)
        menubar.add_cascade(label="Model", menu=model_menu)
        model_menu.add_command(label="Run model", command=self._on_run_model)
        model_menu.add_command(label="Pause animation", command=self._on_stop)
        model_menu.add_command(label="Continue animation", command=self._on_start)
        model_menu.add_command(label="Exit", command=self._on_exit)
        
        
        # Add parameter inputs
        parameters_frame = tkinter.Frame(root)
    
        self.num_of_agents_entry = self._insert_labelled_entry(
            parameters_frame, "Number of Agents:", "")

        self.num_of_iterations_entry = self._insert_labelled_entry(
            parameters_frame, "Number of Iterations:", "",
            1, 0, 1, 1)

        self.neighbourhood_size_entry = self._insert_labelled_entry(
            parameters_frame, "Neighbourhood Size:", "",
            2, 0, 2, 1)

        self.agent_store_size_entry = self._insert_labelled_entry(
            parameters_frame, "Agent Store Size:", "",
            3, 0, 3, 1)

        self.environment_filepath_entry = self._insert_labelled_entry(
            parameters_frame, "Environment File Path:",
            "",
            0, 2, 0, 3)

        self.environment_limit_entry = self._insert_labelled_entry(
            parameters_frame, "Environment Limit (x, y):",
            "",
            1, 2, 1, 3)

        self.start_positions_url_entry = self._insert_labelled_entry(
            parameters_frame, "Starting Positions URL:",
            "",
            2, 2, 2, 3)

        self.agent_bite_size_entry = self._insert_labelled_entry(
            parameters_frame, "Agent Bite Size:",
            "",
            3, 2, 3, 3)
        
        # Add a button to update parameters
        load_button = tkinter.Button(parameters_frame, text="Update Model",
                                     command=self._on_load_parameters)
        load_button.grid(row=0, column=4, padx=12)

        
        # Add the parameters frame to the GUI
        parameters_frame.pack(side=tkinter.TOP, fill=tkinter.X, padx=8, pady=8)

        # Store a reference to the root view
        self.root = root
        
        # Add canvas for rendering
        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.fig, 
                                                                     master=root)
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
                
        # Reset the current view data
        self.fig.clear()
        matplotlib.pyplot.ylim(0, model.environment.y_length)
        matplotlib.pyplot.xlim(0, model.environment.x_length)
        
        # Render the environment
        matplotlib.pyplot.imshow(model.environment.plane)
        
        # Render each agent
        for agent in model.agents:
            color = agent_color_active if agent.can_eat() else agent_color_inactive
            matplotlib.pyplot.scatter(agent.x, agent.y, color=color)


    def show_error(self, message):
        """
        Display error message

        Parameters
        ----------
        message : str
            Error message to be displayed.

        Returns
        -------
        None.

        """
        
        tkinter.messagebox.showinfo("Error", message)


    def _on_close(self):
        """
        Close the application.
        
        This will close the GUI application and clean up associated resources.

        Returns
        -------
        None.

        """
        
        log("Shutting down program.")
        
        # Close all open figures
        matplotlib.pyplot.close('all')
        
        # Quit the GUI program and free up memory
        self.root.quit()
        self.root.destroy()


    def _on_run_model(self):
        """
        Trigger a model run event

        Returns
        -------
        None.

        """
        
        self.controller.run_model()


    def _on_stop(self):
        """
        Trigger an animation stop event

        Returns
        -------
        None.

        """
        
        self.controller.stop_animation()


    def _on_start(self):
        """
        Trigger an animation start event

        Returns
        -------
        None.

        """
        
        self.controller.start_animation()


    def _on_load_parameters(self):
        """
        Trigger a load parameters event

        Returns
        -------
        None.

        """
        
        self.controller.load_parameters()


    def _on_exit(self):
        """
        Exit the program

        Returns
        -------
        None.

        """
        
        self._on_close()
        
        
    def _insert_labelled_entry(self, row, label, default_value="", label_row=0, 
                               label_column=0, entry_row=0, entry_column=1):
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
        label_row : int, optional
            Row to insert the label. The default is 0.
        label_column : int, optional
            Column to insert the label. The default is 0.
        entry_row : int, optional
            Row to insert the entry field. The default is 0.
        entry_column : int, optional
            Column to insert the entry field. The default is 1.

        Returns
        -------
        entry : tkinter.Entry
            A GUI entry component.

        """

        # Create the label element
        label = tkinter.Label(row, text=label)
        label.grid(row=label_row, column=label_column)
        
        # Create the entry element
        entry = tkinter.Entry(row)
        entry.grid(row=entry_row, column=entry_column)
        
        # Set the default value
        entry.insert(0, str(default_value))
        
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
        
        log("Instantiating a Model.")
        
        # Initialize model properties
        self.agents = []
        self.environment = []

        # Set default parameters
        self.set_parameters(default_num_of_agents,
                            default_num_of_iterations,
                            default_neighbourhood_size,
                            default_agent_store_size,
                            default_start_positions_url,
                            default_environment_filepath,
                            default_environment_limit,
                            default_environment_limit,
                            default_agent_bite_size)

        # Initialize model properties
        self.initialize()


    def __str__(self):
         return '''
===============================
Model
-----
Number of agents: {}
Number of iterations: {}
Neighbourhood size: {}
Agent Store size: {}
Environment filepath: {}
Environment limit: {},{}
Start Positions URL: {}
Agent Bite Size: {}
===============================
                '''.format(
                    self.num_of_agents,
                    self.num_of_iterations,
                    self.neighbourhood_size,
                    self.agent_store_size,
                    self.environment_filepath,
                    self.x_lim, self.y_lim,
                    self.start_positions_url,
                    self.agent_bite_size
                )


    def initialize(self):
        """
        Initialize the model properties.

        Returns
        -------
        None.

        """
        
        # Create a new model environment
        self._create_environment(self.environment_filepath)
        
        # Create a new set of agents
        self._create_agents()


    def iterate(self):
        """
        Run a single iteration of the model.
        
        This will cause each agent to move one step, attempt to eat a portion
        of their environment and share with any neighbouring agents.

        Returns
        -------
        is_done : TYPE
            Returns True if the simulation is complete, otherwise returns False.
        """
        
        # Initialize the done flag
        is_done = True
        
        # Simulate an interaction step for each agent in the model
        agents = self.agents
        
        # Shuffle agents to remove artifacts from ordered lists
        random.shuffle(agents)

        # Iterate through each agent
        for i in range(len(agents)):
            agent = agents[i]
            
            # Only move agent if it has store capacity
            if agent.can_eat():
                is_done = False
                agent.move()
                if agent.resources_available():
                    agent.eat()
                agent.share_with_neighbours(self.neighbourhood_size)

        return is_done
    
    def set_parameters(self, num_of_agents=None, num_of_iterations=None,
                       neighbourhood_size=None, agent_store_size=None,
                       start_positions_url=None, environment_filepath=None,
                       environment_x_lim=None, environment_y_lim=None,
                       agent_bite_size=None):
        """
        Set new model parameters

        Parameters
        ----------
        num_of_agents : int
            Number of agents.
        num_of_iterations : int
            Number of iterations.
        neighbourhood_size : int
            Neighbourhood size within which agents can interact with
            each other.
        agent_store_size : int
            Maximum capacity for the agent store.
        start_positions_url : str
            URL from which the agent starting positions will be fetched.
        environment_filepath : int
            Filepath from which the environment data will be fetched.
        environment_x_lim : int
            X-axis limit for the environment.
        environment_y_lim : int
            Y-axis limit for the environment.
        agent_bite_size : int
            Amount of resources consumed in a single agent bite.
            
        Returns
        -------
        None.

        """
        
        # Update number of agents, if provided
        if num_of_agents is not None:
            self.num_of_agents = num_of_agents

        # Update number of iterations, if provided
        if num_of_iterations is not None:
            self.num_of_iterations = num_of_iterations

        # Update neighbourhood size, if provided
        if neighbourhood_size is not None:
            self.neighbourhood_size = neighbourhood_size
        
        # Update agent store size, if provided
        if agent_store_size is not None:
            self.agent_store_size = agent_store_size

        # Update start positions, if provided
        self.start_positions_url = start_positions_url
        if self.start_positions_url is not None and len(self.start_positions_url) > 0:
            log("Fetching start positions from URL: {}".format(self.start_positions_url))
            self.start_positions = self._fetch_start_positions(self.start_positions_url)
        else:
            self.start_positions = ([], [])

        # Update environment filepath
        self.environment_filepath = environment_filepath

        # Update environment limits
        self.x_lim = environment_x_lim
        self.y_lim = environment_y_lim

        # Update agent store size, if provided
        if agent_bite_size is not None:
            self.agent_bite_size = agent_bite_size
        

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
        log("Parsing start positions from HTML content.")
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
                
        # Get the initial start positions
        start_xs, start_ys = self.start_positions
        
        # Create all agents
        for i in range(self.num_of_agents):
            
            # Get the initial start position
            y = int(start_ys[i].text if len(start_ys) > i 
                    else random.randint(0, self.environment.y_length - 1))
            x = int(start_xs[i].text if len(start_xs) > i 
                    else random.randint(0, self.environment.x_length - 1))
            
            # Add new Agent to the model
            self.agents.append(
                agentframework.Agent(self.environment, self.agents, y, x,
                                     self.agent_store_size, self.agent_bite_size))


    def _create_environment(self, filepath):
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
        
        # Initialize the environment plane
        environment_plane = []

        
        # Open the given file
        try:
            with open(filepath, newline='') as f:
                
                # Create a CSV reader
                reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
                
                # Read in each row and column to obtain the 2-D environment data
                for row in reader:
                    row_list = []
                    for value in row:
                        row_list.append(value)
                    environment_plane.append(row_list)
        except:
            # Display error message on enviroment read failure
            raise Exception("Unable to read environment from file: {}".format(filepath))
            
            # Abort creation of new environment
            return

        # Create new environment with the given plane
        log("Creating new environment.")
        self.environment = agentframework.Environment(environment_plane,
                                                      self.x_lim, self.y_lim)



def main():
    log("Starting the Agent-Based Model program...")
    
    # Start the GUI program
    Controller(Model(), View)


# Run the main function when invoked as a script
if __name__ == '__main__':
    main()