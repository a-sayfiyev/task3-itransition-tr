import sys
import hmac
import hashlib
import secrets
from math import floor

class Crypto:
    @staticmethod
    def generate_key():
        return secrets.token_bytes(32)

    @staticmethod
    def generate_hmac(key, message):
        return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

class Rules:
    def __init__(self, moves):
        self.moves = moves
        self.n = len(moves)
        self.p = floor(self.n / 2)

    def get_winner(self, player_move, computer_move):
        a, b = self.moves.index(player_move), self.moves.index(computer_move)
        if a == b:
            return 'Draw'
        elif (a - b + self.p + self.n) % self.n - self.p < 0:
            return 'You win!'
        else:
            return 'Computer wins!'

class HelpTable:
    def generate_table(self, moves):
        n = len(moves)
        p = floor(n / 2)
        table = '+{}+\n'.format('+'.join(['-' * 12 for _ in range(n + 1)]))
        row_format = '| {:^10} ' * (n + 1) + '|\n'
        table += row_format.format('PC \\ User', *moves)
        table += '+{}+\n'.format('+'.join(['-' * 12 for _ in range(n + 1)]))

        for i, move in enumerate(moves):
            results = []
            for j in range(n):
                if i == j:
                    results.append('Draw')
                elif (i - j + p + n) % n - p < 0:
                    results.append('Win')
                else:
                    results.append('Lose')
            table += row_format.format(move, *results)
            table += '+{}+\n'.format('+'.join(['-' * 12 for _ in range(n + 1)]))
        return table

class Game:
    def __init__(self, moves):
        self.moves = moves
        self.rules = Rules(moves)
        self.help_table = HelpTable()

    def play(self):
        self.key = Crypto.generate_key()
        self.computer_move = secrets.choice(self.moves)
        hmac_result = Crypto.generate_hmac(self.key, self.computer_move)

        print(f'HMAC: {hmac_result}')
        self.user_move = self.get_user_move()
        if self.user_move == '0':
            print('Exit the game.')
            return
        if self.user_move == '?':
            print(self.help_table.generate_table(self.moves))
            return self.play()

        result = self.rules.get_winner(self.user_move, self.computer_move)
        print(f'Your move: {self.user_move}')
        print(f'Computer move: {self.computer_move}')
        print(result)
        print(f'HMAC key: {self.key.hex()}')

    def get_user_move(self):
        while True:
            print('\nAvailable moves:')
            for i, move in enumerate(self.moves):
                print(f'{i + 1} - {move}')
            print('0 - exit')
            print('? - help')
            choice = input('Enter your move: ')
            if choice.isdigit() and int(choice) in range(1, len(self.moves) + 1):
                return self.moves[int(choice) - 1]
            elif choice == '0' or choice == '?':
                return choice
            else:
                print('Invalid input, try again.')

def validate_args(args):
    if len(args) < 3 or len(args) % 2 == 0 or len(set(args)) != len(args):
        print('Error: Incorrect number of arguments. Please provide an odd number of non-repeating strings.')
        print('Example: python3 game.py Rock Paper Scissors Lizard Spock')
        sys.exit(1)

if __name__ == '__main__':
    validate_args(sys.argv[1:])
    moves = sys.argv[1:]

    game = Game(moves)
    game.play()
