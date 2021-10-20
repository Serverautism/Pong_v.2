import pygame
import random

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

# general variables
player_height = 200
player_width = 20
player_speed = 2
screen_width = 800
screen_height = 600
title_bar_height = 50
middle_line_count = 10
middle_line_width = 10
middle_line_height = (screen_height - title_bar_height) / 2 / middle_line_count
winning_score = 5
game_mode = 0
single_player_level = 0

title = "Pongus"
menu_message = "Press 1 or 2 for the number of players."

playing = False
running = True

title_bar_color = (52, 58, 64)
background_color = (33, 37, 41)
entity_color = (108, 117, 125)

pong_sound = pygame.mixer.Sound("assets/pong.ogg")
pong_sound.set_volume(0.1)
score_sound = pygame.mixer.Sound("assets/score.ogg")
score_sound.set_volume(0.1)

screen = pygame.display.set_mode((screen_width, screen_height + title_bar_height), pygame.NOFRAME)
title_font = pygame.font.SysFont("Cascadia Code", 50, False, False)
score_font = pygame.font.SysFont("Cascadia Code", 40, True, False)
clock = pygame.time.Clock()

# ball
ball_speed = 3
ball_width = 20
ball_x = screen_width / 2 - ball_width / 2
ball_y = screen_height / 2 + title_bar_height - ball_width / 2
ball_dx = random.choice((-ball_speed, ball_speed))
ball_dy = random.choice((-ball_speed, ball_speed))

# player 1
player1_score = 0
player1_x = 10
player1_y = screen_height / 2 - player_height / 2 + title_bar_height
player1_dy = 0

# player 2
player2_score = 0
player2_x = screen_width - player_width - 10
player2_y = screen_height / 2 - player_height / 2 + title_bar_height
player2_dy = 0


def handle_event():
    global player1_dy, player2_dy, playing, running, menu_message

    for keypress in pygame.event.get():
        if keypress.type == pygame.QUIT:
            running = False

        elif keypress.type == pygame.KEYDOWN:
            if keypress.key == pygame.K_w:
                player1_dy = -player_speed
            elif keypress.key == pygame.K_s:
                player1_dy = player_speed
            elif keypress.key == pygame.K_ESCAPE:
                playing = False
                menu_message = "Press any key to continue..."
            if game_mode == 2:
                if keypress.key == pygame.K_UP:
                    player2_dy = -player_speed
                elif keypress.key == pygame.K_DOWN:
                    player2_dy = player_speed

        elif keypress.type == pygame.KEYUP:
            if keypress.key == pygame.K_w:
                player1_dy = 0
            elif keypress.key == pygame.K_s:
                player1_dy = 0
            if game_mode == 2:
                if keypress.key == pygame.K_UP:
                    player2_dy = 0
                elif keypress.key == pygame.K_DOWN:
                    player2_dy = 0


def main_menu_input():
    global game_mode, single_player_level, running, menu_message, playing

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                if game_mode == 0:
                    game_mode = 1
                    menu_message = "Press 1, 2 or 3 for the difficulty level."
                else:
                    single_player_level = 1
            elif event.key == pygame.K_2:
                if game_mode == 0:
                    game_mode = 2
                else:
                    single_player_level = 2
            elif event.key == pygame.K_3:
                if game_mode == 0:
                    pass
                else:
                    single_player_level = 3

            if game_mode == 2 or single_player_level != 0:
                playing = True


def check_score():
    global menu_message, playing, player1_score, player2_score, player1_dy, player2_dy

    if player1_score >= winning_score:
        menu_message = "Player 1 won! Press any key to play again."
        playing = False
        player1_score = 0
        player2_score = 0
        player1_dy = 0
        player2_score = 0
    elif player2_score >= winning_score:
        menu_message = "Player 2 won! Press any key to play again."
        playing = False
        player1_score = 0
        player2_score = 0
        player1_dy = 0
        player2_score = 0


def draw_title_bar(surface):
    score_text = "{} : {}".format(player1_score, player2_score)
    pygame.draw.rect(surface, title_bar_color, (0, 0, screen_width, title_bar_height))
    title_render = title_font.render(title, True, entity_color)
    score_render = score_font.render(score_text, True, entity_color)
    score_x = screen_width / 2 - score_render.get_width() / 2
    score_y = 15
    surface.blit(title_render, (5, 10))
    surface.blit(score_render, (score_x, score_y))


def draw_menu_message(surface):
    menu_text_render = title_font.render(menu_message, True, entity_color)
    menu_text_render_x = screen_width / 2 - menu_text_render.get_width() / 2
    menu_text_render_y = screen_height / 2 - menu_text_render.get_height() / 2 + title_bar_height
    surface.blit(menu_text_render, (menu_text_render_x, menu_text_render_y))


