import random

class BlackJack:
    def __init__(self):
        self.deck = self.create_deck()
        self.shuffle_deck()
        self.player_hand = []
        self.dealer_hand = []


    def create_deck(self, decks = 4):
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        suits = ["Sinek", "Maça", "Kupa", "Karo"]

        deck = []
        for _ in range(decks):
            for i in suits:
                for j in values:
                    deck.append({"suit": i, "value": j})

        return deck


    def shuffle_deck(self):
        random.shuffle(self.deck)


    def deal_card(self, hand, closed = False):
        if len(self.deck) < 50:
            self.shuffle_deck()
        card = self.deck.pop()

        if closed:
            card["value"] = "Closed"
        hand.append(card)
        return card


    def new_round(self):
        self.player_hand = []
        self.dealer_hand = []
        self.deal_card(self.player_hand) # first card
        self.deal_card(self.player_hand) # second card
        self.deal_card(self.dealer_hand) # dealers first card
        self.deal_card(self.dealer_hand, True) # dealers second card closed




    def show_hands(self):
        def show_dealer_hand():
            return self.dealer_hand
        def show_player_hand():
            return self.player_hand

        return show_dealer_hand(), show_player_hand()
