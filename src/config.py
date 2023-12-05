import os


root_dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(root_dir, 'data')
temp_dir = os.path.join(data_dir, 'temp')
px4_dir = os.path.join(temp_dir, 'PX4-Autopilot')
px4_repo_url = 'https://github.com/PX4/PX4-Autopilot.git'