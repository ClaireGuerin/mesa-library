from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from .portrayal import portrayCell
from .model import ConwaysGameOfLife

model_params = {
    "prob": UserSettableParameter("slider", name="Initial live proportion", value=0.1, min_value=0.0, max_value=1.0, step=0.1),
    "height": 50, 
    "width": 50
}

# Draw a line chart of the real-time number of live cells.
chart_live_cells = ChartModule([{"Label": "NLiveCells", "Color": "Black"}], 
                         data_collector_name="datacollector")

# Make a world that is 50x50, on a 250x250 display.
canvas_element = CanvasGrid(portrayCell, 50, 50, 500, 500)

server = ModularServer(
    ConwaysGameOfLife, 
    [canvas_element, chart_live_cells], 
    "Game of Life", 
    model_params
)
