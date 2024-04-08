import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Game")

# Load background image
background_image = pygame.image.load("Game/background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load card back image
card_back_image = pygame.image.load("Game/card_back.png")

# Load card images
card_images = {f"{rank}_of_{suit}.png": pygame.image.load(f"Game/cards/{rank}_of_{suit}.png") for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] for suit in ['hearts', 'diamonds', 'clubs', 'spades']}

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define fonts
font = pygame.font.Font(None, 36)

# Function to display text
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.selected = False

    def image(self):
        return f"{self.rank}_of_{self.suit}.png"

def game_start_timer():
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))  # Display game background
        draw_text(str(i), WHITE, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        time.sleep(1)
    screen.fill(BLACK)
    screen.blit(background_image, (0, 0))  # Display game background
    pygame.display.flip()

def arrange_cards():
    player_card_positions = []
    for i in range(13):
        card_x = 20 + i * 70
        card_y = HEIGHT - 200
        player_card_positions.append((card_x, card_y))

    computer_card_positions = []
    for i in range(13):
        card_x = 20 + i * 70
        card_y = 20
        computer_card_positions.append((card_x, card_y))

    return player_card_positions, computer_card_positions



def game_loop():
    # Define points for each card rank
    points_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    # Define all suits excluding diamonds
    suits = ['hearts', 'clubs', 'spades']

    # Assign suits to player and computer
    player_suit, computer_suit = random.sample(suits, k=2)

    # Create player's deck with assigned suit
    player_deck = [Card(rank, player_suit) for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]

    # Create computer's deck with assigned suit
    computer_deck = [Card(rank, computer_suit) for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]

    # Shuffle the computer's deck
    random.shuffle(computer_deck)

    # Initialize computer_previous_card outside of the loop
    computer_previous_card = None

    # Shuffle the diamond cards
    diamond_cards = [Card(rank, 'diamonds') for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]
    random.shuffle(diamond_cards)

    # Initialize player and computer scores
    player_score = 0
    computer_score = 0

    # Get card positions
    player_card_positions, computer_card_positions = arrange_cards()

    running = True
    selected_card = None
    bid_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, (card_x, card_y) in enumerate(player_card_positions):
                    if card_x <= mouse_x <= card_x + 70 and card_y <= mouse_y <= card_y + 105:
                        if selected_card:
                            selected_card.selected = False
                        selected_card = player_deck.pop(i)
                        selected_card.selected = True

                        bid_count += 1
                        if bid_count == 13:
                            # Don't end the game here
                            pass

                        if not diamond_cards:
                            # End the game if there are no more diamond cards
                            running = False
                        else:
                            diamond_card = diamond_cards.pop(0)
                            computer_previous_card = computer_deck.pop(0)
                            if points_dict[selected_card.rank] > points_dict[computer_previous_card.rank]:
                                player_score += points_dict[diamond_card.rank]
                            elif points_dict[selected_card.rank] < points_dict[computer_previous_card.rank]:
                                computer_score += points_dict[diamond_card.rank]
                            else:
                                player_score += points_dict[diamond_card.rank] / 2
                                computer_score += points_dict[diamond_card.rank] / 2

        screen.blit(background_image, (0, 0))

        for i, card in enumerate(computer_deck):
            card_x, card_y = computer_card_positions[i]
            card_back_scaled = pygame.transform.scale(card_back_image, (70, 105))
            screen.blit(card_back_scaled, (card_x, card_y))

        if diamond_cards:
            diamond_card = diamond_cards[0]
            diamond_card_image = card_images[diamond_card.image()]
            diamond_card_image_scaled = pygame.transform.scale(diamond_card_image, (70, 105))
            screen.blit(diamond_card_image_scaled, (WIDTH // 2 - 35, HEIGHT // 2 - 52))

            if computer_previous_card:
                computer_previous_card_image = card_images[computer_previous_card.image()]
                computer_previous_card_image_scaled = pygame.transform.scale(computer_previous_card_image, (70, 105))
                screen.blit(computer_previous_card_image_scaled, (WIDTH // 2 + 75, HEIGHT // 2 - 52))

            if selected_card:
                selected_card_image = card_images[selected_card.image()]
                selected_card_image_scaled = pygame.transform.scale(selected_card_image, (70, 105))
                screen.blit(selected_card_image_scaled, (WIDTH // 2 - 185, HEIGHT // 2 - 52))

        for i, card in enumerate(player_deck):
            card_x, card_y = player_card_positions[i]
            card_image = card_images[card.image()]
            if card.selected:
                card_image.fill(BLACK, special_flags=pygame.BLEND_RGB_MULT)
            card_image_scaled = pygame.transform.scale(card_image, (70, 105))
            screen.blit(card_image_scaled, (card_x, card_y))

        # Display scores
        draw_text(f"Player's Score: {player_score}", WHITE, WIDTH // 4, HEIGHT - 50)
        draw_text(f"Computer's Score: {computer_score}", WHITE, 3 * WIDTH // 4, HEIGHT - 50)

        # Display outcome message after 13th bid
        if bid_count == 13:
            if player_score > computer_score:
                draw_text("Congratulations! You won!", WHITE, WIDTH // 2, HEIGHT // 2)
            elif player_score == computer_score:
                draw_text("It's a tie!", WHITE, WIDTH // 2, HEIGHT // 2)
            else:
                draw_text("You lost! Better luck next time", WHITE, WIDTH // 2, HEIGHT // 2)

        # Display bids above player's and computer's deck
        draw_text("Player's Bid", WHITE, WIDTH // 4, HEIGHT - 300)
        draw_text("Bot's Bid", WHITE, 3 * WIDTH // 4, HEIGHT - 300)
        
       

        pygame.display.flip()

game_start_timer()
game_loop()
pygame.quit()
