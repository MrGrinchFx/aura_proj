import cv2
from ultralytics import YOLO

WEIGHTS_PATH = "best.pt"

VIDEO_SOURCE = "kemper.mp4"

def main():
  model = YOLO(WEIGHTS_PATH)
  video_path = VIDEO_SOURCE
  cap = cv2.VideoCapture(video_path)

  while cap.isOpened():
      success, frame = cap.read()

      if success:
          frame = cv2.resize(frame, (840, 640))

          results = model.track(frame, conf=0.50, persist = True, verbose=False)

          if results[0].boxes.id is not None:
              track_ids = results[0].boxes.id.int().cpu().tolist()
              print(track_ids)

          # Visualize the results on the frame
          annotated_frame = results[0].plot()

          # Display the annotated frame
          cv2.imshow("YOLO Inference", annotated_frame)

          # Break the loop if 'q' is pressed
          if cv2.waitKey(1) & 0xFF == ord("q"):
              break
      else:
          break

  cap.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
   main()