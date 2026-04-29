import os
import tables
import numpy as np
from tqdm import tqdm

import matplotlib.pyplot as plt
from bisect import bisect_left


def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before


def create_daq_channel_dict():

    channel_dict = {

    # Daq 1 Channels
    "Reward":0,
    "Static_Onset":1,
    "Trial_End":2,
    "Lick":3,
    "Trial_Start":4,
    "Drift_Onset":5,
    "Stop_Tone":6,
    "Running":7,

    # Daq 2 Channels
    "Trial_End_DAQ_2": 2+7,
    "Microphone": 3+7,
    "Trial_Start_DAQ_2": 4+7,
    "Camera": 5+7,

    }

    return channel_dict



def create_daq_1_dict():
    channel_dict = {
        "Reward": 0,
        "Static_Onset": 1,
        "Trial_End": 2,
        "Lick": 3,
        "Trial_Start": 4,
        "Drift_Onset": 5,
        "Stop_Tone": 6,
        "Running": 7,
    }

    return channel_dict

def create_daq_2_dict():

    channel_dict = {
        "Trial_End":2,
        "Microphone":3,
        "Trial_Start":4,
        "Camera":5,
        }

    return channel_dict


def get_ai_filename(base_directory):

    #Get List of all files
    file_list = os.listdir(base_directory)
    ai_filename = None

    #Get .h5 files
    h5_file_list = []
    for file in file_list:

        if file[-3:] == ".h5":
            h5_file_list.append(file)

    #File the H5 file which is two dates seperated by a dash
    for h5_file in h5_file_list:
        original_filename = h5_file

        # Remove DAQ Numbering
        h5_file = h5_file.replace("_daq_1", "")

        #Remove Ending
        h5_file = h5_file[0:-3]

        #Split By Dashes
        h5_file = h5_file.split("-")

        if len(h5_file) == 2 and h5_file[0].isnumeric() and h5_file[1].isnumeric():
            return original_filename


def get_daq_1_filename(base_directory):
    file_list = os.listdir(base_directory)
    for file_name in file_list:
        if "daq_1" in file_name:
            return file_name

def get_daq_2_filename(base_directory):
    file_list = os.listdir(base_directory)
    for file_name in file_list:
        if "daq_2" in file_name:
            return file_name



def align_traces(trace_1, trace_2, window_size=1000):

    increment_list = []
    coef_list = []
    for increment in tqdm(list(range(-window_size, window_size))):
        shifted_trace_2 = np.roll(trace_2, increment)
        correlation = np.corrcoef(trace_1, shifted_trace_2)[0, 1]

        increment_list.append(increment)
        coef_list.append(correlation)

    max_correlation = np.max(coef_list)
    best_shift = increment_list[coef_list.index(max_correlation)]

    aligned_trace_2 = np.roll(trace_2, best_shift)
    print("Best shift", best_shift)

    return aligned_trace_2



def clip_daq_data(daq_1_data, daq_2_data):
    daq_1_timepoints = np.shape(daq_1_data)[1]
    daq_2_timepoints = np.shape(daq_2_data)[1]
    print("daq_1_timepoints", daq_1_timepoints, "daq_2_timepoints", daq_2_timepoints)
    min_timepoints = np.min([daq_1_timepoints, daq_2_timepoints])
    daq_1_data = daq_1_data[:, 0:min_timepoints]
    daq_2_data = daq_2_data[:, 0:min_timepoints]
    return daq_1_data, daq_2_data




def create_combined_daq(base_directory):

    # Get Filenames
    daq_1_name = get_daq_1_filename(base_directory)
    daq_2_name = get_daq_2_filename(base_directory)

    # Load Data
    daq_1_data = load_ai_data(os.path.join(base_directory, daq_1_name))
    daq_2_data = load_ai_data(os.path.join(base_directory, daq_2_name))

    # Clip Data
    daq_1_data, daq_2_data = clip_daq_data(daq_1_data, daq_2_data)

    # Load Channel Dicts
    daq_1_channel_dict = create_daq_1_dict()
    daq_2_channel_dict = create_daq_2_dict()

    # Align Data
    daq_1_trial_starts = daq_1_data[daq_1_channel_dict["Trial_Start"]]
    daq_2_trial_starts = daq_2_data[daq_2_channel_dict["Trial_Start"]]

    aligned_daq_2_starts = align_traces(daq_1_trial_starts, daq_2_trial_starts)



    plt.plot(daq_1_trial_starts, alpha=0.4)
    plt.plot(daq_2_trial_starts, alpha=0.4)
    plt.plot(aligned_daq_2_starts, alpha=0.4, c='g')
    plt.show()



def load_ai_data(ai_recorder_file_location):

    table = tables.open_file(ai_recorder_file_location, mode='r')
    data = table.root.Data

    number_of_seconds = np.shape(data)[0]
    number_of_channels = np.shape(data)[1]
    sampling_rate = np.shape(data)[2]


    data_matrix = np.zeros((number_of_channels, number_of_seconds * sampling_rate))

    for second in range(number_of_seconds):
        data_window = data[second]
        start_point = second * sampling_rate

        for channel in range(number_of_channels):
            data_matrix[channel, start_point:start_point + sampling_rate] = data_window[channel]

    data_matrix = np.clip(data_matrix, a_min=0, a_max=None)
    table.close()

    return data_matrix


