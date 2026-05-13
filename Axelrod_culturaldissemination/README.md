# Axelrod Cultural Dissemination Model

This project implements Robert Axelrod’s cultural dissemination model as an agent-based simulation using Python, Mesa, and Solara. The model reproduces the core mechanism described in Axelrod’s paper, where local interactions between agents can simultaneously generate cultural convergence and persistent cultural diversity.

## Overview

Each agent occupies a position on a 2D grid and possesses a cultural vector composed of multiple features. Each feature can take one of several possible traits. Agents interact only with their local neighbors, and the probability of interaction depends on how culturally similar the two agents already are.

The model demonstrates an important paradox explored in the original paper:

> Local convergence between similar individuals can generate stable global polarization.

# Project Structure

```text
Axelrod_cultural_dissemination/
│
├── agent.py      # Agent behavior and interaction rules
├── model.py      # Mesa model and scheduler
├── app.py        # Solara visualization app
├── README.md
