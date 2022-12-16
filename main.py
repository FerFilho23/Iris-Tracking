import cv2
import pyautogui as mouse
import time
from gaze_tracking import GazeTracking

gaze = GazeTracking()

# Screen size
screen_width,  screen_height = mouse.size()

# Define camera frame sizes
webcam = cv2.VideoCapture(0)
wCam, hCam = 640, 480
webcam.set(3, wCam)
webcam.set(4, hCam)

pTime = 0

def middle_point(p1, p2):
    x = int((p1[0] + p2[0]) / 2)
    y = int((p1[1] + p2[1]) / 2)
    return (x, y)

while True:
    # Get a new frame from the webcam
    _, frame = webcam.read()
    frame = cv2.flip(frame,1)

    # Send this frame to GazeTracking to analyze it
    gaze.refresh(frame)
    frame = gaze.annotated_frame()

    # Locate the pupils coordinates
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    
    # Control the mouse 
    
    #Move
    if left_pupil and right_pupil:
        x_mid, y_mid = middle_point(left_pupil, right_pupil)
        xToScreenRatio = x_mid/wCam
        yToScreenRatio = y_mid/wCam

        mouse.moveTo(screen_width * xToScreenRatio, screen_height * yToScreenRatio)
    
    # print("Left pupil:  " + str(left_pupil), "Right pupil: " + str(right_pupil), "Mouse Position: " + str(mouse.position()))

    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_DUPLEX, 3,
    (255, 0, 0), 3)
    
    
    # Press q to quit
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) == ord("q") or cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
