#!/usr/bin/env python3

import logging
#from ev3dev2 import Device
import ev3dev2

#logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)5s: %(message)s')

log=logging.getLogger(__name__)


tachoMotors = ev3dev2.list_devices('tacho-motor', 'motor*')

log.info(tachoMotors)

