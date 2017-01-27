# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Firstly, agent walks through all the value in the grid if the agent ecounter value of lenght 2, it will lookthrough all of its peer in peers dictionary. If it find the value that is the same as the one that it first ecounter, it will report naked-twin value found. Then, agent will eliminate that two digit from all the value in its peers' value. Agent will process to do that until the end of the grid value.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: I created a list of diagonal value storage. I create two new lists and two new dictionary for to solve a diagonal sudoku problem. One of the dictionary act like a peers dictionary in the given assingment. Then, I run throught it like a normal grid but only with the diagonal only with eliminate, only choice and naked-twin solution.

[Noted]: There are two solution to above problem, if you put only elimination into the diagonal solver only, it will generate different result if we move order of digoanl solver around in the reduce puzzle function. In fact, the result is correct.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.