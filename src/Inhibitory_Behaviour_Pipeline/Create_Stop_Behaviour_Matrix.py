import numpy as np
import os
from tqdm import tqdm

from Inhibitory_Behaviour_Pipeline.Behaviour_Analysis_Utils import Behaviour_Analysis_Utils



def split_trials_by_type(trial_start_list, trial_end_list, static_channel, stop_channel):

    trial_type_list = []


    n_trials = len(trial_start_list)
    for trial_index in range(n_trials):
        trial_start = trial_start_list[trial_index]
        trial_end = trial_end_list[trial_index]

        # If no static during Trial  - Is a Go trial
        if np.max(static_channel[trial_start:trial_end]) < 1:
            trial_type = 0

        # if No stop during trial - it's a wait trial
        else:

            if np.max(stop_channel[trial_start:trial_end]) < 1:
                trial_type = 1

            else:
                trial_type = 2

        trial_type_list.append(trial_type)

    trial_type_list = np.array(trial_type_list)
    return trial_type_list


def check_trial_has_matched_end(trial_start_time, next_trial_start_time, trial_end_times):

    valid_trial = False
    for trial_end in trial_end_times:

        if trial_end >= trial_start_time and trial_end < next_trial_start_time:

            valid_trial = True
            return valid_trial, trial_end

    return valid_trial, None



def get_valid_trials(start_times, end_times, n_timepoints):

    valid_trial_start_times = []
    valid_trial_end_times = []
    invalid_trial_onsets = []

    n_trial_onsets = len(start_times)
    for onset_index in tqdm(range(n_trial_onsets-1)):

        # Get Current and next Onset
        current_trial_onset = start_times[onset_index]
        next_trial_onset = start_times[onset_index + 1]

        # There must be an end inbetween these times
        trial_valid, trial_end = check_trial_has_matched_end(current_trial_onset, next_trial_onset, end_times)

        if trial_valid == True:
            valid_trial_start_times.append(current_trial_onset)
            valid_trial_end_times.append(trial_end)

        else:
            invalid_trial_onsets.append(current_trial_onset)


    # check Last Trial
    if start_times[-1] > end_times[-1]:
        valid_trial_start_times.append(start_times[-1])
        valid_trial_end_times.append(end_times[-1])
    else:
        invalid_trial_onsets.append(start_times[-1])

    valid_trial_start_times = np.array(valid_trial_start_times)
    valid_trial_end_times = np.array(valid_trial_end_times)
    invalid_trial_onsets = np.array(invalid_trial_onsets)
    return valid_trial_start_times, valid_trial_end_times, invalid_trial_onsets



def get_trial_reaction_time(lick_trace, lick_threshold):
    count = 0
    for timepoint in lick_trace:
        if timepoint >= lick_threshold:
            return count
        else:
            count += 1


def get_reaction_times(trial_start_times, trial_stop_times, lick_trace, lick_threshold):

    reaction_times = []
    n_trials = len(trial_start_times)
    for trial_index in range(n_trials):
        trial_start = trial_start_times[trial_index]
        trial_stop = trial_stop_times[trial_index]
        trial_lick_data = lick_trace[trial_start:trial_stop]

        trial_reaction_time = get_trial_reaction_time(trial_lick_data, lick_threshold)
        reaction_times.append(trial_reaction_time)

    return reaction_times


def get_drift_times(trial_start_list, trial_stop_list, drift_onset_list):

    # Create Empty List To Hold Data
    trial_drift_times = []

    # Iterate Through Each Trial
    n_trials = len(trial_start_list)
    for trial_index in range(n_trials):
        trial_start = trial_start_list[trial_index]
        trial_end = trial_stop_list[trial_index]

        # Get Trial Drift Time
        trial_drift_time = None
        for drift_onset in drift_onset_list:
            if drift_onset >= trial_start and drift_onset <= trial_end:
                trial_drift_time = drift_onset - trial_start

        # Add To list
        trial_drift_times.append(trial_drift_time)

    return trial_drift_times


def get_stop_times(trial_start_list, trial_stop_list, stop_onset_list):

    # Create Empty List To Hold Data
    trial_stop_times = []

    # Iterate Through Each Trial
    n_trials = len(trial_start_list)
    for trial_index in range(n_trials):
        trial_start = trial_start_list[trial_index]
        trial_end = trial_stop_list[trial_index]

        # Get Trial Drift Time
        trial_stop_time = None
        for stop_onset in stop_onset_list:
            if stop_onset >= trial_start and stop_onset <= trial_end:
                trial_stop_time = stop_onset - trial_start

        # Add To list
        trial_stop_times.append(trial_stop_time)

    return trial_stop_times




