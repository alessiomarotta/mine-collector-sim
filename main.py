#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
from time import sleep

SOURCE_FILE = "demo.py"

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

exec(open(SOURCE_FILE).read())

debug_strings = []
dropped_mines = []
collected_mine = None

def move_forward(): 
    global x, y

    delta = ((0, -1), (1, 0), (0, 1), (-1, 0))
    x += delta[direction][0]
    y += delta[direction][1]

def rotate_left():
    global direction

    direction = (direction - 1) % 4

def rotate_right():
    global direction

    direction = (direction + 1) % 4

def collect_mine():
    global collected_mine

    for m in mines:
        if m[1] == x and m[2] == y:
            collected_mine = m
            mines.remove(m)

def drop_mine():
    global collected_mine

    if x == START_X and y == START_Y:
        dropped_mines.append(collected_mine)
        collected_mine = None

# checks for adjacent mines
# returns ' ' if no mines are found
def check_mine():
    delta = ((0, -1), (1, 0), (0, 1), (-1, 0))
    
    for m in mines:
        if m[1] == x+delta[direction][0] and m[2] == y+delta[direction][1]:
            return m[0]

    return ' '

# checks for distant mines in the current direction
# returns ' ' if there aren't any distant mines
def find_mine():
    for mine in mines:
        if direction == UP:
            for m in mines:
                if m[1] == x and 0 <= m[2] < y: return m[0] 

        elif direction == RIGHT:
            for m in mines:
                if m[2] == y and x < m[1] < FIELD_WIDTH: return m[0] 

        elif direction == DOWN:
            for m in mines:
                if m[1] == x and y <= m[2] < FIELD_HEIGHT: return m[0] 

        else:
            for m in mines:
                if m[2] == y and 0 <= m[1] < x: return m[0] 

    return ' '

def debug(line, text):
    debug_strings.append((line, text))

def display_robot(y, x, win):
    ch = ('▲', '▶', '▼', '◀')
    win.addstr(y+1, x+1, ch[direction])

def main(scr):
    global collected_mine

    scr.clear()
    curses.curs_set(0)

    win_debug = curses.newwin(30, 100, FIELD_HEIGHT+2, 0)
    win_field = curses.newwin(FIELD_HEIGHT+2, FIELD_WIDTH+2, 0, 0)
    win_field.border()

    display_robot(y, x, win_field)
    [win_field.addstr(m[2]+1, m[1]+1, m[0]) for m in mines]
    win_field.refresh()
    sleep(TICK_INTERVAL)

    while True:
        if ENABLE_TRACE: win_field.addstr(y+1, x+1, '·')
        else: win_field.addstr(y+1, x+1, ' ')
        
        seek()

        if collected_mine != None:
            win_field.addstr(collected_mine[2]+1, collected_mine[1]+1, ' ')

        dropped_mines_text = ''

        for m in dropped_mines:
            dropped_mines_text += m[0] + ' '

        win_debug.addstr(0, 0, dropped_mines_text)

        [win_debug.addstr(line+2, 0, text) for line, text in debug_strings]
        win_field.addstr(START_Y+1, START_X+1, '□')
        display_robot(y, x, win_field)

        win_debug.refresh()
        win_field.refresh()

        sleep(TICK_INTERVAL)
 
if __name__ == "__main__":
    curses.wrapper(main)
