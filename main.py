import itertools
import curses


class TicTacToe:
    def __init__(self):
        self.data = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
        ]
        self.choice = itertools.cycle('XO')
        self.current = 'X'

    def push(self, x, y):
        if 0 <= x < 3 and 0 <= x < 3 and self.data[x][y] == self.get_winner() == ' ':
            self.data[x][y] = next(self.choice)
            self.current = next(self.choice)
            next(self.choice)

    def get_current(self):
        return self.current

    def is_finished(self):
        return not self.has_empty() or self.get_winner() != ' '

    def has_empty(self):
        return any(map(lambda line: ' ' in line, self.data))

    def get(self, x, y):
        return self.data[x][y]

    def get_winner(self):
        winners = [self.check_rows(), self.check_cols(), self.check_diagonals()]
        winners = [' '] + [winner for winner in winners if winner != ' ']
        return winners[-1]

    def check_rows(self):
        for row in self.data:
            if row[0] != ' ' and all(row[0] == x for x in row):
                return row[0]
        return ' '

    def check_cols(self):
        for col in zip(*self.data):
            if col[0] != ' ' and all(col[0] == x for x in col):
                return col[0]
        return ' '

    def check_diagonals(self):
        main_diagonal = [self.data[i][i] for i in range(3)]
        other_diagonal = [self.data[i][2 - i] for i in range(3)]
        for diagonal in [main_diagonal, other_diagonal]:
            if diagonal[0] != ' ' and all(diagonal[0] == x for x in diagonal):
                return diagonal[0]
        return ' '


class Cell:
    CELL_X_SIZE = 5
    CELL_Y_SIZE = 9

    def __init__(self, x, y, value):
        self.x, self.y, self.value = x, y, value
        self.attr = curses.A_NORMAL

    def draw(self, screen):
        shift = iter(range(Cell.CELL_X_SIZE))
        screen.addstr(self.x + next(shift), self.y, "+" + '-' * (Cell.CELL_Y_SIZE - 2) + "+", self.attr)
        for i in range((Cell.CELL_X_SIZE - 2) // 2):
            screen.addstr(self.x + next(shift), self.y, "|" + " " * (Cell.CELL_Y_SIZE - 2) + "|", self.attr)
        screen.addstr(self.x + next(shift), self.y,
                      "|" + " " * ((Cell.CELL_Y_SIZE - 2) // 2) + self.value + " " * ((Cell.CELL_Y_SIZE - 2) // 2) + "|",
                      self.attr)
        for i in range((Cell.CELL_X_SIZE - 2) // 2):
            screen.addstr(self.x + next(shift), self.y, "|" + " " * (Cell.CELL_Y_SIZE - 2) + "|", self.attr)
        screen.addstr(self.x + next(shift), self.y, "+" + "-" * (Cell.CELL_Y_SIZE - 2) + "+", self.attr)

    def set_value(self, value):
        self.value = value

    def activate(self):
        self.attr = curses.A_REVERSE

    def deactivate(self):
        self.attr = curses.A_NORMAL


class WidgetsManager:
    def __init__(self, screen):
        self.screen = screen
        self.cells = []
        self.active = True
        self.tic_tac_toe = TicTacToe()
        x, y = 8, 8
        self.cells = [[Cell(x + i * Cell.CELL_X_SIZE, y + j * Cell.CELL_Y_SIZE, ' ') for j in range(3)] for i in range(3)]
        self.x, self.y = 0, 0
        self.update_cells()

    def update(self):
        key = self.screen.getkey()
        if key == "KEY_UP":
            self.x = max(0, self.x - 1)
        elif key == "KEY_DOWN":
            self.x = min(2, self.x + 1)
        elif key == "KEY_LEFT":
            self.y = max(0, self.y - 1)
        elif key == "KEY_RIGHT":
            self.y = min(2, self.y + 1)
        elif key == 'r':
            self.tic_tac_toe = TicTacToe()
        elif key == 'q':
            self.active = False
        elif key == " ":
            self.tic_tac_toe.push(self.x, self.y)
        self.update_cells()

    def update_cells(self):
        for i in range(3):
            for j in range(3):
                self.cells[i][j].set_value(self.tic_tac_toe.get(i, j))
                self.cells[i][j].deactivate()
        self.cells[self.x][self.y].activate()

    def draw(self):
        for row in self.cells:
            for cell in row:
                cell.draw(self.screen)
        self.screen.addstr(2, curses.COLS // 2 - 5, "TIC TAC TOE", curses.A_UNDERLINE)
        self.screen.addstr(4, 30, "HELP:", curses.A_UNDERLINE)
        self.screen.addstr(4, 10, "CURRENT MOVE: " + self.tic_tac_toe.get_current())
        self.screen.addstr(6, 10, "WINNER: " + self.tic_tac_toe.get_winner())
        self.screen.addstr(6, 25, "r - RESTART, q - QUIT, space - PUSH")

    def clear(self):
        self.screen.clear()

    def is_active(self):
        return self.active


class Game:
    def __init__(self, screen):
        curses.curs_set(False)
        self.manager = WidgetsManager(screen)

    def main(self):
        while self.manager.is_active():
            self.manager.clear()
            self.manager.draw()
            self.manager.update()


def main(screen):
    game = Game(screen)
    game.main()


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(main)

