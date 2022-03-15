import numpy as np

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from mesa.space import Grid

from .cell import Cell

def count_live_cells(model):
    """Number of cells that are alive"""
    counter = [1 if cell.isAlive else 0 for cell in model.schedule.agents]
    total = np.sum(counter)
    # return the number of live cells
    return total.item()

class ConwaysGameOfLife(Model):
    """
    Represents the 2-dimensional array of cells in Conway's Game of Life. Rules:
    A DEAD cell will come to life if exactly 3 neighbours are alive. 
    A LIVE cell will die if less than 2 or more than 3 neighbours are alive.
    """

    def __init__(self, prob=0.1, width=50, height=50):
        """
        Create a new playing area of (width, height) cells.
        """

        # Set up the grid and schedule.

        # Use SimultaneousActivation which simulates all the cells
        # computing their next state simultaneously.  This needs to
        # be done because each cell's next state depends on the current
        # state of all its neighbors -- before they've changed.
        self.schedule = SimultaneousActivation(self)

        # Use a simple grid, where edges wrap around.
        self.grid = Grid(width, height, torus=True)

        # Place a cell at each location, with some initialized to
        # ALIVE and some to DEAD.
        for (contents, x, y) in self.grid.coord_iter():
            cell = Cell((x, y), self)
            if self.random.random() < prob:
                cell.state = cell.ALIVE
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)

        self.running = True
        self.datacollector = DataCollector(
            model_reporters={"NLiveCells": count_live_cells}
        )
        self.datacollector.collect(self)

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
        self.datacollector.collect(self)
