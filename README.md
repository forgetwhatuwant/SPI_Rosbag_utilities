# SPI Rosbag Utilities

This repository contains utilities for processing ROS bag files.

## `extract_rosbag.py`

This script extracts continuous time segments from a ROS bag file based on a boolean status topic.

### Functionality

1.  Reads the input ROS bag file.
2.  Listens to the `/upi/status/is_action` topic to identify time intervals where the message data is `true`.
3.  For each continuous `true` interval found, it creates a new output bag file containing all messages from all topics within that time interval.

### Usage

```bash
python extract_rosbag.py <path_to_input_bag_file>
```

Replace `<path_to_input_bag_file>` with the actual path to your ROS bag file.

The script will output new bag files named `<original_base_name>_segment_<n>.bag` in the same directory where the script is run, where `<n>` is the segment number (starting from 1). It will also print the number of segments found to the console. 