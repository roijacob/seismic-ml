import os
import shutil
import pandas as pd
from obspy import read

def process_seismic_data(data_folder):
    # Get a list of all files in the folder
    file_list = os.listdir(data_folder)

    # Create an empty list to store the data
    data = []

    # Iterate over each file in the folder
    for file_name in file_list:
        # Construct the full file path
        file_path = os.path.join(data_folder, file_name)
        
        # Read the seismic data using ObsPy with format="MSEED"
        seismic_stream = read(file_path, format="MSEED")
        
        # Get the start and end times of the seismic data
        start_time = seismic_stream[0].stats.starttime
        end_time = seismic_stream[0].stats.endtime
        
        # Append the data to the list
        data.append([file_name, start_time.strftime("%Y-%m-%d"), end_time.strftime("%Y-%m-%d")])

    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=["File Name", "Start Date", "End Date"])

    # Sort the DataFrame by the "File Name" column in ascending order
    df = df.sort_values("File Name")

    # Reset the index of the DataFrame
    df = df.reset_index(drop=True)

    return df


def rename_and_save_files(data_folder, fixed_data_folder, df):
    # Rename the files based on the start date and save them in the fixed_data folder
    for index, row in df.iterrows():
        old_file_path = os.path.join(data_folder, row["File Name"])
        new_file_name = f"{row['Start Date']}.mseed"
        new_file_path = os.path.join(fixed_data_folder, new_file_name)
        
        shutil.copy(old_file_path, new_file_path)
        
        print(f"Copied and renamed: {row['File Name']} -> {new_file_name}")