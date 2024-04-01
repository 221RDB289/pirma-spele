from typing import Optional, List

# minimaksa algoritms:
node_and_result = {}


def minimax(node, is_maximizing=True):
    global node_and_result
    if node.is_terminal():
        return node.evaluate(), None  # Нет следующего хода, так как игра закончена
    best_move = None
    if is_maximizing:
        max_eval = float('-inf')
        for child_node in node.children:
            eval, _ = minimax(child_node, False)
            if eval > max_eval:
                max_eval = eval
                best_move = child_node
    else:
        min_eval = float('inf')
        for child_node in node.children:
            eval, _ = minimax(child_node, True)
            if eval < min_eval:
                min_eval = eval
                best_move = child_node
    node_and_result[node.id] = best_move.id if best_move else None
    # print(f"Considering node {node.number} at level {node.level}")
    return (max_eval if is_maximizing else min_eval), best_move


def alphabeta(node, alpha=float('-inf'), beta=float('inf'), is_maximizing=True):
    global node_and_result
    if node.is_terminal():
        return node.evaluate(), None
    best_move = None
    if is_maximizing:
        for child in node.children:
            eval, _ = alphabeta(child, alpha, beta, False)
            if eval > alpha:
                alpha = eval
                best_move = child
            if beta <= alpha:
                break
        return alpha, best_move
    else:
        for child in node.children:
            eval, _ = alphabeta(child, alpha, beta, True)
            if eval < beta:
                beta = eval
                best_move = child
            if beta <= alpha:
                break
        return beta, best_move


def get_best_move(node):
    global node_and_result
    for child_node in node.children:
        # max līmenis:
        if child_node.level % 2 == 0:
            if node_and_result[child_node.id] == 1:
                return child_node.id
        # min līmenis:
        else:
            if node_and_result[child_node.id] == 0:
                return child_node.id


# spēles stāvoklis:
node_id = 0


class Node:
    # klases inicializācija:
    def __init__(self, number, p1=0, p2=0, level=0, parent=None, first_player='Cilvēks'):
        # galvenie stāvokļa mainīgie:
        self.number: int = number
        self.p1: int = p1
        self.p2: int = p2
        # Если 'Cilvēks' делает первый ход, level остается как есть, иначе для 'Dators' начальный level будет 1
        self.level = level if first_player == 'Cilvēks' else 1
        # stāvokļa unikālais numurs (lai algoritmos varētu atzīmēt, kuras virsotnes jau ir apskatītas):
        global node_id
        self.id: int = node_id
        node_id += 1
        # citi mainīgie:
        self.children: List[Node] = []
        self.parent: Optional[Node] = parent


    # pārbauda vai ir beigu stāvoklis:
    def is_terminal(self):
        if self.number >= 1200:
            return True
        return False

    # pievieno pēctečus (iespējamos spēles stāvokļus atkarībā no reizināšanas):
    def expand(self):
        # skaitli var reizināt ar 2, 3 vai 4:
        for multiplier in [2, 3, 4]:
            new_number = self.number * multiplier

            # punktu piešķiršana/atņemšana:
            p1 = self.p1
            p2 = self.p2
            if new_number % 2 != 0:
                if self.level % 2 == 0:
                    p1 = self.p1 + 1
                else:
                    p2 = self.p2 + 1
            else:
                if self.level % 2 == 0:
                    p2 = self.p2 - 1
                else:
                    p1 = self.p1 - 1

            # pārbauda vai ir beigu stāvoklis un izveido pēcteča virsotni:
            if new_number >= 1200:
                child = Node(new_number, p1=p1, p2=p2, level=self.level + 1, parent=self)
                self.children.append(child)
            else:
                child = Node(new_number, p1=p1, p2=p2, level=self.level + 1, parent=self)
                self.children.append(child)
                child.expand()

    # izvada spēles koku teksta failā:
    def show_node_tree(self, file, indent=0):
        file.write("|  " * indent + f"Number: {self.number}, P1: {self.p1}, P2: {self.p2}, Level: {self.level}, Terminal: {self.is_terminal()}, Evaluation: {self.evaluate()}, Id: {self.id}\n")
        for child in self.children:
            child.show_node_tree(file, indent + 1)

    # heiristiskā novērtējuma funkcija:
    def evaluate(self) -> int:
        """
        Эвристика для оценки состояний игры:
        - Учитывается разница в очках между компьютером и игроком.
        - Добавлена награда за приближение к целевому числу 1200.
        """
        score_difference = self.p2 - self.p1  # p2 - очки компьютера, p1 - очки человека
        closeness_to_goal = max(0, 1200 - self.number)  # Насколько близко текущее число к 1200

        # Если состояние является конечным (игра окончена)
        if self.is_terminal():
            if score_difference > 0:
                return 10000 + closeness_to_goal  # Большая положительная оценка для победы компьютера
            elif score_difference < 0:
                return -10000 - closeness_to_goal  # Большая отрицательная оценка для проигрыша
            else:
                return 0  # Ничья

        # В промежуточных состояниях оценка равна разнице в очках с добавлением награды за приближение к цели
        return score_difference




# if __name__ == "__main__":
#     start_number = 13
#     # Создаем начальное состояние игрового дерева:
#     root_node = Node(start_number)
#     root_node.expand()  # Расширяем дерево для всех возможных ходов

#     # Тестируем алгоритм Minimax:
#     minimax_score, minimax_move = minimax(root_node, True)
#     print(f"Minimax score: {minimax_score}, Minimax best move: {minimax_move.number}")

#     # Тестируем алгоритм Alpha-Beta:
#     alphabeta_score, alphabeta_move = alphabeta(root_node, float('-inf'), float('inf'), True)
#     print(f"Alpha-Beta score: {alphabeta_score}, Alpha-Beta best move: {alphabeta_move.number}")

#     # Выводим информацию о всех узлах для проверки:
#     with open("koks.txt", "w") as file:
#         root_node.show_node_tree(file)
