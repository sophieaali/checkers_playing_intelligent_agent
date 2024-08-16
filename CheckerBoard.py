class CheckerBoard:

    """
    The CheckerBoard class is used to represent the board state of the checkers game. It is used to visualize the board state of the checkers game.
    The method visualize_checkers_board is a simple, compact visualization of the board.
    The method visualize_piece_numbers is a more detailed visualization of the board, showing the piece numbers of each piece on the board.
    """

    @staticmethod
    def visualize_checkers_board(dict_piece_locations):
        # Initialize an 8x8 board with empty squares
        board = [['|  ' for _ in range(8)] for _ in range(8)]

        black_pieces = [location for key, location in dict_piece_locations.items() if key.startswith('black_')]
        white_pieces = [location for key, location in dict_piece_locations.items() if key.startswith('white_')]
        king_black_pieces = [location for key, location in dict_piece_locations.items() if key.startswith('king_black_')]
        king_white_pieces = [location for key, location in dict_piece_locations.items() if key.startswith('king_white_')]
        
        # Place black pieces
        for piece in black_pieces:
            board[piece.x][piece.y] = '|B '
        
        # Place white pieces
        for piece in white_pieces:
            board[piece.x][piece.y] = '|W '

        # Place king pieces
        for piece in king_black_pieces:
            board[piece.x][piece.y] = '|KB'

        for piece in king_white_pieces:
            board[piece.x][piece.y] = '|KW'
        
        # Print the board
        for (i,row) in enumerate(board):
            print(i, ''.join(row) + '|')
        print('   0  1  2  3  4  5  6  7')



    @staticmethod
    def visualize_piece_numbers(dict_piece_locations):
        board = [['|    ' for _ in range(8)] for _ in range(8)]

        for piece, location in dict_piece_locations.items():
            if 'king_black' in piece:
                label = 'KB' + piece.split('_')[-1]
                if label in (['KB10', 'KB11', 'KB12']):
                    board[location.x][location.y] = f'|{label}'
                else:
                    board[location.x][location.y] = f'|{label} '
            
            elif 'king_white' in piece:
                label = 'KW' + piece.split('_')[-1]
                if label in (['KW10', 'KW11', 'KW12']):
                    board[location.x][location.y] = f'|{label}'
                else:
                    board[location.x][location.y] = f'|{label} '

            elif 'black' in piece:
                label = 'B' + piece.split('_')[-1]
                if label in (['B10', 'B11', 'B12']):
                    board[location.x][location.y] = f'|{label} '
                else:
                    board[location.x][location.y] = f'|{label}  '

            elif 'white' in piece:
                label = 'W' + piece.split('_')[-1]
                if label in (['W10', 'W11', 'W12']):
                    board[location.x][location.y] = f'|{label} '
                else:
                    board[location.x][location.y] = f'|{label}  '

            
        for (i,row) in enumerate(board):
            print(i, ''.join(row) + '|')
        print('    0    1    2    3    4    5    6    7')