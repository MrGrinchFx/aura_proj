import cv2
import numpy as np
import pyautogui
from DoorDetector.DoorDetector import DoorDetector
import time

SCREEN_SIZE = tuple(pyautogui.size())
CAPTURE_REGION = (100, 100, 640, 480) # x, y, width, height
OUTPUT_SIZE = (840, 640)
FPS = 12.0


def get_frame():
    # Capture the screen
    screenshot = pyautogui.screenshot(region=CAPTURE_REGION)
    frame = np.array(screenshot)
    
    # Convert RGB to BGR (OpenCV uses BGR)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame


def main():
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter("output_video.mp4", fourcc, FPS, OUTPUT_SIZE)

    Detector = DoorDetector()

    # cap = cv2.VideoCapture("TestVideo.MOV")

    with open("yolo_output.txt", "w") as file:
        start_time = time.time()
        frame_count = 0
        while True:
        # while cap.isOpened():
            frame = get_frame()
            # success, frame = cap.read()

            frame = cv2.resize(frame, (840, 640))
            
            inference = Detector.inference(frame)

            for track_id, bbox in zip(inference["track_ids"], inference["bounding_boxes"]):
                file.write(f"{track_id} | {bbox} | ")

            file.write("\n")

            out.write(frame)
            
            cv2.imshow("Screen Recording", inference["annotation"])

            frame_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                actual_fps = frame_count / elapsed_time
                print(f"Actual FPS: {actual_fps:.2f}")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()
    out.release()

if __name__ == "__main__":
    main()