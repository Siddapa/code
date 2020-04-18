import concurrent.futures.thread
import threading
from time import sleep
import pygame
import mouse
import keyboard


joystick_maps = {
    'FORWARD': 'w',
    'BACKWARD': 's',
    'LEFT': 'a',
    'RIGHT': 'd'
}


def init():
    pygame.quit()
    pygame.init()
    pygame.joystick.init()
    pygame.joystick.Joystick(0).init()


def forward():
    #1 = ly, 0 = lx, 4 = ry, 5 = rx joystick positions
    while True:
        pygame.event.pump()
        if pygame.joystick.Joystick(0).get_axis(1) < 0:
            keyboard.press_and_release(joystick_maps.get('FORWARD'))
        sleep(.1)
        print('Forward--------------------')


def backward():
    while True:
        pygame.event.pump()
        if pygame.joystick.Joystick(0).get_axis(1) > 0:
            keyboard.press_and_release(joystick_maps.get('BACKWARD'))
        sleep(.1)
        print("Backward---------------------")


def right():
    while True:
        pygame.event.pump()
        if pygame.joystick.Joystick(0).get_axis(0) > 0:
            keyboard.press_and_release(joystick_maps.get('RIGHT'))
        sleep(.1)
        print("Right---------------------")


def left():
    while True:
        pygame.event.pump()
        if pygame.joystick.Joystick(0).get_axis(0) < 0:
            keyboard.press_and_release(joystick_maps.get('LEFT'))
        sleep(.1)
        print("Left---------------------")


def list_axes():
    while True:
        pygame.event.pump()
        for axis in range(pygame.joystick.Joystick(0).get_numaxes()):
            print(pygame.joystick.Joystick(0).get_axis(axis))
        sleep(3)
        print()


if __name__ == '__main__':
    init()

    f = threading.Thread(target=forward)
    b = threading.Thread(target=backward)
    l = threading.Thread(target=left)
    r = threading.Thread(target=right)

    f.start()
    b.start()
    l.start()
    r.start()

    while True:
        pass
