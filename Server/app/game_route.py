from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from .models import Game

from . import db

from .game_engine import rookPosibleMoves,toHumanCordinates,make_move,knightPosibleMoves,pc_make_move,create_board,init_knight,init_rook

import json

from .util import to_int

# pyjwt, flask_jwt
game_blueprint=Blueprint('game',__name__)

## get board
## make move

@game_blueprint.route("/game/another",methods=["GET"])
@jwt_required()
def another():
    current_user=get_jwt_identity()
    print(current_user)
    return "Another one"


@game_blueprint.route("/game/board",methods=["GET"])
@jwt_required()
def get_board():
    current_user=get_jwt_identity()
    print(current_user)
    game=Game.query.filter_by(member_id=current_user['id']).first()
    print(game)
    if not game:
        return jsonify({'message':"Game not found"}),400
    board=json.loads(game.board)
    return jsonify({'message':f"Hi {current_user['alias']}  this is your board",'board':board})

@game_blueprint.route("/game/make-move",methods=["PUT"])
@jwt_required()
def human_move():
    body=request.get_json()
    x=body.get("x")
    y=body.get("y")

    x=to_int(x)
    y=to_int(y)

    print(x,y)
    # if not x or not y:
    #     return jsonify({"message":"required fields missing and they must be numbers"})
    current_user=get_jwt_identity()
    game=Game.query.filter_by(member_id=current_user['id']).first()
    if not game:
        return jsonify({'message':"Game not found"}),400
    board=json.loads(game.board)


    to={'x':x,'y':y}
    fr={'x':game.rook_x, 'y':game.rook_y}
    moves=rookPosibleMoves(fr)

    found_move=None

    for move in moves:
        if move['x']==to['x'] and move['y']==to['y']:
            found_move=True
    
    if not found_move:
        return jsonify({'message':"Invalid move selected"})

    make_move(board,fr,to)

    knight_position={'x':game.knight_x, 'y':game.knight_y}
    knight_posible_moves=knightPosibleMoves(knight_position)
    knight_move=pc_make_move(knight_posible_moves)
    make_move(board,knight_position,knight_move,"BN")

    new_board=json.dumps(board)
    game.board=new_board
    game.knight_x=knight_move['x']
    game.knight_y=knight_move['y']
    game.rook_x=to['x']
    game.rook_y=to['y']

    db.session.commit()

    return jsonify({'board':board,"message":"Pc Made a smart move"})

@game_blueprint.route("/game/possible-moves",methods=["GET"])
@jwt_required()
def possible_moves():
    current_user=get_jwt_identity()
    game=Game.query.filter_by(member_id=current_user['id']).first()
    if not game:
        return jsonify({'message':"Game not found"}),400
    rook = {"x": game.rook_x, "y": game.rook_y}
    board=json.loads(game.board)
    moves=rookPosibleMoves(rook)
    human_co=toHumanCordinates(moves)

    for move in moves:
        piece=board[move['x']][move['y']]
        if piece=="":
            board[move['y']][move['x']]="X"

    return jsonify({'moves':moves,'human_co':human_co,"board":board}),200

@game_blueprint.route("/game/new-game",methods=["GET"])
@jwt_required()
def new_game():
    current_user=get_jwt_identity()
    game=Game.query.filter_by(member_id=current_user['id']).first()
    if not game:
        return jsonify({'message':"Game not found"}),400
    board=create_board()
    knight_x=init_knight['x']
    knight_y=init_knight['y']
    rook_x=init_rook['x']
    rook_y=init_rook['y']
    board[knight_y][knight_x]="BN"
    board[rook_y][rook_x]="WR"
    board=json.dumps(board)
    game.board=board
    game.knight_x=knight_x
    game.knight_y=knight_y
    game.rook_x=rook_x
    game.rook_y=rook_y
    db.session.commit()
