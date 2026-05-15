from mesa import Agent
import random
import math


class FriendshipAgent(Agent):
    """
    Agent representing an individual in the friendship formation model.
    """

    def __init__(self, model):
        super().__init__(model)

        # Four nominal traits
        # Use clustered distributions instead of pure uniform to avoid everyone becoming too similar
        self.cluster_center = random.choice([0.2, 0.5, 0.8])

        self.traits = [
            min(1, max(0, random.gauss(self.cluster_center, 0.12)))
            for _ in range(4)
        ]

        # Memory dictionaries
        self.familiarity = {}      # repeated exposure count
        self.liking = {}           # liking score
        self.relationships = set()

    # ---------------------------------------------------
    # Similarity
    # ---------------------------------------------------

    def similarity(self, other):
        """
        Calculate Euclidean-distance similarity; Higher = more similar

        Returns: value between 0 and 1
        """

        dist = math.sqrt(
            sum(
                (a - b) ** 2
                for a, b in zip(self.traits, other.traits)
            )
        )

        max_dist = math.sqrt(4)

        similarity_score = 1 - (dist / max_dist)

        return similarity_score

    # ---------------------------------------------------
    # Movement
    # ---------------------------------------------------

    def move(self):
        """
        Agents move randomly until they form a friendship, then they become stationary.
        """

        # Once an agent has at least one friend, it stops moving permanently.
        if len(self.relationships) > 0:
            return

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        empty_steps = [
            pos for pos in possible_steps
            if self.model.grid.is_cell_empty(pos)
        ]

        if len(empty_steps) > 0:
            new_position = random.choice(empty_steps)
            self.model.grid.move_agent(self, new_position)

    # ---------------------------------------------------
    # Social interaction
    # ---------------------------------------------------

    def interact(self):
        """
        Observe nearby agents and update:
        - familiarity
        - liking
        - close relationships
        """

        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=self.model.vision_radius
        )

        for other in neighbors:

            if other.unique_id == self.unique_id:
                continue

            other_id = other.unique_id

            # Familiarity increases with repeated exposure
            self.familiarity[other_id] = (
                self.familiarity.get(other_id, 0) + 1
            )

            familiarity_score = (
                self.familiarity[other_id] / self.model.max_familiarity
            )

            # capping condition: never existed 1.0 (the score does not increase when two become fully familiar)
            familiarity_score = min(1, familiarity_score)

            # Similarity score
            similarity_score = self.similarity(other)

            # Combined liking
            liking_score = (
                self.model.similarity_weight * similarity_score
                + self.model.familiarity_weight * familiarity_score
            )

            self.liking[other_id] = liking_score

            # Relationship formation
            if liking_score >= self.model.relationship_threshold:
                self.relationships.add(other_id)

    # ---------------------------------------------------
    # Step
    # ---------------------------------------------------

    def step(self):

        self.move()
        self.interact()