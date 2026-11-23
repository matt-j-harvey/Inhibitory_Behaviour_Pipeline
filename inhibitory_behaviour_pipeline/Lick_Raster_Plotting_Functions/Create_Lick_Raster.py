import os
import numpy as np




def convert_lick_trace_to_colour(trial_data, lick_trace):
    n_timepoints = len(lick_trace)
    trial_lick_raster = np.ones((n_timepoints, 3))
    for timepoint_index in range(n_timepoints):
        if lick_trace[timepoint_index] == 1:
            trial_data[timepoint_index] = [0, 0, 0]

    return trial_data


def create_combined_psth(data_matrix, preceeding_window, following_window, fill_static=False, fill_drift=False):

    """
    A combined Matrix Must Be Made
        - Relative Drift Onset Time
        - Relative Static Onset Time
        - Relative Stop Tone Time
        - Reaction Time
        - Lick Data For Window - binary 1 above threshold, 0 below
    """

    static_colour = [57.0 / 255, 104.0 / 255, 204.0 / 255]
    drift_colour = [64.0 / 255, 148.0 / 255, 79.0 / 255]
    stop_colour = [179.0 / 255, 65.0 / 255, 59.0 / 255]
    makrer_window_size = 200

    # Get N Trials
    n_trials = np.shape(data_matrix)[0]

    # Get N Timepoints
    n_timepoints = following_window - preceeding_window

    # Create Empty PSTHs
    trial_psth = np.ones((n_trials, n_timepoints, 3))

    # Iterate Through Trials
    for trial_index in range(n_trials):

        # Unpack
        trial_drift_time = data_matrix[trial_index, 0]
        trial_static_time = data_matrix[trial_index, 1]
        trial_stop_time = data_matrix[trial_index, 2]
        trial_lick_data = data_matrix[trial_index, 4:]

        # Add Drift Colour
        if not np.isnan(trial_drift_time):
            trial_drift_time = int(trial_drift_time)
            trial_psth[trial_index, preceeding_window + trial_drift_time:trial_drift_time + makrer_window_size] = drift_colour

        # Add Static Colour
        if not np.isnan(trial_static_time):
            trial_static_time = int(trial_static_time)
            trial_psth[trial_index, preceeding_window + trial_static_time:trial_static_time + makrer_window_size] = static_colour

        # Add Stop Colour
        if not np.isnan(trial_stop_time):
            trial_stop_time = int(trial_stop_time)
            trial_psth[trial_index, preceeding_window + trial_stop_time:trial_stop_time + makrer_window_size] = stop_colour

        # Add Lick Trace
        trial_lick_data = convert_lick_trace_to_colour(trial_psth[trial_index], trial_lick_data)
        trial_psth[trial_index] = trial_lick_data


    return trial_psth

    """
        trial_type = behaviour_matrix[trial_index, 1]
        if trial_type == 1 or trial_type == 2:
            trial_psth[trial_counter, 0:50] = static_colour

            if fill_static == True:
                if not np.isnan(trial_drift_onset):
                    trial_psth[trial_counter, 0:int(trial_drift_onset)] = static_colour


        # Get Drift Onset
        #trial_drift_duration = int(trial_duration - trial_drift_onset)
        if not np.isnan(trial_drift_onset):
            trial_drift_onset = int(trial_drift_onset)
            trial_psth[trial_counter, trial_drift_onset:trial_drift_onset + 50] = drift_colour
            #trial_psth[trial_counter, trial_drift_onset + trial_drift_duration - 50:trial_drift_onset + trial_drift_duration] = [0, 0, 1]

        # Get Stop Onset
        trial_stop_onset = behaviour_matrix[trial_index, 7]
        if not np.isnan(trial_stop_onset):
            trial_stop_onset = int(trial_stop_onset)
            trial_psth[trial_counter, trial_stop_onset:trial_stop_onset + 50] = stop_colour


        if trial_type == 2:
            if fill_drift == True:
                trial_drift_onset = int(trial_drift_onset)
                trial_duration = int(trial_duration)
                trial_psth[trial_counter, trial_duration-50:trial_duration] = drift_colour

        # Get Trial Lick Data
        trial_lick_trace = behaviour_matrix[trial_index, -5000:]
        trial_lick_data = trial_lick_trace[0:following_window]
        trial_lick_colour = convert_lick_trace_to_colour(trial_lick_data, trial_psth[trial_counter])
        trial_psth[trial_counter] = trial_lick_colour
    """

