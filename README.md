# Dynamic Tech Display

## Project Description
This repository hosts "Dynamic Tech Display," a Python application utilizing the Pygame library to generate a mesmerizing and interactive visual experience. It showcases three distinct animated modes: a captivating starfield, abstract flowing pipes, and a classic binary rain effect. Users can seamlessly switch between modes, control animation speeds, and customize various visual parameters to tailor the display.

## Features
- **Three Dynamic Visual Modes:**
    - **Stars Mode:** Simulates a journey through a starfield with customizable star density, shapes (circles and squares), and vibrant, tech-inspired color palettes for background nebulas. Stars flicker and vary in size based on their simulated distance, creating a sense of depth and motion.
    - **Pipes Mode:** Generates abstract, flowing pipe-like structures that emerge from the screen edges and gracefully traverse the display. Pipes are composed of interconnected segments, offering a dynamic and evolving visual.
    - **Binary Mode:** Emulates the iconic "Matrix" rain effect, displaying falling columns of binary digits (0s and 1s). Features a distinctive fading trail and a bright, leading character.
- **Smooth Mode Transitions:** Seamlessly switch between the different display modes with a fluid fade-to-black and fade-in effect.
- **Global Speed Control:** Adjust the overall animation speed across all modes.

## Dependencies
- Python 3.x
- Pygame

## Installation
1.  **Ensure Python is installed:** If you don't have Python, download and install it from [python.org](https://www.python.org/).
2.  **Install Pygame:** Open your terminal or command prompt and run the following command:
    ```bash
    pip install pygame
    ```

## Running the Script
1.  Navigate to the directory where you saved `starfield.py`.
2.  Run the script using Python:
    ```bash
    python starfield.py
    ```

## Interactive Controls
- **UP Arrow:** Increase global animation speed.
- **DOWN Arrow:** Decrease global animation speed.
- **1:** Switch to Stars Mode.
- **2:** Switch to Pipes Mode.
- **3:** Switch to Binary Mode.
- **LEFT Arrow (Stars Mode only):** Decrease the density of stars.
- **RIGHT Arrow (Stars Mode only):** Increase the density of stars.
- **R (Stars Mode only):** Randomize the nebula color palette.
- **ESC:** Exit the application.

## Customizable Parameters
The `starfield.py` script allows for easy modification of several core settings. You can adjust these parameters directly within the script:
- **Screen Dimensions:** `SCREEN_WIDTH`, `SCREEN_HEIGHT`
- **General:** `FPS` (Frames Per Second)
- **Stars Mode:**
    - `NUM_STARS`: Default number of stars.
    - `STAR_DENSITY`: Initial density of stars (0.1 to 1.0).
    - `TECH_STAR_COLORS`: List of possible star colors.
    - `STAR_VIEW_DISTANCE`: Initial Z-depth of stars.
    - `STAR_FOCAL_LENGTH`: Controls the perspective effect.
    - `NUM_NEBULAE`: Number of nebula elements.
    - `NEBULA_PALETTES`: Predefined color palettes for nebulas.
- **Pipes Mode:**
    - `PIPE_COLOR`, `PIPE_COLOR_ALT`: Colors for pipe segments.
    - `PIPE_THICKNESS`: Base thickness of pipes.
    - `PIPE_MAX_LENGTH`, `PIPE_MIN_LENGTH`: Length range for pipe segments.
    - `PIPE_SPAWN_INTERVAL`: How often new pipes are generated.
    - `PIPE_LIFETIME`: How long pipes persist.
- **Binary Mode:**
    - `FONT_SIZE`: Size of the binary characters.
    - `BINARY_DROP_SPEED_MIN`, `BINARY_DROP_SPEED_MAX`: Range for falling speed of columns.
    - `BINARY_TEXT_COLORS`: Colors for the trailing characters.
    - `BINARY_ACTIVE_COLOR`: Color for the leading character in a column.
    - `BINARY_TRAIL_LENGTH`: Number of characters in a fading trail.
- **Transitions:**
    - `transition_speed`: Speed of the fade-in/fade-out effect between modes.
