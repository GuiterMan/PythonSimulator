import pygame
import random
import time
from car import Car
from pedestrian import Pedestrian
from checkCollision import isCarCollided, pedLight1IsWalking
from carLight1 import carTrafficLight1SignalSwitching
from pedLight1 import pedTrafficLight1SignalSwitching

pygame.init()

waitingTime = 0

# Draw screen data
res_x = 1680
res_y = 1050
screen = pygame.display.set_mode((res_x , res_y))
image = pygame.image.load("rdbg.png")

# Set Simulator
clock = pygame.time.Clock()
running = True
simulatorSpeed = 1;

# Color set
darkBlue = (30, 30, 130)
black = (50, 50, 50)
red = (255, 0, 0)
yellow = (255, 211, 0)
green = (0, 255, 0)
lightBlue = (153, 204, 255)
darkGreen = (0, 200, 0)

# Traffic light signal
carLight1 = "green"
pedLight1 = "red"

# Traffic elements
carArray = []
pedArray = []
# Pedstrian startPosition array
pedStart = [0, 0, 0]
# Car start Y position
yArray = [780, 750, 720, 690]
pedStart0XAry = [res_x * 0.33, res_x * 0.335, res_x * 0.34, res_x * 0.345]
pedStart0YAry = [res_y * 0.785, res_y * 0.65]
carLineArray = []

