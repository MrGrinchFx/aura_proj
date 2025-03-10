import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.animation import FuncAnimation

def load_trajectory(traj_file):
    """
    Loads the trajectory file where each line is in the format:
    frame, x, y, z, qx, qy, qz, qw
    Returns:
      frames: a 1D array of frame numbers (as integers)
      traj: a 2D array of camera positions (x, z) for each frame.
    """
    data = np.loadtxt(traj_file)
    frames = data[:, 0].astype(int)
    # Extract x (col1) and z (col3)
    traj = data[:, [1, 3]]
    return frames, traj

def parse_yolo_line(line):
    """
    Parses a line from the YOLO file.
    Expected format example:
    2 | [751.7017822265625, 1.6057804822921753, 840.0, 633.1400146484375] | 3 | [631.860107421875, 0.0, 704.9998168945312, 615.9223022460938] |
    Returns a list of detections; each detection is a tuple: (door_id, bbox)
    where bbox is a list of four floats: [x, y, width, height].
    """
    tokens = [token.strip() for token in line.split('|') if token.strip()]
    detections = []
    for i in range(0, len(tokens), 2):
        try:
            door_id = int(tokens[i])
        except ValueError:
            continue
        bbox_str = tokens[i+1].strip().lstrip('[').rstrip(']')
        bbox = [float(val.strip()) for val in bbox_str.split(',')]
        detections.append((door_id, bbox))
    return detections

def load_yolo_detections(yolo_file):
    """
    Loads the YOLO detection file.
    Returns a list where each element corresponds to one frame (by line number)
    and is a list of detections (door_id, bbox). If a line is empty,
    an empty list is added to maintain alignment.
    """
    detections_per_frame = []
    with open(yolo_file, 'r') as f:
        for line in f:
            if line.strip() == "":
                detections_per_frame.append([])
            else:
                detections = parse_yolo_line(line)
                detections_per_frame.append(detections)
    return detections_per_frame

def compute_heading(traj, i):
    """
    Compute the heading vector for frame i using the difference between
    consecutive frames. Returns a unit vector (dx, dz).
    """
    if i < len(traj) - 1:
        diff = traj[i+1] - traj[i]
    elif i > 0:
        diff = traj[i] - traj[i-1]
    else:
        diff = np.array([1.0, 0.0])
    norm = np.linalg.norm(diff)
    if norm == 0:
        return np.array([1.0, 0.0])
    return diff / norm

# Global dictionary to store the "best" (lowest error) door detection for each door id.
# The stored value is a tuple: (door_point, color, side, label, error)
door_points = {}
last_processed_frame = -1

def update(frame_index, frames, traj, yolo_detections, img_width, offset_distance, straight_threshold, ax):
    global door_points, last_processed_frame

    ax.clear()
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    ax.set_title('2D Camera Trajectory with Door Detections')
    ax.grid(True)
    ax.axis('equal')
    
    # Plot the trajectory up to the current frame.
    ax.plot(traj[:frame_index+1, 0], traj[:frame_index+1, 1], 'k-', label='Camera Trajectory')
    
    num_yolo = len(yolo_detections)
    center_threshold = img_width / 2.0
    
    # Process frames from last_processed_frame+1 up to current frame_index
    for idx in range(last_processed_frame+1, frame_index+1):
        cam_pos = traj[idx]
        # Use the frame number from trajectory to index YOLO detections if possible.
        frame_num = frames[idx]
        if frame_num < num_yolo:
            detections = yolo_detections[frame_num]
        else:
            detections = yolo_detections[idx]
        
        heading = compute_heading(traj, idx)
        # Compute right and left unit vectors (rotate heading by -90°)
        right_vector = np.array([heading[1], -heading[0]])
        left_vector = -right_vector
        
        for door_id, bbox in detections:
            # Compute the horizontal center of the bounding box.
            bbox_center_x = bbox[0] + bbox[2] / 2.0
            # Compute "error" as distance from the image center.
            error = abs(bbox_center_x - center_threshold)
            # Determine side and compute offset.
            if error <= straight_threshold:
                offset = heading * offset_distance
                color = 'green'
                side = 'straight'
            elif bbox_center_x < center_threshold:
                offset = left_vector * offset_distance
                color = 'blue'
                side = 'left'
            else:
                offset = right_vector * offset_distance
                color = 'red'
                side = 'right'
                
            door_point = cam_pos + offset
            label = f'Door {door_id} ({side})'
            # Update if this is the first detection or if the current detection
            # has a smaller error (i.e. is more centered) than the stored one.
            if door_id not in door_points or error < door_points[door_id][4]:
                door_points[door_id] = (door_point, color, side, label, error)
    
    last_processed_frame = frame_index
    
    # Plot all door detections (using the best instance so far for each door id).
    for dp in door_points.values():
        point, color, side, label, err = dp
        ax.plot(point[0], point[1], marker='o', color=color, markersize=5, linestyle='None', label=label)
    
    # Deduplicate legend entries.
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

def animate_trajectory(traj_file, yolo_file, img_width=1280, offset_distance=1.0, straight_threshold=30, fps=30):
    frames, traj = load_trajectory(traj_file)
    yolo_detections = load_yolo_detections(yolo_file)
    
    num_frames = traj.shape[0]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    anim = FuncAnimation(
        fig, update, frames=num_frames,
        fargs=(frames, traj, yolo_detections, img_width, offset_distance, straight_threshold, ax),
        interval=1000/fps, repeat=False)
    
    plt.show()

if __name__ == '__main__':
    # Update the filenames as needed.
    traj_filename = './trajectory2.txt'
    yolo_filename = './yolo_output.txt'
    animate_trajectory(traj_filename, yolo_filename)
