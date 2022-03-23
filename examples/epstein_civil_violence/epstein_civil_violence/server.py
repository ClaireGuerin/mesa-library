from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from .model import EpsteinCivilViolence
from .agent import Citizen, Cop


COP_COLOR = "#000000"
AGENT_QUIET_COLOR = "#1b9e77"
AGENT_REBEL_COLOR = "#d95f02"
JAIL_COLOR = "#7570b3"

COP_SIZE = 0.5
CITIZEN_SIZE = 0.8


def citizen_cop_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "rect" if agent.selected else "circle",
        "x": agent.pos[0],
        "y": agent.pos[1],
        "Filled": "true",
    }

    if type(agent) is Citizen:
        color = (
            AGENT_QUIET_COLOR if agent.condition == "Quiescent" else AGENT_REBEL_COLOR
        )
        color = JAIL_COLOR if agent.jail_sentence else color
        #portrayal["Shape"] = "circle"
        portrayal["Color"] = color
        portrayal["r"] = CITIZEN_SIZE
        portrayal["h"] = CITIZEN_SIZE
        portrayal["w"] = CITIZEN_SIZE
        portrayal["Layer"] = 0

    elif type(agent) is Cop:
        portrayal["Color"] = COP_COLOR
        #portrayal["Shape"] = "rect"
        portrayal["r"] = COP_SIZE
        portrayal["h"] = COP_SIZE
        portrayal["w"] = COP_SIZE
        portrayal["Layer"] = 1
    return portrayal


model_params = dict(
    height=40,
    width=40,
    citizen_density=UserSettableParameter("slider", name="Citizen Density", value=0.7, min_value=0.1, max_value=0.9, step=0.1),
    cop_density=UserSettableParameter("slider", name="Cop Density", value=0.074, min_value=0.1, max_value=0.9, step=0.1),
    citizen_vision=7,
    cop_vision=7,
    legitimacy=0.8,
    max_jail_term=1000,
    select=UserSettableParameter(
        "number",
        "Select agent",
        0,
        0,
        200,
        1
    )
)

agent_chart = ChartModule([
        {"Label": "Quiescent", "Color": AGENT_QUIET_COLOR},
        {"Label": "Active", "Color": AGENT_REBEL_COLOR},
        {"Label": "Jailed", "Color": JAIL_COLOR}
    ]
)

canvas_element = CanvasGrid(citizen_cop_portrayal, 40, 40, 480, 480)
server = ModularServer(
    EpsteinCivilViolence, [canvas_element, agent_chart], "Epstein Civil Violence", model_params
)
