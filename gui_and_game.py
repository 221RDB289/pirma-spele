# Tkinter dokumentācija (grafiskās vides komandas un opcijas): https://docs.python.org/3/library/tk.html
# Tkinter OptionMenu elementa paraugs: https://www.geeksforgeeks.org/tkinter-optionmenu-widget/
# Tkinter Button elementa komandas izsaukšana ar mainīgo: https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
# Tkinter validācija: https://www.pythontutorial.net/tkinter/tkinter-validation/

from tree_and_algorithms import Node, minimax, alphabeta
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
            self.p1_score = Label(self.state, text=self.current_node.p1)
            self.p1_score.grid(column=0, row=3)

            # pašreizējais skaitlis:
            self.current_number_text = Label(self.state, text="Skaitlis").grid(column=1, row=2, columnspan=4)
            self.current_number = Label(self.state, text=str(self.choose_number.get()))
            self.current_number.grid(column=1, row=3, columnspan=4)

            # dators:
            self.p2_text = Label(self.state, text="Dators").grid(column=5, row=2)
            self.p2_score = Label(self.state, text=self.current_node.p2)
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
            self.multiply_by_2 = Button(self.moves, text="2", command=lambda: self.human_move(0)).grid(column=0, row=2, sticky="ew")
            self.multiply_by_3 = Button(self.moves, text="3", command=lambda: self.human_move(1)).grid(column=1, row=2, sticky="ew")
            self.multiply_by_4 = Button(self.moves, text="4", command=lambda: self.human_move(2)).grid(column=2, row=2, sticky="ew")

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
            if self.current_node.p1 == self.current_node.p2:
                game_result = "Neizšķirts"
            elif self.current_node.p1 > self.current_node.p2:
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
            if self.current_node.p1 == self.current_node.p2:
                game_result = "Neizšķirts"
            elif self.current_node.p1 > self.current_node.p2:
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
        # pārbauda vai drīkst sākt spēli (vai ievadītais skaitlis ir atļauts):
        try:
            n = int(self.choose_number.get())
            if n >= 8 and n <= 18:
                # iegūst vērtību, kurš sāk spēli:
                first_player = self.who_starts_value.get()

                # noņem iestatījumu logu:
                self.options.pack_forget()

                # spēles koka inicializācija (tas arī ir spēles sākuma stāvoklis):
                self.current_node = Node(number=n, first_player=first_player)
                self.current_node.expand()

                # jauni logi (spēles stāvoklis un gājieni):
                self.show_state()
                self.show_moves()

                # ja dators sāk spēli (tad dators veic gājienu):
                if first_player == "Dators":
                    self.computer_move()
            else:
                print("Ievadītais skaitlis nav atļautā diapazonā.")
        except ValueError:
            print("Nepareizi ievadīts skaitlis.")

    # dators veic gājienu:
    def computer_move(self):
        # iepriekšējais skaitlis (pirms gājiena veikšanas), lai to attēlotu datora pēdējā veiktā gājiena sadaļā:
        previous_number = self.current_node.number
        # dators iegūst labāko gājienu atkarībā no algoritma:
        # minimaks:
        if self.algorithm_value.get() == "Minimaksa":
            self.current_node, _ = minimax(self.current_node)  # atjauno spēles koku, jeb tā stāvokli (mums nevajag saglabāt racionālo spēles rezultātu)
        # alfabeta:
        else:
            self.current_node, _ = alphabeta(self.current_node)  # atjauno spēles koku, jeb tā stāvokli (mums nevajag saglabāt racionālo spēles rezultātu)

        # atjauno datus grafiskajā interfeisā:
        self.update_state()
        self.show_computer_last_move(previous_number, self.current_node.number // previous_number, self.current_node.number)  # reizinātājs = self.current_node.number/previous_number

        # pārbauda vai ir spēles beigu stāvoklis:
        if self.current_node.is_terminal():
            # beidz spēli un parāda spēles beigu/rezultāta logu:
            self.show_results()
        # (nav nepieciešams norādīt, ka cilvēkam ir jāveic nākamais gājiens, jo tas notiek spiežot reizinātāja pogas)

    # spēlēt vēlreiz (kad spēle jau ir beigusies):
    def play_again(self):
        self.state.forget()
        self.results.forget()
        self.show_options()

    # atjauno pašreizējā stāvokļa vērtības grafiskajā interfeisā:
    def update_state(self):
        # atjauno pašreizējo skaitli (ņem to no koka, jeb atjaunotā spēles stāvokļa):
        self.current_number.configure(text=self.current_node.number)
        # atjauno punktus (ņem tos no koka, jeb atjaunotā spēles stāvokļa):
        self.p1_score.configure(text=self.current_node.p1)
        self.p2_score.configure(text=self.current_node.p2)

    # cilvēks veic gājienu, jeb veic reizināšanu:
    def human_move(self, move_id: int):
        # atjauno spēles stāvokli atkarībā no cilvēka veiktā gājiena:
        self.current_node = self.current_node.children[move_id]
        # atjauno datus grafiskajā interfeisā:
        self.update_state()

        # pārbauda vai ir spēles beigu stāvoklis:
        if self.current_node.is_terminal():
            # beidz spēli un parāda spēles beigu/rezultāta logu:
            self.show_results()
        else:
            # ja nav beigu stāvoklis, tad dators veic nākamo gājienu:
            self.computer_move()


if __name__ == "__main__":
    # GUI klases izsaukšana, kas arī sāk spēli:
    test = GUI()
