import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from inhibitory_behaviour_pipeline.Behaviour_Analysis_Utils import Behaviour_Analysis_Functions, Behaviour_Analysis_Utils


def binarise_lick_trace(lick_trace, lick_threshold):
    n_timepoints = len(lick_trace)
    trial_lick_raster = np.zeros((n_timepoints))
    for timepoint_index in range(n_timepoints):
        if lick_trace[timepoint_index] > lick_threshold:
            trial_lick_raster[timepoint_index] = 1

    return trial_lick_raster


def get_lick_raster_data(behaviour_matrix, selected_trial_indicies, preceeding_window, following_window, lick_trace, lick_threshold):

    """
    A combined Matrix Must Be Made
        - Relative Drift Onset Time
        - Relative Static Onset Time
        - Relative Stop Tone Time
        - Reaction Time
        - Lick Data For Window - binary 1 above threshold, 0 below
    """

    trial_length = following_window - preceeding_window
    n_timepoints = len(lick_trace)

    data_matrix = []

    for trial_index in selected_trial_indicies:

        # Extract Trial Data From Behaviour Matrix
        trial_data = behaviour_matrix[trial_index]

        # Create Vector For Trial Data
        trial_vector = np.zeros(trial_length + 4)

        trial_type = trial_data[1]

        # Get Drift Onset
        drift_onset = trial_data[5]
        if trial_type == 0:
            drift_onset = 0

        # Get Static Onset
        if trial_type == 1 or trial_type == 2:
            static_onset = 0
        else:
            static_onset = np.nan

        # Get Reaction Time
        reaction_time = trial_data[4]

        # Get Stop Time
        stop_time = trial_data[7]

        # Get Trial Lick Data
        trial_start = int(trial_data[2])
        lick_window_start = trial_start + preceeding_window
        lick_window_stop = trial_start + following_window

        if lick_window_start > 0 and lick_window_stop < n_timepoints:

            trial_lick_data = lick_trace[lick_window_start:lick_window_stop]
            trial_lick_data = binarise_lick_trace(trial_lick_data, lick_threshold)

            trial_vector[0] = drift_onset
            trial_vector[1] = static_onset
            trial_vector[2] = stop_time
            trial_vector[3] = reaction_time
            trial_vector[4:] = trial_lick_data
            data_matrix.append(trial_vector)

    data_matrix = np.array(data_matrix)
    return data_matrix


