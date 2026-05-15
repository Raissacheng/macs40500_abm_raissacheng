from mesa import Model
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from agents import FriendshipAgent

import networkx as nx


class FriendshipModel(Model):

    def __init__(
        self,
        width=25,
        height=25,
        num_agents=80,
        relationship_threshold=0.72,
        familiarity_weight=0.5,
        similarity_weight=0.5,
        max_familiarity=15,
        seed=None
    ):

        super().__init__(seed=seed)

        self.width = width
        self.height = height
        self.num_agents = num_agents

        self.relationship_threshold = relationship_threshold

        self.familiarity_weight = familiarity_weight
        self.similarity_weight = similarity_weight

        self.vision_radius = 1

        self.max_familiarity = max_familiarity

        self.grid = SingleGrid(width, height, torus=True)

        # Generate all coordinates
        all_positions = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
        ]

        # Shuffle positions
        self.random.shuffle(all_positions)

        # Limit num_agents to available positions
        actual_num_agents = min(self.num_agents, len(all_positions))
        self.num_agents = actual_num_agents  # Update to actual number placed

        # Use unique positions only
        for i in range(actual_num_agents):

            agent = FriendshipAgent(self)

            position = all_positions[i]

            self.grid.place_agent(agent, position)        

        # Data collection
        self.datacollector = DataCollector(
            model_reporters={
                "Relationships": self.count_relationships,
                "Average Liking": self.average_liking,
            }
        )

        self.running = True

        self.datacollector.collect(self)

    # ---------------------------------------------------
    # Metrics
    # ---------------------------------------------------

    def count_relationships(self):

        total = sum(
            len(agent.relationships)
            for agent in self.agents
        )

        # divide by 2 because relationships are double counted
        return total / 2

    def average_liking(self):

        liking_values = []

        for agent in self.agents:

            liking_values.extend(agent.liking.values())

        if len(liking_values) == 0:
            return 0

        return sum(liking_values) / len(liking_values)

    # ---------------------------------------------------
    # Relationship Network
    # ---------------------------------------------------

    def relationship_network(self):

        G = nx.Graph()

        for agent in self.agents:

            G.add_node(agent.unique_id)

            for friend_id in agent.relationships:

                G.add_edge(agent.unique_id, friend_id)

        return G

    # ---------------------------------------------------
    # Termination
    # ---------------------------------------------------

    def no_agent_can_move(self):
        """Stop when every agent has at least one friendship and therefore stops moving."""

        return all(
            len(agent.relationships) > 0
            for agent in self.agents
        )

    # ---------------------------------------------------
    # Step
    # ---------------------------------------------------

    def step(self):

        self.agents.shuffle_do("step")

        self.datacollector.collect(self)

        if self.no_agent_can_move():
            self.running = False