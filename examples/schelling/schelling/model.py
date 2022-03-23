from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


class SchellingAgent(Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, pos, model, agent_type):
        """
        Create a new Schelling agent.

        Args:
           unique_id: Unique identifier for the agent.
           x, y: Agent initial location.
           agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    def step(self):
        similar = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:
                similar += 1

        # If unhappy, move:
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1


class Schelling(Model):
    """
    Schelling's model of segregation. 
    Agents are split into two groups and occupy the spaces of the grid and only one agent can occupy a space at a time. 
    Agents desire a fraction of their neighborhood to be from the same group. 
    Increasing this fraction corresponds to increasing the agent's intolerance of outsiders.
    Each round consists of agents checking their neighborhood to see if the fraction of neighbors 
    that matches their group is greater than or equal to their preferred fraction. 
    If not, then the agent will choose to relocate to a vacant spot. 
    This continues until every agent is satisfied.
    """

    def __init__(self, width=20, height=20, density=0.8, minority_pc=0.2, homophily=3, select=None):
        """ """

        self.width = width
        self.height = height
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily
        self.select = select

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        self.happy = 0
        self.datacollector = DataCollector(
            {"happy": "happy"},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        unique_id = 0
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if self.random.random() < self.minority_pc:
                    agent_type = 1
                else:
                    agent_type = 0

                agent = SchellingAgent((x, y), self, agent_type)
                agent.selected = unique_id == self.select
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)
                unique_id += 1

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.happy = 0  # Reset counter of happy agents
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False