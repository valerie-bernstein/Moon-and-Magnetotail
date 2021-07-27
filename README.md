# Identifying and visualizing the moon's position with respect to the Earth's magnetotail

This work contributed in a small way to the experimental design of the [Deep Space Radiation Genomics (DSRG)](https://www.colorado.edu/faculty/zea-luis/deep-space-radiation-genomics-dsrg-artemis-1) experiment on Artemis 1. The DSRG experiment will orbit the moon, and the goal of the experiment is to expose a collection of yeast to a space radiation environment similar to that expected for a trip beyond Earth's protective magnetospheric environment. This will enable the analysis of the effect of microgravity and space radiation in genes.

To ensure the experiment encounters 'pristine' solar wind conditions, it is important to avoid data collection during the spacecraft's (and consequently, the moon's) transit through the magnetotail. The solar wind interacts with the Earth's magnetic field to form the magnetosphere, which includes a long tail that acts as a barrier to energetic particles.

![Moon Orbit Diagram](/images/moon_orbit_graphic.png)

This is where our team - Valerie Bernstein (myself), Kaiya Wahl, and Delores Knipp - step in as space weather researchers! Our specific goal was to predict the position of the moon with respect to the magnetotail in order to provide a yes/no decision table to data collection times.

## Prerequisites (Python 3)
* [NumPy](https://numpy.org/install/)
* [Matplotlib](https://matplotlib.org/stable/users/installing.html)
* [ephem](https://pypi.org/project/ephem/)

## Run the code
1. Clone the repo
   ```sh
   git clone https://github.com/valerie-bernstein/Moon-and-Magnetotail.git
   ```
2. Run the following command in the terminal. Note that start and end dates should be in the format 'MMM D YYYY', i.e. 'Jul 1 2021'
   ```sh
   python main.py 'start date' 'end date' 
   ```