# Maze Solver

This Python program generates and solves mazes using a graphical interface. It creates a random maze and then finds a path from the entrance (top-left) to the exit (bottom-right).

## How It Works

1. **Maze Generation**: The program uses a recursive backtracking algorithm to generate a random maze. It starts with a grid of cells, all surrounded by walls, and then randomly breaks down walls to create paths.

2. **Maze Solving**: After generating the maze, the program uses another recursive algorithm to find a path from the entrance to the exit. It explores possible paths, backtracking when it reaches a dead end, until it finds the solution.

3. **Visualization**: The maze generation and solving processes are visualized in real-time using Tkinter, allowing you to see how the algorithms work step by step.

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)

## How to Run

1. Ensure you have Python installed on your system.
2. Save the provided code in a file named `main.py`.
3. Open a terminal or command prompt.
4. Navigate to the directory containing `main.py`.
5. Run the following command:

   ```
   python main.py
   ```

6. A window will open showing the maze generation process, followed by the solving process.
7. The program will print "Maze solved!" in the console if a solution is found.
8. Close the window to exit the program.

## Customization

You can customize the maze by modifying the following parameters in the `main()` function:

- `num_cols` and `num_rows`: Change the size of the maze
- `cell_size_x` and `cell_size_y`: Adjust the size of each cell
- `seed`: Change or remove the random seed to get different maze layouts

## Note

The solving process may take some time for larger mazes. You can adjust the `time.sleep()` value in the `_animate()` method to speed up or slow down the visualization.
