from typing import Optional, Dict, List
from copy import deepcopy

State = Dict[str, int]

class Node:

    def __init__(self, number: int, parent: Optional['Node'] = None):
        self.children: List[Node] = []
        self.number: int = number
        self.is_terminal: bool = False
        self.parent: Optional[Node] = parent

    def expand(self):
        if self.number >= 1200:
            self.is_terminal = True
            return
        for multiplier in [2, 3, 4]:
            new_number = self.number * multiplier
            if new_number >= 1200:
                self.is_terminal = True
                return
            child = Node(new_number, parent=self)
            self.children.append(child)
            child.expand()

    def __repr__(self) -> str:
        """Node representation as a string"""
        return f"Number: {self.number}, Terminal: {self.is_terminal}"

    def show_node_tree(self, indent=0):
        """Print the node and its children"""
        print("|  " * indent + str(self))
        for child in self.children:
            child.show_node_tree(indent + 1)


class NumberGameTree:

    def __init__(self, start_number: int):
        self.root = Node(start_number)
        self.node_count = 0

    def generate_tree(self):
        self.__expand(self.root)

    def __expand(self, node: Node):
        node.expand()
        self.node_count += 1
        for child in node.children:
            self.__expand(child)

# tiek aprakstīta main() funkcija
def main():
    start_number = int(input("Ievadiet skaitli no 8 līdz 18, lai izveidotu spēles koku"))
    if start_number < 8 or start_number > 18:
        print("Ievadīts neatbilstošs skaitlis!")
        return
    tree = NumberGameTree(start_number)
    # tiek uzģenerēts stāvokļu telpas grafs
    tree.generate_tree()
    
    # tiek izvadītas visas grafa virsotnes
    tree.root.show_node_tree()
    
    # tiek izvadīts kopējais virsotņu skaits
    print(f"Amount of nodes: {tree.node_count}")

# tiek izsaukta main() funkcija
if __name__ == "__main__":
    main()
