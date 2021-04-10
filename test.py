import random

class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.columns = [None for i in range(0, self.width * self.height)]

    def drop(self, column, player):
        for i in range(self.height):
            if self.__at(column, i) == None:
                break
        self.columns[(column * self.height) + i] = player

    def __at(self, x, y):
        if x >= self.width or x < 0:
            return "OFF"

        if y >= self.height or y < 0:
            return "OFF"

        return self.columns[(x * self.height) + y]

    def __check_at(self, x, y):
        def collapse(l):
            f = next(l)
            for i in l:
                if i != f:
                    return None
            return f

        possible = [[(x, y), (x + 1, y), (x + 2, y), (x + 3, y)],
                    [(x, y), (x, y + 1), (x, y + 2), (x, y + 3)],
                    [(x, y), (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)],
                    [(x, y), (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)]]
        possible = map(lambda possibility: map(lambda pos: self.__at(pos[0], pos[1]), possibility), possible)
        possible = map(collapse, possible)
        for res in possible:
            if res:
                return res
        return None

    def __count_at(self, x, y, for_player):
        possible = [[(x, y), (x + 1, y), (x + 2, y), (x + 3, y)],
                    [(x, y), (x, y + 1), (x, y + 2), (x, y + 3)],
                    [(x, y), (x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)],
                    [(x, y), (x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)]]

        possible = map(lambda possibility: map(lambda pos: self.__at(pos[0], pos[1]), possibility), possible)

        c = 0
        for p in possible:
            counts = False
            for player in p:
                if player == for_player:
                    counts = True
                    continue

                if player == "OFF":
                    counts = False
                    break
                if player != None and player != for_player:
                    counts = False
                    break

            if counts:
                c += 1

        return c

    def __is_column_empty(self, x):
        for i in range(self.height):
            if self.__at(x, i) == None:
                return True

        return False

    def get_winner(self):
        for i in range(self.width):
            for j in range(self.height):
                res = self.__check_at(i, j)
                if res:
                    return res

        return None

    def get_heuristic(self, player, other_player):
        c = 0
        for i in range(self.width):
            for j in range(self.height):
                c += self.__count_at(i, j, player)
                c -= self.__count_at(i, j, other_player)

        return c

    def is_draw(self):
        for i in range(self.width):
            for j in range(self.height):
                if not self.__at(i, j):
                    return False
        return True

    def get_moves(self):
        moves = range(self.width)
        moves = filter(lambda x: self.__is_column_empty(x), moves)
        return moves

    def state_for_move(self, move, player):
        toR = GameState(self.width, self.height)
        toR.columns = list(self.columns)

        toR.drop(move, player)
        return toR

    def get_num_turns(self):
        return sum(map(lambda x: len(x), self.columns))

    def __str__(self):
        toR = ""
        toR += "-"*13
        toR += "\n"
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                at = self.__at(x, y)
                toR += (at if at else " ") + " "
            toR += "\n"
        toR += "-" * 13
        toR += "\n"
        for x in range(self.width):
            toR += str(x+1) + " "
        toR += "\n"


        return toR

    def __hash__(self):
        c = 0
        first_found = None
        for i in range(self.width):
            for j in range(self.height):
                here = self.__at(i, j)
                if here != None and first_found == None:
                    first_found = here
                if here == first_found:
                    c += 3 ** ((i * self.height) + j)
                elif here != None and here != first_found:
                    c += 2 * 3 ** ((i * self.height) + j)

        return c

    def rule_based(self, move, player, past):
        toR = GameState(self.width, self.height)
        toR.columns = list(self.columns)

        if all(h == None for h in toR.columns):
            move=3
            print("이 룰은 착수점이 없을때 4열에 두는 룰 입니다.")
        elif toR.columns[12]== 'X' and toR.columns[18]=='X' and toR.columns[30]=='X':
            move=4
            if toR.columns[12]== 'X' and toR.columns[18]=='X' and toR.columns[30]=='X' and toR.columns[24]=='O':
                if toR.columns[(past + 1) * 6 - 1] == None:
                    move = past
                else:
                    for i in range(100):
                        move = random.randrange(0, 7)
                        temp = move + 1
                        if toR.columns[(temp * 6) - 1] == None:
                            break
                        else:
                            toR.columns[(temp * 6) - 1] = toR.columns[(temp * 6) - 1]
            print("이 룰은 초반 공격에 대한 방어 룰 입니다..")
        elif toR.columns[6]== 'X' and toR.columns[18]=='X' and toR.columns[24]=='X':
            move=2
            if toR.columns[6]== 'X' and toR.columns[18]=='X' and toR.columns[24]=='X' and toR.columns[12]=='O':
                if toR.columns[(past + 1) * 6 - 1] == None:
                    move = past
                else:
                    for i in range(100):
                        move = random.randrange(0, 7)
                        temp = move + 1
                        if toR.columns[(temp * 6) - 1] == None:
                            break
                        else:
                            toR.columns[(temp * 6) - 1] = toR.columns[(temp * 6) - 1]
            print("이 룰은 초반 공격에 대한 방어 룰 입니다..")
        elif toR.columns[12]== 'X' and toR.columns[18]=='X':
            move=1
            if toR.columns[12]== 'X' and toR.columns[18]=='X' and toR.columns[6]=='O':
                if toR.columns[(past + 1) * 6 - 1] == None:
                    move = past
                else:
                    for i in range(100):
                        move = random.randrange(0, 7)
                        temp = move + 1
                        if toR.columns[(temp * 6) - 1] == None:
                            break
                        else:
                            toR.columns[(temp * 6) - 1] = toR.columns[(temp * 6) - 1]
            print("이 룰은 초반 공격에 대한 방어 룰 입니다..")
        elif toR.columns[18]== 'X' and toR.columns[24]=='X':
            move=5
            if toR.columns[18]== 'X' and toR.columns[24]=='X' and toR.columns[30]=='O':
                if toR.columns[(past + 1) * 6 - 1] == None:
                    move = past
                else:
                    for i in range(100):
                        move = random.randrange(0, 7)
                        temp = move + 1
                        if toR.columns[(temp * 6) - 1] == None:
                            break
                        else:
                            toR.columns[(temp * 6) - 1] = toR.columns[(temp * 6) - 1]
            print("이 룰은 초반 공격에 대한 방어 룰 입니다..")
        elif toR.columns[(past+1)*6-1]== None:
            move=past
            print("이 룰은 상대방의 착수점 위에 두는 룰 입니다.")
        else:
            for i in range(100):
                move = random.randrange(0, 7)
                temp = move + 1
                if toR.columns[(temp * 6) - 1] == None:
                    break
                else:
                    toR.columns[(temp * 6) - 1] = toR.columns[(temp * 6) - 1]
            print("이 룰은 랜덤 룰베이스입니다.")

        toR.drop(move, player)
        return toR


