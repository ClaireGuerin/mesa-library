from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from .portrayal import portrayPDAgent
from .model import PdGrid


# Make a world that is 50x50, on a 500x500 display.
canvas_element = CanvasGrid(portrayPDAgent, 50, 50, 500, 500)

model_params = {
    "height": 50,
    "width": 50,
    "schedule_type": UserSettableParameter(
        "choice",
        "Scheduler type",
        value="Random",
        choices=list(PdGrid.schedule_types.keys()),
    ),
    "CC": UserSettableParameter("number", name="Payoff for a Cooperator set against a Cooperator", value=1),
    "CD": UserSettableParameter("number", name="Payoff for a Cooperator set against a Defector", value=0),
    "DC": UserSettableParameter("number", name="Payoff for a Defector set against a Cooperator", value=1.6),
    "DD": UserSettableParameter("number", name="Payoff for a Defector set against a Defector", value=0)
}

line_chart = ChartModule(
    [{"Label": "Cooperating Agents", "Color": "yellow"},
     {"Label": "Defecting Agents", "Color": "purple"}],
    data_collector_name="datacollector"
)

server = ModularServer(PdGrid, [canvas_element, line_chart], "Prisoner's Dilemma", model_params)
