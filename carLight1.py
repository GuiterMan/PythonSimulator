import pygame

# Car traffic light1 signal switching
def carTrafficLight1SignalSwitching(carLight1, screen, res_x, res_y, green, yellow, red):
    if carLight1 == "green":
        pygame.draw.rect(screen, green, (res_x * 0.36, res_y * 0.79, 20, 20))
    elif carLight1 == "greenToYellow" or carLight1 == "redToYellow":
        pygame.draw.rect(screen, yellow, (res_x * 0.36, res_y * 0.79, 20, 20))
    elif carLight1 == "red":
        pygame.draw.rect(screen, red, (res_x * 0.36, res_y * 0.79, 20, 20))
