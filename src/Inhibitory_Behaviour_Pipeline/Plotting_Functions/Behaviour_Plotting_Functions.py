import numpy as np
import os
import matplotlib.pyplot as plt
from numpy.lib.recfunctions import drop_fields

from Inhibitory_Behaviour_Pipeline.Behaviour_Analysis_Utils import Behaviour_Analysis_Utils, Behaviour_Analysis_Functions

#plt.rc('font', size=20)



def normalise_trace(trace):

    # Subtract Min
    trace_min = np.min(trace)
    trace = np.subtract(trace, trace_min)

    # Divide By Max
    trace_max = np.max(trace)
    trace = np.divide(trace, trace_max)

    return trace



def plot_static_delay_sanity_checks(base_directory):

    # Load DAQ Data
    ai_data = Behaviour_Analysis_Utils.load_ai_recorder_data(base_directory)
    n_channels, n_timnepoints = np.shape(ai_data)

    # Create DAQ Channel Dict
    channel_dict = Behaviour_Analysis_Utils.create_daq_channel_dict()

    # Unpack DAQ Traces
    #trial_start_trace = ai_data[channel_dict["Trial_Start"]]
    #trial_end_trace = ai_data[channel_dict["Trial_End"]]
    static_trace = ai_data[channel_dict["Static_Onset"]]
    drift_trace = ai_data[channel_dict["Drift_Onset"]]

    # Get Step Onsets
    static_onsets = Behaviour_Analysis_Utils.get_step_onsets(static_trace)
    drift_onsets = Behaviour_Analysis_Utils.get_step_onsets(drift_trace)
    n_static_onsets = len(static_onsets)
    n_drift_onsets = len(drift_onsets)
    print("n_static_onsets", n_static_onsets)
    print("n_drift_onsets", n_drift_onsets)
    drift_fraction = float(n_drift_onsets) / n_static_onsets
    drift_fraction = drift_fraction * 100
    drift_fraction = np.around(drift_fraction, 2)
    print("drift fraction", drift_fraction)


    # Normalise Traces
    #trial_start_trace = normalise_trace(trial_start_trace) # 0 - 1
    #trial_end_trace = normalise_trace(trial_end_trace) # 2- 3
    static_trace = normalise_trace(static_trace) # 4 - 5
    drift_trace = normalise_trace(drift_trace) # 6 - 7

    # Add Offsets
    #trial_end_trace = np.add(trial_end_trace, 2) # 2- 3
    #static_trace = np.add(static_trace, 4) # 4 - 5
    drift_trace = np.add(drift_trace, 1.5) # 6 - 7

    figure_1 = plt.figure(figsize=(15,5))
    axis_1 = figure_1.add_subplot(1,1,1)
    #axis_1.plot(trial_start_trace, c='b')
    #axis_1.plot(trial_end_trace, c='tab:purple')
    axis_1.plot(static_trace, c='k')
    axis_1.plot(drift_trace, c='skyblue')

    axis_1.scatter(static_onsets, np.ones(len(static_onsets)))
    axis_1.scatter(drift_onsets, np.ones(len(drift_onsets)) * 2.5)

    # Remove Borders
    axis_1.spines[['right', 'top', 'bottom', 'left']].set_visible(False)
    axis_1.axis('off')
    plt.title("Drift Fraction " + str(drift_fraction) + "%")

    plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", "Drift_Sanity_Check.png"))
    plt.close()



def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)


def plot_performance_delay(base_directory):

    # Load Performance
    hit_performance = np.load(os.path.join(base_directory, "Behaviour_Analysis", "go_trial_hit_percentage.npy"))
    delay_performance = np.load(os.path.join(base_directory, "Behaviour_Analysis", "delay_trial_hit_percentage.npy"))

    # Convert To Percentage
    hit_performance = hit_performance * 100
    delay_performance = delay_performance * 100

    # Create Figure
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1,1,1)

    axis_1.plot([1, 2], [hit_performance, delay_performance], c='tab:purple')
    axis_1.scatter([1, 2], [hit_performance, delay_performance], c='tab:purple')

    axis_1.set_xticks([1, 2], labels=["Go Trials", "Delay Trials"])
    axis_1.set_ylabel("% Correct")

    axis_1.set_title("Performance")

    axis_1.set_ylim([0, 110])
    axis_1.set_xlim([0.8, 2.2])
    axis_1.set_yticks(list(range(0, 110, 10)))

    # Remove Borders
    axis_1.spines[['right', 'top']].set_visible(False)
    plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", "Performance.png"))
    plt.close()


