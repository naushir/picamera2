#!/usr/bin/python3

# How to do digital zoom using the "ScalerCrop" control.

import cv2
import time

from picamera2 import Picamera2
from libcamera import Size

picam2 = Picamera2()

sensor_modes = [m['size'] for m in picam2.sensor_modes]
resolutions = [(1920, 1200), (1920, 1080), (1280, 960), (1280, 720), (640, 480), (320, 240)]
formats = ['RGB888', 'XRGB8888', 'YUV420']

for s_r in sensor_modes:
    for m_r in resolutions:
        for m_f in formats:
            for l_r in [r for r in resolutions if Size(r[0], r[1]) <= Size(m_r[0], m_r[1])]:
                for l_f in formats:
                    cfg = picam2.create_video_configuration(raw={"size": s_r},
                                                            main={"size": m_r, "format": m_f},
                                                            lores={"size": l_r, "format": l_f})

                    picam2.configure(cfg)
                    #picam2.set_controls({"ScalerCrops": [(0, 0, 4608, 2592), (1896, 1042, 815, 508)]})
                    picam2.start(show_preview=False)
                    print(f'sensor: {s_r}, main: {m_r} {m_f}, lores: {l_r} {l_f}')

                    size = picam2.capture_metadata()['ScalerCrop'][2:]
                    full_res = picam2.camera_properties['PixelArraySize']

                    # Crop window going smaller on both outputs
                    for _ in range(100):
                        im = picam2.capture_array("lores")
                        size = [int(s * 0.98) for s in size]
                        half_size = [int(s / 2) for s in size]
                        offset = [(r - s) // 2 for r, s in zip(full_res, size)]
                        half_offset = [(r - s) // 2 for r, s in zip(full_res, half_size)]
                        rect =  offset + size
                        half_rect = half_offset + half_size
                        print (f'phase 1 {[rect, half_rect]}')
                        picam2.set_controls({"ScalerCrops": [rect, half_rect]})

                    size = half_size
                    offset = half_offset

                    # Full crop on main, and crop window increasing in lores
                    for _ in range(100):
                        im = picam2.capture_array("lores")
                        size = [int(s * 1.02) for s in size]
                        offset = [(r - s) // 2 for r, s in zip(full_res, size)]
                        rect = offset + size
                        print (f'phase 2 {[(0, 0, *full_res), rect]}')
                        picam2.set_controls({"ScalerCrops": [(0, 0, *full_res), rect]})

                    picam2.stop()
    