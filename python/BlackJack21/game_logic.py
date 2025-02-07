import random

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def value(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)


class Deck():
    def __init__(self, number_of_decks = 8):
        self.cards = []
        self.number_of_decks = number_of_decks
        self.create_deck()

    def create_deck(self):
        suits = ['heart', 'club', 'diamond', 'spade']
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = [Card(suit, rank) for _ in range(self.number_of_decks) for suit in suits for rank in ranks]

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def remaining_cards(self):
        return len(self.cards)



class Participant():
    def __init__(self, score = 0):
        self.hand = []
        self.score = score

    def add_card(self, card):
        self.hand.append(card)

class Player(Participant):
    def __init__(self, budget=1000, bet=10):
        super().__init__()
        self.budget = budget
        self.bet = bet

class Dealer(Participant):
    def __init__(self):
        super().__init__()

    def hide_first_card(self):
        if len(self.hand) > 0:
            pass

    def reveal_cards(self):
        return self.hand

    def dealersTurn(self):
        while BlackJack().calculate_score() < 17:
            BlackJack().dealer_hit()


class BlackJack():
    def __init__(self):
        self.player = Player()
        self.dealer = Dealer()
        self.deck = Deck()

    def player_hit(self):
        card = self.deck.draw()
        self.player.add_card(card)

    def dealer_hit(self):
        card = self.deck.draw()
        self.dealer.add_card(card)

    def stand(self):
        self.dealer.dealersTurn()

    def calculate_score(self):
        aces = 0
        score = 0
        for card in self.dealer.hand:
            value = Card().value()
            score += value
            aces += 1 if value == 11 else None
        while score > 21 and aces:
            score -= 10
            aces -= 1

        return score


    def check_winner(self, winner):
        player = self.calculate_score()
        dealer = self.calculate_score()

        if player > 21:
            winner = self.dealer
        elif dealer > 21:
            winner = self.dealer
        elif dealer > player:
            winner = self.dealer
        elif player > dealer:
            winner = self.dealer
        else:
            winner = "Tie"


    def new_round(self):
        pass

    def start(self):
        self.deck.create_deck()
        self.deck.shuffle_deck()

        self.player.add_card(self.deck.draw())
        self.dealer.add_card(self.deck.draw())
        self.player.add_card(self.deck.draw())
        self.dealer.add_card(self.deck.draw())









