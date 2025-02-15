import pygame, os
from game_logic import *

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, font_size, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.action = action

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):   # check if click is on button or not
                if self.action:
                    self.action()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_render = self.font.render(self.text, True, self.text_color)
        text_rect = text_render.get_rect(center=self.rect.center)
        surface.blit(text_render, text_rect)



class BlackJackUI:
    def __init__(self):
        self.running = True
        pygame.init()

        # displaying a window of height
        self.width = 900
        self.height = 500
        self.res = (self.width, self.height)
        self.surface = pygame.display.set_mode(self.res)

        # logo
        logo = pygame.image.load('cards/blackjack.png')
        pygame.display.set_icon(logo)

        # title
        self.title = "BlackJack"
        pygame.display.set_caption(self.title)

        # game objects
        self.game = BlackJack()
        self.game.start_game()

        # background
        self.bg_color = "#096117"
        self.surface.fill(self.bg_color)
        pygame.display.flip()

        # budget and bet amount
        self.font = pygame.font.Font('freesansbold.ttf', 20)

        self.update_budget()
        self.update_score()
        self.case_rect = None
        self.case_text = None
        self.stood = False
        self.busted = False
        self.update_case()

        # buttons
        self.button_color = "#d3ebd4"
        self.center_x = self.width // 2     # center of the screen for button coordinates
        self.hit_button = Button(self.center_x-90, 440, 70, 30,"Hit",
                                 self.button_color, "black", 20, lambda: self.player_hit())
        self.stand_button = Button(self.center_x, 440, 70, 30,"Stand",
                                   self.button_color, "black", 20, lambda: self.stand())
        self.restart_button = Button(800, 30, 70, 30,"Restart",
                                     self.button_color, "black", 20, lambda: self.restart_game())


        # card images
        self.card_images = self.load_card_images()

    def load_card_images(self):
        card_images = {}
        folder = "cards"
        for suit in ["heart", "club", "diamond", "spades"]:
            for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]:
                filename = f"{suit}_{rank}.png"
                path = os.path.join(folder, filename)

                if os.path.exists(path):
                    img = pygame.image.load(path)
                    img = pygame.transform.scale(img,(80, 120))
                    card_images[f"{suit}_{rank}"] = img
        return card_images

    def get_card_img(self, card):
        card_name = f"{card.suit}_{card.rank}"
        img = self.card_images.get(card_name, None)
        return img

    def load_closed_card(self):
        path = "cards/closed_card.png"
        closed_card = pygame.image.load(path)
        closed_card = pygame.transform.scale(closed_card, (80, 120))
        print(f"Kapalı kart {path} başarıyla yüklendi!")  # Başarı mesajı ekle

        return closed_card

    def check_winner(self):
        self.winner = self.game.check_winner()
        self.update_budget()
        self.update_case()


    def restart_game(self):
        self.game.start_game()
        self.game.winner = None
        self.case_text = None
        self.case_rect = None
        self.stood = False
        self.busted = False
        self.update_budget()
        self.update_score()  # reset case_text
        self.update_screen()

    def win_or_lose(self):

        if self.game.winner == self.game.player:
            self.case = 1
            return f"Won ${self.game.player.bet * 2}"
        elif self.game.winner == self.game.dealer:
            self.case = 2
            return f"Lost ${self.game.player.bet}"
        elif self.game.winner == "Tie":
            self.case = 0
            return "Tie"
        else:
            self.case = None
            return None

    def update_case(self):
        case_message = self.win_or_lose()
        case_font = pygame.font.Font('freesansbold.ttf', 70)  # bigger font

        if self.case == 2:      # dealer won
            self.case_text = case_font.render(f" {case_message}! ", True, "white", "#f53646")
            self.case_rect = self.case_text.get_rect(center=(450, 50))

        elif self.case == 1:    # player won
            self.case_text = case_font.render(f" {case_message}! ", True, "white", "#58d4ed")
            self.case_rect = self.case_text.get_rect(center=(450, 50))

        elif self.case == 0:     # tie
            self.case_text = case_font.render(f" {case_message}! ", True, "white", "#c4c40e")
            self.case_rect = self.case_text.get_rect(center=(450, 50))
        else:
            self.case_rect = None
            self.case_text = None

    def update_budget(self):
        self.budget_text = self.font.render(f"Budget: ${self.game.player.budget}", True, "white", self.bg_color)
        self.budget_rect = self.budget_text.get_rect(topleft=(20, 20))

        self.bet_text = self.font.render(f"Bet: ${self.game.player.bet}", True, "white", self.bg_color)
        self.bet_rect = self.bet_text.get_rect(topleft=(20, 50))

    def update_score(self):
        # update score
        self.game.player.score = self.game.player.calculate_score(self.game.player.hand)
        self.game.dealer.score = self.game.dealer.calculate_score(self.game.dealer.hand)

        self.dealers_score_text = self.font.render(f"Dealers hand: {self.game.dealer.score}", True, "white", self.bg_color )
        self.dealers_score_rect = self.dealers_score_text.get_rect(center=(self.width // 2, 240))

        self.players_score_text = self.font.render(f"Players hand: {self.game.player.score}", True, "white", self.bg_color)
        self.players_score_rect = self.players_score_text.get_rect(center=(self.width // 2 , 270))


    def player_hit(self):
        if self.game.player.score <= 21 and self.stood == False:
            self.game.player_hit()
            self.update_score()

            if self.game.player.score > 21:
                self.busted = True
                self.update_score()
                self.check_winner()

    def stand(self):

        if self.stood or self.busted:  # stand button does not work without pressing the restart
            return

        if not self.busted:  # If player busted, button does not work
            self.game.stand()
            self.update_score()

            for card in self.game.dealer.hand:
                if hasattr(card, "hidden") and card.hidden:
                    card.hidden = False  # open card
                    self.update_screen()  # update screen

        self.stood = True  # Stand Button pressed
        self.check_winner()
        self.update_case()
        self.update_screen()


    def update_screen(self):
        self.surface.fill(self.bg_color)  # clear background

        # draw buttons
        self.hit_button.draw(self.surface)
        self.stand_button.draw(self.surface)
        self.restart_button.draw(self.surface)

        # update case
        if self.case_text:
            self.surface.blit(self.case_text, self.case_rect)

        # Budget and bet values
        self.surface.blit(self.budget_text, self.budget_rect)
        self.surface.blit(self.bet_text, self.bet_rect)

        # card values
        self.surface.blit(self.dealers_score_text, self.dealers_score_rect)
        self.surface.blit(self.players_score_text, self.players_score_rect)

        if self.case_text:
            self.surface.blit(self.case_text, self.case_rect)

        # draw player cards
        for index, card in enumerate(self.game.player.hand):
            img = self.get_card_img(card)
            if img:
                x = 250 + index * 100
                y = 300
                self.surface.blit(img, (x, y))

        # draw dealer cards
        for index, card in enumerate(self.game.dealer.hand):
            if hasattr(card, "hidden") and card.hidden:
                img = self.load_closed_card()   # closed card
            else:
                img = self.get_card_img(card)


            if img:
                x = 250 + index * 100
                y = 100
                self.surface.blit(img, (x, y))

        pygame.display.flip()  # update screen

    def run(self):
        # keep game running till running is true
        while self.running:

            if self.game.player.budget < 0:
                self.running = False

            self.update_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # check if click is on button or not
                self.hit_button.check_click(event)
                self.stand_button.check_click(event)
                self.restart_button.check_click(event)

        pygame.quit()
