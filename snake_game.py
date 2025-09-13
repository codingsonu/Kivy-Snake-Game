import pygame
import random
import sys
import time

import os, sys

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init()
screen_width, screen_height = 1000, 500
block_size = 50

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Clone")

image = pygame.image.load(resource_path('media/square.png'))
resized_image = pygame.transform.scale(image, (block_size, block_size))

apple = pygame.image.load(resource_path('media/apple.png'))
apple_image = pygame.transform.scale(apple, (block_size, block_size))

font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 40)

clock = pygame.time.Clock()

# Track last key press time
last_key_time = time.time()

# Game state variables
is_paused = False

def draw_button(text, x, y, w, h, color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, w, h)

    pygame.draw.rect(screen, color, button_rect, border_radius=5)
    label = small_font.render(text, True, (255, 255, 255))
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))

    if button_rect.collidepoint(mouse) and click[0] == 1 and action:
        pygame.time.delay(200)
        action()

def quit_game():
    pygame.quit()
    sys.exit()
    

infoObject = pygame.display.Info()
screen_width, screen_height = infoObject.current_w, infoObject.current_h

block_size = 50


# Baaki aapka game code yahi rahega ...

fullscreen = False

def toggle_fullscreen():
    global fullscreen, screen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen_width // 2, screen_height // 2), pygame.RESIZABLE)


