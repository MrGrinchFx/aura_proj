import cv2
import numpy as np
import time
import mss

RECORDING_VIDEO = "recording.mp4"
CAPTURE_REGION = {"top": 200, "left": 60, "width": 1150, "height": 800}      
OUTPUT_SIZE = (840, 640)
FPS = 30.0


def get_frame(sct):
    # Capture the screen
    screenshot = sct.grab(CAPTURE_REGION)
    frame = np.array(screenshot)
    return frame[:, :, :3]  # Drop alpha channel (BGRA → BGR)


def screen_record(sct, out):
    # Screen Record
    start_time = time.time()
    frame_count = 0
    while True:
        frame = get_frame(sct)
        frame = cv2.resize(frame, (840, 640))

        cv2.imshow("Screen Recording", frame)
        out.write(frame)

        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            actual_fps = frame_count / elapsed_time
            print(f"FPS: {actual_fps:.2f}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


def main():
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(RECORDING_VIDEO, fourcc, FPS, OUTPUT_SIZE)

    sct = mss.mss()

    # Record Screen
    screen_record(sct, out)
    print("Recording stopped.")
    out.release()
    print(f"Saved {RECORDING_VIDEO}")

    
if __name__ == "__main__":
    main()
