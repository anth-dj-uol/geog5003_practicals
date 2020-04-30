---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: page
title: Overview
---

| **Note**: GEOG5003 assessment details and source code references can be found on the [About]({{ site.baseurl }}/about) page |

This repository contains a basic Agent-Based Model (ABM) written in Python. The ABM technique is useful in simulating the complex interaction of a group of subjects (called _agents_) and their environment by defining basic operations that are iteratively evaluated to reveal system-level behaviour.

Additional information about ABMs can be found in the following sources:
- [Bonabeau, E., 2002. Agent-based modeling: Methods and techniques for simulating human systems. Proceedings of the national academy of sciences, 99(suppl 3), pp.7280-7287.](https://www.pnas.org/content/99/suppl_3/7280.short)

- [Macal, C.M. and North, M.J., 2005, December. Tutorial on agent-based modeling and simulation. In Proceedings of the Winter Simulation Conference, 2005. (pp. 14-pp). IEEE.](https://ieeexplore.ieee.org/abstract/document/1574234/)

## Description

The main program (provided by `model.py`) provides a Graphical User Interface (GUI) to run animated model simulations. The ABM implemented in this program consists of a set of agents that move throughout their environment and consume its resources until they reach their configured capacity. Agents can also share the resources they've collected with neighbouring agents.

![alt text](screenshot.png "Screenshot of active ABM simulation")

### Stopping Conditions

There are two main ways that a simulation can stop:

1. **All agents reach their personal store capacity** - the simulation will stop when all agents have consumed engouh resources to fill their personal store, as configured by the _Agent Store Size_ editable parameter
1. **Maximum number of iterations reached** - the simulation will also stop when the configured _Number of Iterations_ has been reached

### User Interface

The GUI provides several features to view and interact with the ABM.

#### Plot

The main plot shows the current state of the model simulation. Agents are rendered as black dots while they are actively moving about the environment. When an agent's store reaches capacity, it will be rendered as a grey dot. The environment cells are rendered from bright yellow to dark purple, representing low values and high values, respectively.

#### Menu Actions
- **Run model** - starts a new model simulation
- **Pause animation** - stops animation for the current model simulation
- **Continue animation** - continues animation for the current model simulation
- **Exit** - exits the program

#### Editable Parameters
Certain parameters for the model can be modified through entry fields in the GUI. When changes are made, the **Update Model** button must be pressed for the changes to take effect. Editable parameters include:

- **Number of Agents** - the number of agents to populate in the environment
- **Number of Iterations** - the maximum number of iterations that can occur
- **Neighbourhood Size** - the maximum distance within which agents will share their store contents
- **Agent Store Size** - the maximum capacity for storing resource values
- **Environment File Path** - file path to the environment data (a 2-D array of integer values, in CSV format)
- **Environment Limit** - the maximum size of the environment in a model simulation (e.g. 100,100)
- **Starting Positions URL** - a URL to an HTML page that specifies x,y coordinates (if left blank, or a higher number of agents are specified, random positions will then be used)
- **Agent Bite Size** - the amount of resources consumed in one "bite"


### Running the Program

The simplest way to run the program is by launching the GUI from the command-line:
```
python python/src/unpackaged/abm/model.py
```

Detailed usage and testing instructions are available in the repository [README](https://github.com/anth-dj/geog5003_practicals/blob/master/README.md) file.


### Code Structure

The ABM framework found in [this repository](https://github.com/anth-dj/geog5003_practicals/tree/master), contains the following files:

- `agentframework.py` - provides classes for the Agent and its associated data, in addition to unit tests for the Agent class

- `model.py` - provides classes to model an ABM, its graphical view and a controller to link the two.


### Future Improvements

There are many potential improvements that can be implemented for this program. Some improvements can include:
- Additional editable model parameters (e.g. animation speed, plot colours)
- Ability to save the current model view to an image or CSV file
- More robust error handling
- Log and display model simulation information (e.g. number of iterations before a stopping condidition is reached)
- Improved user interface design