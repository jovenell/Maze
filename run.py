from cell import Cell
import matplotlib.pyplot as plt
import random
import math
from copy import deepcopy

class Maze:
    def __init__(self, size):
        self.board = [[Cell(j, i) for j in range(size)] for i in range(size)]
        self.size = size
        self.start_y = None
        self.end_y = None

        self.create_maze()

    def create_maze(self):
        current_cell = self.board[random.randint(0, self.size - 1)][random.randint(0, self.size - 1)]
        stack = []
        finished = False

        while not finished:
            current_cell.visited = True

            # 0 - up, 1 - down, 2 - left, 3 - right
            options = [0, 1, 2, 3]
            
            if current_cell.y == 0:
                options.remove(0)
            elif current_cell.y == self.size - 1:
                options.remove(1)
            if current_cell.x == 0:
                options.remove(2)
            elif current_cell.x == self.size - 1:
                options.remove(3)

            if current_cell.y != 0 and self.board[current_cell.y - 1][current_cell.x].visited == True:
                options.remove(0)
            if current_cell.y != self.size - 1 and self.board[current_cell.y + 1][current_cell.x].visited == True:
                options.remove(1)
            if current_cell.x != 0 and self.board[current_cell.y][current_cell.x - 1].visited == True:
                options.remove(2)
            if current_cell.x != self.size - 1 and self.board[current_cell.y][current_cell.x + 1].visited == True:
                options.remove(3)

            if len(options) > 0:
                choice = random.choice(options)

                if choice == 0:
                    current_cell.top_wall = False
                    new_cell = self.board[current_cell.y - 1][current_cell.x]
                    new_cell.bottom_wall = False
                elif choice == 1:
                    current_cell.bottom_wall = False
                    new_cell = self.board[current_cell.y + 1][current_cell.x]
                    new_cell.top_wall = False
                elif choice == 2:
                    current_cell.left_wall = False
                    new_cell = self.board[current_cell.y][current_cell.x - 1]
                    new_cell.right_wall = False
                elif choice == 3:
                    current_cell.right_wall = False
                    new_cell = self.board[current_cell.y][current_cell.x + 1]
                    new_cell.left_wall = False

                stack.append(current_cell)
                current_cell = new_cell
            else:
                if len(stack) > 0:
                    current_cell = stack.pop()
                else:
                    finished = True
        
        self.create_maze_with_walls()

    def create_maze_with_walls(self):
        new_board = [[0 for j in range(self.size * 2 + 1)] for i in range(self.size * 2 + 1)]

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].top_wall:
                    new_board[i * 2][j * 2] = 1
                    new_board[i * 2][j * 2 + 1] = 1
                    new_board[i * 2][j * 2 + 2] = 1
                if self.board[i][j].bottom_wall:
                    new_board[i * 2 + 2][j * 2] = 1
                    new_board[i * 2 + 2][j * 2 + 1] = 1
                    new_board[i * 2 + 2][j * 2 + 2] = 1
                if self.board[i][j].left_wall:
                    new_board[i * 2][j * 2] = 1
                    new_board[i * 2 + 1][j * 2] = 1
                    new_board[i * 2 + 2][j * 2] = 1
                if self.board[i][j].right_wall:
                    new_board[i * 2][j * 2 + 2] = 1
                    new_board[i * 2 + 1][j * 2 + 2] = 1
                    new_board[i * 2 + 2][j * 2 + 2] = 1

        start_y_legal = False
        end_y_legal = False

        while start_y_legal == False:
            self.start_y = random.randint(1, self.size - 1) * 2 + 1
            if new_board[self.start_y][1] == 0:
                start_y_legal = True

        while end_y_legal == False:
            self.end_y = random.randint(1, self.size - 1) * 2 + 1
            if new_board[self.end_y][-2] == 0:
                end_y_legal = True

        new_board[self.start_y][1] = 2
        new_board[self.end_y][-2] = 3

        self.board = new_board
        
        self.print_board()
        self.solve_maze()

    def solve_maze(self):
        open_list = []
        closed_list = []

        start_cell = Cell(1, self.start_y)
        end_cell = Cell(len(self.board) - 2, self.end_y)

        open_list.append(start_cell)

        while len(open_list) > 0:
            choosen_cell = open_list[0]
            for i in open_list:
                if i.value < choosen_cell.value:
                    choosen_cell = i

            open_list.remove(choosen_cell)
            closed_list.append(choosen_cell)

            children = []

            if self.board[choosen_cell.y - 1][choosen_cell.x] == 0 or self.board[choosen_cell.y - 1][choosen_cell.x] == 3:
                children.append(Cell(choosen_cell.x, choosen_cell.y - 1))

            if self.board[choosen_cell.y + 1][choosen_cell.x] == 0 or self.board[choosen_cell.y + 1][choosen_cell.x] == 3:
                children.append(Cell(choosen_cell.x, choosen_cell.y + 1))

            if self.board[choosen_cell.y][choosen_cell.x - 1] == 0 or self.board[choosen_cell.y][choosen_cell.x - 1] == 3:
                children.append(Cell(choosen_cell.x - 1, choosen_cell.y))

            if self.board[choosen_cell.y][choosen_cell.x + 1] == 0 or self.board[choosen_cell.y][choosen_cell.x + 1] == 3:
                children.append(Cell(choosen_cell.x + 1, choosen_cell.y))

            for i in children:
                i.parent = choosen_cell

                if i.x == end_cell.x and i.y == end_cell.y:
                    open_list = []
                    choosen_cell = i
                    break

                i.dist_from_start = choosen_cell.dist_from_start + 1
                i.dist_to_end = abs(i.x - end_cell.x) + abs(i.y - end_cell.y)
                i.value = i.dist_from_start + i.dist_to_end

                closed_same_pos_lower_value = False
                for j in closed_list:
                    if j.x == i.x and j.y == i.y and j.value < i.value:
                        closed_same_pos_lower_value = True
                        break

                if closed_same_pos_lower_value == False:
                    open_same_pos_lower_value = False

                    for j in open_list:
                        if j.x == i.x and j.y == i.y and j.value < i.value:
                            open_same_pos_lower_value = True
                            break

                    if open_same_pos_lower_value == False:
                        open_list.append(i)

        path_cell = choosen_cell.parent

        while path_cell.parent != None:
            self.board[path_cell.y][path_cell.x] = 4
            path_cell = path_cell.parent

    def print_board(self):
        plt.pcolormesh(self.board)
        plt.axes().set_aspect('equal')
        plt.xticks([])
        plt.yticks([])
        plt.axes().invert_yaxis()
        plt.show()

if __name__ == '__main__':
    maze = Maze(10)
    maze.print_board()