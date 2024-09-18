from tkinter import Tk, BOTH, Canvas
import time
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, 
            fill=fill_color, width=2
        )

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self._win is not None:
            self._draw_wall(self.has_left_wall, x1, y1, x1, y2)
            self._draw_wall(self.has_top_wall, x1, y1, x2, y1)
            self._draw_wall(self.has_right_wall, x2, y1, x2, y2)
            self._draw_wall(self.has_bottom_wall, x1, y2, x2, y2)

    def _draw_wall(self, has_wall, x1, y1, x2, y2):
        color = "black" if has_wall else "#d9d9d9"
        line = Line(Point(x1, y1), Point(x2, y2))
        self._win.draw_line(line, color)

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        
        fill_color = "gray" if undo else "red"

        # Calculate the center coordinates of both cells
        x_mid = (self._x1 + self._x2) / 2
        y_mid = (self._y1 + self._y2) / 2
        to_x_mid = (to_cell._x1 + to_cell._x2) / 2
        to_y_mid = (to_cell._y1 + to_cell._y2) / 2

        # Draw the line from the center of this cell to the center of the next cell
        line = Line(Point(x_mid, y_mid), Point(to_x_mid, to_y_mid))
        self._win.draw_line(line, fill_color)

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self.reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                cell = Cell(self._win)
                col_cells.append(cell)
                self._draw_cell(cell, i, j)
            self._cells.append(col_cells)

    def _draw_cell(self, cell, i, j):
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        cell.draw(x1, y1, x2, y2)
        if self._win is not None:
            self._animate()

    def _animate(self):
        if self._win is not None:
            self._win.redraw()
            time.sleep(0.05)

    def _break_entrance_and_exit(self):
        # Break the top wall of the entrance (top-left cell)
        self._cells[0][0].has_top_wall = False
        self._draw_cell(self._cells[0][0], 0, 0)

        # Break the bottom wall of the exit (bottom-right cell)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self._cells[-1][-1], self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            possible_directions = []

            # Check adjacent cells
            if i > 0 and not self._cells[i-1][j].visited:
                possible_directions.append(("left", i-1, j))
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                possible_directions.append(("right", i+1, j))
            if j > 0 and not self._cells[i][j-1].visited:
                possible_directions.append(("up", i, j-1))
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                possible_directions.append(("down", i, j+1))

            if len(possible_directions) == 0:
                self._draw_cell(self._cells[i][j], i, j)
                return

            # Choose a random direction
            direction, next_i, next_j = random.choice(possible_directions)

            # Break down the wall between current cell and chosen cell
            if direction == "left":
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            elif direction == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False
            elif direction == "up":
                self._cells[i][j].has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            elif direction == "down":
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False

            # Recursively visit the next cell
            self._break_walls_r(next_i, next_j)

    def reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        # Reset visited status before solving
        self.reset_cells_visited()
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        
        # Check if we've reached the end cell
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        # Mark the current cell as visited
        self._cells[i][j].visited = True

        # Define possible directions: right, down, left, up
        directions = [
            (1, 0, "has_right_wall"),
            (0, 1, "has_bottom_wall"),
            (-1, 0, "has_left_wall"),
            (0, -1, "has_top_wall")
        ]

        for di, dj, wall_attr in directions:
            next_i, next_j = i + di, j + dj

            if (0 <= next_i < self._num_cols and 
                0 <= next_j < self._num_rows and 
                not self._cells[next_i][next_j].visited):

                # Check if there's no wall between current cell and next cell
                if not getattr(self._cells[i][j], wall_attr):
                    # Draw move to next cell
                    self._cells[i][j].draw_move(self._cells[next_i][next_j])

                    # Recursively solve from next cell
                    if self._solve_r(next_i, next_j):
                        return True

                    # If the path didn't work out, undo the move
                    self._cells[i][j].draw_move(self._cells[next_i][next_j], undo=True)

        # Mark this cell as unvisited as we backtrack
        self._cells[i][j].visited = False
        return False

def main():
    win = Window(800, 600)
    
    # Test creating a maze
    num_cols = 12
    num_rows = 10
    margin = 50
    cell_size_x = 50
    cell_size_y = 50
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=0)  # Use seed=0 for debugging

    # Add a small delay to allow the maze to be drawn completely
    time.sleep(1)

    print("Solving the maze...")
    is_solved = maze.solve()
    if is_solved:
        print("Maze solved!")
    else:
        print("Maze could not be solved.")

    win.wait_for_close()

if __name__ == "__main__":
    main()