def pause_screen():
    global is_paused, last_key_time
    is_paused = True
    while is_paused:
        screen.fill((30, 30, 30))

        pause_text = font.render("Paused", True, (255, 255, 0))
        screen.blit(pause_text, ((screen_width - pause_text.get_width()) // 2, 100))

        def on_resume():
            global is_paused, last_key_time
            is_paused = False
            last_key_time = time.time()

        draw_button("Resume", 400, 200, 200, 50, (0, 128, 255), on_resume)
        draw_button("Restart", 400, 270, 200, 50, (0, 128, 0), game_loop)
        draw_button("Quit", 400, 340, 200, 50, (128, 0, 0), quit_game)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

def game_over_screen(score):
    while True:
        screen.fill((0, 0, 0))

        score_text = font.render(f"Score: {score}", True, (255, 255, 0))
        screen.blit(score_text, ((screen_width - score_text.get_width()) // 2, 60))

        game_over_text = font.render("Game is Over", True, (255, 0, 0))
        screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2, 130))

        draw_button("Restart", 400, 230, 200, 50, (0, 128, 0), game_loop)
        draw_button("Quit", 400, 300, 200, 50, (128, 0, 0), quit_game)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

def game_loop():
    global last_key_time, is_paused, pause_button, screen, fullscreen
    global screen_width, screen_height
    fullscreen = False
    screen = pygame.display.set_mode((screen_width // 2, screen_height // 2), pygame.RESIZABLE)
    
    X, Y = 100, 100
    direction = 'RIGHT'
    player_segments = [(X, Y)]
    length = 1
    score = 0

    target_x = random.randint(0, (screen_width - block_size) // block_size) * block_size
    target_y = random.randint(0, (screen_height - block_size) // block_size) * block_size

    running = True
    is_paused = False

    last_key_time = time.time()

    pause_button = pygame.Rect(screen_width - 90, 10, 80, 35)  # Pause button rectangle

    while running:
        screen_width, screen_height = screen.get_width(), screen.get_height()
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # F11 press karne par toggle hoga
                    toggle_fullscreen()
            elif event.type == pygame.VIDEORESIZE:
                # Window resize hone par screen update karna ho to yahan karein
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if pause_button.collidepoint(mouse_x, mouse_y):
                    pause_screen()

        key = pygame.key.get_pressed()
        if any(key):
            last_key_time = current_time

        if current_time - last_key_time > 60:
            pause_screen()

        if key[pygame.K_LEFT] and direction != 'RIGHT':
            direction = 'LEFT'
        elif key[pygame.K_RIGHT] and direction != 'LEFT':
            direction = 'RIGHT'
        elif key[pygame.K_UP] and direction != 'DOWN':
            direction = 'UP'
        elif key[pygame.K_DOWN] and direction != 'UP':
            direction = 'DOWN'

        # Auto boundary turn
        if direction == 'LEFT' and X <= 0:
            direction = 'UP' if Y > 0 else 'DOWN'
        elif direction == 'RIGHT' and X >= screen_width - block_size:
            direction = 'DOWN' if Y < screen_height - block_size else 'UP'
        elif direction == 'UP' and Y <= 0:
            direction = 'RIGHT' if X < screen_width - block_size else 'LEFT'
        elif direction == 'DOWN' and Y >= screen_height - block_size:
            direction = 'LEFT' if X > 0 else 'RIGHT'

        if direction == 'LEFT':
            X -= block_size
        elif direction == 'RIGHT':
            X += block_size
        elif direction == 'UP':
            Y -= block_size
        elif direction == 'DOWN':
            Y += block_size

        new_head = (X, Y)
        player_segments.insert(0, new_head)

        if new_head in player_segments[1:]:
            sound = pygame.mixer.Sound(resource_path('media/destroy.wav'))
            pygame.mixer.Sound.play(sound)
            game_over_screen(score)

        if len(player_segments) > length:
            player_segments.pop()

        player_rect = pygame.Rect(X, Y, block_size, block_size)
        apple_rect = pygame.Rect(target_x, target_y, block_size, block_size)

        if player_rect.colliderect(apple_rect):
            sound = pygame.mixer.Sound(resource_path('media/eat_apple.wav'))
            channel = sound.play(fade_ms=100)
            pygame.time.delay(360)
           
             # play for 200 milliseconds
            channel.stop()
            # pygame.mixer.Sound.play(sound)
            length += 1
            score += 1
            target_x = random.randint(0, (screen_width - block_size) // block_size) * block_size
            target_y = random.randint(0, (screen_height - block_size) // block_size) * block_size

        screen.fill((38, 235, 110))
        screen.blit(apple_image, (target_x, target_y))
        for segment in player_segments:
            screen.blit(resized_image, segment)

        # Right alignment values
        right_padding = 20
        top_padding = 10
        space_between = 20  # space between score and pause

        # Render score text
        score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))

        # Calculate score background size
        score_bg_padding_x = 10
        score_bg_padding_y = 5
        score_bg_width = score_text.get_width() + 2 * score_bg_padding_x
        score_bg_height = score_text.get_height() + 2 * score_bg_padding_y

        # Pause button size
        pause_button_width = 80
        pause_button_height = 35

        # X positions based on screen width (from right to left)
        pause_button_x = screen_width - right_padding - pause_button_width
        score_bg_x = pause_button_x - space_between - score_bg_width

        # Y positions (top aligned)
        pause_button_y = top_padding
        score_bg_y = top_padding

        # Update pause_button rect (if you are using it for collision check)
        pause_button.x = pause_button_x
        pause_button.y = pause_button_y
        pause_button.width = pause_button_width
        pause_button.height = pause_button_height

        # Draw score background
        pygame.draw.rect(screen, (0, 0, 255), (score_bg_x, score_bg_y, score_bg_width, score_bg_height), border_radius=5)
        screen.blit(score_text, (score_bg_x + score_bg_padding_x, score_bg_y + score_bg_padding_y))

        # Draw pause button
        pygame.draw.rect(screen, (0, 0, 255), pause_button, border_radius=5)
        pause_label = small_font.render("Pause", True, (255, 255, 255))
        label_x = pause_button.x + (pause_button.width - pause_label.get_width()) // 2
        label_y = pause_button.y + (pause_button.height - pause_label.get_height()) // 2
        screen.blit(pause_label, (label_x, label_y))
        pygame.display.update()
        clock.tick(7)

# Start game
game_loop()
