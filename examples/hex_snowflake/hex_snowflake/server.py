from mesa.visualization.modules import CanvasHexGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from hex_snowflake.portrayal import portrayCell
from hex_snowflake.model import HexSnowflake

width, height = 50, 50

# Make a world that is 50x50, on a 500x500 display.
canvas_element = CanvasHexGrid(portrayCell, width, height, 500, 500)

""" model_params = dict(
    height=UserSettableParameter("slider", name="Grid Height", value=height, min_value=50, max_value=100, step=10),
    width=UserSettableParameter("slider", name="Grid Width", value=width, min_value=50, max_value=100, step=10)
) """

model_params = {"height": height, "width": width}

server = ModularServer(
    HexSnowflake, [canvas_element], "Hex Snowflake", model_params
)
