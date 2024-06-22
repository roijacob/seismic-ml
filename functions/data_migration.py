import os
import shutil

# Define the paths
project_dir = '.'
fixed_data_dir = os.path.join(project_dir, 'fixed_data')
data_dir = os.path.join(project_dir, 'data')

# Create the data directory if it doesn't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Get the contents of week-1 and week-2 directories
week1_dir = os.path.join(fixed_data_dir, 'week_1')
week2_dir = os.path.join(fixed_data_dir, 'week_2')

# Iterate over the files in week-1 and week-2 and move them to the data folder with the prefix "ehz-"
for week_dir in [week1_dir, week2_dir]:
    for file_name in os.listdir(week_dir):
        file_path = os.path.join(week_dir, file_name)
        new_file_name = "ehz-" + file_name
        destination_path = os.path.join(data_dir, new_file_name)
        shutil.move(file_path, destination_path)

# Delete the fixed_data directory
shutil.rmtree(fixed_data_dir)