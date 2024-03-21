from typing import Optional, Dict, List
from copy import deepcopy

State = Dict[str, int]

i=0 # testam
class Node:
    # p1 goes first
    def __init__(self, number: int, p1: Optional[int] = 0, p2: Optional[int] = 0, level: Optional[int] = 0, is_terminal: Optional[bool] = False, parent: Optional["Node"] = None):
        global i # testam
        i = i+1 # testam
        self.p1: int = p1
        self.p2: int = p2
        self.children: List[Node] = []
        self.number: int = number
        self.is_terminal: bool = is_terminal
        self.parent: Optional[Node] = parent
        self.level: int = level

    def expand(self):
        for multiplier in [2, 3, 4]:
            new_number = self.number * multiplier

            # par punktiem:
            p1 = self.p1
            p2 = self.p2
            if new_number % 2 != 0:
                if self.level % 2 == 0:
                    p1 = self.p1+1
                else:
                    p2 = self.p2+1
            else:
                if self.level % 2 == 0:
                    if self.p2 != 0:
                        p2 = self.p2-1
                else:
                    if self.p1 != 0:
                        p1 = self.p1-1
            
            # child izveide + is_terminal:
            if new_number >= 1200:
                is_terminal = True
                child = Node(new_number, p1=p1,p2=p2,level=self.level+1,is_terminal=is_terminal, parent=self)
                self.children.append(child)
            else:
                is_terminal = False
                child = Node(new_number, p1=p1,p2=p2,level=self.level+1,is_terminal=is_terminal, parent=self)
                self.children.append(child)
                child.expand()

    def show_node_tree(self, indent=0):
        """Print the node and its children"""
        print("|  " * indent + f"Number: {self.number}, Terminal: {self.is_terminal}, p1: {self.p1}, p2: {self.p2}")
        global fi
        fi.write("|  " * indent+f"Number: {self.number}, Terminal: {self.is_terminal}, p1: {self.p1}, p2: {self.p2}, level: {self.level} {self.is_terminal}\n")
        for child in self.children:
            child.show_node_tree(indent + 1)


# tiek aprakstīta main() funkcija
fi = open("test_koks.txt", "w")
def main():
    start_number = 10
    # tiek uzģenerēts stāvokļu telpas grafs
    tree = Node(start_number)
    tree.expand()
    tree.show_node_tree()
    fi.close()

# tiek izsaukta main() funkcija
if __name__ == "__main__":
    main()
    print('Amount of nodes:', i) # testam
