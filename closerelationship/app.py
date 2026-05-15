import solara
import matplotlib.pyplot as plt

from model import FriendshipModel
from mesa.visualization import SolaraViz


# ---------------------------------------------------
# Boundary visualization
# ---------------------------------------------------

def friendship_boundary_plot(model):

    fig, ax = plt.subplots(figsize=(8, 8))

    width = model.width
    height = model.height

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_xticks([])
    ax.set_yticks([])

    # Draw grid background - grey for empty cells
    for x in range(width):
        for y in range(height):
            if model.grid.is_cell_empty((x, y)):
                ax.add_patch(plt.Rectangle((x, y), 1, 1, color='lightgrey', alpha=0.3))

    # Draw agent squares with blue gradient based on the number of relationships
    max_relationships = max(
        1,
        max((len(agent.relationships) for agent in model.agents), default=0)
    )

    for x in range(width):
        for y in range(height):
            cell = model.grid.get_cell_list_contents((x, y))
            if cell:
                agent = cell[0]
                relation_count = len(agent.relationships)
                ratio = relation_count / max_relationships

                # Light blue for agents with no relationships, darker blue as relationship count increases.
                color = plt.cm.Blues(0.15 + 0.75 * ratio)

                ax.add_patch(
                    plt.Rectangle(
                        (x, y),
                        1,
                        1,
                        facecolor=color,
                        edgecolor='black',
                        linewidth=0.5,
                        alpha=0.9,
                    )
                )

    # Draw relationship boundaries
    for x in range(width):
        for y in range(height):
            cell = model.grid.get_cell_list_contents((x, y))
            if not cell:
                continue

            agent = cell[0]

            # -------------------
            # RIGHT neighbor
            # -------------------
            if x < width - 1:

                neighbor_cell = model.grid.get_cell_list_contents((x + 1, y))
                if neighbor_cell:
                    neighbor = neighbor_cell[0]

                    # Check if agents have a relationship
                    has_relationship = (
                        neighbor.unique_id in agent.relationships or
                        agent.unique_id in neighbor.relationships
                    )

                    if has_relationship:
                        linestyle = "solid"
                    else:
                        linestyle = "dashed"

                    sim = agent.similarity(neighbor)
                    boundary = 1 - sim

                    ax.plot(
                        [x + 1, x + 1],
                        [y, y + 1],
                        color="black",
                        linewidth=0.5 + sim * 4,  # Thicker boundaries = more similar
                        alpha=0.2 + sim * 0.8,
                        linestyle=linestyle,
                    )

            # -------------------
            # TOP neighbor
            # -------------------
            if y < height - 1:

                neighbor_cell = model.grid.get_cell_list_contents((x, y + 1))
                if neighbor_cell:
                    neighbor = neighbor_cell[0]

                    # Check if agents have a relationship
                    has_relationship = (
                        neighbor.unique_id in agent.relationships or
                        agent.unique_id in neighbor.relationships
                    )

                    if has_relationship:
                        linestyle = "solid"
                    else:
                        linestyle = "dashed"

                    sim = agent.similarity(neighbor)
                    boundary = 1 - sim

                    ax.plot(
                        [x, x + 1],
                        [y + 1, y + 1],
                        color="black",
                        linewidth=0.5 + sim * 4,  # Thicker = more similar
                        alpha=0.2 + sim * 0.8,    # More opaque = more similar
                        linestyle=linestyle,
                    )

    ax.invert_yaxis()

    return solara.FigureMatplotlib(fig)


# ---------------------------------------------------
# Graph: relationship density over time
# ---------------------------------------------------

def relationship_over_time(model):

    fig, ax = plt.subplots()

    data = model.datacollector.get_model_vars_dataframe()

    ax.plot(data["Relationships"])
    ax.set_title("Number of Close Relationships Over Time")
    ax.set_xlabel("Step")
    ax.set_ylabel("Relationships")

    return solara.FigureMatplotlib(fig)


# ---------------------------------------------------
# Model parameters
# ---------------------------------------------------

model_params = {

    "width": {
        "type": "SliderInt",
        "value": 25,
        "label": "Width",
        "min": 10,
        "max": 50,
        "step": 1,
    },

    "height": {
        "type": "SliderInt",
        "value": 25,
        "label": "Height",
        "min": 10,
        "max": 50,
        "step": 1,
    },

    "num_agents": {
        "type": "SliderInt",
        "value": 80,
        "label": "Number of Agents",
        "min": 10,
        "max": 2500,
        "step": 10,
    },

    "relationship_threshold": {
        "type": "SliderFloat",
        "value": 0.72,
        "label": "Relationship Threshold",
        "min": 0.3,
        "max": 1.0,
        "step": 0.01,
    },

    "familiarity_weight": {
        "type": "SliderFloat",
        "value": 0.5,
        "label": "Familiarity Weight",
        "min": 0.0,
        "max": 1.0,
        "step": 0.05,
    },

    "similarity_weight": {
        "type": "SliderFloat",
        "value": 0.5,
        "label": "Similarity Weight",
        "min": 0.0,
        "max": 1.0,
        "step": 0.05,
    },
}


model = FriendshipModel()

page = SolaraViz(
    model,
    components=[
        friendship_boundary_plot,
        relationship_over_time,
    ],
    model_params=model_params,
    name="Friendship Formation Model",
)

page