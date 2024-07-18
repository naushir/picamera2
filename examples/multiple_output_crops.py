#!/usr/bin/python3

# How to do digital zoom using the "ScalerCrop" control.

import cv2
import time

from picamera2 import Picamera2

picam2 = Picamera2()
cfg = picam2.create_video_configuration(main={"size": (1920, 1080), "format": "RGB888"},
                                        lores={"size": (1280, 720), "format": "RGB888"})
picam2.configure(cfg)
picam2.start(show_preview=True)

size = picam2.capture_metadata()['ScalerCrop'][2:]
full_res = picam2.camera_properties['PixelArraySize']

max = 20
while True:
    im = picam2.capture_array("lores")

    if max != 0:
        size = [int(s * 0.95) for s in size]
        half_size = [int(s / 2) for s in size]
        offset = [(r - s) // 2 for r, s in zip(full_res, size)]
        half_offset = [(r - s) // 2 for r, s in zip(full_res, half_size)]
        #print(offset, size)
        rect =  offset + size
        half_rect = half_offset + half_size
        print(rect, half_rect)
        #picam2.set_controls({"ScalerCrop": offset + size})
        picam2.set_controls({"ScalerCrops": [rect, half_rect]})
        max = max - 1

    cv2.imshow("Camera", im)
    cv2.waitKey(1)
