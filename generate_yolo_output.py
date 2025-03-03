import cv2
from DoorDetector.DoorDetector import DoorDetector


VIDEO = "recording.mp4"
ANNOTATION_VIDEO = "recording_annotations.mp4"
YOLO_OUTPUT_FILE = "yolo_output.txt"
OUTPUT_SIZE = (840, 640)
FPS = 30.0

Detector = DoorDetector()
cap = cv2.VideoCapture(VIDEO)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

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