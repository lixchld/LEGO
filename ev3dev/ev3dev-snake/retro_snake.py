#!/usr/bin/env python3

import logging
from time import sleep
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.display import Display
import array
import random
import os

#logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)5s: %(message)s')

log=logging.getLogger(__name__)
log.info("Starting Snake")

btn=Button()
sound=Sound()
display=Display()

# declare the variables
# direction x: 0-no move; 1-left; -1-right
dx=0
# direction y: 0-no move; 1-down; -1-up
dy=0
# Set burger position x
hx=random.randint(10, 170)
# set burger position y
hy=random.randint(20, 120)
# set the start x position of snake
Sx=[80]
# set the start y position of snake
Sy=[60]
# set the start x position of snake
x=80
# set the start y position of snake
y=60
# set the step of each move
step=5
# set length of snake
length=1
# set the time to sleep between each scan
waittime=0.15

# create new position for the burger
def createBuger():
	global hx,hy
	hx=random.randint(10, 170)
	hy=random.randint(10, 120)

# event handler for left button
def left(state):
	global dx,dy
	dx=-1
	dy=0

# event handler for right button
def right(state):
	global dx,dy
	dx=1
	dy=0

# event handler for up button
def up(state):
	global dx,dy
	dx=0
	dy=-1

# event handler for down button
def down(state):
	global dx,dy
	dx=0
	dy=1

# detect whether met the game over condition
def isDead(Sx, Sy):
	cnt=len(Sx)
	x=Sx[cnt-1]
	y=Sy[cnt-1]

	# reach the range limitation
	if(x > 177 or x < 0 or y > 122 or y < 0):
		return True

	# touch any part of the body
	if( cnt >= 3):
		indx=-3
		while indx > 0-cnt:
			tmpX=Sx[indx]
			tmpY=Sy[indx]
			if( tmpX==x and tmpY==y):
				return True
			indx -= 3

	return False

# subscribe the button events
btn.on_left = left
btn.on_right = right
btn.on_up = up
btn.on_down = down
createBuger()
display.clear()
lcd=Display()

# draw hanburger
display.draw.ellipse((hx,hy,hx+step,hy+step))

while True:
	# draw score on the screen
	lcd.draw.text((10,20), 'Score {0}'.format(length), fill='black')

	# process the button event
	btn.process()

	# start the game while any direction is given
	if dx!=0 or dy!=0:
		# Calculate the new head position
		x=x+dx*step
		y=y+dy*step
		# record the new position by appending to list
		Sx.append(x)
		Sy.append(y)

		# detect whether the snake touch the burger
		if (abs(hx-x) < step-1) and (abs(hy-y) < step-1):
			sound.beep()
			# clean hanburger
			display.draw.ellipse((hx,hy,hx+step,hy+step),fill=None, outline='white')
			# regenerate hanburger
			createBuger()
			# draw hanburger
			display.draw.ellipse((hx,hy,hx+step,hy+step))
			length += 1
		else:
			tmpx=Sx[0]
			tmpy=Sy[0]
			# clean the snake tail
			display.draw.rectangle((tmpx,tmpy,tmpx+step,tmpy+step), fill='white', outline='white')	
			# pop the unused element
			Sx.pop(0)
			Sy.pop(0)

		dead = isDead(Sx, Sy)
		if dead:
			sound.beep()
			sleep(3)
			exit()
	
	# Draw snake head
	display.draw.rectangle((x, y, x+step, y+step),fill='black')

	display.update()
	sleep(waittime)