def load_stop_performance(base_directory):

    # Load Performance
    hit_performance = np.load(os.path.join(base_directory, "Behaviour_Analysis", "go_trial_hit_percentage.npy"))
    delay_performance = np.load(os.path.join(base_directory, "Behaviour_Analysis", "delay_trial_hit_percentage.npy"))
    stop_performance = np.load(os.path.join(base_directory, "Behaviour_Analysis", "stop_trial_correct_reject_percentage.npy"))

    # Convert To Percentage
    hit_performance = hit_performance * 100
    delay_performance = delay_performance * 100
    stop_performance = stop_performance * 100

    return hit_performance, delay_performance, stop_performance




def load_delay_performance(base_directory):

    # Load Performance
    hit_performance = np.load(os.path.join(base_directory, "Behaviour_Analysis", "go_trial_hit_percentage.npy"))
    delay_performance = np.load(os.path.join(base_directory, "Behaviour_Analysis", "delay_trial_hit_percentage.npy"))

    # Convert To Percentage
    hit_performance = hit_performance * 100
    delay_performance = delay_performance * 100

    return hit_performance, delay_performance


def plot_performance(base_directory):

    # Load Performance
    score_list, trial_type_list, x_values = Behaviour_Analysis_Utils.load_performance(base_directory)

    # Create Figure
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1, 1, 1)

    axis_1.plot(x_values, score_list, c='tab:purple')
    axis_1.scatter(x_values, score_list, c='tab:purple')

    axis_1.set_xticks(x_values, labels=trial_type_list)
    axis_1.set_ylabel("% Correct")

    axis_1.set_title("Performance")

    axis_1.set_ylim([0, 110])
    axis_1.set_xlim([0.8, len(score_list) + 0.2])
    axis_1.set_yticks(list(range(0, 110, 10)))

    # Remove Borders
    axis_1.spines[['right', 'top']].set_visible(False)
    plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", "Performance.png"))
    plt.close()




def plot_performance_d_prime(base_directory):

    # Create Figure
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1, 1, 1)
    axis_1.set_ylabel("d prime")
    axis_1.set_title("Performance")
    axis_1.set_ylim([-0.2, 4])

    # Get File Names
    static_drift_file = os.path.join(base_directory, "Behaviour_Analysis", "static_drift_d_prime.npy")
    tone_file = os.path.join(base_directory,  "Behaviour_Analysis", "tone_d_prime.npy")

    if os.path.isfile(static_drift_file):
        static_d_prime = np.load(static_drift_file)
        axis_1.scatter([1], [static_d_prime], c='tab:purple')
        axis_1.set_xticks([1], labels=["Static v Drift"])

    if os.path.isfile(tone_file):
        tone_d_prime = np.load(tone_file)
        axis_1.scatter([2], [tone_d_prime], c='tab:purple')
        axis_1.set_xticks([1, 2], labels=["Static v Drift", "Tone v No Tone"])

    axis_1.set_xlim([0.8, 2.2])
    axis_1.axhline(2, c='k', linestyle='dashed')
    # Remove Borders
    axis_1.spines[['right', 'top']].set_visible(False)
    plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", "Performance_d_prime.png"))
    plt.close()



def plot_performance_stop(base_directory):

    # Load Performance
    hit_performance, delay_performance, stop_performance = load_stop_performance(base_directory)

    # Create Figure
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1, 1, 1)

    axis_1.plot([1, 2, 3], [hit_performance, delay_performance, stop_performance], c='tab:purple')
    axis_1.scatter([1, 2, 3], [hit_performance, delay_performance, stop_performance], c='tab:purple')

    axis_1.set_xticks([1, 2, 3], labels=["Go Trials", "Delay Trials", "Stop_Trials"])
    axis_1.set_ylabel("% Correct")

    axis_1.set_title("Performance")

    axis_1.set_ylim([0, 110])
    axis_1.set_xlim([0.8, 3.2])
    axis_1.set_yticks(list(range(0, 110, 10)))

    # Remove Borders
    axis_1.spines[['right', 'top']].set_visible(False)
    plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", "Performance.png"))
    plt.close()



