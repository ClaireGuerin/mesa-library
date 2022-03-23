from mesa.visualization.ModularVisualization import ModularServer

from .model import BoidFlockers
from .SimpleContinuousModule import SimpleCanvas
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

line_chart = ChartModule([{"Label": "Velocity", "Color": "Teal"}], 
                         data_collector_name="datacollector")

def boid_draw(agent):
    portrayal = {}
    
    if agent.selected:
        portrayal["Shape"] = "rect"
        portrayal["h"] = 0.02
        portrayal["w"] = 0.02
        portrayal["Filled"] = "false"
        portrayal["Color"] = "DarkSlateGray"
    else:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 2
        portrayal["Filled"] = "true"
        portrayal["Color"] = "Teal"
        
    return portrayal

boid_canvas = SimpleCanvas(boid_draw, 500, 500)
model_params = {
    "schedule_type": UserSettableParameter(
        "choice",
        "Scheduler type",
        value="Random",
        choices=list(BoidFlockers.schedule_types.keys()),
    ),
    "population": UserSettableParameter("slider", name="Population size", value=100, min_value=100, max_value=1000),
    "width": 100,
    "height": 100,
    "speed": 5,
    "vision": 10,
    "separation": 2,
    "cohere": UserSettableParameter("slider", name="Cohesion", value=0.45, min_value=0.1, max_value=0.9, step=0.1),
    "separate": UserSettableParameter("slider", name="Separation", value=0.45, min_value=0.1, max_value=0.9, step=0.1),
    "match": UserSettableParameter("slider", name="Alignment", value=0.45, min_value=0.1, max_value=0.9, step=0.1),
    #"select": UserSettableParameter("number", "Select individual", 0, 0, 1000, 1)
}

server = ModularServer(BoidFlockers, [boid_canvas, line_chart], "Boids", model_params)
