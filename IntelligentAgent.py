import numpy as np
from Move import Move
from Location import Location
from CheckerBoard import CheckerBoard


class IntelligentAgent():
    """
    The IntelligentAgent class is used to represent an intelligent agent that makes moves on the board using the minimax algorithm.
    """

    def __init__(self, color, board_state):
        self.color = color
        self.board_state = board_state
        self.nextMove = Move(self.board_state, self.color)


    def ia_winner_check(self):
        """
        Check if the game is over and return the winner
        """
        black_pieces = [location for key, location in self.board_state.items() if key.startswith('black_')]
        white_pieces = [location for key, location in self.board_state.items() if key.startswith('white_')]
        king_black_pieces = [location for key, location in self.board_state.items() if key.startswith('king_black_')]
        king_white_pieces = [location for key, location in self.board_state.items() if key.startswith('king_white_')]
        
        if len(white_pieces) == 0 and len(king_white_pieces) == 0:
            return 'Black'
        elif len(black_pieces) == 0 and len(king_black_pieces) == 0:
            return 'White'
        # check if there are no possible moves for the current player
        nextMoveblack = Move(self.board_state, 'black')
        nextMovewhite = Move(self.board_state, 'white')
        if len(nextMoveblack.get_legal_moves()) == 0:
            print('No possible moves for black, white wins')
            return 'White'
        if len(nextMovewhite.get_legal_moves()) == 0:
            print('No possible moves for white, black wins')
            return 'Black'
            
        return None # game is not over yet
    
    def ia_game_evaluation(self, color, board_state):
        """
        Returns the evaluation of the game state.
        White is the maximizing player and Black is the minimizing player.
        """
        winning_player = self.ia_winner_check()
        if winning_player == 'Black': 
            return -1000
        elif winning_player == 'White':
            return 1000

        black_pieces = [location for key, location in board_state.items() if key.startswith('black_')]
        white_pieces = [location for key, location in board_state.items() if key.startswith('white_')]
        king_black_pieces = [location for key, location in board_state.items() if key.startswith('king_black_')]
        king_white_pieces = [location for key, location in board_state.items() if key.startswith('king_white_')]

        return len(white_pieces) + (len(king_white_pieces)*2) - len(black_pieces) - (len(king_black_pieces)*2)


  
        

    def minimax_try2(self, board_state, is_maximizing, depth=3, show_minimax_boards=True):
        """
        The minimax algorithm is used to determine the best move for the current player.

        board_state: dict, the current board state
        is_maximizing: bool, True if the current player is maximizing (white), False if the current player is minimizing (black)
        depth: int, the depth of the minimax tree
        show_minimax_boards: bool, if True, print the board state and some testing print statements at each depth of the minimax tree
        """

        if show_minimax_boards:
            print('The board state is:', board_state)
            print('The depth is:', depth)
        if is_maximizing:
            color = 'white'
        else:
            color = 'black'
        nextMove = Move(board_state, color)

        if depth == 0 or self.ia_winner_check() != None:
            ia_results = self.ia_game_evaluation(color, board_state), None
            return ia_results
        
        if is_maximizing: #white's turn
            maxEval = -np.inf
            best_move = None
            for move in nextMove.get_legal_moves():
                if show_minimax_boards: # print the possible moves for error checking
                    print("White's turn")
                    CheckerBoard.visualize_piece_numbers(move)
                    for key in move:
                        if key in move and move[key] != self.board_state[key]:
                            print(f'{key} can move from {self.board_state[key]} to {move[key]}')
                    for key in self.board_state:
                        if key not in move:
                            print(f'and can capture {key}')
                
                minimax_results = self.minimax_try2(board_state=move, depth = depth - 1, is_maximizing = False, show_minimax_boards = show_minimax_boards)
                eval, _ = minimax_results

                if show_minimax_boards:
                    print('The results of minimax are:', minimax_results)
                    print(maxEval, eval)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
                if show_minimax_boards:
                    print('The maxEval is:', maxEval)
            return maxEval, best_move
    
        else: #black's turn
            minEval = np.inf
            best_move = None
            for move in nextMove.get_legal_moves():
                if show_minimax_boards: # print the possible moves for error checking
                    print("Black's turn")
                    CheckerBoard.visualize_piece_numbers(move)
                    for key in move:
                        if key in move:
                            if move[key] != self.board_state[key]:
                                print(f'{key} can move from {self.board_state[key]} to {move[key]}')
                    for key in self.board_state:
                        if key not in move:
                            print(f'and can capture {key}')
                
                minimax_results = self.minimax_try2(board_state=move, depth = depth - 1, is_maximizing = True, show_minimax_boards = show_minimax_boards)
                eval, _ = minimax_results
                if show_minimax_boards:
                    print('The results of minimax are:', minimax_results)
                    print(minEval, eval)
                if eval < minEval:
                    minEval = eval
                    best_move = move
                if show_minimax_boards:
                    print('The minEval is:', minEval)
            return minEval, best_move
        

    def make_intelligent_move(self, board_state, depth, is_maximizing, show_minimax_boards=True):
        """
        Takes the best move from the minimax algorithm and returns the new board state.
        
        board_state: dict, the current board state
        depth: int, the depth of the minimax tree
        is_maximizing: bool, True if the current player is maximizing (white), False if the current player is minimizing (black)
        show_minimax_boards: bool, if True, print the minimax board states and some testing print statements at each depth of the minimax tree
        """
        new_board_state = self.minimax_try2(board_state, depth=depth, is_maximizing=is_maximizing, show_minimax_boards=show_minimax_boards)[1]
        # print what that move was
        if show_minimax_boards:
            for k,v in self.board_state.items():
                if k not in new_board_state.keys(): # this means a capture happened
                    print(f'{k} was captured by')
                if k in new_board_state.keys() and new_board_state[k] != self.board_state[k]:
                    print(f'{k} moved from {self.board_state[k]} to {new_board_state[k]}')
        return new_board_state