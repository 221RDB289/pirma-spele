# spēlētājs:
class Player:
    score = 0


# spēle:
class Game:
    # klases inicializācija:
    def __init__(self, start_number: int, first_move_p1: bool):
        # pārbauda vai sākuma skaitlis ir diapazonā no 8 līdz 18:
        if start_number >= 8 and start_number <= 18:
            self.current_number = start_number
            self.next_move_p1 = first_move_p1
            # izveido spēlētājus:
            self.p1 = Player()
            self.p2 = Player()
        else:
            raise Exception("Sākuma skaitlis nav diapazonā no 8 līdz 18")  # kļūdas paziņojums

    # pārbauda vai ir spēles beigas (skaitlis ir lielāks vai vienāds ar 1200):
    def game_over(self) -> bool:
        if self.current_number >= 1200:
            return True
        return False

    def multipy(self, number: int):
        # pārbauda vai reizinātājs ir 2, 3 vai 4:
        match number:
            case 2:
                self.current_number *= 2
            case 3:
                self.current_number *= 3
            case 4:
                self.current_number *= 4
            # ja reizinātājs nav 2, 3 vai 4:
            case _:
                raise Exception("Reizinātājs nav 2, 3 vai 4")  # kļūdas paziņojums

        # atjauno spēlētāju punktu skaitus un nākamo gājienu secību:
        if self.next_move_p1:
            # ja sanāk nepāra skaitlis:
            if self.current_number % 2 != 0:
                self.p1.score += 1  # palielina paša punktu skaitu par 1
            # ja sanāk pāra skaitlis un pretinieka punktu skaits nav nulle:
            elif self.p2.score != 0:
                self.p2.score -= 1  # atņem vienu punktu no pretinieka
            self.next_move_p1 = False
        else:
            # ja sanāk nepāra skaitlis:
            if self.current_number % 2 != 0:
                self.p2.score += 1  # palielina paša punktu skaitu par 1
            # ja sanāk pāra skaitlis un pretinieka punktu skaits nav nulle:
            elif self.p1.score != 0:
                self.p1.score -= 1  # atņem vienu punktu no pretinieka
            self.next_move_p1 = True


# testi:
if __name__ == "__main__":
    game = Game(9, True)
    while not game.game_over():
        game.multipy(3)
        print(game.current_number, game.next_move_p1, game.p1.score, game.p2.score, game.game_over())
