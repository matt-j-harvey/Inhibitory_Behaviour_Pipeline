import numpy as np
import os
import matplotlib.pyplot as plt

"""
0 Trial Number
1 Trial Type
2 Trial Start
3 Trial End
4 Reaction Time
5 Drift Time
6 Trial Outcome
7 Stop Time
"""

def get_session_stop_trial_outcomes(behaviour_matrix):
    static_to_drift = []
    tone_to_drift = []
    outcomes = []

    for trial in behaviour_matrix:
        trial_type = trial[1]
        trial_outcome = trial[6]
        trial_stop_time = trial[7]
        trial_drift_time = trial[5]
        print("trial_type", trial_type)
        print("trial_drift_time", trial_drift_time)

        if trial_type == 2:
            if not np.isnan(trial_drift_time):

                static_to_drift.append(trial_drift_time)
                tone_to_drift.append(trial_drift_time - trial_stop_time)
                outcomes.append(trial_outcome)


    return static_to_drift, tone_to_drift, outcomes



def get_mouse_stop_outcomes(mouse_root, mouse_sessions):

    mouse_stop_outcomes = []
    mouse_static_to_drift = []
    mouse_tone_to_drift = []

    # Loop Through Each Session
    for session in mouse_sessions:

        # Set Base Directory
        base_directory = os.path.join(data_directory_root, mouse_root, session)

        # Load Behaviour Matrix
        behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"), allow_pickle=True)

        # Get Session Stop Outcomes
        session_static_to_drift, session_tone_to_drift, session_outcomes = get_session_stop_trial_outcomes(behaviour_matrix)
        print("session static to drift", len(session_static_to_drift))
        mouse_static_to_drift.append(session_static_to_drift)
        mouse_tone_to_drift.append(session_tone_to_drift)
        mouse_stop_outcomes.append(session_outcomes)

    mouse_stop_outcomes = np.concatenate(mouse_stop_outcomes)
    mouse_static_to_drift = np.concatenate(mouse_static_to_drift)
    mouse_tone_to_drift = np.concatenate(mouse_tone_to_drift)
    print("mouse_static_to_drift", len(mouse_static_to_drift))

    return mouse_stop_outcomes, mouse_static_to_drift, mouse_tone_to_drift





def get_bin_succsess_rate(times, outcomes, window_start, window_stop):

    bin_outcomes = []

    n_trials = len(times)
    for trial_index in range(n_trials):
        trial_time = times[trial_index]
        trial_outcome = outcomes[trial_index]

        if trial_time >= window_start and trial_time < window_stop:
            if trial_outcome == 1:
                bin_outcomes.append(1)
            elif trial_outcome == 2:
                bin_outcomes.append(0)

    bin_size = len(bin_outcomes)

    if bin_size == 0:
        return np.nan
    else:
        bin_correct = np.sum(bin_outcomes)
        bin_proportion = float(bin_correct)/bin_size
        return bin_proportion



def get_binwise_success_rate(mouse_times, mouse_outcomes, bin_starts, bin_stops):

    n_bins = len(bin_starts)
    bin_proportion_list = np.empty(n_bins)
    bin_proportion_list[:] = np.nan

    for bin_index in range(n_bins):
        bin_start = bin_starts[bin_index]
        bin_stop = bin_stops[bin_index]
        bin_proportion = get_bin_succsess_rate(mouse_times, mouse_outcomes, bin_start, bin_stop)
        bin_proportion_list[bin_index] = bin_proportion

    return bin_proportion_list



def get_dual_bin_success_rate(stop_times, drift_times, outcomes, stop_bin_start, stop_bin_stop, drift_bin_start, drift_bin_stop):

    bin_outcomes = []

    n_trials = len(outcomes)
    for trial_index in range(n_trials):
        trial_stop_time = stop_times[trial_index]
        trial_drift_time = drift_times[trial_index]
        trial_outcome = outcomes[trial_index]

        if trial_stop_time >= stop_bin_start and trial_stop_time < stop_bin_stop:
            if trial_drift_time >= drift_bin_start and trial_drift_time < drift_bin_stop:

                if trial_outcome == 1:
                    bin_outcomes.append(1)
                elif trial_outcome == 2:
                    bin_outcomes.append(0)

    bin_size = len(bin_outcomes)
    if bin_size == 0:
        return np.nan
    else:
        bin_correct = np.sum(bin_outcomes)
        bin_proportion = float(bin_correct)/bin_size
        return bin_proportion




