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
