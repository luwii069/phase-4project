def make_move(board,fr,to,symbol="WR"):
    fr_x=fr['x']
    fr_y=fr['y']
    to_x=to['x']
    to_y=to['y']

    board[fr_y][fr_x]=f""
    board[to_y][to_x]=symbol