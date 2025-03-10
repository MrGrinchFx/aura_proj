import sys

def adjust_and_convert_to_frames(input_file, output_file):
    # Read all lines from the input file.
    with open(input_file, 'r') as f:
        lines = f.readlines()

    if not lines:
        print("Error: Input file is empty.")
        return

    # Use the first value of the first line to calculate the adjustment.
    first_line = lines[0].strip()
    parts = first_line.split()
    try:
        original_first_val = float(parts[0])
    except ValueError:
        print("Error: The first value in the file is not a valid float.")
        return

    # Set the target starting timestamp.
    target = 1000000000500000000.0
    # Compute the difference to subtract from every timestamp.
    diff = original_first_val - target

    # Calculate frame interval in nanoseconds for 30 fps.
    frame_interval_ns = 1e9 / 30

    with open(output_file, 'w') as out_f:
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip empty lines.
            parts = line.split()
            try:
                current_ts = float(parts[0])
            except ValueError:
                print(f"Warning: Skipping line with invalid number: {line}")
                continue

            # Adjust the timestamp so that the first timestamp becomes target.
            adjusted_ts = current_ts - diff
            # Compute the frame number based on the adjusted timestamp.
            # Frame 0 corresponds to the target timestamp.
            frame_number = int(round((adjusted_ts - target) / frame_interval_ns))
            # Reconstruct the line with the frame number replacing the timestamp.
            rest_of_line = " ".join(parts[1:])
            out_f.write(f"{frame_number} {rest_of_line}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python adjust_and_convert.py input.txt output.txt")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        adjust_and_convert_to_frames(input_file, output_file)