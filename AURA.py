import cv2
import numpy as np
import time
import mss
import ffmpeg
import os
from DoorDetector.DoorDetector import DoorDetector

RECORDING_VIDEO = "recording.mp4"
TEMP_VIDEO = "temp.mp4"
ANNOTATION_VIDEO = "yolo_annotations.mp4"
YOLO_OUTPUT_FILE = "yolo_output.txt"
TRIM = 2
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


def get_video_duration(video_file):
    probe = ffmpeg.probe(video_file, v='error', select_streams='v:0', show_entries='format=duration')
    duration = float(probe['format']['duration'])
    
    return duration


def trim_video(input_video, output_video, trim_seconds):
    print(input_video)
    duration = get_video_duration(input_video)

    if duration <= 2 * trim_seconds:
        print("Error: Video is too short to trim.")
        return False

    # Trim first and last 3 seconds
    start_time = trim_seconds
    end_time = duration - trim_seconds

    ffmpeg.input(input_video, ss=start_time, to=end_time).output(output_video).run()

    os.replace(input_video, output_video)
    return True


def main():
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(TEMP_VIDEO, fourcc, FPS, OUTPUT_SIZE)

    sct = mss.mss()

    # Record Screen
    screen_record(sct, out)
    print("Recording stopped.")
    out.release()
    time.sleep(5)

    # Trim Video
    trim_video(TEMP_VIDEO, RECORDING_VIDEO, TRIM)
    print(f"Saved {RECORDING_VIDEO}")

    # Run Yolo on Recording
    Detector = DoorDetector()
    cap = cv2.VideoCapture(RECORDING_VIDEO)

    print("Running Yolo on Recording")
    with open(YOLO_OUTPUT_FILE, "w") as file:
        out = cv2.VideoWriter(ANNOTATION_VIDEO, fourcc, FPS, OUTPUT_SIZE)

        while cap.isOpened():

            success, frame = cap.read()

            if not success:
                print("End of video or cannot read frame.")
                break

            frame = cv2.resize(frame, (840, 640))
            
            inference = Detector.inference(frame)

            for track_id, bbox in zip(inference["track_ids"], inference["bounding_boxes"]):
                file.write(f"{track_id} | {bbox} | ")

            file.write("\n")

            out.write(inference["annotation"])
            cv2.imshow("Yolo Annotation ", inference["annotation"])

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        cv2.destroyAllWindows()
        out.release()

    print(f"Saved {ANNOTATION_VIDEO}")
    print(f"Saved {YOLO_OUTPUT_FILE}")

if __name__ == "__main__":
    main()
