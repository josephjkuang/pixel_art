# Depixalizing Pixel Art

CS 445 Final Project to Upscale Pixel Art

## Organization

The Project is organized such that the various methods are stored in python files. The various available inputs are placed in the inputs folder, but other inputs can also be added if desired.

The `bilinear.py`, `nearestNeighbors.py` and `epx.py` are implementations of the naive methods that we implemented and can be referenced in the Upscale notebook.

The `utils.py` file has utilities for displaying images.

The `similarityGraph.py` has the functions used to create the similarity graphs used in the Voronoi cell graph implementation (Milestone 1).
The `voronoi.py` has the Voronoi cell graph implementation (Milestones 2).
The `splines.py` has the spline curve generation functions (Milestone 3) however, this is currently unused for the full method.
The `curves.py` has the replacement implementation for the spline curve generation (Milestones 3 and 4).
The `render.py` has the functions necessary for rendering the images after everything has been calculated (Milestone 5).

## To Run

To run the tests, open Test.ipynb in Jupyter Notebook.

To run the code on the inputs, open the Upscale.ipynb in Jupyter notebook and run the cells in order with the correct input files specified.

## Requirements

You may need to install from the requirements.txt using `pip install -r requirements. txt`
