import numpy as np
import os

import matplotlib.pyplot as plt


def scatter_outcomes(mean_response_list, outcome_list, rt_list):
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1, 1, 1)

    min_rt = np.min(rt_list)
    print("min rt", min_rt)

    rt_list = np.subtract(rt_list, min_rt)
    max_rt = np.percentile(rt_list, q=99)
    print("max rt", np.max(rt_list))
    for rt in rt_list:
        print(rt)
    rt_list = np.divide(rt_list, max_rt)
    rt_list = np.clip(rt_list, a_min=0, a_max=1)

    colourmap = plt.cm.get_cmap("plasma")

    n_trials = len(mean_response_list)
    for trial_index in range(n_trials):

        trial_response = mean_response_list[trial_index]
        trial_outcome = outcome_list[trial_index]
        if trial_outcome == 1:
            colour = 'g'
            x_value = np.random.uniform(low=-0.1, high=0.1, size=1)
        elif trial_outcome == 2:
            colour = colourmap(rt_list[trial_index])
            x_value = np.random.uniform(low=0.9, high=1.1, size=1)
        plt.scatter(x_value, [trial_response], c=colour, alpha=0.5)
    plt.show()



def get_window_responses_in_rt_bin(response_list, mean_response_list, outcome_list, rt_list, window_start, window_stop):

    window_responses = []
    window_means = []

    n_trials = len(outcome_list)
    for trial_index in range(n_trials):
        trial_outcome = outcome_list[trial_index]
        trial_rt = rt_list[trial_index]
        trial_mean_response = mean_response_list[trial_index]
        trial_response = response_list[trial_index]

        if trial_outcome == 2:
            if trial_rt >= window_start and trial_rt < window_stop:
                window_responses.append(trial_response)
                window_means.append(trial_mean_response)

    return window_responses, window_means


def get_fa_rt_windows(outcome_list, rt_list):

    fa_rts = []
    n_trials = len(outcome_list)
    for trial_index in range(n_trials):
        trial_outcome = outcome_list[trial_index]
        trial_rt = rt_list[trial_index]
        if trial_outcome == 2:
            fa_rts.append(trial_rt)

    min_rt = np.min(fa_rts)
    max_rt = np.max(fa_rts)
    q1, q2, q3 = np.nanquantile(fa_rts, [0.25, 0.5, 0.75])
    window_starts = [min_rt, q1, q2, q3]
    window_stops = [q1, q2, q3, max_rt]
    return window_starts, window_stops


def get_correct_means(outcome_list, mean_response_list):

    correct_means = []
    n_trials = len(outcome_list)
    for trial_index in range(n_trials):
        trial_outcome = outcome_list[trial_index]
        trial_mean = mean_response_list[trial_index]
        if trial_outcome == 1:
            correct_means.append(trial_mean)

    return correct_means


def get_correct_responses(outcome_list, response_list):

    correct_means = []
    n_trials = len(outcome_list)
    for trial_index in range(n_trials):
        trial_outcome = outcome_list[trial_index]
        trial_mean = response_list[trial_index]
        if trial_outcome == 1:
            correct_means.append(trial_mean)

    correct_means = np.array(correct_means)
    return correct_means



def get_fa_rts(outcome_list, rt_list):
    fa_rts = []
    n_trials = len(outcome_list)
    for trial_index in range(n_trials):
        trial_outcome = outcome_list[trial_index]
        trial_rt = rt_list[trial_index]
        if trial_outcome == 2:
            fa_rts.append(trial_rt)
    return fa_rts



def scatter_outcomes_bin_rt_bin(response_list, mean_response_list, outcome_list, rt_list):

    # Create Figure
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1, 1, 1)

    # Plot Correct Trials
    correct_means = get_correct_means(outcome_list, mean_response_list)
    correct_grand_mean = np.mean(correct_means)
    axis_1.scatter(np.zeros(len(correct_means)), correct_means, alpha=0.2)
    axis_1.scatter([0], [correct_grand_mean], c='k', s=200)

    # Get FA Rts
    fa_rts = get_fa_rts(outcome_list, rt_list)

    # Get FA RT Quartiles
    #window_starts, window_stops = get_fa_rt_windows(outcome_list, rt_list)

    window_starts = [0, 500, 1000, 1500]
    window_stops = [500, 1000, 1500, 2000]
    print("window_starts", window_starts, "window_stops", window_stops)
    n_windows = len(window_starts)

    # Iterate Through Each RT Window
    for window_index in range(n_windows):
        window_start = window_starts[window_index]
        window_stop = window_stops[window_index]
        window_responses, window_means = get_window_responses_in_rt_bin(response_list, mean_response_list, outcome_list, rt_list, window_start, window_stop)
        window_grand_mean = np.mean(window_means)

        axis_1.scatter(np.ones(len(window_means)) * (window_index+1), window_means, alpha=0.2)
        axis_1.scatter(np.ones(1) * (window_index + 1), window_grand_mean, c='k', s=200)


    axis_1.spines[['right', 'top']].set_visible(False)
    axis_1.axhline(correct_grand_mean, c='Grey', linestyle='dashed')
    plt.show()



def plot_traces(response_list, mean_response_list, outcome_list, rt_list, preceeding_window, following_window):

    # Create Figure
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1, 1, 1)

    # Get X Values
    x_values = list(range(preceeding_window, following_window))

    # Plot Correct Trials
    correct_responses = get_correct_responses(outcome_list, response_list)
    correct_response_mean = np.mean(correct_responses, axis=0)
    axis_1.plot(x_values, correct_response_mean, c='cyan')

    # Get FA RT Quartiles
    #window_starts, window_stops = get_fa_rt_windows(outcome_list, rt_list)
    window_starts = [0, 500, 1000, 1500]
    window_stops = [500, 1000, 1500, 2000]

    # Iterate Through Each RT Window
    colourmap = plt.cm.get_cmap("plasma")
    colour_values = np.linspace(start=0, stop=0.8, num=4)

    n_windows = len(window_starts)
    for window_index in range(n_windows):
        window_start = window_starts[window_index]
        window_stop = window_stops[window_index]
        window_responses, window_means = get_window_responses_in_rt_bin(response_list, mean_response_list, outcome_list, rt_list, window_start, window_stop)
        window_response_mean = np.mean(window_responses, axis=0)

        window_colour = colourmap(colour_values[window_index])
        axis_1.plot(x_values, window_response_mean, c=window_colour)

    axis_1.axvline(0, c='k', linestyle='dashed')
    axis_1.spines[['right', 'top']].set_visible(False)
    plt.show()





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
    print("lick cd Projeciton", np.shape(lick_cd_projection))
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

                # Get Trial Lick Data
                trial_start = int(trial_onset + preceeding_window)
                trial_stop = int(trial_onset + following_window)

                if trial_start > 0 and trial_stop < n_timepoints:
                    if not np.isnan(trial_rt):
                        trial_lick_data = lick_cd_projection[trial_start:trial_stop]
                        trial_baseline = trial_lick_data[0:250]
                        trial_baseline = np.mean(trial_baseline)
                        trial_lick_data = np.subtract(trial_lick_data, trial_baseline)

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

preceeding_window = -500
following_window = 500
mean_response_window_start = np.abs(preceeding_window)
mean_response_window_stop = mean_response_window_start + 500

get_cohort_response_outcomes(session_list, preceeding_window, following_window, mean_response_window_start, mean_response_window_stop)
