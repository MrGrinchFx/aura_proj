# aura_proj
AURA | Autonomous Unified Routing and Analysis

## Dataset Creation
### Dependencies
#### Pillow
python3 -m pip install --upgrade Pillow

#### Opencv
pip install opencv-python

In order to create a dataset with a standard mp4 video. Run the following command
```./dataset_creator.py <timestamp_start> <timestamp_end>```
where timestamp_start is an arbitrary start time, and timestamp_end is timestamp_start plus the video length in nanoseconds

## Fixing Trajectory
The trajectory txt file that ORB-SLAM3 outputs needs to be adjusted such that the timestamps are adjusted to a center of 1000000000500000000 and then converted to frames. This allows it to operate with visualize.py and plot the trajectory and doors accurately. Useage is as follows.
```./fix_trajectory.py <input.txt> <output.txt>```

## Visualize
After updating the trajectory file, it can be visualized alongside the detection file that YOLO outputs. Useage for the visualizer is as follows.
```./visualize.py <trajectory.txt> <yolo.txt>```
