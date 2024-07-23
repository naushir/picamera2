#!/usr/bin/python3

# How to do digital zoom using the "ScalerCrop" control.

import cv2
import time

from picamera2 import Picamera2
from libcamera import Size

picam2 = Picamera2()


cfg = picam2.create_video_configuration(raw={"size": (4608, 2592)},
                                        main={"size": (1280, 720), "format": 'RGB888'},
                                        lores={"size": (320, 240), "format": 'RGB888'},
                                        display="main")

picam2.configure(cfg)
#picam2.set_controls({"ScalerCrops": [(0, 0, 4608, 2592), (1175, 661, 2257, 1270)]})
picam2.start(show_preview=True)

while True:
    im = picam2.capture_array("lores")
    cv2.imshow("vf", im)
    cv2.waitKey(1)