from mesa import Agent
import random


class AxelrodAgent(Agent):
    def __init__(self, model, num_features, num_traits):
        super().__init__(model)
        self.num_features = num_features
        self.num_traits = num_traits

        # Initialize culture vector
        self.culture = [
            self.random.randrange(num_traits) for _ in range(num_features)
        ]

    def similarity(self, other):
        matches = sum(
            1 for a, b in zip(self.culture, other.culture) if a == b
        )
        return matches / self.num_features

    def interact(self, other):
        differing = [
            i for i, (a, b) in enumerate(zip(self.culture, other.culture))
            if a != b
        ]

        if differing:
            f = self.random.choice(differing)
            self.culture[f] = other.culture[f]

    def step(self):
        # Pick random neighbor
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=False, include_center=False
        )

        if not neighbors:
            return

        neighbor = self.random.choice(neighbors)

        sim = self.similarity(neighbor)

        # Interaction with probability = similarity
        if self.random.random() < sim:
            self.interact(neighbor)