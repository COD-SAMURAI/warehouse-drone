import pygame

def init():
    # initialize pygame library
    pygame.init()
    # set Control Display as 400x400 pixel
    window = pygame.display.set_mode((400,400))
    return window

def main():
    # Main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Your game logic and rendering code goes here

if __name__ == '__main__':
    window = init()
    while True:
        main()
