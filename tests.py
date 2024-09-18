import unittest
from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win=None)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_different_size(self):
        num_cols = 5
        num_rows = 8
        m2 = Maze(0, 0, num_rows, num_cols, 20, 20, win=None)
        self.assertEqual(
            len(m2._cells),
            num_cols,
        )
        self.assertEqual(
            len(m2._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_single_cell(self):
        num_cols = 1
        num_rows = 1
        m3 = Maze(0, 0, num_rows, num_cols, 50, 50, win=None)
        self.assertEqual(
            len(m3._cells),
            num_cols,
        )
        self.assertEqual(
            len(m3._cells[0]),
            num_rows,
        )

    def test_break_entrance_and_exit(self):
        num_cols = 3
        num_rows = 3
        m = Maze(0, 0, num_rows, num_cols, 10, 10, win=None)
        
        # Check entrance (top-left cell)
        self.assertFalse(m._cells[0][0].has_top_wall)
        
        # Check exit (bottom-right cell)
        self.assertFalse(m._cells[-1][-1].has_bottom_wall)
        
        # Check that other outer walls are still intact
        self.assertTrue(m._cells[0][0].has_left_wall)
        self.assertTrue(m._cells[-1][-1].has_right_wall)

    def test_break_walls(self):
        num_cols = 5
        num_rows = 5
        m = Maze(0, 0, num_rows, num_cols, 10, 10, win=None, seed=0)
        
        # Check if some walls are broken
        walls_broken = False
        for i in range(num_cols):
            for j in range(num_rows):
                cell = m._cells[i][j]
                if not (cell.has_left_wall and cell.has_right_wall and cell.has_top_wall and cell.has_bottom_wall):
                    walls_broken = True
                    break
            if walls_broken:
                break
        
        self.assertTrue(walls_broken, "No walls were broken in the maze")

        # Check if all cells were visited
        all_visited = all(cell.visited for col in m._cells for cell in col)
        self.assertTrue(all_visited, "Not all cells were visited during wall breaking")

        # Now reset the cells and check if they're all not visited
        m.reset_cells_visited()
        all_not_visited = all(not cell.visited for col in m._cells for cell in col)
        self.assertTrue(all_not_visited, "Not all cells were reset to not visited")

    def test_reset_cells_visited(self):
        num_cols = 5
        num_rows = 5
        m = Maze(0, 0, num_rows, num_cols, 10, 10, win=None, seed=0)
        
        # Check if all cells are not visited after reset
        all_not_visited = all(not cell.visited for col in m._cells for cell in col)
        self.assertTrue(all_not_visited, "Not all cells were reset to not visited")

        # Mark some cells as visited
        m._cells[0][0].visited = True
        m._cells[2][2].visited = True
        m._cells[4][4].visited = True

        # Reset cells
        m.reset_cells_visited()  # Changed from m._reset_cells_visited() to m.reset_cells_visited()

        # Check again if all cells are not visited after reset
        all_not_visited = all(not cell.visited for col in m._cells for cell in col)
        self.assertTrue(all_not_visited, "Not all cells were reset to not visited after marking some as visited")

if __name__ == "__main__":
    unittest.main()