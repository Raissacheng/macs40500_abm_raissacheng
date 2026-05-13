from mesa import Model
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from agents import AxelrodAgent


class AxelrodModel(Model):
    def __init__(
        self,
        width=30,
        height=30,
        num_features=5,
        num_traits=10,
        density=1.0,
        seed=None,
    ):
        super().__init__(rng=seed)

        self.width = width
        self.height = height
        self.num_features = num_features
        self.num_traits = num_traits
        self.density = density

        self.grid = SingleGrid(width, height, torus=True)

        # Data collector
        self.datacollector = DataCollector(
            model_reporters={
                "avg_similarity": self.compute_average_similarity,
            }
        )

        # Create agents
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.density:
                agent = AxelrodAgent(self, num_features, num_traits)
                self.grid.place_agent(agent, pos)

        self.datacollector.collect(self)

    def compute_average_similarity(self):
        total = 0
        count = 0

        for agent in self.agents:
            neighbors = self.grid.get_neighbors(
                agent.pos, moore=False, include_center=False
            )
            for n in neighbors:
                total += agent.similarity(n)
                count += 1

        return total / count if count > 0 else 0

    def is_in_equilibrium(self):
        """Check if interactions are possible"""
        for agent in self.agents:
            neighbors = self.grid.get_neighbors(agent.pos, moore=False)
            for neighbor in neighbors:
                sim = agent.similarity(neighbor)
                if sim > 0 and sim < 1:
                    return False
        return True

    def step(self): 
        # Synchronous update: shuffle agents and execute each step
        agents = list(self.agents)
        self.random.shuffle(agents)
        for agent in agents:
            agent.step()
        self.datacollector.collect(self)
        self.running = not self.is_in_equilibrium()