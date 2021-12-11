import pygame
import random
import os

pygame.mixer.init()

pygame.init()




white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
c=(0,255,0)
d=(0,0,255)
e=(123,3,32)
color=[white,red,black,c,d,e]


screen_width = 1300
screen_height = 656
gameWindow = pygame.display.set_mode((screen_width, screen_height))


bgimg = pygame.image.load("Components\snake.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()


icon=pygame.image.load("Components\snake-icon.jpg").convert_alpha()
pygame.display.set_icon(icon)


pygame.display.set_caption("Snakes")
pygame.display.update()


pygame.mixer.music.load("Sounds\music.wav")
eat = pygame.mixer.Sound("Sounds\mixkit-chewing-something-crunchy-2244.wav")
lose = pygame.mixer.Sound("Sounds\lose.wav")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size,vx,vy):
    t=0
    for x,y in snk_list:




        pygame.draw.circle(gameWindow, color[t], [x+snake_size*(1/2), y+snake_size*(1/2)], int(snake_size*(1/2)))
        t=(t+1)%6 

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(bgimg, (0, 0))
        text_screen("Welcome to Snakes", black, 260, 250)
        text_screen("Press Space Bar To Play", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    
                    
                    gameloop()

        pygame.display.update()
        clock.tick(60)



def gameloop():
    pygame.mixer.music.play(-1)

    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    a=1.5
    b=1
    
    if(not os.path.exists("snake_hiscore.txt")):
        with open("snake_hiscore.txt", "w") as f:
            f.write("0")

    with open("snake_hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, int(screen_width / 2))
    food_y = random.randint(20, int(screen_height / 2))
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60
    while not exit_game:
        if game_over:
            pygame.mixer.music.pause()
            with open("snake_hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.blit(bgimg, (0, 0))
            text_screen(f"SCORE = {score}", c, 100, 250)
            text_screen("Game Over! Press Enter To Continue", red, 100, 300)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                        a=1.5
                        b=1
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                        a=1.5
                        b=1
                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                        a=1
                        b=1.5
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                        a=1
                        b=1.5
                    if event.key == pygame.K_q:
                        score +=10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            if abs(snake_x - food_x)<6 and abs(snake_y - food_y)<6:
                score +=10
                pygame.mixer.Sound.play(eat)
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length +=5
                if score>int(hiscore):
                    hiscore = score

            
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  Hiscore: "+str(hiscore), red, 5, 5)
            pygame.draw.ellipse(gameWindow, red, [food_x, food_y, snake_size, snake_size])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.Sound.play(lose)
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.Sound.play(lose)
            plot_snake(gameWindow, color, snk_list, snake_size,velocity_x,velocity_y)
            pygame.draw.ellipse(gameWindow, c, [snake_x, snake_y, snake_size*(a), snake_size*(b)])
            d=1
            e=-1
            if(velocity_x>0):
                d=1
                e=-1
            if(velocity_x<0):
                d=-1
                e=-1
            if(velocity_y>0):
                d=1
                e=1
            if(velocity_y<0):
                d=-1
                e=-1
            pygame.draw.circle(gameWindow, red, (snake_x + int(snake_size/2)*a+d*(snake_size)*a/4, snake_y + int(snake_size/2)*b + e*(snake_size)*b/4), int(snake_size/5))
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
