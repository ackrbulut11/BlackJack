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

        # buttons
        self.button_color = "#d3ebd4"
        self.center_x = self.width // 2     # center of the screen for button coordinates
        self.hit_button = Button(self.center_x-90, 440, 70, 30,
                                 "Hit", self.button_color, "black", 20, lambda: self.player_hit())
        self.stand_button = Button(self.center_x, 440, 70, 30,
                                   "Stand", self.button_color, "black", 20, lambda: self.stand())

        # card images
        self.card_images = self.load_card_images()

    def load_card_images(self):
        card_images = {}
        folder = "cards"
        for suit in ["heart", "club", "diamond", "spade"]:
            for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]:
                filename = f"{suit} of {rank}.png"
                path = os.path.join(folder, filename)

                if os.path.exists(path):
                    img = pygame.image.load(path)
                    img = pygame.transform.scale(img,(80, 120))
                    card_images[f"{suit} of {rank}"] = img
        return card_images

    def get_card_img(self, card):
        return self.card_images.get(f"{card.suit} of {card.rank}", None)    # if there is no card return None

    def update_budget(self):
        self.budget_text = self.font.render(f"Budget: ${self.game.player.budget}", True, "black", "#d3ebd4")
        self.budget_rect = self.budget_text.get_rect(topleft=(20, 20))

        self.bet_text = self.font.render(f"Bet: ${self.game.player.bet}", True, "black", "#d3ebd4")
        self.bet_rect = self.bet_text.get_rect(topleft=(20, 50))

    def player_hit(self):
        self.game.player_hit()

    def stand(self):
        self.game.stand()

    def run(self):

        # keep game running till running is true
        while self.running:
            # draw Button
            self.hit_button.draw(self.surface)
            self.stand_button.draw(self.surface)

            # budget and bet
            self.surface.blit(self.budget_text, self.budget_rect)
            self.surface.blit(self.bet_text, self.bet_rect)

            # draw players cards
            for index, card in enumerate(self.game.player.hand):
                img = self.get_card_img(card)
                if img:
                    x = 250 + index * 100
                    y = 300
                    self.surface.blit(img, (x, y))

            # draw dealers cards
            for index, card in enumerate(self.game.dealer.hand):
                if index == 0 and hasattr(card, "hidden") and card.hidden:
                    img = pygame.image.load("closed_card.png")
                    img.pygame.transform.scale(img(80,120))
                img = self.get_card_img(card)
                if img:
                    x = 250 + index * 100
                    y = 100
                    self.surface.blit(img, (x, y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # check if click is on button or not
                self.hit_button.check_click(event)
                self.stand_button.check_click(event)

            pygame.display.flip()

        pygame.quit()
