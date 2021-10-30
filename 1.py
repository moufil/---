import cards, games
class BJ_Card(cards.Positionable_Card):
    """Карта для игры в Блэк Джэк"""
    ACE_VALUE=1
    @property  
    def value(self):
        if self.is_face_up:
            v=BJ_Card.Ranks.index(self.rank)+1
            if v>10:
                v=10
        else:
            v=None
        return v
class BJ_Deck(cards.Deck):
    """колода для игры в Блэк Джэк"""
    def populate(self):
        for suit in BJ_Card.Suits:
            for rank in BJ_Card.Ranks:
                self.cards.append(BJ_Card(rank,suit))
class BJ_Hand(cards.Hand):
    """Рука игрока в Блэк Джэк"""
    def init(self,name):
        super().init()
        self.name=name
    def str(self):
        rep=self.name+":\t"+super().str()
        if self.total:
            rep+="("+str(self.total)+")"
        return rep
    @property  
    def total(self):
        for card in self.cards:
            if not card.value:
                return None
        t=0
        contains_ace=False
        for card in self.cards:
            t+=card.value
            if card.value==BJ_Card.ACE_VALUE:
                contains_ace=True
        if contains_ace and t<11:
            t+=10
        return t
    def is_busted(self):
        return self.total>21
class BJ_Player(BJ_Hand):
    """Игрок в блэк джэк"""
    def is_hitting(self):
        response=games.ask_yes_no("\n"+self.name+
        ",будете брать ещё карты")
        return response=="y"
    def bust(self):
        print(self.name,"пребрал(а).")
        self.lose()
    def lose(self):
        print(self.name, "проиграл(а).")
    def win(self):
        print(self.name,"выиграл(а).")
    def push(self):
        print(self.name,"сыграл(а) сдиллером в ничью")
class BJ_Dealer(BJ_Hand):
    """Диллер в Блэк Джэк"""
    def is_hitting(self):
        return self.total<17
    def bust(self):
        print(self.name,"перебрал(а).")
    def flip_first_card(self):
        first_card=self.cards[0]
        first_card.flip()
class BJ_Game:
    """Игра в Блэк Джэк"""
    def init(self,names):
        self.players=[]
        for name in names:
            player=BJ_Player(name)
            self.players.append(player)
        self.dealer=BJ_Dealer("Диллер")
        self.deck=BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()
    @property  
    def still_playing(self):
        sp=[]
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp
    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()
    def play(self):
        count = len(self.deck.cards)
        if count > 156:
            self.deck.clear()
            self.deck.populate()
            self.deck.shuffle()            
        self.deck.deal(self.players+[self.dealer],
            per_hand=2)
        self.dealer.flip_first_card()
        for player in self.players:
            print(player)
        print(self.dealer)
        for player in self.players:
            self.__additional_cards(player)
        self.dealer.flip_first_card()
        if not self.still_playing:
            print(self.dealer)
        else:
            print(self.dealer)
            self.__additional_cards(self.dealer)
            if self.dealer.is_busted():
                for player in self.still_playing:
                    player.win()
            else:
                for player in self.still_playing:
                    if player.total> self.dealer.total:
                        player.win()
                    elif player.total<self.dealer.total:
                        player.lose()
                    else:
                       player.push
        for player in self.players:
            player.clear()
        self.dealer.clear()
def main():
    print("\t\tДобро пожаловать в игру Блэк Джэк\n")
    names=[]
    number = games.ask_number("Сколько всего игроков?(1 - 7)", low = 1, high = 7)

    for i in range(number):
        name = input("Ввведите имя игрока №" + str(i + 1) + " :")
        names.append(name)
    print()

    game = BJ_Game(names)
    again = None
    while again != "n":
        game.play()
        again = games.ask_yes_no("\nХотите сыграть еще раз?")


main()

