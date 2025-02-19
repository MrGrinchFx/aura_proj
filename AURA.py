import cv2
import numpy as np
import pyautogui
from DoorDetector.DoorDetector import DoorDetector

SCREEN_SIZE = tuple(pyautogui.size())


def get_frame():
        # Capture the screen
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        
        # Convert RGB to BGR (OpenCV uses BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame


def main():
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    fps = 30.0

    out = cv2.VideoWriter("output_video.mp4", fourcc, fps, (SCREEN_SIZE))

    Detector = DoorDetector()

    while True:
        frame = get_frame()
        frame = cv2.resize(frame, (840, 640))
        
        inference = Detector.inference(frame)

        for track_id, bbox in zip(inference["track_ids"], inference["bounding_boxes"]):
            print(f"ID: {track_id}, BBox: {bbox}")

        out.write(inference["annotation"])
        
        cv2.imshow("Screen Recording", inference["annotation"])
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # make sure everything is closed when exited
    cv2.destroyAllWindows()
    out.release()

if __name__ == "__main__":
    main()