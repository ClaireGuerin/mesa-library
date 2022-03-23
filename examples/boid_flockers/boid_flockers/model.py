"""
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""

import numpy as np

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector
from mesa.time import BaseScheduler, RandomActivation, SimultaneousActivation

from .boid import Boid

def get_average_speed(model):
    """average speed of all agents (boids)"""
    
    boid_speeds = [boid.velocity for boid in model.schedule.agents]
    # return the average agent (boid) speed
    return np.mean(boid_speeds)
    

class BoidFlockers(Model):
    """
    This model is an implementation of Craig Reynolds's Boids flocker model. 
    Boids is an example of emergent behavior, such that the complexity of Boids arises from 
    the interaction of individual agents (the boids, in this case) adhering to a set of simple rules. 
    The rules applied in the simplest Boids world are as three-fold:
    **separation**: steer to avoid crowding local flockmates;
    **alignment**: steer towards the average heading of local flockmates;
    **cohesion**: steer to move towards the average position (center of mass) of local flockmates.
    """
    
    schedule_types = {
        "Sequential": BaseScheduler,
        "Random": RandomActivation,
        "Simultaneous": SimultaneousActivation,
    }

    def __init__(
        self,
        schedule_type="Random",
        population=100,
        width=100,
        height=100,
        speed=1,
        vision=10,
        separation=2,
        cohere=0.025,
        separate=0.25,
        match=0.04,
        select=None,
    ):
        """
        Create a new Flockers model.

        Args:
            population: Number of Boids
            width, height: Size of the space.
            speed: How fast should the Boids move.
            vision: How far around should each Boid look for its neighbors
            separation: What's the minimum distance each Boid will attempt to
                    keep from any other
            cohere, separate, match: factors for the relative importance of
                    the three drives."""
        self.population = population
        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.schedule_type = schedule_type
        self.schedule = self.schedule_types[self.schedule_type](self) # either random, sequential or simultaneous
        self.space = ContinuousSpace(width, height, True)
        self.factors = dict(cohere=cohere, separate=separate, match=match)
        self.select = select
        self.make_agents()
        self.running = True
        self.datacollector = DataCollector(
            model_reporters={"Velocity": get_average_speed}
        )
        self.datacollector.collect(self)

    def make_agents(self):
        """
        Create self.population agents, with random positions and starting headings.
        """
        for i in range(self.population):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            boid = Boid(
                i,
                self,
                pos,
                i==self.select,
                self.speed,
                velocity,
                self.vision,
                self.separation,
                **self.factors,
            )
            self.space.place_agent(boid, pos)
            self.schedule.add(boid)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
