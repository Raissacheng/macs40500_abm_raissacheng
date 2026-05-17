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

    # ---------------------------------------------------
    # Draw neighborhood boundary field + agent overlay
    # ---------------------------------------------------

    max_relationships = max(
        1,
        max((len(agent.relationships) for agent in model.agents), default=0)
    )

    for x in range(width):
        for y in range(height):

            cell = model.grid.get_cell_list_contents((x, y))

            if not cell:
                continue

            agent = cell[0]

            # -----------------------------------
            # Compute local boundary strength
            # -----------------------------------

            neighbors = model.grid.get_neighbors(
                (x, y),
                moore=True,
                include_center=False,
                radius=1
            )

            if neighbors:

                avg_similarity = sum(
                    agent.similarity(neighbor)
                    for neighbor in neighbors
                ) / len(neighbors)

                boundary_strength = 1 - avg_similarity

            else:
                boundary_strength = 0

            # -----------------------------------
            # Background = local boundary field
            # -----------------------------------

            boundary_color = plt.cm.Greys(boundary_strength)

            ax.add_patch(
                plt.Rectangle(
                    (x, y),
                    1,
                    1,
                    facecolor=boundary_color,
                    edgecolor=None,
                    alpha=0.6,
                )
            )

            # -----------------------------------
            # Agent color = relationship status
            # -----------------------------------

            relation_count = len(agent.relationships)

            if relation_count == 0:

                agent_color = "lightblue"

            else:

                ratio = relation_count / max_relationships

                agent_color = plt.cm.Blues(
                    0.4 + 0.6 * ratio
                )

            # -----------------------------------
            # Draw smaller agent square
            # -----------------------------------

            ax.add_patch(
                plt.Rectangle(
                    (x + 0.2, y + 0.2),
                    0.6,
                    0.6,
                    facecolor=agent_color,
                    edgecolor='black',
                    linewidth=0.5,
                    alpha=1.0,
                )
            )

    ax.invert_yaxis()

    return solara.FigureMatplotlib(fig)


# ---------------------------------------------------
# Graph: relationship density over time
# ---------------------------------------------------

def relationship_over_time(model):

    fig, ax = plt.subplots(figsize=(7, 4))

    data = model.datacollector.get_model_vars_dataframe()

    relationships = data["Relationships"]

    # the graph
    ax.plot(relationships)

    ax.set_title("Number of Close Relationships Over Time")
    ax.set_xlabel("Step")
    ax.set_ylabel("Relationships")

    # current exact count
    current_count = relationships.iloc[-1]

    info_text = (
        f"Current Relationships: {current_count:.0f}"
    )

    # text under graph
    fig.text(
        0.5,
        0.01,
        info_text,
        ha='center',
        fontsize=10,
    )

    plt.tight_layout(rect=[0, 0.05, 1, 1])

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