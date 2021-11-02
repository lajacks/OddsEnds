class puzzle(object):
    '''The main object used to contain all information in the puzzle.'''
    def __init__(self, difficulty: int = 9, known: dict = None) -> None:
        self.difficulty: int = difficulty
        self.cells: dict = {}
        self.rows: dict = {}
        self.columns: dict = {}
        self.sectors: dict = {}
        self.solveOrder: list = []
        self.solved: bool = False

        for i in range(1, difficulty + 1):
            self.rows[i] = puzzle.family(self)
            self.columns[i] = puzzle.family(self)
            self.sectors[i] = puzzle.family(self)

        for i in range(1, difficulty**2 + 1):
            x = 1 + ((i - 1) // 9)
            y = 1 + ((i - 1) % 9)

            self.cells[(x, y)] = puzzle.cell(self, (x, y))

        self.unsolvedCells: dict = dict(self.cells)

        for row in self.rows.values():
            if not row.verify():
                raise ValueError

        for column in self.columns.values():
            if not column.verify():
                raise ValueError

        for sector in self.sectors.values():
            if not sector.verify():
                raise ValueError

        for key, val in known.items():
            self.cells[key].solve(val)

    class cell(object):
        '''The smallest atomic unit for the puzzle, containing a single value.'''
        def __init__(self, puzzle: object, loc: tuple, value: int = None):
            self.puzzle: object = puzzle
            self.possible: list = list(range(1, puzzle.difficulty + 1))
            self.solved: bool = False
            self.loc: tuple = loc
            self.value: int == None

            self.row: object = puzzle.rows[loc[0]]
            puzzle.rows[loc[0]].cells[loc] = self

            self.column: object = puzzle.columns[loc[1]]
            puzzle.columns[loc[1]].cells[loc] = self

            self.sector: object = puzzle.sectors[puzzle.getSector(loc)]
            puzzle.sectors[puzzle.getSector(loc)].cells[loc] = self

            if value is not None:
                self.solve(value)

        def solve(self, value: int):
            '''Set the given value to be the cell value and initiate checking
            functions for the cell's families.
            '''
            if 0 > value > self.puzzle.difficulty:
                raise ValueError
            self.value = value
            self.solved = True
            self.possible.clear()

            self.puzzle.unsolvedCells[self.loc] = None
            del self.puzzle.unsolvedCells[self.loc]
            self.puzzle.solveOrder.append(self.loc)
            self.puzzle.checkSolveStatus()

            self.row.checkSolve(self)
            self.column.checkSolve(self)
            self.sector.checkSolve(self)

        def trySolve(self, value: int):
            '''Set the given value to be the cell value if it is a possible
            value for the cell.
            '''
            if value in self.possible:
                self.solve(value)

    class family(object):
        '''A containing object used to relate a row, column, or sector.'''
        def __init__(self, puzzle):
            self.puzzle = puzzle
            self.solved = False
            self.cells = {}

        def verify(self) -> bool:
            '''Return a boolean indicating if the family contains the required
            amount of cells. 
            '''
            if len(self.cells) != self.puzzle.difficulty:
                return False

            return True

        def checkSolve(self, callingCell) -> None:
            '''Set the family solved status.

            If the family has unsolved cells, the callingCell value will be
            removed from their possible lists.
            '''
            booSolved: bool = True
            for cel in self.cells.values():
                if not cel.solved:
                    booSolved = False
                    if callingCell.value in cel.possible:
                        cel.possible.remove(callingCell.value)

            if booSolved:
                self.solved = True

        def solve(self) -> bool:
            '''Attempt to solve the family, and return if any progress is made
            in advancing the puzzle.
            
            Advancing the puzzle includes assigning values to cells and
            removing possible values from cells.
            '''
            booProgress: bool = False

            for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                intPossible: int = 0

                for cel in self.cells.values():
                    if i in cel.possible:
                        intPossible += 1

                if intPossible == 2:
                    cell1: object = None
                    cell2: object = None

                    for cel in self.cells.values():
                        if i in cel.possible and cell1:
                            cell2 = cel
                        elif i in cel.possible:
                            cell1 = cel

                    if cell1.loc[0] == cell2.loc[0]:
                        for cel in self.puzzle.rows[
                                cell1.loc[0]].cells.values():
                            if cel.loc != cell1.loc and cel.loc != cell2.loc and i in cel.possible:
                                cel.possible.remove(i)
                                booProgress = True

                    if cell1.loc[1] == cell2.loc[1]:
                        for cel in self.puzzle.columns[
                                cell1.loc[1]].cells.values():
                            if cel.loc != cell1.loc and cel.loc != cell2.loc and i in cel.possible:
                                cel.possible.remove(i)
                                booProgress = True

                    if self.puzzle.getSector(
                            cell1.loc) == self.puzzle.getSector(cell2.loc):
                        for cel in self.puzzle.sectors[self.puzzle.getSector(
                                cell1.loc)].cells.values():
                            if cel.loc != cell1.loc and cel.loc != cell2.loc and i in cel.possible:
                                cel.possible.remove(i)
                                booProgress = True

                if intPossible == 1:
                    for cel in self.cells.values():
                        cel.trySolve(i)

                    booProgress = True

            return booProgress

    def getSector(self, loc: tuple) -> int:
        '''Return an integer indicating the sector of the puzzle the given
        location exists in.
        '''
        i = loc[0] - 1
        j = loc[1] - 1

        if self.difficulty == 6:
            return int(1 + 2 * (i // 2) + (j // 3))
        else:
            sqrt = int(self.difficulty**0.5)
            return int(1 + sqrt * (i // sqrt) + (j // sqrt))

    def getPrintout(self) -> str:
        '''Return a print-friendly string representing the puzzle.'''
        strOut: str = ''

        sqrt: int = int(self.difficulty**0.5)
        intRow: int = 0

        for row in self.rows.values():
            for cel in row.cells.values():
                if cel.solved:
                    strOut += str(cel.value)
                else:
                    strOut += ' '

                if cel.loc[1] % sqrt == 0 and cel.loc[1] != self.difficulty:
                    strOut += '|'

            strOut += '\n'
            intRow += 1

            if intRow % sqrt == 0 and intRow != self.difficulty:
                strBlanks = ''

                for i in range(self.difficulty):
                    if (i + 1) % sqrt == 0:
                        strBlanks += '-+'
                    else:
                        strBlanks += '-'

                strBlanks = strBlanks[:-1]  # Trims out the last '+'
                strOut += strBlanks + '\n'

        return strOut

    def checkSolveStatus(self):
        '''Check if there are zero unsolved cells, and if so, set the
        self.solved parameter to True.
        '''
        if len(self.unsolvedCells) == 0:
            self.solved = True

    def solve(self):
        '''Run the main loop, attempting to solve the puzzle.'''
        while not self.solved:
            dictUnsolved: dict = dict(self.unsolvedCells)
            booCell: bool = False
            booRow: bool = False
            booCol: bool = False
            booSec: bool = False

            for cel in dictUnsolved.values():
                if len(cel.possible) == 1:
                    cel.solve(cel.possible[0])
                    booCell = True

            for row in self.rows.values():
                booRow = row.solve()

            for col in self.columns.values():
                booCol = col.solve()

            for sec in self.sectors.values():
                booSec = sec.solve()

            if not booCell and not booRow and not booCol and not booSec:
                print('Major Wumpus')

                print(self.getPrintout())

                for cel2 in self.unsolvedCells.values():
                    print(cel2.possible)
                return

        self.verify()
        print('Job\'s Done')
        print(self.getPrintout())

    def verify(self):
        '''Raise a ValueError if the puzzle does not satisfy the row, column,
        and sector requirements.
        '''
        for row in self.rows.values():
            listAll = list(range(1, self.difficulty + 1))
            for cel in row.cells.values():
                listAll.remove(cel.value)
            if len(listAll) != 0:
                raise ValueError

        for col in self.columns.values():
            listAll = list(range(1, self.difficulty + 1))
            for cel in col.cells.values():
                listAll.remove(cel.value)
            if len(listAll) != 0:
                raise ValueError

        for sec in self.sectors.values():
            listAll = list(range(1, self.difficulty + 1))
            for cel in sec.cells.values():
                listAll.remove(cel.value)
            if len(listAll) != 0:
                raise ValueError

##Test
known: dict = {
    (1, 7): 3,
    (1, 8): 5,
    (2, 3): 7,
    (2, 9): 6,
    (3, 1): 5,
    (3, 2): 2,
    (3, 3): 8,
    (3, 5): 4,
    (4, 3): 5,
    (4, 6): 1,
    (5, 1): 4,
    (5, 4): 2,
    (5, 7): 8,
    (6, 2): 6,
    (6, 5): 5,
    (6, 9): 3,
    (7, 2): 7,
    (7, 4): 6,
    (7, 8): 9,
    (8, 2): 9,
    (8, 4): 4,
    (8, 5): 7,
    (9, 8): 4,
    (9, 9): 8
}

puz = puzzle(known=known)

print()

puz.solve()

print()

print(puz.solveOrder)