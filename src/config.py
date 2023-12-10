import os


root_dir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
project_dir = os.path.join(root_dir, '665A_Project')
data_dir = os.path.join(project_dir, 'data')
px4_src_dir = os.path.join(root_dir, 'PX4-Autopilot')
px4_repo_url = 'https://github.com/PX4/PX4-Autopilot.git'