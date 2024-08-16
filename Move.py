from Location import Location
from copy import deepcopy

class Move:
    """Represents a move on the checkerboard, specifying the piece being moved and the target position"""

    def __init__(self, dict_piece_locations, color) -> None:
        self.dict_piece_locations = dict_piece_locations
        self.color = color
        
        # check which pieces have moves available
        self.available_moves = {} #self.list_available_moves()
        
        # check which pieces have captures available
        self.is_capture_available = None
        self.captures_available = {} # maybe to be deleted
        self.valid_moves = {}
        self.list_of_board_states = []  

   

############################## Functions for Simple Jumps ########################################

    def list_available_jumps(self):    
        """
        Which pieces can move and where can they move to?
        """

        # Helper function to check if a move is valid
        def is_valid_move(x, y):
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7 and move not in [(piece_location.x, piece_location.y) for piece_location in self.dict_piece_locations.values()]:
                # Check if the location is not occupied
                return (x,y)
            return False
        
        if self.color == 'black':
            black_dict_piece_locations = {key: value for key, value in self.dict_piece_locations.items() if key.startswith('black_')}
            king_black_dict_piece_locations = {key: value for key, value in self.dict_piece_locations.items() if key.startswith('king_black_')}
            
            for piece_name, location in black_dict_piece_locations.items():
                moves = []
                potential_moves = [(location.x + 1, location.y - 1), (location.x + 1, location.y + 1)]
                for move in potential_moves:
                    if is_valid_move(*move):
                        moves.append(move)
                self.available_moves[piece_name] = moves


            for piece_name, location in king_black_dict_piece_locations.items():
                moves = []
                potential_moves = [(location.x + 1, location.y - 1), (location.x + 1, location.y + 1), (location.x - 1, location.y - 1),(location.x - 1, location.y + 1)]       
                for move in potential_moves:
                    if is_valid_move(*move):
                        moves.append(move)
                self.available_moves[piece_name] = moves
        

        else: # color == 'white'
            white_dict_piece_locations = {key: value for key, value in self.dict_piece_locations.items() if key.startswith('white_')}
            king_white_dict_piece_locations = {key: value for key, value in self.dict_piece_locations.items() if key.startswith('king_white_')}

            for piece_name, location in white_dict_piece_locations.items():
                moves = []
                potential_moves = [(location.x - 1, location.y - 1), (location.x - 1, location.y + 1)]
                for move in potential_moves:
                    if is_valid_move(*move):
                        moves.append(move)
                self.available_moves[piece_name] = moves

            for piece_name, location in king_white_dict_piece_locations.items():
                moves = []
                potential_moves = [(location.x + 1, location.y - 1), (location.x + 1, location.y + 1), (location.x - 1, location.y - 1),(location.x - 1, location.y + 1)]       
                for move in potential_moves:
                    if is_valid_move(*move):
                        moves.append(move)
                self.available_moves[piece_name] = moves
        
        self.available_moves = {key: val for key, val in self.available_moves.items() if len(val) > 0}
        return self.available_moves
    
    def make_jump(self, piece_name, landing_position):
        """
        Returns a new board state after a piece has moved to a new location
        """
        dict_piece_locations_new = deepcopy(self.dict_piece_locations)
        original_position = self.dict_piece_locations[piece_name]
        dict_piece_locations_new[piece_name] = Location(landing_position[0], landing_position[1])
        # print(f'{piece_name} can move from {original_position} to {dict_piece_locations_new[piece_name]}')
        return dict_piece_locations_new
    

