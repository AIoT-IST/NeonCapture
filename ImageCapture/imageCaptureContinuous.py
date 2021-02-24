#!/usr/bin/python3

"""
    This sample demonstrate the continuously image capturing of the build-in Basler camera.
    The camera python API used is called pypylon and the official package github url is https://github.com/basler/pypylon
"""

import logging
import os
import sys
from pypylon import pylon
import cv2

logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO, stream=sys.stdout)
log = logging.getLogger()

def main():
    title = "Image Capture continuously"
    log.info("Starting initial camera...")
    # --------Basler camera--------------------
    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
    
    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    log.info("Starting cature image...")
    print("To close the application, press 'CTRL+C' here or switch to the output window and press ESC key")

    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)
            frame = image.GetArray()
            cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            cv2.imshow(title, frame)

            key = cv2.waitKey(1)

            # ESC key
            if key == 27:
                break
    
    cv2.destroyAllWindows()


if __name__ == '__main__':
    sys.exit(main() or 0)