def plot_performance_stop_group(session_list, output_directory, cmap='viridis'):

    # Create Figure
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1, 1, 1)

    # Create Colourmap
    colourmap = plt.get_cmap(cmap)
    n_mice = float(len(session_list))

    count = 0
    hit_performance_list = []
    delay_performance_list = []
    stop_performance_list = []

    for session in session_list:

        # Load Performance
        hit_performance, delay_performance, stop_performance = load_stop_performance(session)
        hit_performance_list.append(hit_performance)
        delay_performance_list.append(delay_performance)
        stop_performance_list.append(stop_performance)

        # Get Mouse Colour
        mouse_colour = colourmap((count / n_mice))

        axis_1.plot([1, 2, 3], [hit_performance, delay_performance, stop_performance], c=mouse_colour, alpha=0.4)
        axis_1.scatter([1, 2, 3], [hit_performance, delay_performance, stop_performance], c=mouse_colour, alpha=0.4)

        count += 1

    print("mean hit", np.mean(hit_performance_list))
    print("mean delay", np.mean(delay_performance_list))
    print("mean stop", np.mean(stop_performance_list))

    axis_1.set_xticks([1, 2, 3], labels=["Go Trials", "Delay Trials", "Stop_Trials"])
    axis_1.set_ylabel("% Correct")

    axis_1.set_title("Performance")

    axis_1.set_ylim([0, 110])
    axis_1.set_xlim([0.8, 3.2])
    axis_1.set_yticks(list(range(0, 110, 10)))

    # Remove Borders
    axis_1.spines[['right', 'top']].set_visible(False)

    plt.savefig(os.path.join(output_directory, "Performance.png"))
    plt.close()






def plot_performance_delay_group(session_list, output_directory, cmap='viridis'):

    # Create Figure
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1, 1, 1)

    # Create Colourmap
    colourmap = plt.get_cmap(cmap)
    n_mice = float(len(session_list))

    count = 0
    hit_performance_list = []
    delay_performance_list = []

    for session in session_list:

        # Load Performance
        hit_performance, delay_performance = load_delay_performance(session)
        hit_performance_list.append(hit_performance)
        delay_performance_list.append(delay_performance)

        # Get Mouse Colour
        mouse_colour = colourmap((count / n_mice))

        axis_1.plot([1, 2], [hit_performance, delay_performance], c=mouse_colour, alpha=0.4)
        axis_1.scatter([1, 2], [hit_performance, delay_performance], c=mouse_colour, alpha=0.4)

        count += 1

    print("mean hit", np.mean(hit_performance_list))
    print("mean delay", np.mean(delay_performance_list))

    axis_1.set_xticks([1, 2], labels=["Go Trials", "Delay Trials"])
    axis_1.set_ylabel("% Correct")

    axis_1.set_title("Performance")

    axis_1.set_ylim([0, 110])
    axis_1.set_xlim([0.8, 2.2])
    axis_1.set_yticks(list(range(0, 110, 10)))

    # Remove Borders
    axis_1.spines[['right', 'top']].set_visible(False)

    plt.savefig(os.path.join(output_directory, "Performance.png"))
    plt.close()





def overlay_rt_distributions(base_directory, go_rts, delay_rts, bin_width=250, title="", save=True):

    # Get Max RTs
    #max_rt = np.max(np.concatenate([go_rts, delay_rts]))
    max_rt = 4000

    # Get Bin List
    bin_list = list(range(0, int(max_rt) + bin_width, bin_width))

    # Create Figure
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1,1,1)

    # Plot Histograms
    axis_1.hist(go_rts, bins=bin_list, color='g', alpha=0.4)
    axis_1.hist(delay_rts, bins=bin_list, color='cornflowerblue', alpha=0.4)

    # Set Axis Labels
    axis_1.set_xlabel("Time (Ms)")
    axis_1.set_ylabel("N Trials")

    # Remove Borders
    axis_1.spines[['right', 'top']].set_visible(False)
    axis_1.set_title(title)

    if save == True:
        plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", title + ".png"))
        plt.close()

    else:
        plt.show()

def get_hist_bins(data, bin_start_list, bin_stop_list):

    n_bins = len(bin_start_list)
    bin_counts = np.zeros(n_bins)

    for datapoint in data:

        for bin_index in range(n_bins):
            bin_start = bin_start_list[bin_index]
            bin_stop = bin_stop_list[bin_index]

            if datapoint >= bin_start and datapoint < bin_stop:
                    bin_counts[bin_index] += 1

    return bin_counts







