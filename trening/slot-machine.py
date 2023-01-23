import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    columns = []
    current_symbols = all_symbols[:]
    for col in range(cols):
        column = []
        for row in range(rows):
            value = random.choice(all_symbols)
            column.append(value)
            current_symbols.remove(value)
        columns.append(column)
    return columns


def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=' | ')
            else:
                print(column[row] )



def deposit():
    while True:
        amount = input("What would you like to deposit: $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amaunt must be greater than 0.")
        else:
            print("Please enter a number.")
    return amount


def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1/{MAX_LINES})")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= 3:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")
    return lines

def bet_with():
    while True:
        bet = input(f"Bet with ({MIN_BET}/{MAX_BET}$):")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            else:
                print("Enter a valid amount")
        else:
            print("Please enter a number.")
    return bet


def main():
    balance = deposit()
    lines = get_number_of_lines()
    while True:
        bet = bet_with()
        if bet <= balance:
            break
        else:
            question = input("You don't have enough money in your balance. Do you want to deposit? (y/n)")
            if question == 'y':
                deposit()

    total_bet = lines * bet
    print(get_slot_machine_spin(3, 3, symbol_count))
    print(f'You are betting {bet} on {lines}. Total bet is {total_bet}')
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)


main()
