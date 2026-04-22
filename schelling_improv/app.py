import solara
from model import SchellingModel
from mesa.visualization import (  
    SolaraViz,
    make_space_component,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle

## Define agent portrayal: color, shape, and size
def agent_portrayal(agent):
    # Define base colors for light (desired_share_alike=0) and dark (desired_share_alike=1)
    if agent.type == 1:
        # Blue gradient: light blue to dark blue
        light_r, light_g, light_b = 173, 216, 230  # Light blue
        dark_r, dark_g, dark_b = 0, 0, 255  # Dark blue
    else:
        # Red gradient: light red to dark red
        light_r, light_g, light_b = 255, 182, 193  # Light pink/red
        dark_r, dark_g, dark_b = 255, 0, 0  # Dark red
    
    # Interpolate based on desired_share_alike
    r = int(light_r + (dark_r - light_r) * agent.desired_share_alike)
    g = int(light_g + (dark_g - light_g) * agent.desired_share_alike)
    b = int(light_b + (dark_b - light_b) * agent.desired_share_alike)
    
    color = (r / 255, g / 255, b / 255)
    
    return AgentPortrayalStyle(
        color=color,
        marker="s",
        size=75,
    )

## Enumerate variable parameters in model: seed, grid dimensions, population density, agent preferences, vision, and relative size of groups.
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
    "density": {
        "type": "SliderFloat",
        "value": 0.7,
        "label": "Population Density",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "group_one_share": {
        "type": "SliderFloat",
        "value": 0.7,
        "label": "Share Type 1 Agents",
        "min": 0,
        "max": 1,
        "step": 0.01,
    },
    "radius": {
        "type": "SliderInt",
        "value": 1,
        "label": "Vision Radius",
        "min": 1,
        "max": 5,
        "step": 1,
    },
}

## Instantiate model
schelling_model = SchellingModel()

## Define happiness over time plot
HappyPlot = make_plot_component({"share_happy": "tab:green"})

## Define space component
SpaceGraph = make_space_component(agent_portrayal, draw_grid=False)

## Instantiate page inclusing all components
page = SolaraViz(
    schelling_model,
    components=[SpaceGraph, HappyPlot],
    model_params=model_params,
    name="Schelling Segregation Model",
)
## Return page
page
    
