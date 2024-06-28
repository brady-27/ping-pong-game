import pygame
import sys
import random
import time

pygame.init()

# Font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)
font40 = pygame.font.Font('freesansbold.ttf', 40)

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

clock = pygame.time.Clock()
FPS = 30

class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.geekRect = pygame.Rect(posx, posy, width, height)
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def display(self):
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def update(self, yFac):
        self.posy += self.speed * yFac
        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height
        self.geekRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)

    def getRect(self):
        return self.geekRect

class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.initial_speed = speed  # Store the initial speed
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    def display(self):
        self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.xFac *= -1
        self.speed = self.initial_speed  # Reset speed to initial speed
        self.firstTime = 1

    def hit(self):
        self.xFac *= -1
        self.speed += 1  # Increase speed after hitting paddle

    def getRect(self):
        return self.ball



def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_net():
    net_width = 5
    net_height = 20
    for y in range(0, HEIGHT, net_height * 2):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - net_width // 2, y, net_width, net_height))

def menu():
    while True:
        screen.fill(BLACK)
        draw_text('Pong Game', font40, WHITE, screen, WIDTH // 2, HEIGHT // 4)
        draw_text('Press 1 for 2 Players', font20, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text('Press 2 for Player vs AI', font20, WHITE, screen, WIDTH // 2, HEIGHT // 2)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main(False)  # 2 Players
                if event.key == pygame.K_2:
                    difficulty_menu()  # Difficulty selection screen

def difficulty_menu():
    while True:
        screen.fill(BLACK)
        draw_text('Select Difficulty', font40, WHITE, screen, WIDTH // 2, HEIGHT // 4)
        draw_text('Press 1 for Easy', font20, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text('Press 2 for Medium', font20, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text('Press 3 for Hard', font20, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    time_limit_menu(True, 0.6)  # Easy
                if event.key == pygame.K_2:
                    time_limit_menu(True, 0.8)  # Medium
                if event.key == pygame.K_3:
                    time_limit_menu(True, 1)  # Hard

def time_limit_menu(ai_mode, difficulty):
    while True:
        screen.fill(BLACK)
        draw_text('Select Time Limit', font40, WHITE, screen, WIDTH // 2, HEIGHT // 4)
        draw_text('Press 1 for 1 Minute', font20, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text('Press 2 for 3 Minutes', font20, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text('Press 3 for 5 Minutes', font20, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main(ai_mode, difficulty, 1)  # 1 Minute
                if event.key == pygame.K_2:
                    main(ai_mode, difficulty, 3)  # 3 Minutes
                if event.key == pygame.K_3:
                    main(ai_mode, difficulty, 5)  # 5 Minutes

def main(ai_mode, difficulty=0.7, time_limit=1):
    running = True

    geek1 = Striker(20, 0, 10, 100, 10, GREEN)
    geek2 = Striker(WIDTH - 30, 0, 10, 100, 10, GREEN)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, WHITE)

    listOfGeeks = [geek1, geek2]

    geek1Score, geek2Score = 0, 0
    geek1YFac, geek2YFac = 0, 0

    start_time = time.time()
    end_time = start_time + time_limit * 60

    while running:
        screen.fill(BLACK)
        draw_net()  # Draw the net

        elapsed_time = time.time() - start_time
        remaining_time = max(0, end_time - time.time())
        draw_text(f'Time: {int(remaining_time // 60)}:{int(remaining_time % 60):02}', font20, WHITE, screen, WIDTH // 2, 20)

        if remaining_time <= 0:
            running = False
            if geek1Score > geek2Score:
                winner = "Geek 1 Wins!"
            elif geek2Score > geek1Score:
                winner = "Geek 2 Wins!"
            else:
                winner = "It's a Tie!"
            screen.fill(BLACK)
            draw_text(winner, font40, WHITE, screen, WIDTH // 2, HEIGHT // 2)
            pygame.display.update()
            pygame.time.wait(3000)
            menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    geek2YFac = -1
                if event.key == pygame.K_DOWN:
                    geek2YFac = 1
                if event.key == pygame.K_w:
                    geek1YFac = -1
                if event.key == pygame.K_s:
                    geek1YFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    geek2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    geek1YFac = 0

        for geek in listOfGeeks:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                ball.hit()

        geek1.update(geek1YFac)

        if ai_mode:
            if random.random() < difficulty:
                if geek2.posy + geek2.height / 2 < ball.posy:
                    geek2.update(1)
                elif geek2.posy + geek2.height / 2 > ball.posy:
                    geek2.update(-1)
        else:
            geek2.update(geek2YFac)

        point = ball.update()

        if point == -1:
            geek1Score += 1
        elif point == 1:
            geek2Score += 1

        if point:
            ball.reset()

        geek1.display()
        geek2.display()
        ball.display()

        geek1.displayScore("Geek 1: ", geek1Score, 100, 50, WHITE)
        geek2.displayScore("Geek 2: ", geek2Score, WIDTH - 100, 50, WHITE)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    menu()
    pygame.quit()