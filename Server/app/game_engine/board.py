def create_board():
    board=[]
    for i in range(0,8):
        board.append(["","","","","","","",""])
    
    return board


init_knight = {"x": 1, "y": 0}
init_rook = {"x": 0, "y": 7}