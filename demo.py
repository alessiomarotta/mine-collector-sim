#!/usr/bin/env python
# -*- coding: utf-8 -*-

# public variables:
# - direction
# - x
# - y
#
# private variables:
# - mines
#
# public functions:
# - move_forward()
# - rotate_left()
# - rotate_right()
# - collect_mine()
# - drop_mine()
# - check_mine()
# - find_mine()
# - debug(line, text)

TICK_INTERVAL = 0.1
ENABLE_TRACE = False

FIELD_WIDTH = 7
FIELD_HEIGHT = 7
START_X = 0
START_Y = 6

mines = [('R', 3, 1), ('Y', 0, 3), ('B', 5, 6)]
direction = UP 
x = START_X
y = START_Y

queue = []
init_flags = [False for n in range(6)]
init_completed = False
trial_completed = False
mines_left = len(mines)

# executed at every movement
def seek():
    global mines_left

    if not init_completed:
        init()

    if not trial_completed:
        run()

    print_status()
    queue_exec()

# searches and collects mines in the field
def run():
    global trial_completed

    if not queue_isempty():
        return

    # trial completed, go to base and set direction to UP
    if x == FIELD_WIDTH-1 and mines_left == 0:
        queue_add(rotate_left)

        for n in range(START_X, x):
            queue_add(move_forward)

        queue_add(rotate_right)
        trial_completed = True

    # looks for mines in the current column and collects them
    if direction == UP and find_mine() != ' ':
        get_mine()

        if check_mine() != ' ':
            deposit_mine()

    # if no mines are found move to next column 
    elif x < FIELD_WIDTH-1:
            queue_add(rotate_right)
            queue_add(move_forward)
            queue_add(rotate_left)

# drops mine and goes back to previous position
def deposit_mine():
    global trial_completed, init_completed

    queue_add(rotate_left)
    queue_add(rotate_left)

    for n in range(y, FIELD_HEIGHT):
        queue_add(move_forward)

    # distance from base to the previous column
    steps = 0

    if x < START_X:
        queue_add(rotate_left)

        for n in range(x, START_X):
            queue_add(move_forward)
            steps += 1

        queue_add(rotate_right)
        queue_add(drop_mine)
        queue_add(rotate_right)

        for n in range(steps):
            queue_add(move_forward)

        queue_add(rotate_right)

    elif x > START_X:
        queue_add(rotate_right)

        for n in range(START_X, x):
            queue_add(move_forward)
            steps += 1

        queue_add(rotate_left)
        queue_add(drop_mine)
        queue_add(rotate_left)

        for n in range(steps):
            queue_add(move_forward)

        queue_add(rotate_left)

    else:
        queue_add(drop_mine)
        queue_add(rotate_left)
        queue_add(rotate_left)

# checks for mines at row FIELD_HEIGHT-1 and goes to (0, FIELD_HEIGHT-1)
def init():
    global init_completed, init_flags

    if not init_flags[0]:
        queue_add(rotate_right)
        init_flags[0] = True

    # right mine check
    if not init_flags[2] and queue_isempty():
        get_mine()

        if init_flags[5]:
            init_flags[1] = True

        if queue_isempty():
            go_to(START_X, START_Y)

            if not init_flags[1]:
                queue_add(rotate_left)
                queue_add(rotate_left)
                init_flags[2] = True # no mines found

            else:
                queue_add(rotate_left)
                queue_add(drop_mine)
                queue_add(rotate_right)

            init_flags[2] = True
            init_flags[5] = False

    # left mine check
    if init_flags[2] and not init_flags[4] and queue_isempty():
        get_mine()

        if init_flags[5]:
            init_flags[3] = True # left mine collected

        if queue_isempty():
            if init_flags[3]:
                go_to(START_X, START_Y)
                queue_add(rotate_right)
                queue_add(drop_mine)
                queue_add(rotate_right)

            init_flags[4] = True

    if init_flags[4] and queue_isempty():
        go_to(0, y)
        queue_add(rotate_right)
        init_completed = True

def get_mine():
    global init_flags

    if find_mine() != ' ':
        queue_add(move_forward)

        if (check_mine() != ' '):
            queue_add(collect_mine)
            init_flags[5] = True

def go_to(cx, cy):
    x_delta = abs(cx - x) 
    y_delta = abs(cy - y) 

    actions = (((0, None), (1, rotate_left), (2, rotate_left), (1, rotate_right)),
               ((2, rotate_left), (1, rotate_right), (0, None), (1, rotate_left)),
               ((1, rotate_left), (2, rotate_left), (1, rotate_right), (0, None)),
               ((1, rotate_right), (0, None), (1, rotate_left), (2, rotate_left)))
    
    if cy < y:
        for n in range(actions[0][direction][0]):
            queue_add(actions[0][direction][1])

    elif cy > y:
        for n in range(actions[1][direction][0]):
            queue_add(actions[1][direction][1])

    for n in range(y_delta):
        queue_add(move_forward)

    if cx < x:
        for n in range(actions[2][direction][0]):
            queue_add(actions[2][direction][1])

    elif cx > x:
        for n in range(actions[3][direction][0]):
            queue_add(actions[3][direction][1])

    for n in range(x_delta):
        queue_add(move_forward)

def print_status():
    global trial_completed, mines_left

    debug(1, "mines left: " + str(mines_left) + ' ')

    if not trial_completed:
        debug(0, "status: running")

    elif x == START_X and y == START_Y and direction == UP:
        debug(0, "status: completed")

    if len(queue) > 0 and queue[0] == drop_mine:
        mines_left -= 1

def queue_isempty():
    return len(queue) == 0

def queue_add(action):
    queue.append(action)

def queue_exec():
    if not queue_isempty():
        queue.pop(0)()
