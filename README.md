# crc-proj
CRC Project (Generalized Schelling Model of Segregation)

### Repository structure
  - main.py: file to use when running simulations.
  - schelling/: folder with source code for the simulation.
  - configs/: folder with configurations of the experiments used for the report.
 
 ### How to run
  - For Python >= 3.8, install dependencies on requirements.txt
  - Use an existing config, or write a YAML configuration file for the experiment you wish to run. The parameters are as follows:
    - <groups>: dict - keys are group names, and values are there percentage on the grid. For example "blue: 0.5" means that the blue group will occupy 50% of the grid's squares.
    - empty: float - percentage of empty squares in the grid.
    - is_costs: bool - if True, players spend resources to move squares at each iteration. The farther the square, the more resources spent.
    - is_smart: bool - if True, player movement is no longer random, but they select the square with more neighbors of their group.
    - shape: list - shape of the grid (each entry is a number of squares; must have two and only two entries)
    - similar_list: list - tolerance threshold for each group. Must have the same length as the groups dictionary; first entry corresponds to first group, etc...
    - resources_list: list - same as similar_list but for resources.
    - adaptivities_list: list - same as the previous two, but for adaptivity. The higher this value, the faster agents adapt their tolerance with their surroundings.
  - Run main.py with the variable "path" equal to the name of the config you wish to run. For example, "path = base" will have main run the config base.yaml. Alternatively, uncomment the lines with the sys args to feed the config file from the terminal.
