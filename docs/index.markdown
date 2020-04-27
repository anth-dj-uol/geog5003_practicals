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

A simple ABM framework can be found in [this repository](https://github.com/anth-dj/geog5003_practicals/tree/master), containing the following files:

- `agentframework.py` - provides an Agent class that defines behaviour for interacting with other agents and its environment

- `model.py` - provides a GUI to edit model parameters and run an animated simulation using the Agent class mentioned above

When run, the model will simulate numerous agents randomly moving through their environment, "eating" the resources in each cell as they pass through. Agents can also share the resources they've eaten with neighbouring agents if they are within a distance threshold.


## Instructions

This section describes how to launch the GUI and run the ABM simulation.

#### Requirements

- [Python3](https://www.python.org/downloads/)

#### Launching the GUI

**Spyder IDE**

If the Spyder IDE is installed on your system:

- Run the Spyder application
- Open `python/src/unpackaged/abm/model.py`
- Ensure the correct graphic settings are configured:
    - Tools > Preferences > IPython console > Graphics tab > Graphics backend
    - Set Bakcend to _Tkinter_
    - Click _OK_
    - Click Consoles menu item > _Restart Kernel_ 
- Click _Run file_ (or press F5) 

**Command Prompt**

- Navigate into the `python/src/unpackaged/abm/` directory
- Run: `python model` (or use an absolute path to the Python executable if the `python` command is not in the environment path)

#### Running the Model

To start the model simulation:
- Click the Model menu item
- Select _Run model_