def load_ai_recorder_data(base_directory):
    ai_filename = get_ai_filename(base_directory)
    ai_recorder_file_location = os.path.join(base_directory, ai_filename)
    data_matrix = load_ai_data(ai_recorder_file_location)
    return data_matrix


def load_lick_trace(base_directory):

    # Load DAQ Data
    ai_data = load_ai_recorder_data(base_directory)

    # Create DAQ Channel Dict
    channel_dict = create_daq_channel_dict()

    # Unpack DAQ Traces
    lick_trace = ai_data[channel_dict["Lick"]]

    return lick_trace


def get_step_onsets(trace, threshold=1, window=10):
    state = 0
    number_of_timepoints = len(trace)
    onset_times = []
    time_below_threshold = 0

    onset_line = []

    for timepoint in range(number_of_timepoints):
        if state == 0:
            if trace[timepoint] > threshold:
                state = 1
                onset_times.append(timepoint)
                time_below_threshold = 0
            else:
                pass
        elif state == 1:
            if trace[timepoint] > threshold:
                time_below_threshold = 0
            else:
                time_below_threshold += 1
                if time_below_threshold > window:
                    state = 0
                    time_below_threshold = 0
        onset_line.append(state)

    return onset_times


def load_performance_d_prime(base_directory):
    # Create Lists To Hold Scores
    score_list = []
    score_types = []
    x_values = []

    # Get Filepaths
    drift_d_prime_filepath = os.path.join(base_directory, "Behaviour_Analysis", "static_drift_d_prime.npy")
    tone_d_prime_filepath = os.path.join(base_directory, "Behaviour_Analysis", "tone_d_prime.npy")

    if os.path.isfile(drift_d_prime_filepath):
        drift_d_prime = np.load(drift_d_prime_filepath)
        print("drift_d_prime", drift_d_prime)
        score_list.append(drift_d_prime)
        score_types.append("Drift d'")
        x_values.append(1)

    if os.path.isfile(tone_d_prime_filepath):
        tone_d_prime = np.load(tone_d_prime_filepath)
        score_list.append(tone_d_prime)
        score_types.append("Tone d'")
        x_values.append(2)

    return score_list, score_types, x_values



def load_performance(base_directory):

    # Create Lists To Hold Scores
    score_list = []
    score_types = []
    x_values = []

    # Get Filepaths
    go_performance_filepath = os.path.join(base_directory, "Behaviour_Analysis", "go_trial_hit_percentage.npy")
    delay_performance_filepath = os.path.join(base_directory, "Behaviour_Analysis", "delay_trial_hit_percentage.npy")
    stop_performance_filepath = os.path.join(base_directory, "Behaviour_Analysis", "stop_trial_correct_reject_percentage.npy")

    if os.path.isfile(go_performance_filepath):
        go_performance = np.load(go_performance_filepath)
        go_performance = go_performance * 100
        score_list.append(go_performance)
        score_types.append("Go Trials")
        x_values.append(1)

    if os.path.isfile(delay_performance_filepath):
        delay_performance = np.load(delay_performance_filepath)
        delay_performance = delay_performance * 100
        score_list.append(delay_performance)
        score_types.append("Delay Trials")
        x_values.append(2)

    if os.path.isfile(stop_performance_filepath):
        stop_performance = np.load(stop_performance_filepath)
        stop_performance = stop_performance * 100
        score_list.append(stop_performance)
        score_types.append("Stop Trials")
        x_values.append(3)

    return score_list, score_types, x_values




def create_behaviour_matrix_with_lick_data(base_directory, preceeding_window, following_window):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Create Lick Matrix
    duration = following_window - preceeding_window
    n_trials = np.shape(behaviour_matrix)[0]
    lick_matrix = np.empty((n_trials, duration))
    lick_matrix[:] = np.nan

    # Load AI Recorder File
    ai_matrix = load_ai_recorder_data(base_directory)

    # Get Lick Trace
    channel_dict = create_daq_channel_dict()
    lick_trace = ai_matrix[channel_dict["Lick"]]

    n_timepoints = len(lick_trace)
    for trial_index in range(n_trials):
        trial = behaviour_matrix[trial_index]
        trial_start = int(trial[2])

        if trial_start + duration >= n_timepoints:
            trial_stop = n_timepoints
        else:
            trial_stop = trial_start + duration

        trial_lick_data = lick_trace[trial_start:trial_stop]
        lick_matrix[trial_index, 0:len(trial_lick_data)] = trial_lick_data

    combined_matrix = np.hstack([behaviour_matrix, lick_matrix])
    print("Behaviour_Matrix", np.shape(behaviour_matrix))
    print("Lick_Matrix", np.shape(lick_matrix))
    print("combined_matrix", np.shape(combined_matrix))

    return combined_matrix