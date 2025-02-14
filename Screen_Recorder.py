import cv2
import numpy as np
import pyautogui

# display screen resolution, get it using pyautogui itself
SCREEN_SIZE = tuple(pyautogui.size())
# define the codec
fourcc = cv2.VideoWriter_fourcc(*"XVID")
# frames per second
fps = 30.0
# create the video write object
out = cv2.VideoWriter("output_video.mp4", fourcc, fps, (SCREEN_SIZE))
# the time you want to record in seconds

while True:
    # Capture the screen
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    
    # Convert RGB to BGR (OpenCV uses BGR)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Write frame to video file
    out.write(frame)
    
    # Display the frame (optional)
    cv2.imshow("Screen Recording", frame)
    
    # Stop recording when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# make sure everything is closed when exited
cv2.destroyAllWindows()
out.release()
