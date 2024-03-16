# Tkinter dokumentācija (grafiskās vides komandas un opcijas): https://docs.python.org/3/library/tk.html
# Tkinter OptionMenu elementa paraugs: https://www.geeksforgeeks.org/tkinter-optionmenu-widget/
# Tkinter Button elementa komandas izsaukšana ar mainīgo: https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
from tkinter import *
from tkinter import ttk


def main():
    # sāk spēli:
    def start_game():
        # iegūst skaitli no grafiskās vides elementa:
        global NUMBER
        NUMBER = int(choose_number.get())

        # atjauno skaitli pēc reizināšanas:
        # metode ir zem start_game(), lai varētu piekļūt "current_number" elementam
        def update_number(multiplier):
            # sāk jaunu spēli:
            def play_again():
                game.forget()
                main()

            global NUMBER
            NUMBER = NUMBER * multiplier
            current_number.configure(text=NUMBER)  # atjauno skaitli grafiskajā vidē

            # pārbauda vai skaitlis ir sasniedzis beigu stāvokli:
            if NUMBER >= 1200:
                # noņem pašlaik nevajadzīgos grafiskās vides elementus:
                separator1.forget()
                separator2.forget()
                options.forget()
                moves.forget()

                # spēlēt vēlreiz poga:
                play_again_button = Button(score, text="Spēlēt vēlreiz", command=play_again)
                play_again_button.grid(column=0, row=5, columnspan=6, sticky="ew")

        # noņem vecos grafiskās vides elementus:
        who_starts_frame.forget()
        other_options.forget()

        # izveido jaunus grafiskās vides elementus:

        # spēles elementi:
        game = Frame(root, width=321)
        game.pack()

        # punktu skaits:
        score = Frame(game)
        score.pack(fill="x")

        separator1 = ttk.Separator(score, orient="horizontal")
        separator1.grid(column=0, row=0, columnspan=6, sticky="ew")

        score_text = Label(score, text="Spēles stāvoklis", justify="center", width=45).grid(column=0, row=1, columnspan=6)
        p1_text = Label(score, text="Cilvēks").grid(column=0, row=2)
        p2_text = Label(score, text="Dators").grid(column=5, row=2)

        p1_score = Label(score, text="0").grid(column=0, row=3)
        p2_score = Label(score, text="0").grid(column=5, row=3)

        current_number_text = Label(score, text="Skaitlis").grid(column=1, row=2, columnspan=4)
        current_number = Label(score, text=str(NUMBER))
        current_number.grid(column=1, row=3, columnspan=4)

        separator2 = ttk.Separator(score, orient="horizontal")
        separator2.grid(column=0, row=4, columnspan=6, sticky="ew")

        # spēlētāja gājienu opcijas:
        moves = Frame(game)
        moves.pack(fill="x")

        moves_text = Label(moves, text="Izvēlies reizinātāju:", justify="center", width=45).grid(column=0, row=0, columnspan=3)
        multiply_by_2 = Button(moves, text="2", command=lambda: update_number(2)).grid(column=0, row=1, sticky="ew")
        multiply_by_3 = Button(moves, text="3", command=lambda: update_number(3)).grid(column=1, row=1, sticky="ew")
        multiply_by_4 = Button(moves, text="4", command=lambda: update_number(4)).grid(column=2, row=1, sticky="ew")

    # spēles opcijas:

    options = Frame(root, width=321)
    options.pack()

    # kurš uzsāk spēli:
    who_starts_frame = Frame(options)
    who_starts_frame.pack(fill="x")

    text1 = Label(who_starts_frame, text="Izvēlies kurš uzsāks spēli:", width=30, anchor="w")
    text1.grid(column=0, row=0)

    who_starts_list = ["Cilvēks", "Dators"]  # izvēles/opcijas

    who_starts_value = StringVar(who_starts_frame)  # saglabā izvēlēto vērtību mainīgajā
    who_starts_value.set(who_starts_list[0])  # izvēlētā vērība pēc noklusējuma

    choose_who_starts = OptionMenu(who_starts_frame, who_starts_value, *who_starts_list)
    choose_who_starts.configure(width=10)
    choose_who_starts.configure(anchor="w")  # teksts pa labi
    choose_who_starts.grid(column=1, row=0)

    # algoritma izvēle:
    algorithm_frame = Frame(options)
    algorithm_frame.pack(fill="x")

    text2 = Label(algorithm_frame, text="Izvēlies algoritmu:", width=30, anchor="w")
    text2.grid(column=0, row=0)

    algorithm_list = ["Minimaksa", "Alfa-beta"]  # izvēles/opcijas

    algorithm_value = StringVar(algorithm_frame)  # saglabā izvēlēto vērtību mainīgajā
    algorithm_value.set(algorithm_list[0])  # izvēlētā vērība pēc noklusējuma

    choose_algorithm = OptionMenu(algorithm_frame, algorithm_value, *algorithm_list)
    choose_algorithm.configure(width=10)
    choose_algorithm.configure(anchor="w")  # teksts pa labi
    choose_algorithm.grid(column=1, row=0)

    # citas opcijas:

    # sākuma skaitlis:
    other_options = Frame(options)
    other_options.pack(fill="x")

    text3 = Label(other_options, text="Izvēlies sākuma skaitli (no 8 līdz 18):", width=30, anchor="w")
    text3.grid(column=0, row=0)

    choose_number = Spinbox(other_options, from_=8, to=18, width=15)
    choose_number.grid(column=1, row=0)

    # start poga:
    start_button = Button(other_options, text="Sākt spēli", command=start_game)
    start_button.grid(column=0, row=1, sticky="ew", columnspan=2)


if __name__ == "__main__":
    # grafiksā vide:
    root = Tk()
    root.title("Pirmā spēle")
    root.minsize(400, 400)

    main()

    mainloop()
