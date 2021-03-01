import pygame
from random import randrange as rand

WIDTH, HEIGHT = 1200, 800

fps = 60
w = 330
h = 35
speed = 15
paddle = pygame.Rect(WIDTH // 2 - w // 2, HEIGHT - h - 10, w, h)
ball_radius = 25
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rand(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
x, y = 1, -1
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rand(30, 256), rand(30, 256), rand(30, 256)) for i in range(10) for j in range(4)]
pygame.init()

sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
img = pygame.image.load("1.jpg").convert()


def collusiop(x, y, ball, rect):
    if x > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if y > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        x, y = -x, -y
    elif delta_x > delta_y:
        y = -y
    elif delta_y > delta_x:
        x = -x
    return x, y


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0, 0))
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('white'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
    ball.x += ball_speed * x
    ball.y += ball_speed * y

    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        x = - x
    if ball.centery < ball_radius:
        y = -y
    if ball.colliderect(paddle) and y > 0:
        x, y = collusiop(x, y, ball, paddle)
    index = ball.collidelist(block_list)
    if index != -1:
        hrect = block_list.pop(index)
        hcolor = color_list.pop(index)
        x, y = collusiop(x, y, ball, hrect)
        hrect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hcolor, hrect)
        fps += 3
    if ball.bottom > HEIGHT:
        print("GAME OVER")
        exit()
    elif not len(block_list):
        print("YOU WON!")
        exit()
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += speed

    pygame.display.flip()
    clock.tick(fps)
