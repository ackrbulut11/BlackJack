import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.suit} of {self.rank}"

    def value(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)


class Deck:
    def __init__(self, number_of_decks = 8):
        self.cards = []
        self.number_of_decks = number_of_decks
        self.create_deck()

    def create_deck(self):
        suits = ['heart', 'club', 'diamond', 'spades']
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = [Card(suit, rank) for _ in range(self.number_of_decks) for suit in suits for rank in ranks]

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def remaining_cards(self):
        return len(self.cards)



class Participant:
    def __init__(self):
        self.hand = []
        self.score = self.calculate_score(self.hand)

    def add_card(self, card):
        self.hand.append(card)

    def calculate_score(self, hand):
        aces = 0
        score = 0
        for card in hand:
            value = card.value()
            score += value
            if value == 11:
                aces += 1

        while score > 21 and aces:
            score -= 10
            aces -= 1

        return score

class Player(Participant):
    def __init__(self, budget=1000, bet=10):
        super().__init__()
        self.budget = budget
        self.bet = bet

class Dealer(Participant):
    def __init__(self):
        super().__init__()
        self.player = Player()

    def hide_first_card(self):
        if len(self.hand) > 0:
            self.hand[0].hidden = True

    def reveal_cards(self):
        return self.hand

    def dealersTurn(self, deck):
        while (self.calculate_score(self.hand) < 17 and
               self.calculate_score(self.hand) <= self.player.calculate_score(self.player.hand)):
            self.add_card(deck.draw())


class BlackJack():
    def __init__(self, winner = None):
        self.player = Player()
        self.dealer = Dealer()
        self.deck = Deck()
        self.winner = winner

    def player_hit(self):
        card = self.deck.draw()
        self.player.add_card(card)

    def dealer_hit(self):
        card = self.deck.draw()
        self.dealer.add_card(card)

    def stand(self):
        self.dealer.hand[0].hidden = False
        self.dealer.dealersTurn(self.deck)
        self.check_winner()


    def check_winner(self):
        player = self.player.calculate_score(self.player.hand)
        dealer = self.dealer.calculate_score(self.dealer.hand)

        if player > 21:
            self.winner = self.dealer
        elif dealer > 21:
            self.winner = self.player
        elif dealer > player:
            self.winner = self.dealer
        elif player > dealer:
            self.winner = self.player
        else:
            self.winner = "Tie"

        # pay award
        if self.winner == self.player:
            self.player.budget += self.player.bet * 2
        elif self.winner == "Tie":
            self.player.budget += self.player.bet


    def new_round(self):
        self.player.hand = []
        self.player.score = 0
        self.dealer.hand = []
        self.dealer.score = 0

        self.player.budget -= self.player.bet

        self.start_new_round()

    def start_new_round(self):
        self.player.add_card(self.deck.draw())
        self.hidden_card = self.deck.draw()  # hidden card
        self.player.add_card(self.deck.draw())
        self.dealer.add_card(self.deck.draw())


    def start_game(self):
        self.deck.create_deck()
        self.deck.shuffle_deck()

        self.start_new_round()

