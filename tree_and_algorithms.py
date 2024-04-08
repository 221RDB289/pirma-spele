from typing import Optional, List


# minimaksa algoritms:
def minimax(node, is_maximizing=True):
    global node_and_result
    # ja ir beigu stāvoklis:
    if node.is_terminal():
        eval = node.evaluate()  # stāvokļa heiristiskais novērtējums
        return node, eval
    # ja nav beigu stāvoklis:
    # sākuma vērtības (pirmā stāvokļa pēcteča vērtības):
    best_move = node.children[0]
    if is_maximizing:  # ja notiek maksimizācija
        _, max_eval = minimax(best_move, False)  # jaunā stāvokļa heiristiskais novērtējums (pašu stāvokļa instanci vēlreiz mums iegūt nevajag)
        for child_node in node.children[1:]:  # (izņemot pirmo vērtību, jo tā jau tika izmantota)
            _, eval = minimax(child_node, False)  # jaunā stāvokļa heiristiskais novērtējums (pašu stāvokļa instanci vēlreiz mums iegūt nevajag)
            # pārbauda vai jaunā stāvokļa novērtējums ir labāks nekā iepriekšējā stāvokļa:
            if eval > max_eval:
                max_eval = eval
                best_move = child_node
        return best_move, max_eval
    else:  # ja notiek minimizācija
        _, max_eval = minimax(best_move, True)  # jaunā stāvokļa heiristiskais novērtējums (pašu stāvokļa instanci vēlreiz mums iegūt nevajag)
        for child_node in node.children[1:]:  # (izņemot pirmo vērtību, jo tā jau tika izmantota)
            _, eval = minimax(child_node, True)  # jaunā stāvokļa heiristiskais novērtējums (pašu stāvokļa instanci vēlreiz mums iegūt nevajag)
            # pārbauda vai jaunā stāvokļa novērtējums ir labāks nekā iepriekšējā stāvokļa:
            if eval < max_eval:
                max_eval = eval
                best_move = child_node
        return best_move, max_eval


# alfabeta algoritms:
def alphabeta(node, alpha=float("-inf"), beta=float("inf"), is_maximizing=True):
    global node_and_result
    # ja ir beigu stāvoklis:
    if node.is_terminal():
        eval = node.evaluate()  # stāvokļa heiristiskais novērtējums
        return node, eval
    # ja nav beigu stāvoklis:
    # sākuma vērtības (pirmā stāvokļa pēcteča vērtības):
    best_move = node.children[0]
    if is_maximizing:  # ja notiek maksimizācija
        _, alpha = alphabeta(best_move, alpha, beta, False)  # jaunā stāvokļa heiristiskais novērtējums (pašu stāvokļa instanci vēlreiz mums iegūt nevajag)
        for child_node in node.children[1:]:  # (izņemot pirmo vērtību, jo tā jau tika izmantota)
            _, eval = alphabeta(child_node, False)  # jaunā stāvokļa heiristiskais novērtējums (pašu stāvokļa instanci vēlreiz mums iegūt nevajag)
            # pārbauda vai jaunā stāvokļa novērtējums ir labāks nekā iepriekšējā stāvokļa:
            if eval > alpha:
                alpha = eval
                best_move = child_node
            if beta <= alpha:  # ja beta vērtība ir mazāka vai vienāda ar alfu, tad tiek pārtraukts cikls - zars netiek tālāk apskatīts
                break
        return best_move, alpha
    else:  # ja notiek minimizācija
        _, beta = alphabeta(best_move, alpha, beta, True)  # jaunā stāvokļa heiristiskais novērtējums (pašu stāvokļa instanci vēlreiz mums iegūt nevajag)
        for child_node in node.children[1:]:  # (izņemot pirmo vērtību, jo tā jau tika izmantota)
            _, eval = alphabeta(child_node, alpha, beta, True)  # jaunā stāvokļa heiristiskais novērtējums (pašu stāvokļa instanci vēlreiz mums iegūt nevajag)
            # pārbauda vai jaunā stāvokļa novērtējums ir labāks nekā iepriekšējā stāvokļa:
            if eval < beta:
                beta = eval
                best_move = child_node
            if beta <= alpha:  # ja beta vērtība ir mazāka vai vienāda ar alfu, tad tiek pārtraukts cikls - zars netiek tālāk apskatīts
                break
        return best_move, beta


# spēles stāvoklis/koks:
node_id = 0


class Node:
    # klases inicializācija:
    def __init__(self, number, p1=0, p2=0, level=0, parent=None, first_player="Cilvēks"):
        # galvenie stāvokļa mainīgie:
        self.number: int = number
        self.p1: int = p1
        self.p2: int = p2
        # Ja 'Cilvēks' izdara pirmo gājienu, līmenis paliek kā ir, pretējā gadījumā 'Dators' sākuma līmenis būs 1
        self.level = level if first_player == "Cilvēks" else 1
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
    def evaluate(self):
        # tiek ņemta vērā punktu atšķirība starp datoru un cilvēku
        score_difference = self.p2 - self.p1  # p2 - datora punktu skaits, p1 - cilvēka punktu skaits

        # starpposma stāvokļos vērtējums ir vienāds ar punktu starpību
        return score_difference
