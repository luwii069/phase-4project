all_cordinate=[
    {'x':-1,'y':2},
    {'x':1,'y':2},
    {'x':2,'y':1},
    {'x':2,'y':-1},
    {'x':1,'y':-2},
    {'x':-1,'y':-2},
    {'x':-2,'y':-1},
    {'x':-2,'y':1},
               ]

def knightPosibleMoves(knigt):
    moves=[]
    x0=knigt['x']
    y0=knigt['y']
    for piece_co in all_cordinate:
        n_x=x0+piece_co['x']
        n_y=y0+piece_co['y']
        if n_x>=0 and n_x<=7 and n_y>=0 and n_y<=7:
            moves.append({"x":n_x, "y":n_y})
    return moves

def pc_make_move(moves):
    return moves[0]