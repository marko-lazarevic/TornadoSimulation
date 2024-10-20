# Tornado Simulation Project

This project is a Tornado Simulation that models the behavior of an object caught in a tornado. The simulation allows the user to control parameters such as the launch angle, initial speed, and tornado strength. The results are visualized in a 3D animated plot using `matplotlib` and an interactive GUI made with `tkinter`.

## Example simulation

![seminarski](https://github.com/user-attachments/assets/dabd33b3-4932-49d9-8dfd-41fdf43699e8)


## File Descriptions

### `animacija.py`

This file contains the main simulation logic for the tornado, user input sliders for angle, speed, and tornado strength using `tkinter`. It creates a 3D animation showing the movement of an object under the influence of a tornado.

- **Key Functions**:
  - `tornado(ALPHA, V0, TORNADO)`: Simulates the movement of an object based on parameters such as launch angle (`ALPHA`), initial speed (`V0`), and tornado strength (`TORNADO`).
  - The GUI uses `tkinter` to provide sliders for user input. The simulation result is then animated using `matplotlib`'s `FuncAnimation`.

### `tornado_slajderi.py`

This file contains an alternate version of the tornado simulation where the tornado's power can be adjusted using dropdown menus, and sliders control the launch angle and speed. It includes 3D visualization of the object's trajectory, as well as additional concentric tornado lines for better representation of tornado behavior.

- **Key Features**:
  - Sliders for controlling launch speed and angle.
  - Dropdown menu for tornado intensity selection.
  - The `tornado` function computes the trajectory, and `matplotlib` is used to visualize it in a 3D space.
  - The animation is updated dynamically with `matplotlib.animation.FuncAnimation`.

## Usage

1. Adjust the parameters using the sliders in the GUI:
   - **Angle**: Launch angle of the object (10-90 degrees).
   - **Speed**: Initial speed of the object (50-150).
   - **Tornado Strength**: Intensity of the tornado (25-100).

2. After setting your desired parameters, click the button to animate the trajectory of the object in the tornado's influence.

Enjoy experimenting with different parameters to see how the object's trajectory changes based on tornado strength and launch conditions!