def get_trial_outcomes(trial_start_list, trial_type_list, reaction_time_list, drift_times_list, reaction_window=3000):

    """
    Outcomes
    0 - Miss
    1 - Correct
    2 - False Alarm
    """

    trial_outcome_list = []

    n_trials = len(trial_start_list)
    for trial_index in range(n_trials):

        trial_type = trial_type_list[trial_index]
        trial_reaction_time = reaction_time_list[trial_index]
        trial_drift_time = drift_times_list[trial_index]

        # If It's A Go Trial - Check Lick Within Response Window
        if trial_type == 0:
            if trial_reaction_time == None:
                trial_outcome_list.append(0)

            elif trial_reaction_time < reaction_window:
                trial_outcome_list.append(1)

            else:
                trial_outcome_list.append(0)


        # If It's a Delay Trial - Check Lick After Drift and Within Response Window
        elif trial_type == 1:

            # Licked and Drift Never Appeared
            if trial_drift_time == None:
                trial_outcome_list.append(2)

            elif trial_reaction_time == None:
                trial_outcome_list.append(0)

            elif trial_reaction_time < trial_drift_time + reaction_window:
                trial_outcome_list.append(1)

            else:
                trial_outcome_list.append(0)

    # If It's a Stop Trial - Check No Lick
        elif trial_type == 2:
            if trial_reaction_time == None:
                trial_outcome_list.append(1)
            else:
                trial_outcome_list.append(2)

    return trial_outcome_list



def save_behaviour_matrix_as_csv(base_directory, behaviour_matrix):

    header = [
    "0 Trial Number,"
    "1 Trial Type,"
    "2 Trial Start,"
    "3 Trial End,"
    "4 Reaction Time,"
    "5 Drift Time,"
    "6 Trial Outcome,"
    "7 Stop Time,"
    ]
    header = " ".join(header)

    np.savetxt(os.path.join(base_directory, "Behaviour_Matrix.csv"), behaviour_matrix, delimiter=",", fmt="%s", header=header, comments="",  newline='\n')




def create_behaviour_matrix(base_directory):

    """
    0 - Trial Number
    1 - Trial Type
    2 - Trial Start
    3 - Trial End
    4 - Reaction Times
    5 - Drift Times
    6 - Trial Outcomes
    7 - Stop Times
    """

    # Load Lick Threshold
    lick_threshold = np.load(os.path.join(base_directory, "Lick_Threshold.npy"))

    # Load DAQ Data
    ai_data = Behaviour_Analysis_Utils.load_ai_recorder_data(base_directory)
    n_channels, n_timnepoints = np.shape(ai_data)

    # Create DAQ Channel Dict
    channel_dict = Behaviour_Analysis_Utils.create_daq_channel_dict()

    # Unpack DAQ Traces
    trial_start_trace = ai_data[channel_dict["Trial_Start"]]
    trial_end_trace = ai_data[channel_dict["Trial_End"]]
    static_trace = ai_data[channel_dict["Static_Onset"]]
    drift_trace = ai_data[channel_dict["Drift_Onset"]]
    lick_trace = ai_data[channel_dict["Lick"]]
    reward_trace = ai_data[channel_dict["Reward"]]
    stop_trace = ai_data[channel_dict["Stop_Tone"]]

    # Get Step Onsets
    trial_start_times = Behaviour_Analysis_Utils.get_step_onsets(trial_start_trace)
    trial_end_times = Behaviour_Analysis_Utils.get_step_onsets(trial_end_trace)

    # Get Valid Trials
    valid_trial_start_times, valid_trial_end_times, invalid_trial_onsets = get_valid_trials(trial_start_times, trial_end_times, n_timnepoints)

    # Split Trials By Trial Type
    trial_type_list = split_trials_by_type(valid_trial_start_times, valid_trial_end_times, static_trace, stop_trace)

    # Get Reaction Times
    reaction_times = get_reaction_times(valid_trial_start_times, valid_trial_end_times, lick_trace, lick_threshold)

    # Get Trial Drift Times
    drift_onsets = Behaviour_Analysis_Utils.get_step_onsets(drift_trace)
    trial_drift_times = get_drift_times(valid_trial_start_times, valid_trial_end_times, drift_onsets)

    # Get Trial Stop Times
    stop_onsets = Behaviour_Analysis_Utils.get_step_onsets(stop_trace)
    trial_stop_times = get_stop_times(valid_trial_start_times, valid_trial_end_times, stop_onsets)

    # Get Trial Outcomes
    trial_outcomes = get_trial_outcomes(valid_trial_start_times, trial_type_list, reaction_times, trial_drift_times, reaction_window=3000)

    # Create Behaviour Matrix
    n_trials = len(valid_trial_start_times)
    behaviour_matrix = np.zeros((n_trials, 8))

    # Add Trial Numbers
    trial_numbers = list(range(n_trials))
    behaviour_matrix[:, 0] = trial_numbers

    # Add Trial Types
    behaviour_matrix[:, 1] = trial_type_list

    # Add Trial Starts and Stops
    behaviour_matrix[:, 2] = valid_trial_start_times
    behaviour_matrix[:, 3] = valid_trial_end_times

    # Add Reaction Times
    behaviour_matrix[:, 4] = reaction_times

    # Add Drift Times
    behaviour_matrix[:, 5] = trial_drift_times

    # Add Trial Outcomes
    behaviour_matrix[:, 6] = trial_outcomes

    # Add Stop Times
    behaviour_matrix[:, 7] = trial_stop_times

    # Save Behaviour Matrix
    np.save(os.path.join(base_directory, "Behaviour_Matrix.npy"), behaviour_matrix)

    # Save Behaviour Matrix as CSV
    save_behaviour_matrix_as_csv(base_directory, behaviour_matrix)


