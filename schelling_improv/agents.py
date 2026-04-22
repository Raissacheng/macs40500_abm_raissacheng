from mesa import Agent
import random

class SchellingAgent(Agent):
    ## Initiate agent instance, inherit model trait from parent class
    def __init__(self, model, agent_type):
        super().__init__(model) # Essence: calling the initiation from the parent class
        ## Set agent type
        self.type = agent_type
        ## Set individual desired share alike randomly between 0 and 1
        self.desired_share_alike = self.random.random()

    ## Define basic decision rule
    def move(self):
        ## Get list of neighbors within range of sight
        neighbors = self.model.grid.get_neighbors(
           self.pos, moore=True, include_center=False, radius=self.model.radius)
        
        ## Count neighbors of same type as self
        similar_neighbors = len([neighbor for neighbor in neighbors if neighbor.type == self.type])

        ## If an agent has any neighbors (to avoid division by zero), calculate share of neighbors of same type
        if len(neighbors) > 0:
            share_alike = similar_neighbors / len(neighbors)
        else:
            share_alike = 0

        ## If unhappy with neighbors, move to random empty slot. Otherwise add one to model count of happy agents.
        if share_alike < self.desired_share_alike:
            # Find all empty cells
            empty_cells = [
                (x, y)
                for x in range(self.model.grid.width)
                for y in range(self.model.grid.height)
                if self.model.grid.is_cell_empty((x, y))
            ]
            if empty_cells:
                new_pos = random.choice(empty_cells)
                self.model.grid.move_agent(self, new_pos)
        else: 
            self.model.happy += 1
