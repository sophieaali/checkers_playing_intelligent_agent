from Move import Move
import random


class NaiveAgent():
    """
    The NaiveAgent class is used to represent a naive agent that makes random moves on the board.
    If a capture is possible, the NaiveAgent must make a capture. If multiple captures are possible, 
    the NaiveAgent will choose one of the captures at random.
    If no capture is possible, the NaiveAgent must make a random move.
    """
    def __init__(self, color, board_state):
        self.color = color
        self.board_state = board_state
        self.nextMove = Move(self.board_state, self.color)


    def make_next_random_move(self, show_board=True):
        """
        Using the Move class's get_legal_moves method, get all the legal moves for the current player.
        Then for all legal/valid moves, pick a random move and return the new board state.
        
        show_board: bool, if True, print the move made by the NaiveAgent.
        """

        valid_moves = self.nextMove.get_legal_moves()
        # pick a random board state from all valid moves
        new_board_state = random.choice(valid_moves)
        if show_board:  # print what that move was
            if self.nextMove.is_capture_available == True:
                for k,v in new_board_state.items():
                    if self.board_state[k] != new_board_state[k]:
                        print(f'{k} moved from {self.board_state[k]} to {v}')
                for k in self.board_state.keys():    
                    if k not in new_board_state:
                        print(f'and {k} was captured')
            else:
                for k,v in new_board_state.items():
                    if self.board_state[k] != new_board_state[k]:
                        print(f'{k} moved from {self.board_state[k]} to {v}')
        return new_board_state
            

    