import numpy as np
import os

import matplotlib.pyplot as plt




def get_ramp_start(activity, preceeding_window):
    response_window = 500
    response_start = np.abs(preceeding_window) + response_window
    post_response_activity = activity[response_start:]
    min_value = np.min(post_response_activity)
    ramp_start = np.where(post_response_activity == min_value)[0][0]
    print("ramp_start", ramp_start)
    ramp_start = np.add(ramp_start, response_start)
    print("min_value", min_value)
    print("ramp_start", ramp_start)
    plt.plot(activity)
    plt.axvline(np.abs(preceeding_window), c='k')
    plt.axvline(np.abs(preceeding_window)+1000, c='k')
    plt.axvline(len(activity)-250, c='k')
    plt.scatter([ramp_start],[min_value])
    plt.show()

    return ramp_start

def get_session_responses_and_outcomes(base_directory, preceeding_window, following_window, mean_response_window_start, mean_response_window_stop):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"), allow_pickle=True)

    # Load Neural Activity
    spike_raster = np.load(os.path.join(base_directory, "Neuropixel_Recording", "Smoothed_Raster.npy"))
    print("Spike Raster", np.shape(spike_raster))

    # Load Lick CD
    lick_cd = np.load(os.path.join(base_directory, "Neural_Analysis", "Lick_CD.npy"))
    print("lick cd", np.shape(lick_cd))

    # Get lick CD Projection
    lick_cd_projection = np.dot(spike_raster, lick_cd)
    n_timepoints = np.shape(lick_cd_projection)[0]

    lick_cd_projection = np.divide(lick_cd_projection, np.max(lick_cd_projection))

    response_list = []
    mean_window_list = []
    outcome_list = []
    rt_list = []
    # Get Delay Trials With Response

    n_trials = np.shape(behaviour_matrix)[0]
    for trial_index in range(n_trials):
        trial_data = behaviour_matrix[trial_index]
        trial_type = trial_data[1]
        trial_outcome = trial_data[6]
        trial_onset = trial_data[2]
        trial_rt = trial_data[4]

        if trial_type == 1:
            if trial_outcome == 1 or trial_outcome == 2:
                if trial_rt > 1000:
                    trial_start = int(trial_onset + preceeding_window)
                    trial_stop = int(trial_onset + trial_rt)

                    if trial_start > 0 and trial_stop < n_timepoints:


                        # Get Trial Lick Data
                        trial_lick_data = lick_cd_projection[trial_start:trial_stop]
                        trial_baseline = trial_lick_data[0:250]
                        trial_baseline = np.mean(trial_baseline)
                        trial_lick_data = np.subtract(trial_lick_data, trial_baseline)

                        # Get Ramp Rate - lowest point from 500ms after stimulus onset
                        get_ramp_start(trial_lick_data, preceeding_window)

                        trial_mean_response = np.mean(trial_lick_data[mean_response_window_start:mean_response_window_stop])

                        response_list.append(trial_lick_data)
                        mean_window_list.append(trial_mean_response)
                        outcome_list.append(trial_outcome)
                        rt_list.append(trial_rt)

    return response_list, mean_window_list, outcome_list, rt_list




def get_cohort_response_outcomes(session_list, preceeding_window, following_window, mean_response_window_start, mean_response_window_stop):
    group_response_list = []
    group_mean_window_list = []
    group_outcome_list = []
    group_rt_list = []

    for base_directory in session_list:
        response_list, mean_window_list, outcome_list, rt_list = get_session_responses_and_outcomes(base_directory, preceeding_window, following_window, mean_response_window_start, mean_response_window_stop)
        group_response_list.append(response_list)
        group_mean_window_list.append(mean_window_list)
        group_outcome_list.append(outcome_list)
        group_rt_list.append(rt_list)

    print("group_rt_list", group_rt_list)
    group_response_list = np.concatenate(group_response_list)
    group_mean_window_list = np.concatenate(group_mean_window_list)
    group_outcome_list = np.concatenate(group_outcome_list)
    group_rt_list = np.concatenate(group_rt_list)
    print("group_rt_list", group_rt_list)

    scatter_outcomes(group_mean_window_list, group_outcome_list, group_rt_list)
    scatter_outcomes_bin_rt_bin(group_response_list, group_mean_window_list, group_outcome_list, group_rt_list)
    plot_traces(group_response_list, group_mean_window_list, group_outcome_list, group_rt_list, preceeding_window, following_window)


session_list = [
    r"C:\Users\matth\Dropbox\Behaviour_Data\Cohort 3\BRAC_11766_1E_Purple\2026_02_09",
    r"C:\Users\matth\Dropbox\Behaviour_Data\Cohort 3\BRAC_11766_1E_Purple\2026_02_10",
    r"C:\Users\matth\Dropbox\Behaviour_Data\Cohort 3\BRAC_11766_1E_Purple\2026_03_27",
    r"C:\Users\matth\Dropbox\Behaviour_Data\Cohort 3\BRAC_11766_1E_Purple\2026_03_31",
    r"C:\Users\matth\Dropbox\Behaviour_Data\Cohort 3\BRAC_11766_1E_Purple\2026_04_01",
]

preceeding_window = -2800
following_window = 500
mean_response_window_start = np.abs(preceeding_window)
mean_response_window_stop = mean_response_window_start + 500

get_cohort_response_outcomes(session_list, preceeding_window, following_window, mean_response_window_start, mean_response_window_stop)
