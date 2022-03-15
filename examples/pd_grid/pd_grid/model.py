import numpy as np

from mesa import Model
from mesa.time import BaseScheduler, RandomActivation, SimultaneousActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from .agent import PDAgent

def count_cooperators(model):
    counter = [a for a in model.schedule.agents if a.move == "C"]
    return len(counter)
    
class PdGrid(Model):
    """Model class for iterated, spatial (multi-player) prisoner's dilemma model."""

    schedule_types = {
        "Sequential": BaseScheduler,
        "Random": RandomActivation,
        "Simultaneous": SimultaneousActivation,
    }

    # This dictionary holds the payoff for this agent,
    # keyed on: (my_move, other_move)

    payoff = {("C", "C"): 1, ("C", "D"): 0, ("D", "C"): 1.6, ("D", "D"): 0}

    def __init__(
        self, width=50, height=50, schedule_type="Random", CC=None, CD=None, DC=None, DD=None, seed=None
    ):
        """
        Create a new Spatial Prisoners' Dilemma Model.

        Args:
            width, height: Grid size. There will be one agent per grid cell.
            schedule_type: Can be "Sequential", "Random", or "Simultaneous".
                           Determines the agent activation regime.
            payoffs: (optional) Dictionary of (move, neighbor_move) payoffs.
        """
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule_type = schedule_type
        self.schedule = self.schedule_types[self.schedule_type](self)
        
        if np.all(np.array([CC,CD,DC,DD]) > 0):
            self.payoff = {("C", "C"): CC, 
                           ("C", "D"): CD, 
                           ("D", "C"): DC, 
                           ("D", "D"): DD}

        # Create agents
        for x in range(width):
            for y in range(height):
                agent = PDAgent((x, y), self)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)

        self.datacollector = DataCollector(
            {
                "Cooperating Agents": count_cooperators,
                "Defecting Agents": lambda m: width*height - count_cooperators(m)
            }
        )

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run(self, n):
        """Run the model for n steps."""
        for _ in range(n):
            self.step()
