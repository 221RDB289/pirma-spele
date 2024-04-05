from TestKoks import Node, minimax, alphabeta

# Tkinter dokumentācija (grafiskās vides komandas un opcijas): https://docs.python.org/3/library/tk.html
# Tkinter OptionMenu elementa paraugs: https://www.geeksforgeeks.org/tkinter-optionmenu-widget/
# Tkinter Button elementa komandas izsaukšana ar mainīgo: https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
# Tkinter validācija: https://www.pythontutorial.net/tkinter/tkinter-validation/
from tkinter import *
from tkinter import ttk


class GUI:
    # GUI klases inicializācija:
    def __init__(self):
        self.root = Tk()
        self.root.title("Pirmā spēle")
        self.root.minsize(400, 400)
        self.show_options()  # izsauc spēles opciju logu
        mainloop()

    # spēles opcijas (pirms spēles sākuma):
    def show_options(self):
        if hasattr(self, "options"):
            self.options.pack()
        else:
            self.options = Frame(self.root, width=321)
            self.options.pack()

            # kurš uzsāk spēli:
            self.who_starts_text = Label(self.options, text="Izvēlies kurš uzsāks spēli:", width=30, anchor="w").grid(column=0, row=0)
            self.who_starts_list = ["Cilvēks", "Dators"]  # izvēles/opcijas
            self.who_starts_value = StringVar(self.options)  # saglabā izvēlēto vērtību mainīgajā
            self.who_starts_value.set(self.who_starts_list[0])  # izvēlētā vērība pēc noklusējuma
            self.who_starts_menu = OptionMenu(self.options, self.who_starts_value, *self.who_starts_list)
            self.who_starts_menu.configure(width=10, anchor="w")
            self.who_starts_menu.grid(column=1, row=0)

            # algoritma izvēle:
            self.algorithm_text = Label(self.options, text="Izvēlies algoritmu:", width=30, anchor="w").grid(column=0, row=1)
            self.algorithm_list = ["Minimaksa", "Alfa-beta"]  # izvēles/opcijas
            self.algorithm_value = StringVar(self.options)  # saglabā izvēlēto vērtību mainīgajā
            self.algorithm_value.set(self.algorithm_list[0])  # izvēlētā vērība pēc noklusējuma
            self.algorithm_menu = OptionMenu(self.options, self.algorithm_value, *self.algorithm_list)
            self.algorithm_menu.configure(width=10, anchor="w")
            self.algorithm_menu.grid(column=1, row=1)

            # sākuma skaitlis:
            self.choose_number_text = Label(self.options, text="Izvēlies sākuma skaitli (no 8 līdz 18):", width=30, anchor="w").grid(column=0, row=2)
            self.choose_number = Spinbox(self.options, from_=8, to=18, width=15)
            self.choose_number.grid(column=1, row=2)

            # sākt spēli - poga:
            self.start_button = Button(self.options, text="Sākt spēli", command=self.start_game)
            self.start_button.grid(column=0, row=3, sticky="ew", columnspan=2)

    # spēles pašreizējais stāvoklis (punkti un skaitlis):
    def show_state(self):
        if hasattr(self, "state"):
            self.state.pack()
            self.update_state()
        else:
            self.state = Frame(self.root, width=321)
            self.state.pack()

            self.score_text = Label(self.state, text="Spēles stāvoklis", justify="center", width=45).grid(column=0, row=1, columnspan=6)

            # cilvēks:
            self.p1_text = Label(self.state, text="Cilvēks").grid(column=0, row=2)
            self.p1_score = Label(self.state, text=self.p1_score_value)
            self.p1_score.grid(column=0, row=3)

            # pašreizējais skaitlis:
            self.current_number_text = Label(self.state, text="Skaitlis").grid(column=1, row=2, columnspan=4)
            self.current_number = Label(self.state, text=str(self.choose_number.get()))
            self.current_number.grid(column=1, row=3, columnspan=4)

            # dators:
            self.p2_text = Label(self.state, text="Dators").grid(column=5, row=2)
            self.p2_score = Label(self.state, text=self.p2_score_value)
            self.p2_score.grid(column=5, row=3)

    # spēlētāja iespējamie gājieni:
    def show_moves(self):
        if hasattr(self, "moves"):
            self.moves.pack()
        else:
            self.moves = Frame(self.root)
            self.moves.pack()

            self.separator = ttk.Separator(self.moves, orient="horizontal").grid(column=0, row=0, columnspan=3, sticky="ew")
            self.moves_text = Label(self.moves, text="Izvēlies reizinātāju:", justify="center", width=45).grid(column=0, row=1, columnspan=3)
            self.multiply_by_2 = Button(self.moves, text="2", command=lambda: self.multiply(2)).grid(column=0, row=2, sticky="ew")
            self.multiply_by_3 = Button(self.moves, text="3", command=lambda: self.multiply(3)).grid(column=1, row=2, sticky="ew")
            self.multiply_by_4 = Button(self.moves, text="4", command=lambda: self.multiply(4)).grid(column=2, row=2, sticky="ew")

    # datora pēdējais veiktais gājiens:
    def show_computer_last_move(self, previous_number, multiplier, new_number):
        if hasattr(self, "computer_last_move"):
            self.computer_last_move.pack()
            self.computer_last_move_value = Label(self.computer_last_move, text=f"{previous_number} reizināja ar {multiplier} un ieguva jaunu skaitli {new_number}").grid(column=0, row=1, sticky="ew")
        else:
            self.computer_last_move = Frame(self.root)
            self.computer_last_move.pack()

            self.computer_last_move_text = Label(self.computer_last_move, text="Datora pēdējais gājiens:").grid(column=0, row=0, sticky="ew")
            self.computer_last_move_value = Label(self.computer_last_move, text=f"{previous_number} reizināja ar {multiplier} un ieguva jaunu skaitli {new_number}").grid(column=0, row=1, sticky="ew")

    # spēles rezultāts (kad spēle ir beigusies):
    def show_results(self):
        if hasattr(self, "results"):
            self.results.pack()
            # kurš uzvarēja:
            if self.p1_score_value == self.p2_score_value:
                game_result = "Neizšķirts"
            elif self.p1_score_value > self.p2_score_value:
                game_result = "Cilvēks uzvarēja"
            else:
                game_result = "Dators uzvarēja"
            self.who_won_text = Label(self.results, text="Spēles rezultāts:").grid(column=0, row=1, sticky="ew")
            self.who_won_value = Label(self.results, text=game_result).grid(column=0, row=2, sticky="ew")
        else:
            self.results = Frame(self.root)
            self.results.pack()
            self.play_again_button = Button(self.results, text="Spēlēt vēlreiz", command=self.play_again).grid(column=0, row=0, sticky="ew")
            # kurš uzvarēja:
            if self.p1_score_value == self.p2_score_value:
                game_result = "Neizšķirts"
            elif self.p1_score_value > self.p2_score_value:
                game_result = "Cilvēks uzvarēja"
            else:
                game_result = "Dators uzvarēja"
            self.who_won_text = Label(self.results, text="Spēles rezultāts:").grid(column=0, row=1, sticky="ew")
            self.who_won_value = Label(self.results, text=game_result).grid(column=0, row=2, sticky="ew")
        # atbrīvojas no iespējamo gājienu pogām:
        self.moves.forget()
        # atbrīvojas no datora pēdējā veiktā gājiena loga:
        self.computer_last_move.forget()

    # sāk spēli (pēc sākuma opciju izvēles):
    def start_game(self):
        # Pārbaudam, vai skaitlis ir korekts
        try:
            n = int(self.choose_number.get())
            if 8 <= n <= 18:
                # Iepriekšējo rezultātu atiestatīšana
                self.p1_score_value = 0
                self.p2_score_value = 0
                self.number = n

                # Noteikšana, kurš sāk spēli:
                self.current_player = self.who_starts_value.get()

                # Iestatījumu saskarnes noņemšana
                self.options.pack_forget()

                # Spēles koka inicializācija:
                self.tree = Node(self.number, first_player=self.current_player)
                self.tree.expand()

                # Spēles stāvokļa un iespējamo gājienu saskarnes attēlošana:
                self.show_state()
                self.show_moves()

                # Ja dators sāk spēli:
                if self.current_player == "Dators":
                    self.computer_move()
            else:
                print("Ievadītais skaitlis nav atļautā diapazonā.")
        except ValueError:
            print("Nepareizi ievadīts skaitlis.")

    def computer_move(self):
        print("Computer is making a move")
        best_eval, best_move = None, None
        if self.algorithm_value.get() == "Minimaksa":
            best_eval, best_move = minimax(self.tree)
        else:
            best_eval, best_move = alphabeta(self.tree)

        print(f"Best move evaluated: {best_eval}, move: {best_move}")

        if best_move:
            # Izmantot labāko gājienu
            self.apply_move(best_move)
            self.update_state()
            if self.tree.is_terminal():
                self.show_results()
        else:
            # Ja nav gājienu, spēle beidzas
            self.show_results()
        print(f"Computer. New number is: {self.number}")

    def apply_move(self, move):
        print(f"Applying move from node {self.tree.number} to {move.number}")
        print(f"Applying move: {move}")
        previous_number = self.number
        # Atjauninot pašreizējo koka mezglu uz labāko pārvietošanas mezglu
        self.tree = move
        self.number = move.number  # Ņemam jauno skaitli no koka

        # Logs, kurš parāda datora gājienu
        if previous_number != 0:
            multiplier = int(self.number / previous_number)
            print(f"Computer used multiplier: {multiplier}. New number is: {self.number}")
            self.show_computer_last_move(previous_number, multiplier, self.number)
        else:
            print("Error: previous number is zero, cannot determine the multiplier.")

        # Punktu atjaunošana
        self.p1_score_value = move.p1
        self.p2_score_value = move.p2
        self.update_state()  # Interfejsa atjaunošana

        # Gājiena nodošana citam cilvēkam
        self.current_player = "Cilvēks"

        # spēlēt vēlreiz (kad spēle jau ir beigusies):

    def play_again(self):
        self.state.forget()
        self.results.forget()
        self.show_options()

        # atjauno pašreizējā stāvokļa vērtības grafiskajā interfeisā:

    def update_state(self):
        self.p1_score.configure(text=self.p1_score_value)
        self.current_number.configure(text=self.number)
        self.p2_score.configure(text=self.p2_score_value)

        # skaitļa reizināšana (gājiena veikšana):

    def multiply(self, multiplier: int):
        new_number = self.number * multiplier

        # Atradam mezglu ar pašreizējo skaitli
        new_node = next((child for child in self.tree.children if child.number == new_number), None)

        # Ja cilvēks veic pēdējo gājienu
        if self.current_player == "Cilvēks":
            if new_number % 2 == 0:
                self.p2_score_value -= 1
            else:
                self.p1_score_value += 1

        if new_node:
            self.tree = new_node
            self.number = new_node.number

            # Pārbaudam vai nav spēles beigums
            if not self.tree.is_terminal():
                #
                self.current_player = "Cilvēks" if self.current_player == "Dators" else "Dators"
                # Ja nakamajs gajiens ir datora tad dators dara gajienu
                if self.current_player == "Dators":
                    self.computer_move()
            else:

                print(f"p2_score: {self.p2_score}, p1_score: {self.p1_score}")
                print(f"show_results")
                self.show_results()

            self.update_state()
        else:
            print("No valid move found in the tree. This should not happen.")


if __name__ == "__main__":
    # testēšana:
    test = GUI()