def plot_cohort_performance(group_times_list, group_outcomes_list, bin_starts, bin_stops):


    n_mice = len(group_times_list)
    n_bins = len(bin_starts)

    colourmap = plt.get_cmap('Purples')
    colour_values = np.linspace(start=0.2, stop=1, num=n_mice)
    colours_list = colourmap(colour_values)

    x_values = list(range(len(bin_starts)))

    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1,1,1)

    group_proportions = []
    for mouse_index in range(n_mice):
        mouse_times = group_times_list[mouse_index]
        mouse_outcomes = group_outcomes_list[mouse_index]
        mouse_bin_proportions = get_binwise_success_rate(mouse_times, mouse_outcomes, bin_starts, bin_stops)
        axis_1.scatter(x_values, mouse_bin_proportions, c="mediumslateblue", alpha=0.7)
        axis_1.plot(x_values, mouse_bin_proportions, c="mediumslateblue", alpha=0.2)

        group_proportions.append(mouse_bin_proportions)

    group_proportions = np.array(group_proportions)
    group_mean = np.nanmean(group_proportions, axis=0)

    axis_1.plot(x_values, group_mean, c='k', linewidth=6)

    axis_1.set_ylim([0, 1.1])
    axis_1.spines[['right', 'top']].set_visible(False)
    axis_1.set_xticks(x_values, labels=bin_starts)

    axis_1.set_ylabel("Succsessfull stop proportion")

    plt.show()


def set_imshow_tick_labels(axis, x_labels=None, y_labels=None, x_rotation=0):
    if x_labels is not None:
        axis.set_xticks(np.arange(len(x_labels)))
        axis.set_xticklabels(x_labels, rotation=x_rotation)

    if y_labels is not None:
        axis.set_yticks(np.arange(len(y_labels)))
        axis.set_yticklabels(y_labels)



def view_2d_grid(stop_times, drift_times, outcomes, stop_window_starts, stop_window_stops, drift_window_starts, drift_window_stops):

    n_stop_bins = len(stop_window_starts)
    n_drift_bins = len(drift_window_starts)


    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1,1,1)

    matrix = np.zeros((n_stop_bins, n_drift_bins))
    #matrix[:] = np.nan
    for stop_bin_index in range(n_stop_bins):
        for drift_bin_index in range(n_drift_bins):

            stop_bin_start = stop_window_starts[stop_bin_index]
            stop_bin_stop = stop_window_stops[stop_bin_index]

            drift_bin_start = drift_window_starts[drift_bin_index]
            drift_bin_stop = drift_window_stops[drift_bin_index]

            bin_outcome = get_dual_bin_success_rate(stop_times, drift_times, outcomes, stop_bin_start, stop_bin_stop, drift_bin_start, drift_bin_stop)
            print("stop_bin_start", stop_bin_start, "stop_bin_stop", stop_bin_stop, "drift_bin_start", drift_bin_start, "drift_bin_stop", drift_bin_stop, "bin_outcome", bin_outcome)

            if not np.isnan(bin_outcome):
                matrix[stop_bin_index, drift_bin_index] = bin_outcome

    set_imshow_tick_labels(
        axis_1,
        x_labels=drift_window_starts,
        y_labels=stop_window_starts,
        x_rotation=45
    )
    axis_1.imshow(matrix, vmin=0, vmax=1, cmap='Purples')

    axis_1.set_xlabel("Time between static and drift onset")
    axis_1.set_ylabel("Time between stop tone and drift onset")


    plt.show()


def analyse_group_stopping_probability(mouse_list, session_list):

    # Lets Say 500 - 4000
    group_stop_outcomes = []
    group_static_to_drift = []
    group_tone_to_drift = []

    # Loop Through Each Mouse
    n_mice = len(mouse_list)
    for mouse_index in range(n_mice):

        mouse_root = mouse_list[mouse_index]
        mouse_sessions = session_list[mouse_index]
        mouse_stop_outcomes, mouse_static_to_drift, mouse_tone_to_drift = get_mouse_stop_outcomes(mouse_root, mouse_sessions)
        group_stop_outcomes.append(mouse_stop_outcomes)
        group_static_to_drift.append(mouse_static_to_drift)
        group_tone_to_drift.append(mouse_tone_to_drift)

    plt.hist(np.concatenate(group_tone_to_drift))
    plt.show()

    drift_bin_starts = list(range(500, 3500, 500))
    drift_bin_stops = np.add(drift_bin_starts, 500)
    plot_cohort_performance(group_static_to_drift, group_stop_outcomes, drift_bin_starts, drift_bin_stops)

    stop_bin_starts = list(range(500, 2500, 500))
    stop_bin_stops = np.add(stop_bin_starts, 500)
    plot_cohort_performance(group_tone_to_drift, group_stop_outcomes, stop_bin_starts, stop_bin_stops)

    group_stop_outcomes = np.concatenate(group_stop_outcomes)
    group_static_to_drift = np.concatenate(group_static_to_drift)
    group_tone_to_drift = np.concatenate(group_tone_to_drift)

    view_2d_grid(group_tone_to_drift, group_static_to_drift, group_stop_outcomes, stop_bin_starts, stop_bin_stops, drift_bin_starts, drift_bin_stops)



# Set Data Directories
data_directory_root = r"C:\Users\matth\Dropbox\Behaviour_Data"
output_root = r"C:\Fens_Analysis"

# Load Post Criteria Session Dict
session_dict = np.load(os.path.join(output_root, "Sessions_Above_Both_Criteria.npy"), allow_pickle=True)[()]
mouse_list = session_dict['data_root_list']
session_list = session_dict['session_lists']

# Analyse Group
analyse_group_stopping_probability(mouse_list, session_list)