############################## Functions for Captures ########################################


    def is_opponent_piece(self, x, y, current_color):
        # Helper function to check if a cell is occupied by an opponent
        opponent_color = 'white' if current_color == 'black' else 'black'
        return any(piece.x == x and piece.y == y and opponent_color in name for name, piece in self.dict_piece_locations.items())

    def is_unoccupied(self, x, y):
        # Helper function to check if a cell is unoccupied
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        return not any(piece.x == x and piece.y == y for piece in self.dict_piece_locations.values())
    

    def _find_valid_captures_per_piece(self, piece_name, dict_piece_locations):
        """
        Which pieces have the possibility to capture an opponent's piece(s)?
        In this version of the game, a piece must capture if it can.
        """
        location = dict_piece_locations[piece_name]
        if self.color == 'black':
            if piece_name.startswith('black'): # Check for potential captures for a black piece
                potential_captures = [
                    ((location.x + 1, location.y - 1), (location.x + 2, location.y - 2)),
                    ((location.x + 1, location.y + 1), (location.x + 2, location.y + 2))
                ]
            elif piece_name.startswith('king_black'): # Check if it's a king piece
                potential_captures = [
                    ((location.x + 1, location.y - 1), (location.x + 2, location.y - 2)),
                    ((location.x + 1, location.y + 1), (location.x + 2, location.y + 2)),
                    ((location.x - 1, location.y - 1), (location.x - 2, location.y - 2)),
                    ((location.x - 1, location.y + 1), (location.x - 2, location.y + 2))
                ]
        else: # color == 'white'
            if piece_name.startswith('white'): # Check for potential captures for a white piece
                potential_captures = [
                    ((location.x - 1, location.y - 1), (location.x - 2, location.y - 2)),
                    ((location.x - 1, location.y + 1), (location.x - 2, location.y + 2))
                ]

            elif piece_name.startswith('king_white'): # Check if it's a king piece
                potential_captures = [
                    ((location.x + 1, location.y - 1), (location.x + 2, location.y - 2)),
                    ((location.x + 1, location.y + 1), (location.x + 2, location.y + 2)),
                    ((location.x - 1, location.y - 1), (location.x - 2, location.y - 2)),
                    ((location.x - 1, location.y + 1), (location.x - 2, location.y + 2))
                ]

        temp_list_possible_captures = []
        for opponent_pos, landing_pos in potential_captures:
            if self.is_opponent_piece(opponent_pos[0], opponent_pos[1], self.color) and self.is_unoccupied(landing_pos[0], landing_pos[1]):
                # build list of pieces with potential captures:
                captured_piece = [key for key, value in dict_piece_locations.items() if value.x == opponent_pos[0] and value.y == opponent_pos[1]][0]
                temp_list_possible_captures.append((captured_piece, landing_pos))
        # if len(temp_list_possible_captures) > 0: # only add to dictionary if there are captures available
        #     self.captures_available[piece_name] = temp_list_possible_captures
        #     print(self.captures_available)
        return temp_list_possible_captures


    def _recursive_capture(self, piece_name, dict_piece_locations, color):
        """
        Recursively find all possible captures for a piece. Used to find all possible captures for one piece at a time.
        """
        possible_captures = Move(dict_piece_locations, color)._find_valid_captures_per_piece(piece_name, dict_piece_locations)

        if len(possible_captures) == 0: # no more captures possible 
            self.list_of_board_states.append(dict_piece_locations)
            #### return what the difference is between the initial board state and the final board state
            # for key in dict_piece_locations:
                # if key in self.dict_piece_locations:
                    # if dict_piece_locations[key] != self.dict_piece_locations[key]:
                        # print(f'{key} can move from {self.dict_piece_locations[key]} to {dict_piece_locations[key]}')
            # for key in self.dict_piece_locations:
                # if key not in dict_piece_locations:
                    # print(f'and can capture {key}')
            return dict_piece_locations # end recursive capturing
        
        for possible_capture in possible_captures: 
            board_state_new = deepcopy(dict_piece_locations) # make a copy of the board state for each possible capture

            deleted_piece = possible_capture[0]
            new_location = possible_capture[1]
            board_state_new[piece_name] = Location(new_location[0], new_location[1])
            del board_state_new[deleted_piece]

            self._recursive_capture(piece_name, board_state_new, color)


    def get_all_valid_captures(self):
        """
        Returns the list of all possible board states after all possible captures have been made.
        Can be used if more than one piece can make captures.
        """
        # self.captures_available = {}
        for piece_name in self.dict_piece_locations.keys():
            if self.color in piece_name:
                self._recursive_capture(piece_name, self.dict_piece_locations, self.color)
         
        self.list_of_board_states = [x for x in self.list_of_board_states if x != self.dict_piece_locations]
        return self.list_of_board_states
        

############################## Functions for Both Simple Jumps and Captures
    def get_legal_moves(self):
        """
        Returns a list of board states after all possible moves have been made.
        If captures are possible, only a list of board states with captures are returned.
        Otherwise, a list of board states with simple jumps are returned.
        """
        self.valid_moves = []

        if self.get_all_valid_captures():
            self.valid_moves = self.list_of_board_states
            self.is_capture_available = True

        else: # no captures possible, only simple jumps
            # print('no captures available')  
            self.list_available_jumps()
            for piece_name, moves in self.available_moves.items():
                for move in moves:
                    self.valid_moves.append(self.make_jump(piece_name, move))

        return self.valid_moves