prune = 0
no_prune = 0
terminals = 0
table_hits = 0


class GameTreeNode:
    def __init__(self, game_state, player, other_player, turn, alpha, beta, transpose, p):
        self.state = game_state
        self.player = player
        self.other_player = other_player
        self.turn = turn
        self.weight = 0
        self.transposition_table = transpose

        self.alpha = alpha
        self.beta = beta

        self.min_child = None
        self.max_child = None
        self.p = p

    def __is_min_node(self):
        return not self.turn

    def __is_max_node(self):
        return self.turn

    def is_terminal(self):
        return self.state.get_winner() or self.state.is_draw()

    def __heuristic_for_state(self, state):
        term_stat = state.get_winner() or state.is_draw()
        if term_stat:
            if term_stat and term_stat == self.player:
                return 1000
            if term_stat and term_stat == True:
                return 0
            return -1000

        return state.get_heuristic(self.player, self.other_player)

    def get_weight(self, max_moves=1000):
        global prune, no_prune, table_hits, terminals

        term_stat = self.is_terminal()
        if term_stat:
            terminals += 1
            if term_stat and term_stat == self.player:
                return 1000
            if term_stat and term_stat == True:
                return 0

            return -1000

        if max_moves == 0:
            # 휴리스틱 설정
            return self.state.get_heuristic(self.player, self.other_player)

        move_states = map(lambda x: (x, self.state.state_for_move(x, self.player if self.turn else self.other_player)),
                          self.state.get_moves())
        new_states = sorted(move_states, key=lambda x: self.__heuristic_for_state(x[1]), reverse=self.__is_max_node())
        for move, state in new_states:
            child = GameTreeNode(state, self.player, self.other_player, not self.turn,
                                 self.alpha, self.beta, self.transposition_table, False)

            if hash(child.state) not in self.transposition_table:
                child = (child.get_weight(max_moves=max_moves - 1), child)
                self.transposition_table[hash(child[1].state)] = child[0]
            else:
                child = (self.transposition_table[hash(child.state)], child)
                table_hits += 1

            # 알파-베타 프루닝
            if self.__is_min_node():
                if child[0] <= self.alpha:
                    # MAX가 더이상 서치할 필요가 없다는 것은 ensure 하기에 서치 중지
                    prune += 1
                    return child[0]
                self.beta = min(self.beta, child[0])

            if self.__is_max_node():
                if child[0] >= self.beta:
                    # MIN가 더이상 서치할 필요가 없다는 것은 ensure 하기에 서치 중지
                    prune += 1
                    return child[0]
                self.alpha = max(self.alpha, child[0])

            no_prune += 1

            if self.min_child == None:
                self.min_child = child
            else:
                self.min_child = min(self.min_child, child, key=lambda x: x[0])

            if self.max_child == None:
                self.max_child = child
            else:
                self.max_child = max(self.max_child, child, key=lambda x: x[0])

        if self.__is_max_node():
            return self.max_child[0] if self.max_child else None
        else:
            return self.min_child[0] if self.min_child else None

    def get_best_child(self, max_moves=1000):
        self.get_weight(max_moves=max_moves)
        if self.__is_min_node():
            return self.min_child[1]

        return self.max_child[1]


