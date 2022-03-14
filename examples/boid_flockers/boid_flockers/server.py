from mesa.visualization.ModularVisualization import ModularServer

from .model import BoidFlockers
from .SimpleContinuousModule import SimpleCanvas
from mesa.visualization.UserParam import UserSettableParameter


def boid_draw(agent):
    return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Red"}


boid_canvas = SimpleCanvas(boid_draw, 500, 500)
model_params = {
    "schedule_type": UserSettableParameter(
        "choice",
        "Scheduler type",
        value="Random",
        choices=list(BoidFlockers.schedule_types.keys()),
    ),
    "population": UserSettableParameter("slider", "Population size", 10, 100, 1000),
    "width": 100,
    "height": 100,
    "speed": 5,
    "vision": 10,
    "separation": 2
}

server = ModularServer(BoidFlockers, [boid_canvas], "Boids", model_params)
