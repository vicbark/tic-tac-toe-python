import random
import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Крестики-нолики")

board = [' ' for _ in range(9)]  # Инициализация доски / Laud initialisation / Board initialization

player_symbol = 'X'  # Символ игрока / Mängija sümbol / Player symbol
computer_symbol = 'O'  # Символ компьютера / Arvuti sümbol / Computer symbol
game_count = 0  # Счетчик игр / Mängude loendur / Game count
player_starts = game_count % 2 == 0  # Определение, кто начинает игру / Määratakse, kes alustab mängu / Determine who starts the game

score_label = tk.Label(window, text="Счет: Игрок 0 - Компьютер 0", font=('Arial', 16))
score_label.grid(row=0, column=0, columnspan=3)

player_wins = 0  # Счетчик побед игрока / Mängija võitude loendur / Player wins count
computer_wins = 0  # Счетчик побед компьютера / Arvuti võitude loendur / Computer wins count

def display_board():
    for i in range(9):
        button_list[i].config(text=board[i])

def update_turn_label():
    if player_starts:
        turn_label.config(text="Ход: Игрок")  # Mängija käik / Player's turn
    else:
        turn_label.config(text="Ход: Компьютер")  # Arvuti käik / Computer's turn

def update_score_label():
    score_label.config(text=f"Счет: Игрок {player_wins} - {computer_wins} Компьютер ")  # Mängija skoor - Arvuti skoor / Player score - Computer score

def player_move(idx):
    global player_wins, game_count, player_starts
    if player_starts and board[idx] == ' ':
        board[idx] = player_symbol
        display_board()

        if check_winner(player_symbol):
            messagebox.showinfo("Результат", "Игрок победил!")  # Mängija võitis! / Player wins!
            player_wins += 1
            update_score_label()
            reset_game()
        elif ' ' not in board:
            messagebox.showinfo("Результат", "Ничья!")  # Viik! / Draw!
            reset_game()
        else:
            player_starts = False
            update_turn_label()
            if not player_starts:
                window.after(1000, computer_move)

def computer_move():
    global computer_wins, game_count, player_starts
    empty_cells = [i for i in range(9) if board[i] == ' ']

    # Проверяем возможность победы компьютера на следующем ходу / Kontrollitakse arvuti järgmise käigu võiduvõimalust / Check if the computer can win on the next move
    for cell in empty_cells:
        board[cell] = computer_symbol
        if check_winner(computer_symbol):
            board[cell] = computer_symbol
            display_board()
            messagebox.showinfo("Результат", "Компьютер победил!")  # Arvuti võitis! / Computer wins!
            computer_wins += 1
            update_score_label()
            reset_game()
            return
        board[cell] = ' '

    # Проверяем возможность блокировать победу игрока на следующем ходу / Kontrollitakse mängija järgmise käigu võiduvõimalust / Check if the player can win on the next move and block it
    for cell in empty_cells:
        board[cell] = player_symbol
        if check_winner(player_symbol):
            board[cell] = computer_symbol
            display_board()
            player_starts = True
            update_turn_label()
            return
        board[cell] = ' '

    # Выбираем случайную свободную ячейку / Valitakse juhuslik vaba lahtris / Choose a random empty cell
    move = random.choice(empty_cells)
    board[move] = computer_symbol
    display_board()

    if check_winner(computer_symbol):
        messagebox.showinfo("Результат", "Компьютер победил!")  # Arvuti võitis! / Computer wins!
        computer_wins += 1
        update_score_label()
        reset_game()
    elif ' ' not in board:
        messagebox.showinfo("Результат", "Ничья!")  # Viik! / Draw!
        reset_game()
    else:
        player_starts = True
        update_turn_label()

def check_winner(player):
    winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for combination in winning_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] == player:
            return True
    return False

def reset_game():
    global player_symbol, computer_symbol, game_count, player_starts, board
    choice = messagebox.askquestion("Новая игра", "Хотите начать новую игру?")  # Uus mäng? / New game?
    if choice == 'yes':
        game_count += 1
        player_starts = game_count % 2 == 0
        player_symbol, computer_symbol = computer_symbol, player_symbol
        board = [' ' for _ in range(9)]
        display_board()
        update_turn_label()

        if not player_starts:
            window.after(1000, computer_move)

button_list = []
for i in range(9):
    button = tk.Button(window, text=' ', font=('Arial', 20), width=6, height=3, command=lambda idx=i: player_move(idx))
    button.grid(row=(i // 3) + 2, column=i % 3)
    button_list.append(button)

display_board()

turn_label = tk.Label(window, text="Ход: Игрок", font=('Arial', 12))
turn_label.grid(row=12, column=0, columnspan=3, pady=10)

update_turn_label()
update_score_label()

window.mainloop()
