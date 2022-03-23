from mesa.visualization.ModularVisualization import ModularServer
from .model import BoltzmannWealthModel

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    portrayal = {"Filled": "true"}
    
    if agent.selected:
        portrayal["Shape"] = "rect"
        portrayal["h"] = 0.5
        portrayal["w"] = 0.5
    else:
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5

    if agent.wealth > 0:
        portrayal["Color"] = "#e7298a"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "#66c2a5"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
chart = ChartModule(
    [{"Label": "Gini Coefficient", "Color": "Black"}], data_collector_name="datacollector"
)

model_params = {
    "N": UserSettableParameter(
        "slider",
        "Number of agents",
        100,
        2,
        200,
        1,
        description="Choose how many agents to include in the model",
    ),
    "width": 10,
    "height": 10,
    "select": UserSettableParameter(
        "number",
        "Select agent",
        0,
        0,
        200,
        1
    )
}

server = ModularServer(BoltzmannWealthModel, [grid, chart], "Money Model", model_params)
server.port = 8521
