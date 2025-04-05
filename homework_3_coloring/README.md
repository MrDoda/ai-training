
# Graph Coloring via Local Search

This project implements a graph coloring algorithm using local search techniques. It includes:

in `local_search.py`:

- **iscoloring**: A function to verify if a given color assignment is a valid graph coloring.
- **color**: A function that uses a combination of hill climbing and random walks to find a valid coloring with a specified number of colors. GPU acceleration via Numba's CUDA is available for conflict counting.

The algorithm is designed to work with large graphs (e.g., the dsjc125.9 instance) and gradually lower the number of colors to approach the known optimum.


## Setup Instructions


1. **Install Required Packages**  
   Install NumPy and Numba via pip:
   ```bash
   pip install numpy numba matplotlib networkx
   ```

2. **GPU Acceleration Setup (Optional)**  
   - **Install NVIDIA Drivers & CUDA Toolkit:**  
     Ensure your system (with an RTX 3080) has the correct NVIDIA drivers installed and download the [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) (CUDA 11.x or later is recommended).
   - **Verify GPU Availability:**  
     In a Python shell, run:
     ```python
     >>> from numba import cuda
     >>> cuda.is_available()
     ```
     This should return `True` if your CUDA installation is properly set up.

## How to Run the Project

From the project folder, run the program using:

```bash
python main.py dsjc125.9.col --colors 44 --steps 1000000 --random 0.4 --min_hill_climb 100 --gpu
```

- **Arguments:**
  - `dsjc125.9.col`: Path to your graph file in DIMACS .col format.
  - `--colors 44`: Number of colors to use (default is 44).
  - `--steps 100000`: Maximum number of local search steps.
  - `--gpu`: Enable GPU acceleration for conflict counting.
  - `--random 0.4`: Chance to go on a random walk instead of Hill Climbing.
  - `--min_hill_climb 100`: Minimum Hill Climbing streak.
  - `--interactive`: Adds interactive graph into the html report.

  

Adjust the number of colors and steps as needed. Note that running the algorithm on large graphs might take a significant amount of time.

## Notes

- The algorithm uses a mix of hill climbing and random walks to reduce conflicts.
- GPU acceleration is only applied to conflict counting; the overall search remains sequential.
