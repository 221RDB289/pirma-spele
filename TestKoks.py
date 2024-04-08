from typing import Optional, List

# virsotņu skaits
virsotnu_skaits = 0
# Minimaksa algoritms, kurš saņem spēles virsotni un bool tipa parametru, kas norāda, vai pašreizējais spēlētājs ir maksimizētājs
def minimax(node, is_maximizing=True): 
    global virsotnu_skaits
    virsotnu_skaits += 1
    print(f"Considering node {virsotnu_skaits} ")
    if node.is_terminal():
        return node.evaluate(), None  # Nākamā gājiena nav, jo spēle ir beigusies
    best_move = None # mainīgais, kas glabā labāko gājienu
    if is_maximizing: # ja pašreizējais spēlētājs ir maksimizētājs, tad iziet cauri visām virsotnēm un saglabā labāko
        max_eval = float('-inf')
        for child_node in node.children:
            eval, _ = minimax(child_node, False) # rekursīvi izsaucam Minimaksa funkciju virsotnes pēctecim, pārslēdzoties uz minimizētāju
            if eval > max_eval:
                max_eval = eval
                best_move = child_node
    else: # līdzīgi iziet cauri visām virsotnēm, bet ar mērķi minimizēt vērtējumu
        min_eval = float('inf')
        for child_node in node.children:
            eval, _ = minimax(child_node, True) # rekursīvi izsaucam Minimaksa funkciju virsotnes pēctecim, pārslēdzoties uz maksimizētāju
            if eval < min_eval:
                min_eval = eval
                best_move = child_node
    # print(f"Considering node {node.number} at level {node.level}") # logs testēšanai
    return (max_eval if is_maximizing else min_eval), best_move # Atgriež maksimālo vai minimālo vērtējumu atkarībā no spēlētāja veida, un labāko gājienu

# Alfabeta algoritms, kurš saņem spēles virsotni, alfa un beta vērtības, kā arī bool tipa parametru,kas norāda, vai pašreizējais spēlētājs ir maksimizētājs
def alphabeta(node, alpha=float('-inf'), beta=float('inf'), is_maximizing=True):
    global virsotnu_skaits
    virsotnu_skaits += 1
    print(f"Considering node {virsotnu_skaits} ")
    if node.is_terminal():
        return node.evaluate(), None # Nākamā gājiena nav, jo spēle ir beigusies
    best_move = None
    if is_maximizing: # ja pašreizējais spēlētājs ir maksimizētājs, tad iziet cauri visām virsotnēm un saglabā labāko 
        for child in node.children:
            eval, _ = alphabeta(child, alpha, beta, False) # tiek rekursīvi izsaukta Alfabeta funkciju virsotnes pēctecim, pārslēdzoties uz minimizētāju
            if eval > alpha:
                alpha = eval
                best_move = child
            if beta <= alpha: # ja beta vērtība ir mazāka vai vienāda ar alfu, tad tiek pārtraukts cikls - zars netiek tālāk apskatīts
                break
        return alpha, best_move # atgriež alfa vērtību un labāko gājienu maksimizētājam
    else: # līdzīgi iziet cauri visām virsotnēm, bet ar mērķi minimizēt vērtējumu
        for child in node.children:
            eval, _ = alphabeta(child, alpha, beta, True) # rekursīvi izsaucam Alfabeta funkciju virsotnes pēctecim, pārslēdzoties uz maksimizētāju
            if eval < beta:
                beta = eval
                best_move = child
            if beta <= alpha:
                break
        return beta, best_move # atgriež alfa vērtību un labāko gājienu minimizētājam





# spēles stāvoklis:
node_id = 0


class Node:
    # klases inicializācija:
    def __init__(self, number, p1=0, p2=0, level=0, parent=None, first_player='Cilvēks'):
        # galvenie stāvokļa mainīgie:
        self.number: int = number
        self.p1: int = p1
        self.p2: int = p2
        # Ja 'Cilvēks' izdara pirmo gājienu, līmenis paliek kā ir, pretējā gadījumā 'Dators' sākuma līmenis būs 1
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
        Heiristika spēļu stāvokļu novērtēšanai:
        - Tiek ņemta vērā punktu atšķirība starp datoru un cilvēku.
        """
        score_difference = self.p2 - self.p1  # p2 - datora punktu skaits, p1 - cilvēka punktu skaits

        # Starpposma stāvokļos vērtējums ir vienāds ar punktu starpību
        return score_difference





