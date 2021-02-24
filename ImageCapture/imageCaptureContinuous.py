#!/usr/bin/python3

"""
    This sample demonstrate the continuously image capturing of the build-in Basler and Appropho camera.
    The basler camera python API used is called pypylon and the official package github url is https://github.com/basler/pypylon
"""

import logging
import os
import sys
from pypylon import pylon
import cv2

logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO, stream=sys.stdout)
log = logging.getLogger()

def main():
    log.info("To close the application, press 'CTRL+C' here or switch to the output window and press ESC key")
    
    # --------Basler camera--------------------    
    try:        
        # conecting to the first available camera
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        log.info("Starting initialize Basler camera...")
        camera.Open()

        # Grabing Continusely (video) with minimal delay
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        log.info("Starting cature image...")        

        while camera.IsGrabbing():
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                    # Access the image data
                    image = converter.Convert(grabResult)
                    frame = image.GetArray()
                    cv2.imshow("Preview of Basler Camera --- Exit by press 'ESC' key", frame)

                    # Exit by press "ESC" key
                    if cv2.waitKey(1) == 27:
                            break
    
        cv2.destroyAllWindows()

    except Exception as e:
        # --------Appropho camera--------------------
        log.info("Starting initialize Appropho camera...")
        cap = cv2.VideoCapture(0)

        #Check if camera was opened correctly
        if not (cap.isOpened()):
            log.info("Could not open Appropho camera")


        #Set the resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        log.info("Starting cature image...") 

        # Capture frame-by-frame
        while(True):
            ret, frame = cap.read()

            # Display the resulting frame     
            cv2.imshow("Preview of Appropho Camera --- Exit by press 'ESC' key",frame)                        

            #Waits for a user input to quit the application
            if cv2.waitKey(1) == 27:
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    sys.exit(main() or 0)