def check_win(g):
    win = g.get_winner()
    if win:
        print("게임 오버", win, "가 이겼습니다")
        print(g)
        exit(0)

    if g.is_draw():
        print("게임 오버", "비겼습니다")
        print(g)
        exit(0)


def human_move(g, move):
    g = g.state_for_move(move, "X")
    check_win(g)
    return g


def computer_move(g, player="O", other="X", moves=8):
    gtn = GameTreeNode(g, player, other, True, float("-inf"), float("inf"), dict(), True)
    gtn = gtn.get_best_child(max_moves=moves)
    g = gtn.state
    check_win(g)
    return g

def rule_move(g, past):
    move=0
    g = g.rule_based(move, "O", past)
    check_win(g)
    return g

def hvc():
    g = GameState(7, 6)
    first = input("이 AI가 먼저 두게 하시겠습니까? (Y/N): ")
    if first == "N" or first == 'n':
        while True:
            print(g)
            past = int(input("두고 싶은 열의 숫자를 입력하세요:")) - 1
            g = human_move(g, past)
            print("Search Algorithm은 1, Rule-based는 2를 입력하세요 (1/2)")
            temp = input()
            if temp == '1':
                g = computer_move(g)
            else :
                g = rule_move(g, past)


    if first == "Y" or first == 'y':
        i=0
        while True:
            print("Search Algorithm은 1, Rule-based는 2를 입력하세요 (1/2)")
            temp = input()
            if temp == '1':
                g = computer_move(g)
            else:
                if i==0:
                    past=0
                g = rule_move(g, past)
            print(g)
            past = int(input("두고 싶은 열의 숫자를 입력하세요:")) - 1
            g = human_move(g, past)
            i=i+1


def cvc():
    g = GameState(7, 6)
    while True:
        g = computer_move(g, player="1", other="2", moves=8)
        print(g)
        g = computer_move(g, player="2", other="1", moves=8)
        print(g)


hvc()