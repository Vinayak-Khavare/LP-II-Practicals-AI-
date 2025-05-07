def is_safe_bt(board, row, col):
    for i in range(row):
        if board[i] == col or \
           abs(board[i] - col) == abs(i - row):
            return False
    return True

def solve_queens_bt(n, row=0, board=None, solutions=None):
    if board is None:
        board = [-1] * n
    if solutions is None:
        solutions = []

    if row == n:
        solutions.append(board[:])
        return

    for col in range(n):
        if is_safe_bt(board, row, col):
            board[row] = col
            solve_queens_bt(n, row + 1, board, solutions)
            board[row] = -1  # Backtrack

    return solutions

print("Backtracking 4-Queens Solutions:")
solutions_bt = solve_queens_bt(4)
for sol in solutions_bt:
    print(sol)
