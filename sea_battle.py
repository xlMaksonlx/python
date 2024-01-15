from random import randint

class BoardException(Exception):
    pass

#класс исключения выстрела за пределы поля
class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

#класс исключения выстрела в одну и ту же клетку
class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    def __str__(self):
        return "Корабль находится не внути поля"

class Player:
    pass
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Ship:
    def __init__(self,coors:Dot, life:int, course:bool):
        self.coors = coors
        self.life = life
        self.course = course
        self.ship_len = life
        self.course = course

    @property
    def ship_coors(self):
        res = []
        for i in range(self.ship_len):
            coor_x = self.coors.x
            coor_y = self.coors.y

            if not self.course:
                coor_x +=i
            else:
                coor_y +=i

            res.append(Dot(coor_x,coor_y))

        return res


class Board:
    def __init__(self, hid = False, size=6):
        self.size = size
        self.hid = hid
        self.ships = []
        self.busy = []
        self.field = [['O']*size for i in range(size)]
        self.count = 0

    def add_ship(self, ship):
        for d in ship.ship_coors:
            if self.chek_dot(d) or d in self.busy:
                raise BoardWrongShipException()
            elif not self.chek_dot(d) and d not in self.busy:
                self.field[d.x][d.y] = "■"
                self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        n = [(-1,-1), (-1,0),(-1,1),
             (0,-1), (0,0), (0,1),
             (1,-1),(1,0),(1,1)]
        for d in ship.ship_coors:
            for x,y in n:
                con = Dot(d.x + x, d.y + y)
                if not self.chek_dot(con) and con not in self.busy:
                    if verb:
                        self.field[con.x][con.y] = "*"
                    self.busy.append(con)


    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")

        return res

    def chek_dot(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self,d):
        if self.chek_dot(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.ship_coors:
                ship.life -= 1
                self.field[d.x][d.y] = 'X'
                if ship.life == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Корабль уничтожен')
                    return False
                else:
                    print('Корабль ранен')
                    return True

        self.field[d.x][d.y] = '*'
        print('Мимо')
        return False

    def begin(self):
        self.busy = []

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy


    def ask(self):
        pass

    def move(self):
        try:
            target = self.ask()
            repeat = self.enemy.shot(target)
        except BoardException as e:
            print(e)


class Comp(Player):
    def ask(self):
        d= Dot(randint(0,5), randint(0,5))
        print(f'Ход компьютера {d.x +1} {d.y +1}')
        return d

class User(Player):

    def ask(self):

        while True:
            cord_x = input('Введите координату строки: ')
            cord_y = input('Введите координату столбца: ')

            self.escape = (cord_x == 'exit') or (cord_y == 'exit')

            x, y = cord_x, cord_y

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x-1,y-1)

class Game:
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = Comp(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3,2,2,1,1,1,1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def start(self):

        print('      Игра ')
        print('  "Морской бой" ')
        print("_"*40)
        print("Вы будете играть против компьютера ")
        print("Корабли расставлены в случайном порядке")
        print("Правила ввода координат: ")
        print('По очереди вводим координату х, затем координату у')
        print("х - номер строки, у - номер столбца")

        num = 0

        while True:
            print('Поле пользователя')
            print(self.us.board)
            print('_'*10)
            print('Поле компьютера')
            print(self.ai.board)
            print('_' * 10)

            if num % 2 == 0:
                print("Ход пользователя!")
                repeat = self.us.move()
            else:
                print("Ход компьютера!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Вы выиграли!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Вы проиграли!")
                break
            num += 1

a = Game()
a.start()


