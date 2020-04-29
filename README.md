# GEOG5003 Assessment 1

This repository contains all source code for the University of Leeds GEOG5003 Assessment 1 and practical outputs.

Information about this repository can be found on the associated [Agent Based Modelling](https://anth-dj.github.io/geog5003_practicals/) website.

# Instructions

This section describes how to launch the GUI and run the ABM simulation.

## Requirements

- [Python3](https://www.python.org/downloads/)

## Launching the GUI

### Spyder IDE

If the Spyder IDE is installed on your system:

- Run the Spyder application
- Open `python/src/unpackaged/abm/model.py`
- Ensure the correct graphic settings are configured:
    - Tools > Preferences > IPython console > Graphics tab > Graphics backend
    - Set Bakcend to _Tkinter_
    - Click _OK_
    - Click Consoles menu item > _Restart Kernel_ 
- Click _Run file_ (or press F5) 

### Command Prompt

- Navigate into the `python/src/unpackaged/abm/` directory
- Run: `python model` (or use an absolute path to the Python executable if the `python` command is not in the environment path)

## Running the Model

To start the model simulation:
- Select the Model menu item
- Click _Run model_


# Testing Instructions

To run unit tests, run the following command from the repository root directory:
```
python -m unittest python/src/unpackaged/abm/agentframework.py
```

# License

This repository uses the MIT license (see the [LICENSE](./LICENSE) file).