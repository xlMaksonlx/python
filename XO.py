board_size = 3
board = [1,2,3,4,5,6,7,8,9]
val_input = '0123456789'
def drow_board():
    for i in range(board_size):
        print(board[i*3],'|',board[1+i*3],'|',board[2+i*3])
def step_player(index, cur_player):
    if index not in board or board[index - 1] in ('X', 'O'):
        return False
    board[index-1] = cur_player
    return True
def chek():
    win = ''
    win_combo = ((0,1,2),(3,4,5),(6,7,8),
                 (0,3,6),(1,4,7),(2,5,8),
                 (0,4,8),(2,4,6)
                 )
    for pos in win_combo:
        if board[pos[0]] == board[pos[1]] and board[pos[1]] == board[pos[2]]:
            win = board[pos[0]]
    return win
def start():
    cur_player = 'X'
    num_step =1
    drow_board()
    while num_step <= 9 and not chek():
        in_val = input('Ходит игрок ' + cur_player + ' Введите номер клетки для хода, 0 - выход из игры')
        if in_val in val_input:
            index = int(in_val)
            if index == 0:
                print('Игрок ' + cur_player + ' вышел из игры.')
                break
            if step_player(index, cur_player):
                print('Ход совершен')
                if cur_player == 'X':
                    cur_player = 'O'
                elif cur_player == 'O':
                    cur_player = 'X'
                drow_board()
                num_step += 1
            else:
                print('Неверный ход, повторите')
        else:
            print('Введено неприемлимое значение, введите число от 0 до 9')
    if (num_step > 9 and not chek()):
        print('Игра окончена. Ничья.')
    else:
        print('Выиграл '+ chek())

start()

