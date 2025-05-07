def solve_queens_bb(n, row=0, board=None, cols=None, diag1=None, diag2=None, solutions=None):
    if board is None:
        board = [-1] * n
    if cols is None:
        cols = [False] * n
    if diag1 is None:
        diag1 = [False] * (2 * n - 1)  # r + c
    if diag2 is None:
        diag2 = [False] * (2 * n - 1)  # r - c + n - 1
    if solutions is None:
        solutions = []

    if row == n:
        solutions.append(board[:])
        return

    for col in range(n):
        d1 = row + col
        d2 = row - col + n - 1
        if not cols[col] and not diag1[d1] and not diag2[d2]:
            board[row] = col
            cols[col] = diag1[d1] = diag2[d2] = True
            solve_queens_bb(n, row + 1, board, cols, diag1, diag2, solutions)
            cols[col] = diag1[d1] = diag2[d2] = False  # Backtrack

    return solutions

print("\nBranch and Bound 4-Queens Solutions:")
solutions_bb = solve_queens_bb(4)
for sol in solutions_bb:
    print(sol)
