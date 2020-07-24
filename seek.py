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

# executed at every movement
def seek():
    pass