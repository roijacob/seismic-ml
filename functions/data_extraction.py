import pywt
import numpy as np
from scipy import signal
from scipy.signal import find_peaks
from scipy.stats import kurtosis, skew


def extract_date_from_file_path(file_path):
    """
    Extracts the date string from the given file path.
    """
    return file_path.split("/")[-1].split(".")[0].split("-", 1)[1]

def mad(data):
    median = np.median(data)
    return np.median(np.abs(data - median))

def analyze_seismic_data(stream):
    """
    Performs statistical analysis on a seismic data stream.

    Args:
        stream (obspy.Stream): The seismic data stream.

    Returns:
        dict: A dictionary containing the statistical analysis results.
    """
    # Select the trace of interest
    tr = stream[0]

    # Get the data as a numpy array
    data = tr.data

    # Get the date from the trace stats
    date = tr.stats.starttime.date.isoformat()

    # Get the data quality from the trace stats (if available)
    data_quality = tr.stats.mseed.dataquality if hasattr(tr.stats, 'mseed') and hasattr(tr.stats.mseed, 'dataquality') else None

    # Calculate standard deviation
    std_dev = np.std(data)

    # Calculate peak-to-peak amplitude
    peak_to_peak = np.max(data) - np.min(data)

    # Calculate root mean square (RMS)
    rms = np.sqrt(np.mean(np.square(data)))

    # Perform spectral analysis
    freq, psd = signal.welch(data, fs=tr.stats.sampling_rate)

    # Calculate total PSD
    total_psd = np.sum(psd)

    # Calculate mean PSD
    mean_psd = np.mean(psd)

    # Estimate signal-to-noise ratio (SNR)
    signal_level = np.max(data)
    noise_level = np.std(data)
    snr = signal_level / noise_level

    # Calculate median absolute deviation (MAD)
    mad_value = mad(data)

    # Calculate kurtosis
    kurtosis_value = kurtosis(data)
        
    # Calculate skewness
    skewness_value = skew(data)

    # Calculate interquartile range (IQR)
    iqr_value = np.percentile(data, 75) - np.percentile(data, 25)

    # Calculate autocorrelation peak
    autocorr = np.correlate(data, data, mode='full')
    autocorr_peaks, _ = find_peaks(autocorr)
    autocorr_peak = autocorr_peaks[0] if len(autocorr_peaks) > 0 else None

    # Calculate wavelet energy
    coeffs = pywt.wavedec(data, 'db4', level=5)
    wavelet_energy = sum(np.sum(np.square(c)) for c in coeffs)

    # Store the results in a dictionary
    results = {
        "Date": date,
        "Data Quality": data_quality,
        "Standard Deviation": round(std_dev, 4),
        "Peak-to-Peak Amplitude": round(peak_to_peak, 4),
        "Root Mean Square (RMS)": round(rms, 4),
        "Total PSD": round(total_psd, 4),
        "Mean PSD": round(mean_psd, 4),
        "Signal-to-Noise Ratio (SNR)": round(snr, 4),
        "Median Absolute Deviation (MAD)": round(mad_value, 4),
        "Kurtosis": round(kurtosis_value, 4),
        "Skewness": round(skewness_value, 4),
        "Interquartile Range (IQR)": round(iqr_value, 4),
        "Autocorrelation Peak": round(autocorr_peak, 4) if autocorr_peak is not None else None,
        "Wavelet Energy": round(wavelet_energy, 4)
    }

    return results