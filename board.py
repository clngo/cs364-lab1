class Board:
    def __init__(self):
        self.board = [str(i+1) for i in range(9)]

    def display(self):
        return (
            f"\n{self.board[0]} | {self.board[1]} | {self.board[2]}"
            f"\n--+---+--\n"
            f"{self.board[3]} | {self.board[4]} | {self.board[5]}"
            f"\n--+---+--\n"
            f"{self.board[6]} | {self.board[7]} | {self.board[8]}"
        )

    def update(self, position, marker):
        self.board[position] = marker

    def is_winner(self, marker):
        winning_combos = [
            [0,1,2],[3,4,5],[6,7,8],  # rows
            [0,3,6],[1,4,7],[2,5,8],  # columns
            [0,4,8],[2,4,6]           # diagonals
        ]
        for combo in winning_combos:
            if set(self.board[i] for i in combo) == {marker}:
                return True
        return False

    def is_draw(self):
        return all(space in ["X", "O"] for space in self.board)
