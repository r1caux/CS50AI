import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()
        
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) record move + safety
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # 2) collect neighbors
        neighbors = set()
        r, c = cell
        # Loop over all cells within one row and column
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))

        # 3) prune neighbors I already know about and adjust count
        adjusted_count = count
        pruned = set()
        for n in neighbors:
            if n in self.safes:
                # known safes --> drop from sentence
                continue
            if n in self.mines:
                # known minces --> drop and decrement count
                adjusted_count -= 1
                continue
            pruned.add(n)
        
        # 4) add the new sentence (if it has any unkowns left)
        if pruned:
            new_sentence = Sentence(pruned, adjusted_count)
            # avoid duplicates
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)

        # 5) try to mark new safes/mines from all sentences
        changed = True
        while changed:
            changed = False

            # a) direct deductions
            to_mark_safe = set()
            to_mark_mine = set()
            for s in self.knowledge:
                to_mark_safe |= s.known_safes()
                to_mark_mine |= s.known_mines()

            # apply
            if to_mark_safe:
                changed = True
                for cell_safe in to_mark_safe:
                    self.mark_safe(cell_safe)
            if to_mark_mine:
                changed = True
                for cell_mine in to_mark_mine:
                    self.mark_mine(cell_mine)

            # b) subset inference: S2 - S1 if S1 c S2
            new_inferred = []
            for a in self.knowledge:
                for b in self.knowledge:
                    if a is b:
                        continue
                    if a.cells and b.cells and a.cells < b.cells:
                        diff_cells = b.cells - a.cells
                        diff_count = b.count - a.count
                        if diff_cells:
                            inferred = Sentence(diff_cells, diff_count)
                            if inferred not in self.knowledge and inferred not in new_inferred:
                                new_inferred.append(inferred)
            if new_inferred:
                changed = True
                self.knowledge.extend(new_inferred)
        
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        candidates = self.safes - self.moves_made
        return next(iter(sorted(candidates))) if candidates else None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        self.moves_made
        self.mines

        all_cells = {(i, j) for i in range(self.height) for j in range(self.width)}
        candidates = list(all_cells - self.moves_made - self.mines)
        return random.choice(candidates) if candidates else None
