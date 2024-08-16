from Location import Location
from Move import Move
from CheckerBoard import CheckerBoard
from NaiveAgent import NaiveAgent
from IntelligentAgent import IntelligentAgent
import time


class Game:
    """
    The Game class is used to run one or multiple games of checkers. 
    It also maintains the rules of the game including initializing the board, checking for promotions (kings), and checking for the winner.
    """

    def __init__(self) -> None:
        self.board_state = {}

    def initialize_board(self):
        self.board_state = {'black_piece_1': Location(0, 1), 
                                'black_piece_2': Location(0, 3), 
                                'black_piece_3': Location(0, 5),
                                'black_piece_4': Location(0, 7),
                                'black_piece_5': Location(1, 0),
                                'black_piece_6': Location(1, 2),
                                'black_piece_7': Location(1, 4),
                                'black_piece_8': Location(1, 6),
                                'black_piece_9': Location(2, 1),
                                'black_piece_10': Location(2, 3),
                                'black_piece_11': Location(2, 5),
                                'black_piece_12': Location(2, 7),
                                'white_piece_1': Location(5, 0), 
                                'white_piece_2': Location(5, 2), 
                                'white_piece_3': Location(5, 4),
                                'white_piece_4': Location(5, 6),
                                'white_piece_5': Location(6, 1),
                                'white_piece_6': Location(6, 3),
                                'white_piece_7': Location(6, 5),
                                'white_piece_8': Location(6, 7),
                                'white_piece_9': Location(7, 0),
                                'white_piece_10': Location(7, 2),
                                'white_piece_11': Location(7, 4),
                                'white_piece_12': Location(7, 6)}
        return self.board_state
    
    def check_for_promotion(self):
        """
        Check if a piece reaches the other end of the board and promote it to a King.

        :param board_state: A dictionary representing the board state, with keys as positions and values as piece identifiers.
        :param position: The position of the piece to check for promotion, in (row, column) format.

        Returns the board state with the piece promoted to king
        """
        black_dict_piece_locations = {key: value for key, value in self.board_state.items() if key.startswith('black_')}
        white_dict_piece_locations = {key: value for key, value in self.board_state.items() if key.startswith('white_')}

        
        # Promote to King if conditions are met
        for key in white_dict_piece_locations.keys():
            if white_dict_piece_locations[key].x == 0:
                self.board_state[f'king_{key}'] = white_dict_piece_locations[key]
                del self.board_state[key]

        for key in black_dict_piece_locations.keys():
            if black_dict_piece_locations[key].x == 7:
                self.board_state[f'king_{key}'] = black_dict_piece_locations[key]
                del self.board_state[key]
        
        return self.board_state

    def winner(self):
        """Check if the game is over and return the winner"""
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


    def game_evaluation(self, color):
        """
        Returns the evaluation of the game state.
        White is the maximizing player and Black is the minimizing player.
        """
        winning_player = self.winner()
        if winning_player == 'Black': 
            return -1000
        elif winning_player == 'White':
            return 1000

        black_pieces = [location for key, location in self.board_state.items() if key.startswith('black_')]
        white_pieces = [location for key, location in self.board_state.items() if key.startswith('white_')]
        king_black_pieces = [location for key, location in self.board_state.items() if key.startswith('king_black_')]
        king_white_pieces = [location for key, location in self.board_state.items() if key.startswith('king_white_')]

        return len(white_pieces) + (len(king_white_pieces)*2) - len(black_pieces) - (len(king_black_pieces)*2)





    def run(self, show_board=True):
        """
        The run() method runs a game of checkers. It initializes the board, and then runs the game turn by turn until there is a winner.
        In this version of the game, both black and white players are naive agents that make random moves.
        """
        self.board_state = self.initialize_board()
        if show_board:
            print('Initialize Board:')
            CheckerBoard.visualize_piece_numbers(self.board_state)
        i = 0
        current_player = 'black'  # Start with black
        while self.winner() is None:
            i += 1
            if show_board:
                print(f"\n\n{current_player.capitalize()}'s turn (turn {i}):")
            naiveagent = NaiveAgent(current_player, self.board_state)
            self.board_state = naiveagent.make_next_random_move(show_board) 
            self.check_for_promotion()  # did any of the moves make any pieces a king?
            if show_board:
                print()
                CheckerBoard.visualize_piece_numbers(self.board_state)
                print(self.board_state)
            
            winning_player = self.winner()
            if winning_player != None:
                print(f"{winning_player} wins!")
                break
            if show_board:
                print(f'Board score: {self.game_evaluation(current_player)}')
            # Switch player
            current_player = 'white' if current_player == 'black' else 'black'
        if show_board:
            print(f'Final board score: {self.game_evaluation(current_player)}')




    def run_with_ia(self, black='intelligent', white='naive', board_depth = 3, show_board=True):
        """
        The run_with_ia() method runs a game of checkers. It initializes the board, and then runs the game turn by turn until there is a winner.
        In this version of the game, the black player is an intelligent agent that uses the minimax algorithm and the white player is a naive agent that makes random moves.
        """
        
        self.board_state = self.initialize_board()
        if show_board:
            print('Black is the Intelligent Agent, White is the Naive Agent')
            print('Initialize Board:')
            CheckerBoard.visualize_piece_numbers(self.board_state)
        i = 0
        current_player = 'black'  # Start with black
        while self.winner() is None:
            i += 1
            if show_board:
                print(f"\n\n{current_player.capitalize()}'s turn (turn {i}):")
            if current_player == 'black':
                if black == 'naive':
                    naiveagent = NaiveAgent(current_player, self.board_state)
                    self.board_state = naiveagent.make_next_random_move(show_board=False) 
                elif black == 'intelligent':
                    intelligentagent = IntelligentAgent(current_player, self.board_state)
                    self.board_state = intelligentagent.make_intelligent_move(self.board_state, board_depth, False, show_minimax_boards=False)
            else: # white's turn
                if white == 'naive':
                    naiveagent = NaiveAgent(current_player, self.board_state)
                    self.board_state = naiveagent.make_next_random_move(show_board=False) 
                elif white == 'intelligent':
                    intelligentagent = IntelligentAgent(current_player, self.board_state)
                    self.board_state = intelligentagent.make_intelligent_move(self.board_state, board_depth, True, show_minimax_boards=False)

            self.check_for_promotion()  # did any of the moves make any pieces a king?
            if show_board:
                print()
                CheckerBoard.visualize_piece_numbers(self.board_state)
                print(self.board_state)
            
            winning_player = self.winner()
            if winning_player != None:
                print(f"{winning_player} wins!")
                if show_board:
                    print(f'Board score: {self.game_evaluation(current_player)}')
                return winning_player, i
            # Switch player
            time.sleep(0.5)
            current_player = 'white' if current_player == 'black' else 'black'
        if show_board:
            print(f'Final board score: {self.game_evaluation(current_player)}')

    
    def run_naive_multiple_games(self, num_games=1000):
        """
        Run multiple games of checkers with two naive agents and print the results.
        """
        black_wins = 0
        white_wins = 0
        game_durations = []

        for _ in range(num_games):
            print(f"\n\nPlaying Game {_ + 1}:")
            start_time = time.time()
            self.run(show_board=False)
            end_time = time.time()
            duration = end_time - start_time
            game_durations.append(duration)

            winning_player = self.winner()  # Check the winner after the game ends
            if winning_player == 'Black':
                black_wins += 1
            elif winning_player == 'White':
                white_wins += 1
        
        print(f"Black wins: {black_wins}")
        print(f"White wins: {white_wins}")
        print(f"Average game duration: {sum(game_durations) / len(game_durations):.2f} seconds")


    def run_ia_multiple_games(self, board_depth, num_games=1000):
        """
        Runs multiple games of checkers with an intelligent agent and a naive agent and prints the results.
        """
        black_wins = 0
        white_wins = 0
        game_durations = []
        turns_to_win = []

        for _ in range(num_games):
            print(f"\n\nPlaying Game {_ + 1}:")
            start_time = time.time()
            winning_player, nb_turns = self.run_with_ia(board_depth=board_depth, show_board=False)
            end_time = time.time()
            duration = end_time - start_time
            game_durations.append(duration)

            # Check the winner after the game ends
            if winning_player == 'Black':
                black_wins += 1
            elif winning_player == 'White':
                white_wins += 1

            # Check the number of turns it took to win
            turns_to_win.append(nb_turns)

        print(f"Black wins: {black_wins}")
        print(f"White wins: {white_wins}")
        print(f"Average game duration: {sum(game_durations) / len(game_durations):.2f} seconds")
        print(f"Average number of turns to win: {sum(turns_to_win) / len(turns_to_win):.2f}")