def overlay_rt_distributions_density(base_directory, go_rts, delay_rts, bin_width=250, title="", save=True):

    # Get Max RTs
    max_rt = 4000
    #max_rt = np.max(np.concatenate([go_rts, delay_rts]))

    # Get Bin List
    bin_start_list = list(range(0, int(max_rt) + bin_width, bin_width))
    bin_stop_list = np.add(bin_start_list, bin_width)
    print("bin_start_list", bin_start_list)
    print("bin_stop_list", bin_stop_list)

    # Get Bin Counts
    go_counts = get_hist_bins(go_rts, bin_start_list, bin_stop_list)
    delay_counts = get_hist_bins(delay_rts, bin_start_list, bin_stop_list)
    print("go_counts", go_counts)
    print("delay_counts", delay_counts)

    # Convert To Densities
    go_counts = 100 * np.divide(go_counts, np.sum(go_counts))
    delay_counts = 100 * np.divide(delay_counts, np.sum(delay_counts))

    # Create Figure
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1,1,1)

    # Plot Histograms
    axis_1.bar(x=bin_start_list, height=go_counts, width=bin_width, color='g', alpha=0.4, align='edge')
    axis_1.bar(x=bin_start_list, height=delay_counts, width=bin_width, color='cornflowerblue', alpha=0.4, align='edge')

    # Set Axis Labels
    axis_1.set_xlabel("Time (Ms)")
    axis_1.set_ylabel("% Trials")

    axis_1.set_xlim([0, max_rt])
    axis_1.set_ylim([0, 80])

    axis_1.set_xticks(list(range(0, max_rt, 1000)))
    axis_1.set_title(title)

    # Remove Borders
    axis_1.spines[['right', 'top']].set_visible(False)

    if save == True:
        plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", title + ".png"))
        plt.close()

    else:
        plt.show()

def single_histogram(base_directory, rts, bin_width=250, title=""):
    max_rt = 4000

    # Get Bin List
    bin_start_list = list(range(0, int(max_rt) + bin_width, bin_width))
    bin_stop_list = np.add(bin_start_list, bin_width)

    # Get Bin Counts
    rts_counts = get_hist_bins(rts, bin_start_list, bin_stop_list)

    # Convert To Densities
    rts_counts = 100 * np.divide(rts_counts, np.sum(rts_counts))

    # Create Figure
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1, 1, 1)

    # Plot Histograms
    axis_1.bar(x=bin_start_list, height=rts_counts, width=bin_width, color='g', alpha=0.4, align='edge')

    # Set Axis Labels
    axis_1.set_xlabel("Time (Ms)")
    axis_1.set_ylabel("% Trials")

    axis_1.set_xlim([0, max_rt])
    axis_1.set_ylim([0, 80])
    axis_1.set_xticks(list(range(0, max_rt, 1000)))

    # Remove Borders
    axis_1.spines[['right', 'top']].set_visible(False)

    axis_1.set_title(title)
    plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", title + ".png"))
    plt.close()


def convert_lick_trace_to_colour(lick_trace, lick_threshold=2):

    n_timepoints = len(lick_trace)
    lick_trace_colour = np.ones((n_timepoints, 3))
    for timepoint_index in range(n_timepoints):
        if lick_trace[timepoint_index] > lick_threshold:
            lick_trace_colour[timepoint_index] = [0, 0, 0]

    return lick_trace_colour