def draw_middle_line(surface):
    for i in range(middle_line_count):
        x = screen_width / 2 - middle_line_width / 2
        y = i * 2 * middle_line_height + title_bar_height + 1.5 * middle_line_height
        pygame.draw.rect(surface, entity_color, pygame.Rect(x, y, middle_line_width, middle_line_height))


def move_players():
    global player1_y, player2_y, player2_dy

    if game_mode == 1:
        if player2_x - ball_x <= (single_player_level - 1) * (screen_width / 6) + screen_width / 2:
            if ball_y > player2_y + player_height / 2:
                player2_dy = player_speed
            elif ball_y < player2_y + player_height / 2:
                player2_dy = -player_speed
        elif player2_dy != 0:
            player2_dy = 0

    player1_y += player1_dy
    player2_y += player2_dy

    if player1_y < 0 + title_bar_height:
        player1_y = 0 + title_bar_height
    if player1_y + player_height > screen_height + title_bar_height:
        player1_y = screen_height - player_height + title_bar_height

    if player2_y < 0 + title_bar_height:
        player2_y = 0 + title_bar_height
    if player2_y + player_height > screen_height + title_bar_height:
        player2_y = screen_height - player_height + title_bar_height


def move_ball():
    global ball_x, ball_y, ball_dx, ball_dy, player1_score, player2_score, player1_y, player2_y

    ball_x += ball_dx
    ball_y += ball_dy

    if ball_y <= 0 + title_bar_height or ball_y + ball_width > screen_height + title_bar_height:
        ball_dy *= -1
        pong_sound.play()

    if ball_x <= 0:
        player2_score += 1
        score_sound.play()
        player1_y = screen_height / 2 - player_height / 2 + title_bar_height
        player2_y = screen_height / 2 - player_height / 2 + title_bar_height
        ball_x = screen_width / 2 - ball_width / 2
        ball_y = screen_height / 2 + title_bar_height - ball_width / 2
        ball_dx = ball_speed
        ball_dy = random.choice((-ball_speed, ball_speed))

    elif ball_x + ball_width >= screen_width:
        player1_score += 1
        score_sound.play()
        player1_y = screen_height / 2 - player_height / 2 + title_bar_height
        player2_y = screen_height / 2 - player_height / 2 + title_bar_height
        ball_x = screen_width / 2 - ball_width / 2
        ball_y = screen_height / 2 + title_bar_height - ball_width / 2
        ball_dx = -ball_speed
        ball_dy = random.choice((-ball_speed, ball_speed))

    elif player1_x <= ball_x <= player1_x + player_width:
        if ball_y + ball_width > player1_y and player1_y + player_height > ball_y:
            ball_dx *= -1
            pong_sound.play()
            if player1_dy != 0:
                if ball_dy < 0 and player1_dy < 0:
                    ball_dy -= 1
                elif ball_dy > 0 and player1_dy > 0:
                    ball_dy += 1
                elif ball_dy < 0 and player1_dy > 0:
                    ball_dy += 1
                    ball_dx += 1
                elif ball_dy > 0 and player1_dy < 0:
                    ball_dy -= 1
                    ball_dx += 1
                elif ball_dy == 0:
                    if player1_dy < 0:
                        ball_dy -= 1
                    else:
                        ball_dy += 1

    elif player2_x <= ball_x + ball_width <= player2_x + player_width:
        if ball_y + ball_width > player2_y and player2_y + player_height > ball_y:
            ball_dx *= -1
            pong_sound.play()
            if player2_dy != 0:
                if ball_dy < 0 and player2_dy < 0:
                    ball_dy -= 1
                elif ball_dy > 0 and player2_dy > 0:
                    ball_dy += 1
                elif ball_dy < 0 and player2_dy > 0:
                    ball_dy += 1
                    ball_dx -= 1
                elif ball_dy > 0 and player2_dy < 0:
                    ball_dy -= 1
                    ball_dx -= 1
                elif ball_dy == 0:
                    if player2_dy < 0:
                        ball_dy -= 1
                    else:
                        ball_dy += 1


if __name__ == "__main__":
    # game loop
    while running:
        clock.tick(60)
        screen.fill(background_color)

        draw_title_bar(screen)

        if playing:
            draw_middle_line(screen)

            # move stuff
            handle_event()
            move_players()
            move_ball()

            pygame.draw.rect(screen, entity_color, pygame.Rect(ball_x, ball_y, ball_width, ball_width))

            check_score()

        else:
            draw_menu_message(screen)
            main_menu_input()

        pygame.draw.rect(screen, entity_color, pygame.Rect(player1_x, player1_y, player_width, player_height))
        pygame.draw.rect(screen, entity_color, pygame.Rect(player2_x, player2_y, player_width, player_height))

        pygame.display.update()

pygame.quit()
quit()
