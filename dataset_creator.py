import os
import sys
import cv2
import math
from PIL import Image
import csv
import shutil

currentPath = str(os.path.dirname(os.path.abspath(__file__)))
extractionPath = currentPath + r"\result"

if len(sys.argv) != 4:
  print("Please launch the script as following:")
  print("python3 dataset_creator.py <<video name>> <<first timestamp>> <<last timestamp>>")
  sys.exit()

try:
    videoName = sys.argv[1]
    firstTimestamp = int(sys.argv[2])
    lastTimestamp = int(sys.argv[3])
except:
    print("Timestamps must be numbers!")

if os.path.exists(currentPath+r"\results") == False:
  os.mkdir(currentPath+r"\results")
if os.path.exists(currentPath+r"\resized_results") == False:
    os.mkdir(currentPath+r"\resized_results")
if os.path.exists(currentPath+r"\Custom\mav0\cam0\data") == False:
    os.makedirs(currentPath+r"\Custom\mav0\cam0\data")

print("Created directories: results, resized_results, Custom/mav0/cam0/data")

vidcap = cv2.VideoCapture(videoName)
success,image = vidcap.read()
count = 0

while success:
  cv2.imwrite("results\\%d.png" % count, image)     # save frame as JPEG file
  success, image = vidcap.read()
  count += 1

print("Video splitted into frames! Results are stored in \"results\" folder.")

for i in range(count):
    image = Image.open("results\\"+str(i)+".png")
    new_image = image.resize((752,480))
    new_image.save("resized_results\\" + str(i) + ".png")

print("Images are resized into 752x480! Results are stored in \"resized_results\" folder.")

increaseRate = math.floor((lastTimestamp - firstTimestamp) / count)

for i in range(count):
    image = cv2.imread("resized_results\\" + str(i) + ".png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("Custom\\mav0\\cam0\\data\\" + str(i*increaseRate + firstTimestamp) + ".png", gray)

print("Images are grayscaled and renamed! Results are stored in \"Custom/mav0/cam0/data\" folder.")

with open("./Custom/mav0/cam0/data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["#timestamp [ns]", "filename"])
    for i in range(count):
        writer.writerow([str(i*increaseRate + firstTimestamp), str(i*increaseRate + firstTimestamp)+".png"])

def list_timestamp(folder_path, output_file):
    # Get all PNG files in the folder
    png_files = [os.path.splitext(f)[0] for f in os.listdir(folder_path) if f.endswith('.png')]
    
    # Write filenames to the output file
    with open(output_file, 'w') as f:
        for file in png_files:
            f.write(file + '\n')

# Example usage
folder_path = './Custom/mav0/cam0/data'  # Change this to your folder path
os.makedirs("./Custom/TimeStamps", exist_ok=True)
output_file = './Custom/TimeStamps/Custom.txt'       # Output file name
list_timestamp(folder_path, output_file)

# Remove the results and resized_results directories after processing
shutil.rmtree(currentPath + r"\results", ignore_errors=True)
shutil.rmtree(currentPath + r"\resized_results", ignore_errors=True)

print("Temporary directories \"results\" and \"resized_results\" deleted.")