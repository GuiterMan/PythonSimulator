import pygame
import time


# ped traffic light1 signal switching
def pedTrafficLight1SignalSwitching(pedLight1, screen, res_x, res_y, green, darkGreen, black, red, simStartTime):

    if pedLight1 == "green":
        pygame.draw.rect(screen, green, (res_x * 0.33, res_y * 0.8, 12, 12))
    elif pedLight1 == "flashingGreen":
        if (int(time.time() - simStartTime)) % 2 > 0:
            pygame.draw.rect(screen, darkGreen, (res_x * 0.33, res_y * 0.8, 12, 12))
        else:
            pygame.draw.rect(screen, black, (res_x * 0.33, res_y * 0.8, 12, 12))
    elif pedLight1 == "red" or pedLight1 == "bufferRed":
        pygame.draw.rect(screen, red, (res_x * 0.33, res_y * 0.8, 12, 12))
