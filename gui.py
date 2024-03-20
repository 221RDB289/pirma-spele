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

    # spēles rezultāts (kad spēle ir beigusies):
    def show_results(self):
        if hasattr(self, "results"):
            self.results.pack()
        else:
            self.results = Frame(self.root)
            self.results.pack()
            self.play_again_button = Button(self.results, text="Spēlēt vēlreiz", command=self.play_again).grid(column=0, row=0, sticky="ew")

    # sāk spēli (pēc sākuma opciju izvēles):
    def start_game(self):
        # pārbauda vai drīkst sākt spēli (vai ievadītais skaitlis ir atļauts):
        try:
            n = int(self.choose_number.get())
            if n >= 8 and n <= 18:
                # noklusētās vērtības (abiem spēlētājiem 0 punkti):
                self.p1_score_value = 0
                self.p2_score_value = 0
                self.number = int(self.choose_number.get())

                self.options.forget()  # noņem iestatījumu logu
                print(self.who_starts_value.get())
                print(self.algorithm_value.get())
                print(self.choose_number.get())

                # jauni logi (spēles stāvoklis un gājieni):
                self.show_state()
                self.show_moves()
        except:
            print("Nepareizi ievadīts skaitlis")  # kļūda

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
        self.number = self.number * multiplier

        # ja sanāk nepāra skaitlis:
        if self.number % 2 != 0:
            self.p1_score_value += 1  # palielina punktu skaitu par 1
        # ja sanāk pāra skaitlis:
        elif self.p2_score_value != 0:
            self.p2_score_value -= 1  # atņem vienu punktu no pretinieka

        self.update_state()

        # pārbauda vai ir sasniegts beigu stāvoklis (vai spēli ir jābeidz):
        if self.number >= 1200:
            self.moves.forget()
            self.show_results()


if __name__ == "__main__":
    # testēšana:
    test = GUI()