#Count TrafficModel Time
countCarLight1Time = True
countPedLight1Time = True
totalCarWaitingTime = 0
totalPedWaitingTime = 0
simStartTime = 0
if __name__ == "__main__":
    simStartTime = time.time()
    # Simulation Start
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        #Draw screen
        screen.fill((255, 255, 255))
        screen.blit(image, (0, 0))

        # Draw title
        sys_font = pygame.font.SysFont("None", 50)
        rendered = sys_font.render("Traffic Model(Intelligent Traffic Light System)", 0, black)
        screen.blit(rendered, (res_x * 0.05, res_y * 0.05))
        # Draw road description
        sys_font = pygame.font.SysFont("None", 15)
        rendered = sys_font.render("carLight1", 0, black)
        screen.blit(rendered, (res_x * 0.35, res_y * 0.82))
        rendered = sys_font.render("pedStart01", 0, black)
        screen.blit(rendered, (res_x * 0.3, res_y * 0.82))
        # Draw video record area
        pygame.draw.rect(screen, (200, 0, 0), (res_x * 0.474, res_y * 0.5, 5, 400))
        sys_font = pygame.font.SysFont("None", 15)
        rendered = sys_font.render("Car Record Line", 0, black)
        screen.blit(rendered, (res_x * 0.455, res_y * 0.48))

        # Car traffic light1 signal switching
        carTrafficLight1SignalSwitching(carLight1, screen, res_x, res_y, green, yellow, red)

        # ped traffic light1 signal switching
        pedTrafficLight1SignalSwitching(pedLight1, screen, res_x, res_y, green, darkGreen, black, red, simStartTime)

        # Count traffic flow at junction
        carCountAtCarLight1 = 0
        pedCountAtPedStart01 = 0
        for wCar in carArray:
            if 800 > wCar.x > 590:
                carCountAtCarLight1 += 1
        for ped in pedArray:
            if ped.y == pedStart0YAry[0] and ped.pedStartNum == 0:
                pedCountAtPedStart01 += 1
            if ped.y == pedStart0YAry[1] and ped.pedStartNum == 1:
                pedCountAtPedStart01 += 1
        sys_font = pygame.font.SysFont("None", 20)
        rendered = sys_font.render("Car at carLight1: " + str(carCountAtCarLight1), 0, black)
        screen.blit(rendered, (res_x * 0.5, res_y * 0.8))
        rendered = sys_font.render("Ped at pedStart01: " + str(pedCountAtPedStart01), 0, black)
        screen.blit(rendered, (res_x * 0.5, res_y * 0.83))

        # CarLight1 ITLS
        if countCarLight1Time:
            carLight1ChgTime = time.time()
            countCarLight1Time = False

        if carLight1 == "green" and (pedCountAtPedStart01 > 30 or time.time() - carLight1ChgTime >= 120):
            carLight1 = "greenToYellow"
            # print("carLight1 switched to yellow.")
            # print("carLight1 status: " + carLight1 + ".\n")
            countCarLight1Time = True

        elif carLight1 == "greenToYellow" and time.time() - carLight1ChgTime >= 3:
            carLight1 = "red"
            pedLight1 = "green"
            # print("carLight1 switched to red.")
            # print("carLight1 status: " + carLight1 + ".\n")
            countCarLight1Time = True

        elif carLight1 == "red" and time.time() - carLight1ChgTime >= 13:
            carLight1 = "redToYellow"
            # print("carLight1 switched to yellow.")
            # print("carLight1 status: " + carLight1 + ".\n")
            countCarLight1Time = True

        elif carLight1 == "red" and 12 >= time.time() - carLight1ChgTime >= 7:
            pedLight1 = "flashingGreen"

        elif carLight1 == "red" and time.time() - carLight1ChgTime > 9:
            pedLight1 = "red"

        elif carLight1 == "redToYellow" and time.time() - carLight1ChgTime >= 3:
            carLight1 = "green"
            # print("carLight1 switched to green.")
            # print("carLight1 status: " + carLight1 + ".\n")
            countCarLight1Time = True

        # Put car on the road
        if random.randint(0, 10) == 1:
            line = random.randint(0, 3)
            c = Car(res_x-200,yArray[line], random.uniform(3, 8), 0, line)
            carArray.append(c)
            carLineArray.append([line, c])

        for c in carArray:
            if c.x > 150:
                c.carStart(screen, darkBlue)

            if isCarCollided(carLineArray, c) and c.x > 210:
                c.x -= 0
                c.waitingTime += 1

            else:
                # 1st part Route movement
                if c.x >= 800:
                    c.x -= c.speed
                # 2nd part Route movement
                elif 800 > c.x > 600:
                        c.x -= c.speed * 0.95
                        c.y += c.speed * 0.05
                # Check 3rd part carlight1 junction movement
                elif 600 >= c.x > 590:
                    if carLight1 == "green":
                        if pedLight1IsWalking(pedArray, pedStart0YAry):
                            c.x -=0
                            c.waitingTime += 1
                        else:
                            c.x -= c.speed * 0.95
                            c.y += c.speed * 0.05
                    elif carLight1 == "greenToYellow" or carLight1 == "redToYellow":
                        if c.x >= 590:
                            c.x -= 0
                            c.waitingTime += 1
                        else:
                            c.x -= c.speed * 0.95
                            c.y += c.speed * 0.05
                    elif carLight1 == "red":
                            c.x -= 0
                            c.waitingTime += 1
                # 4rd part Route movement
                elif 590 >= c.x > 150:
                    c.x -= c.speed * 0.9
                    c.y += c.speed * 0.1


        # Put pedestrian on the road
        if random.randint(0, 10) == 1:
            line = random.randint(0, 3)
            pedStartNum = random.randint(0, 1)
            c = Pedestrian(pedStart0XAry[line], pedStart0YAry[pedStartNum], random.uniform(1, 1.5), 0, line, pedStartNum)
            pedArray.append(c)

        for p in pedArray:
            # pedStart0 to pedStart1
            if p.y >= pedStart0YAry[1] and p.pedStartNum == 0:
                p.pedStart(screen, lightBlue)
                # Check Traffic light
                if pedLight1 == "red" and p.y == pedStart0YAry[0]:
                    p.y -= 0
                    p.waitingTime += 1
                elif pedLight1 == "green" or p.y != pedStart0YAry[0]:
                    p.y -= p.speed

            # pedStart1 to pedStart0
            if p.y <= pedStart0YAry[0] and p.pedStartNum == 1:
                p.pedStart(screen, lightBlue)
                # Check Traffic light
                if pedLight1 == "red" and p.y == pedStart0YAry[1]:
                    p.y += 0
                    p.waitingTime += 1
                elif pedLight1 == "green" or p.y != pedStart0YAry[1]:
                    p.y += p.speed


        # Print pedestrian number
        for ped in pedArray:
            if ped.y == pedStart0YAry[0] and ped.pedStartNum == 0:
                pedStart[0] += 1
            if ped.y == pedStart0YAry[1] and ped.pedStartNum == 1:
                pedStart[1] += 1

        sys_font = pygame.font.SysFont("None", 30)

        rendered = sys_font.render(str(pedStart[0]), 0,(35, 20, 245))
        screen.blit(rendered, (res_x * 0.315, res_y * 0.8))

        rendered = sys_font.render(str(pedStart[1]), 0, (35, 20, 245))
        screen.blit(rendered, (res_x * 0.315, res_y * 0.63))

        rendered = sys_font.render(str(pedStart[2]), 0, (35, 20, 245))
        screen.blit(rendered, (res_x * 0.32, res_y * 0.57))

        pedStart[0] = 0
        pedStart[1] = 0

        # Update Game
        clock.tick(30)
        pygame.display.update()
# Print Simulation data
print()
print("Simulation has run for " + str(time.time() - simStartTime) + " second(s)")

print("Total car number on the street: " + str(len(carArray)))
for car in carArray:
    totalCarWaitingTime += car.waitingTime
print("Average car watiting time: " + str(totalCarWaitingTime / len(carArray) / 30) + " seconds")

print("Total pedestrian number on the street: " + str(len(pedArray)))
for ped in pedArray:
    totalPedWaitingTime += ped.waitingTime
print("Average pedestrian watiting time: " + str(totalPedWaitingTime / len(carArray) / 30) + " seconds")
