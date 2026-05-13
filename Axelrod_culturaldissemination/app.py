import solara
import matplotlib.pyplot as plt
from model import AxelrodModel
from mesa.visualization import SolaraViz
from mesa.visualization.utils import update_counter


# Boundary visualization
def cultural_boundary_plot(model):

    fig, ax = plt.subplots(figsize=(8, 8))

    width = model.width
    height = model.height

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)

    ax.set_xticks([])
    ax.set_yticks([])

    # Draw boundaries
    for x in range(width):
        for y in range(height):

            contents = model.grid.get_cell_list_contents((x, y))

            if not contents:
                continue

            agent = contents[0]

            # RIGHT neighbor
            if x < width - 1:

                neighbor_contents = model.grid.get_cell_list_contents((x + 1, y))

                if neighbor_contents:

                    neighbor = neighbor_contents[0]

                    sim = agent.similarity(neighbor)
                    boundary = 1 - sim

                    ax.plot(
                        [x + 1, x + 1],
                        [y, y + 1],
                        color="black",
                        linewidth=boundary * 5,
                        alpha=boundary,
                    )

            # TOP neighbor
            if y < height - 1:

                neighbor_contents = model.grid.get_cell_list_contents((x, y + 1))

                if neighbor_contents:

                    neighbor = neighbor_contents[0]

                    sim = agent.similarity(neighbor)
                    boundary = 1 - sim

                    ax.plot(
                        [x, x + 1],
                        [y + 1, y + 1],
                        color="black",
                        linewidth=boundary * 5,
                        alpha=boundary,
                    )

    ax.invert_yaxis()

    return solara.FigureMatplotlib(fig)

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": {
        "type": "SliderInt",
        "value": 30,
        "label": "Width",
        "min": 5,
        "max": 100,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 30,
        "label": "Height",
        "min": 5,
        "max": 100,
        "step": 1,
    },
    "num_features": {
        "type": "SliderInt",
        "value": 5,
        "label": "Features",
        "min": 2,
        "max": 15,
        "step": 1,
    },
    "num_traits": {
        "type": "SliderInt",
        "value": 10,
        "label": "Traits",
        "min": 2,
        "max": 20,
        "step": 1,
    },
}

model = AxelrodModel()

page = SolaraViz(
    model,
    components=[cultural_boundary_plot],
    model_params=model_params,
    name="Axelrod Cultural Dissemination",
)

page