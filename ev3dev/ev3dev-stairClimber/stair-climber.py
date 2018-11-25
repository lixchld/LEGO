#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import MediumMotor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.button import Button
from ev3dev2.display import Display
from ev3dev2.sound import Sound
from time import sleep
import logging

#logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)5s: %(message)s')
log=logging.getLogger(__name__)

log.info('Stair climber starting......')

# define the touch sensor
ts = TouchSensor(INPUT_3)
# define the gyro sensor
gy = GyroSensor(INPUT_2)

# define the large motor on port B
lm_move = LargeMotor(OUTPUT_B)
# define the large motor on port D
lm_lifter = LargeMotor(OUTPUT_D)
# define the midium motor on port A
mm_move = MediumMotor(OUTPUT_A)

# define the button
btn = Button()

# define lcd display
lcd = Display()

# define sound
snd = Sound()

# define the steps to go, initial value is 0
steps = 1

# Declare function for one step
def oneStep():
	global gy
	global ts

	# reset gyro sensor
	# gy.reset()
	gy.mode = 'GYRO-RATE'
	gy.mode = 'GYRO-ANG'

	# start front/rear wheel
	# let rear wheel rotate faster than front wheel
	# in order to let rear wheel has more power to 
	# left the front wheel up while hitting the vertial surface of stair
	log.info('start drive wheels to move towards to the stair')
	mm_move.on(-90)
	lm_move.on(-100)
	# Waiting for the front wheel to lift up
	gy.wait_until_angle_changed_by(7.5)
	log.info('hit the stair')

	# slow down the speed of drive wheel
	# in order to save energy meanwhile
	# front wheel could climb up to the stair
	# keep the car stay steady on the flor
	mm_move.on(-8)
	lm_move.on(-15)

	# reset the lift motor to star record the degree to rotate
	lm_lifter.reset()
	# start the lift motor to lift the front part of car up
	lm_lifter.on(-90)
	
	log.info('Lifting front part ......')

	# keep going up until touch sensor being hit or
	# the front part of car higher than the horizental surface of stair
	while( not ts.is_pressed and (gy.angle > -3) ):
		sleep(0.01)
	
	log.info('Front part reach the position')
	# stop the lift motor
	lm_lifter.stop()
	# move towards the next level of stair
	log.info('move towards the next level of stair')
	lm_move.on(-30)
	mm_move.on(-30)
	sleep(0.5)
	
	# play a sound to indicate the lifting action
	snd.play_file('sounds/Air release.rsf')

	# keep a force on the drive wheel while lifting rear part of the car
	# to avoid the machine following down from the higher place
	mm_move.on(-8)
	lm_move.on(-15)

	log.info('Lifting the rear part')
	# lift the rear part of the car
	lm_lifter.on_for_degrees(-100, lm_lifter.degrees)

	# stop drive motor
	lm_move.stop()
	mm_move.stop()
	# reset gyro sensor
	gy.mode = 'GYRO-RATE'
	gy.mode = 'GYRO-ANG'



log.info('prepare for the initial position')
# prepare for the initial position
# detect the upper position of the lifter
lm_lifter.on( -100, brake=True)
while( not ts.is_pressed ):
	sleep(0.05)
# approaching the initial position with high speed
lm_lifter.on_for_rotations(90, 7)
# nearly approached the initial position, approaching with lower speed
lm_lifter.on_for_degrees(20, 240)

# clear the lcd display
lcd.clear()

# show the steps
lcd.text_pixels( str(steps), True, 80, 50, font='courB18')
lcd.update()

log.info('wait user to supply the steps')
# wait user to supply the steps to go
while( True ):
	if(not btn.buttons_pressed):
		sleep(0.01)
		continue

	if btn.check_buttons(buttons=['up']):
		steps += 1
	elif(btn.check_buttons(buttons=['down']) ):
		steps -= 1
		if( steps < 0 ):
			steps = 0
	elif(btn.check_buttons(buttons=['enter'])):
		break

	# update the steps on screen
	lcd.text_pixels( str(steps), True, 80, 50, font='courB18')
	lcd.update()

	# btn.wait_for_released(buttons=['up','down', 'left', 'right','enter'])

log.info('Climbing ......')
while( steps > 0 ):
	oneStep()
	steps -= 1
	# update the steps on screen
	lcd.text_pixels( str(steps), True, 80, 50, font='courB18')
	lcd.update()


# move forward & stop
mm_move.on(-90)
lm_move.on(-100)
sleep(0.5)
mm_move.stop()
lm_move.stop()




