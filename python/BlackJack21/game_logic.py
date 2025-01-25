import random


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_value(self):
        if self.value in ["Jack", "Queen", "King"]:
            return 10
        elif self.value == "Ace":
            return 11
        else:
            return int(self.value)


class Deck:
    def __init__(self, decks = 4):
        self.deck = self.create_deck(decks)
        self.shuffle_deck()

    def create_deck(self, decks):
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        suits = ["Sinek", "Maça", "Kupa", "Karo"]

        deck = []
        for _ in range(decks):
            for suit in suits:
                for value in values:
                    deck.append(Card(suit, value))

        return deck

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_card(self):
        if len(self.deck) == 0:
            self.deck = self.create_deck(self.decks)
            self.shuffle_deck()

        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card, closed=False):
        if closed:
            self.cards.append(Card(card.suit, "Closed"))
        else:
            self.cards.append(card)

    def show_hand(self):
        return self.cards

    def calculate(self):
        total = 0
        for card in self.cards:
            if card.value() != ("Closed"):
                total += card.get_value()







class PlayerHand(Hand):
    def __init__(self):
        super().__init__()
        self.splitted = False
        self.stood = False
        self.split_hands = []


    def hit(self, deck):
        if not self.stood:
            card = deck.draw_card()
            self.add_card(card)

            return card


    def stand(self):
        self.stood = True

    def split(self, deck):
        if len(self.cards) == 2 and self.cards[0].value == self.cards[1].value:
            self.splitted = True
            card1 = self.cards.pop()
            card2 = self.cards.pop()

            hand1 = PlayerHand()
            hand2 = PlayerHand()

            hand1.add_card(card1)
            hand2.add_card(card2)

            hand1.add_card(deck.draw_card())
            hand2.add_card(deck.draw_card())

            self.split_hands = [hand1, hand2]
            return hand1, hand2

        else:
            return None

    def resetHand(self):
        self.stood = False
        self.splitted = False
        self.split_hands = []


class DealerHand(Hand):
    def __init__(self):
        super().__init__()
        self.second_card_closed = True  # dealers second card is closed

        def open_second_card(self):
            if self.second_card_closed and len(self.cards) > 1:
                self.cards[1].value = self.cards[1].value
                self.second_card_closed = False

                return self.cards[1]



class BlackJack:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = PlayerHand()
        self.dealer_hand = DealerHand()
        self.winner = None


    def deal_card(self, hand, closed=False):
        card = self.deck.draw_card()
        hand.add_card(card, closed)

        return card


    def new_round(self):
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.deal_card(self.player_hand)  # first card
        self.deal_card(self.player_hand)  # second card
        self.deal_card(self.dealer_hand)  # dealer's first card
        self.deal_card(self.dealer_hand, True)  # dealer's second card closed

    def show_hands(self):

        return self.dealer_hand.show_hand(), self.player_hand.show_hand()

    def check_winner(self):
        playerTotal = self.player_hand.calculate()
        dealerTotal = self.dealer_hand.calculate()

        if playerTotal>21:
            self.winner = "Dealer"
        elif dealerTotal > 21:
            self.winner = "Player"
        elif dealerTotal > playerTotal:
            self.winner = "Dealer"
        elif playerTotal > dealerTotal:
            self.winner = "Player"
        else:
            self.winner = None

    def dealerTurn(self):

        self.dealer_hand.open_second_card()

        while self.dealer_hand.calculate() < 17:
            self.dealer_hand.add_card(self.deck.draw_card())






