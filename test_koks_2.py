from typing import Optional, List

# minimaksa algoritms:
node_and_result = {}


def minimax(node, result=None):
    global node_and_result
    # ja tā ir strupceļa virsotne:
    if node.is_terminal():
        result = node.p1 - node.p2
    else:
        results = []
        for child_node in node.children:
            results.append(minimax(child_node))
        # max līmenis:
        if node.level % 2 == 0:
            result = max(results)
        # min līmenis:
        else:
            result = min(results)
    node_and_result[node.id] = result
    # if result == 1:
    #     print(node.id, result)
    print(node.id, result)
    return result


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
    def __init__(self, number, p1=0, p2=0, level=0, parent=None):
        # galvenie stāvokļa mainīgie:
        self.number: int = number
        self.p1: int = p1
        self.p2: int = p2
        # stāvokļa unikālais numurs (lai algoritmos varētu atzīmēt, kuras virsotnes jau ir apskatītas):
        global node_id
        self.id: int = node_id
        node_id += 1
        # citi mainīgie:
        self.children: List[Node] = []
        self.parent: Optional[Node] = parent
        self.level: int = level

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
        ja ir vienāds punktu skaits un ir beigu stāvoklis, tad 0
        ja ir vienāds punktu skaits un nav beigu stāvoklis, tad 1
        ja ir lielāks punktu skaits un nav beigu stāvoklis, tad 1
        ja ir lielāks punktu skaits un ir beigu stāvoklis, tad 2

        labākais gājiens ir tur, kur ir lielākā funkcijas vērtība
        """
        if self.p1 - self.p2 > 0:
            if self.is_terminal:
                evaluation = 2
            else:
                evaluation = 1
        elif self.p1 == self.p2:
            if self.is_terminal:
                evaluation = 0
            else:
                evaluation = 1
        return evaluation


# testēšana:
if __name__ == "__main__":
    start_number = 13
    # tiek izveidots spēles koks:
    tree = Node(start_number)
    tree.expand()
    # print("Number of nodes:", node_id)
    # tiek izvadīts spēles koks:
    file = open("koks.txt", "w")
    tree.show_node_tree(file)
    file.close()
    # minimax:
    outcome = minimax(tree)
    print("Outcome:", outcome)
    print("Best (1st) move:", get_best_move(tree))
