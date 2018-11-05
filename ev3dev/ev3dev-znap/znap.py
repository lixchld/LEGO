#!/usr/bin/env python3
# An EV3 Python (library v2) solution to Exercise 3
# of the official Lego Robot Educator lessons that
# are part of the EV3 education software

import logging
from ev3dev2.motor import MoveSteering, OUTPUT_A, OUTPUT_D, OUTPUT_B, MediumMotor
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sound import Sound
from time import sleep
from threading import Thread
import random

#logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)5s: %(message)s')
log=logging.getLogger(__name__)

log.info('Znap starting......')

# initialize Lego motor
ms = MoveSteering(OUTPUT_A, OUTPUT_D)
mm = MediumMotor(OUTPUT_B)
# initialize lego ultrasonic sensor
us = UltrasonicSensor(INPUT_3)
sd = Sound()

CHK = False
MoveLoop = True

# thread 1:　moving around
def move_around():
	global CHK
	global MoveLoop
	log.info('Move thread stringing ......')
	while(True):
		while(MoveLoop):
			CHK = True
			log.info('Turn left ......')
			ms.on_for_rotations( 100, 100, random.randint(1, 3) )
			sleep( random.randint(0,2))
			log.info('Turn right ......')
			ms.on_for_rotations( -100, 100, random.randint(1, 3) )
			sleep( random.randint(0,2))
			
		log.info('Stop moving ......')
		CHK = False
		MoveLoop = True
		ms.stop()

		log.info('Sleep for 2 seconds ......')
		sleep(2)

	log.info('Move thread Stoping ......')

# thread 2: detect any object near by
def detect_object():
	global CHK
	global MoveLoop
	global us
	log.info('Detect thread stringing ......')
	while(True):
		distance = us.distance_centimeters
		log.info('detecting object in range ......{0}'.format(distance))

		if CHK and (distance < 50):

			log.info('Object detected in range ......')
			MoveLoop = False

			if(us.distance_centimeters < 20):

				log.info('Bite ********')
				mm.on(-100)

				sd.play('/home/robot/ev3dev-znap/sounds/T-rex-roar.rsf')
				sleep(0.25)

				mm.stop()
				sleep(0.5)

				log.info('Back to original position for next bite ********')
				mm.on_for_seconds(100, 1, True)

				log.info('Bite,　wait for 0.8s')
				# waiting for the head back to its original position
				# to avoid detecting by ultrasonic sensor
				sleep(0.8)
			else:
				log.info('Object is not in range, move more close')
				mm.on_for_degrees(-100, 120, True)

				sd.play('/home/robot/ev3dev-znap/sounds/Snake-hiss.rsf')

				log.info('Back to original position')
				mm.on_for_seconds(100, 1, True)

				log.info('Detect,　wait for 0.8s')
				# waiting for the head back to its original position
				# to avoid detecting by ultrasonic sensor
				sleep(0.8)

	log.info('Detect thread Stoping ......')


move_thread = Thread(target=move_around)
move_thread.start()

detect_thread = Thread(target=detect_object)
detect_thread.start()

