import numpy as np
import pandas as pd

from obspy import read, UTCDateTime
from obspy.clients.fdsn import Client
from scipy.signal import savgol_filter
from obspy.signal.filter import bandpass


def process_data(date, time, window_size, file_path):
    """
    Reads and trims the data based on the specified time window.

    Args:
        date (str): The date in the format 'YYYY-MM-DD'.
        time (str): The time in the format 'HH:MM:SS'.
        window_size (int): The size of the time window in seconds.
        file_path (str): The path to the data file.

    Returns:
        obspy.Stream: The trimmed data stream.
    """

    # Combine the date and time into a single string
    datetime_str = f"{date}T{time}"

    # Create a UTCDateTime object for the specific time
    specific_time = UTCDateTime(datetime_str)

    # Calculate the start and end times based on the window size
    start_time = specific_time - window_size
    end_time = specific_time + window_size

    # Read and trim the data file
    stream = read(file_path).trim(start_time, end_time)

    return stream


def remove_stream_response(stream, station):
    """
    Removes the instrument response from the given data stream for the specified station.

    Args:
        stream (obspy.Stream): The data stream.
        station (str): The station code.

    Returns:
        obspy.Stream: The data stream with the instrument response removed.
    """
    # Get the station inventory
    inv = Client('RASPISHAKE').get_stations(network='AM', station=station, level='RESP')

    # Attach the response to the stream
    stream.attach_response(inv)

    # Remove the instrument response
    resp_removed = stream.remove_response(output='ACC')

    return resp_removed


def save_to_csv(resp_removed, csv_file_name):
    """
    Saves the acceleration data and time component from the first trace of the resp_removed stream to a CSV file.

    Args:
        resp_removed (obspy.Stream): The data stream with the instrument response removed.
        csv_file_name (str): The name of the CSV file to save the data to.
    """
    # Extract the acceleration data from the first trace of the resp_removed stream
    data = resp_removed[0].data

    # Get the sampling rate of the trace
    sampling_rate = resp_removed[0].stats.sampling_rate

    # Generate the time array based on the sampling rate
    time_array = [i / sampling_rate for i in range(len(data))]

    # Create a DataFrame with the time and data columns
    df = pd.DataFrame({"Time": time_array, "Acceleration": data})

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_name, index=False)


def bandpass_filter(stream, lowcut, highcut, order):
    """
    Apply a Butterworth bandpass filter (4th order) to each trace in the stream.

    Parameters:
    - stream: The input stream containing the traces to be filtered.
    - lowcut: The low-cut frequency (Hz) of the bandpass filter.
    - highcut: The high-cut frequency (Hz) of the bandpass filter.
    - order: The order of the Butterworth filter.

    Returns:
    - The filtered stream.
    """
    # Create a copy of the input stream to avoid modifying the original
    filtered_stream = stream.copy()

    # Iterate over each trace in the stream
    for trace in filtered_stream:
        # Remove the mean
        trace.detrend(type='demean')
        
        # Apply the Butterworth bandpass filter
        trace.data = bandpass(trace.data, lowcut, highcut, trace.stats.sampling_rate, corners=order, zerophase=True)
    
    return filtered_stream


def savitzky_golay_filter(stream, window_length=11, polyorder=4):
    """
    Apply a Savitzky-Golay filter to each trace in the stream.

    Parameters:
    - stream: The input stream containing the traces to be filtered.
    - window_length: The window length for the Savitzky-Golay filter (default: 11, must be odd).
    - polyorder: The polynomial order for the Savitzky-Golay filter (default: 4).

    Returns:
    - The filtered stream.
    """
    # Create a copy of the input stream to avoid modifying the original
    filtered_stream = stream.copy()

    # Iterate over each trace in the stream
    for trace in filtered_stream:
        # Apply the Savitzky-Golay filter
        trace.data = savgol_filter(trace.data, window_length, polyorder)

    return filtered_stream