def plot_psths(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Load DAQ Data
    ai_data = Behaviour_Analysis_Utils.load_ai_recorder_data(base_directory)
    n_channels, n_timnepoints = np.shape(ai_data)

    # Create DAQ Channel Dict
    channel_dict = Behaviour_Analysis_Utils.create_daq_channel_dict()

    # Unpack DAQ Traces
    lick_trace = ai_data[channel_dict["Lick"]]

    # Get Trial Indicies
    go_trial_indicies = np.where(behaviour_matrix[:, 1] == 0)[0]
    delay_trial_indicies = np.where(behaviour_matrix[:, 1] == 1)[0]

    n_go_trials = len(go_trial_indicies)
    n_delay_trials = len(delay_trial_indicies)

    # Sort By Reaction Times
    go_trial_rts = behaviour_matrix[go_trial_indicies, 4]
    delay_trial_rts = behaviour_matrix[delay_trial_indicies, 4]

    go_sorting_indicies = np.argsort(go_trial_rts)
    go_sorting_indicies = np.flip(go_sorting_indicies)

    delay_sorting_indicies = np.argsort(delay_trial_rts)
    delay_sorting_indicies = np.flip(delay_sorting_indicies)

    go_trial_indicies = go_trial_indicies[go_sorting_indicies]
    delay_trial_indicies = delay_trial_indicies[delay_sorting_indicies]

    # Set Plot Settings
    preceeding_window = 1000
    following_window = 3000
    row_length = preceeding_window + following_window

    # Create Figure
    figure_1 = plt.figure(figsize=(20, 10))
    go_axis = figure_1.add_subplot(2, 1, 1)
    delay_axis = figure_1.add_subplot(2, 1, 2)

    # Set Axis Limits
    go_axis.set_xlim([0, preceeding_window + following_window])
    delay_axis.set_xlim([0, preceeding_window + following_window])
    go_axis.set_ylim([0, n_go_trials + 1])
    delay_axis.set_ylim([0, n_delay_trials + 1])

    # Create Empty PSTHs
    go_trial_psth = np.ones((n_go_trials, row_length, 3))
    delay_trial_psth = np.ones((n_delay_trials, row_length, 3))

    # Iterate Through Go Trials
    for trial_n in range(n_go_trials):
        trial_index = go_trial_indicies[trial_n]

        # Get Trial Start Times
        trial_start = behaviour_matrix[trial_index, 2]
        window_start = int(trial_start - preceeding_window)
        window_stop = int(trial_start + following_window)

        # Get Trial Lick Data
        trial_lick_data = lick_trace[window_start:window_stop]
        trial_lick_colour = convert_lick_trace_to_colour(trial_lick_data)
        go_trial_psth[trial_n] = trial_lick_colour

    # Iterate Through Delay Trials
    for trial_n in range(n_delay_trials):
        trial_index = delay_trial_indicies[trial_n]

        # Get Trial Start Times
        trial_start = behaviour_matrix[trial_index, 2]
        window_start = int(trial_start - preceeding_window)
        window_stop = int(trial_start + following_window)

        if window_start > 0 and window_stop < n_timnepoints:
            print("window starrt", window_start, "Window stop", window_stop)

            # Get Trial Lick Data
            trial_lick_data = lick_trace[window_start:window_stop]
            trial_lick_colour = convert_lick_trace_to_colour(trial_lick_data)
            print("trial_lick_colour", trial_lick_colour)
            delay_trial_psth[trial_n] = trial_lick_colour

            # Get Drift Onset
            trial_drift_onset = behaviour_matrix[trial_index, 5]
            if not np.isnan(trial_drift_onset):
                trial_drift_onset = int(trial_drift_onset)
                delay_trial_psth[trial_n, trial_drift_onset + preceeding_window:trial_drift_onset + preceeding_window + 50] = [0, 0, 1]

    # Show PSTHs
    go_axis.imshow(go_trial_psth, vmin=0.3, vmax=1, origin='lower')
    delay_axis.imshow(delay_trial_psth, vmin=0.3, vmax=1, origin='lower')

    go_axis.axvline(preceeding_window, c='k', linestyle='dashed')
    delay_axis.axvline(preceeding_window, c='k', linestyle='dashed')

    go_axis.set_xticks(list(range(0, preceeding_window + following_window, 500)), labels=list(range(-1000, following_window, 500)))
    delay_axis.set_xticks(list(range(0, preceeding_window + following_window, 500)), labels=list(range(-1000, following_window, 500)))

    forceAspect(go_axis, aspect=3)
    forceAspect(delay_axis, aspect=3)

    go_axis.set_ylabel("Trials")
    delay_axis.set_ylabel("Trials")

    delay_axis.set_xlabel("Time (ms)")

    plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", "Combined_PSTH.png"))
    plt.close()

def plot_delay_psth(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Load DAQ Data
    ai_data = Behaviour_Analysis_Utils.load_ai_recorder_data(base_directory)
    n_channels, n_timnepoints = np.shape(ai_data)

    # Create DAQ Channel Dict
    channel_dict = Behaviour_Analysis_Utils.create_daq_channel_dict()

    # Unpack DAQ Traces
    lick_trace = ai_data[channel_dict["Lick"]]

    # Get Delay Trial Indicies
    delay_trial_indicies = np.where(behaviour_matrix[:, 1] == 1)[0]
    n_trials = len(delay_trial_indicies)

    # Sort By Reaction Times
    trial_rts = behaviour_matrix[delay_trial_indicies, 4]
    sorting_indicies = np.argsort(trial_rts)
    sorting_indicies = np.flip(sorting_indicies)

    delay_trial_indicies = delay_trial_indicies[sorting_indicies]

    # Set Plot Settings
    preceeding_window = 1000
    following_window = 2500
    row_length = preceeding_window + following_window

    # Create Figure
    figure_1 = plt.figure(figsize=(10, 5))
    axis_1 = figure_1.add_subplot(1, 1, 1)
    axis_1.set_xlim([0, preceeding_window + following_window])
    axis_1.set_ylim([0, n_trials + 1])

    # Create Empty PSTH
    trial_psth = np.ones((n_trials, row_length, 3))

    # Iterate Through Each Trial
    for trial_n in range(n_trials):
        trial_index = delay_trial_indicies[trial_n]


        # Get Trial Start Times
        trial_start = behaviour_matrix[trial_index, 2]
        print("trial start", trial_start)
        window_start = int(trial_start - preceeding_window)
        window_stop = int(trial_start + following_window)
        print("window_start", window_start)
        print("window_stop", window_stop)

        # Get Trial Lick Data
        trial_lick_data = lick_trace[window_start:window_stop]
        trial_lick_colour = convert_lick_trace_to_colour(trial_lick_data)
        trial_psth[trial_n] = trial_lick_colour

        # Get Drift Onset
        trial_drift_onset = behaviour_matrix[trial_index, 5]
        if not np.isnan(trial_drift_onset):
            trial_drift_onset = int(trial_drift_onset)
            trial_psth[trial_n, trial_drift_onset + preceeding_window:trial_drift_onset + preceeding_window + 20] = [0,0,1]

        #axis_1.scatter(x=[trial_drift_onset + preceeding_window], y=[trial_n])


    axis_1.imshow(trial_psth, vmin=0.3, vmax=1, origin='lower')
    axis_1.axvline(preceeding_window, c='k', linestyle='dashed')

    axis_1.set_xticks(list(range(0, preceeding_window + following_window, 500)), labels=list(range(-1000, following_window, 500)))

    forceAspect(axis_1, aspect=2)

    plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", "Delay_PSTH.png"))
    plt.close()



def plot_delay_correct_psth(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Load DAQ Data
    ai_data = Behaviour_Analysis_Utils.load_ai_recorder_data(base_directory)
    n_channels, n_timnepoints = np.shape(ai_data)

    # Create DAQ Channel Dict
    channel_dict = Behaviour_Analysis_Utils.create_daq_channel_dict()

    # Unpack DAQ Traces
    lick_trace = ai_data[channel_dict["Lick"]]

    # Get Delay Trial Indicies
    correct_delay_trials = Behaviour_Analysis_Functions.get_correct_delay_trials(behaviour_matrix)
    n_trials = len(correct_delay_trials)
    print("correct_delay_trials", correct_delay_trials)

    # Sort By Delay Times
    trial_drift_onsets = behaviour_matrix[correct_delay_trials, 5]
    print("trial_drift_onsets", trial_drift_onsets)
    sorting_indicies = np.argsort(trial_drift_onsets)
    sorting_indicies = np.flip(sorting_indicies)
    print("sorting_indicies", sorting_indicies)
    correct_delay_trials = correct_delay_trials[sorting_indicies]

    # Set Plot Settings
    preceeding_window = 1000
    following_window = 2500
    row_length = preceeding_window + following_window

    # Create Figure
    figure_1 = plt.figure(figsize=(10, 5))
    axis_1 = figure_1.add_subplot(1, 1, 1)
    axis_1.set_xlim([0, preceeding_window + following_window])
    axis_1.set_ylim([0, n_trials + 1])

    # Create Empty PSTH
    trial_psth = np.ones((n_trials, row_length, 3))

    # Iterate Through Each Trial
    for trial_n in range(n_trials):
        trial_index = correct_delay_trials[trial_n]

        # Get Trial Start Times
        trial_start = behaviour_matrix[trial_index, 2]
        window_start = int(trial_start - preceeding_window)
        window_stop = int(trial_start + following_window)

        if window_start > 0 and window_stop < n_timnepoints:

            # Get Trial Lick Data
            trial_lick_data = lick_trace[window_start:window_stop]
            trial_lick_colour = convert_lick_trace_to_colour(trial_lick_data)
            trial_psth[trial_n] = trial_lick_colour

            # Get Drift Onset
            trial_drift_onset = behaviour_matrix[trial_index, 5]
            if not np.isnan(trial_drift_onset):
                trial_drift_onset = int(trial_drift_onset)
                trial_psth[trial_n, trial_drift_onset + preceeding_window:trial_drift_onset + preceeding_window + 20] = [0, 0, 1]

    axis_1.imshow(trial_psth, vmin=0.3, vmax=1, origin='lower')
    axis_1.axvline(preceeding_window, c='k', linestyle='dashed')

    axis_1.set_xticks(list(range(0, preceeding_window + following_window, 500)), labels=list(range(-1000, following_window, 500)))

    forceAspect(axis_1, aspect=2)

    plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", "Correct_Delay_PSTH.png"))
    plt.close()



def plot_learning_performance(session_list):

    # Create Figure
    figure_1 = plt.figure(figsize=(10, 5))
    axis_1 = figure_1.add_subplot(1, 1, 1)

    colourmap = plt.get_cmap("viridis")
    n_sessions = len(session_list)

    session_count = 1
    for session in session_list:

        session_fraction = float(session_count) / n_sessions
        session_colour = colourmap(session_fraction)

        session_scores = np.load(os.path.join(session, "Behaviour_Analysis", "bin_delay_performance_list.npy"))
        axis_1.plot(session_scores, c=session_colour)
        #axis_1.scatter(session_scores)

        session_count += 1
    plt.show()





def plot_stop_psth(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Load DAQ Data
    ai_data = Behaviour_Analysis_Utils.load_ai_recorder_data(base_directory)
    n_channels, n_timnepoints = np.shape(ai_data)

    # Create DAQ Channel Dict
    channel_dict = Behaviour_Analysis_Utils.create_daq_channel_dict()

    # Unpack DAQ Traces
    lick_trace = ai_data[channel_dict["Lick"]]

    # Get Trial Indicies
    delay_trial_indicies = np.where(behaviour_matrix[:, 1] == 1)[0]
    n_trials = len(delay_trial_indicies)

    # Sort By Reaction Times
    trial_rts = behaviour_matrix[delay_trial_indicies, 4]
    sorting_indicies = np.argsort(trial_rts)
    sorting_indicies = np.flip(sorting_indicies)

    delay_trial_indicies = delay_trial_indicies[sorting_indicies]

    # Set Plot Settings
    preceeding_window = 1000
    following_window = 2500
    row_length = preceeding_window + following_window

    # Create Figure
    figure_1 = plt.figure(figsize=(10, 5))
    axis_1 = figure_1.add_subplot(1, 1, 1)
    axis_1.set_xlim([0, preceeding_window + following_window])
    axis_1.set_ylim([0, n_trials + 1])

    # Create Empty PSTH
    trial_psth = np.ones((n_trials, row_length, 3))

    # Iterate Through Each Trial
    for trial_n in range(n_trials):
        trial_index = delay_trial_indicies[trial_n]


        # Get Trial Start Times
        trial_start = behaviour_matrix[trial_index, 2]
        print("trial start", trial_start)
        window_start = int(trial_start - preceeding_window)
        window_stop = int(trial_start + following_window)
        print("window_start", window_start)
        print("window_stop", window_stop)

        # Get Trial Lick Data
        trial_lick_data = lick_trace[window_start:window_stop]
        trial_lick_colour = convert_lick_trace_to_colour(trial_lick_data)
        trial_psth[trial_n] = trial_lick_colour

        # Get Drift Onset
        trial_drift_onset = behaviour_matrix[trial_index, 5]
        if not np.isnan(trial_drift_onset):
            trial_drift_onset = int(trial_drift_onset)
            trial_psth[trial_n, trial_drift_onset + preceeding_window:trial_drift_onset + preceeding_window + 20] = [0,0,1]

        #axis_1.scatter(x=[trial_drift_onset + preceeding_window], y=[trial_n])


    axis_1.imshow(trial_psth, vmin=0.3, vmax=1, origin='lower')
    axis_1.axvline(preceeding_window, c='k', linestyle='dashed')

    axis_1.set_xticks(list(range(0, preceeding_window + following_window, 500)), labels=list(range(-1000, following_window, 500)))

    forceAspect(axis_1, aspect=2)

    plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", "Delay_PSTH.png"))
    plt.close()







