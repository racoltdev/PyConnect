boardState = []
def reset():
    boardState = []
    for row in range(6):
        boardState.append([])
        for col in range(7):
            boardState[-1].append(0)
    return boardState
def moveChecker(col, turn, board, player=True):
    for row in range(len(board)):
        if board[row][col] != 0:
            if row == 0:
                if player:
                    print ('Invalid move')
                return 'none'
            else:
                return [row - 1, col]
        elif row == len(board) - 1:
            return [row, col]
reset()