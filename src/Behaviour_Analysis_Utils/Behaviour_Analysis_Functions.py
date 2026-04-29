import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from scipy.stats import norm
import numpy as np
import os


"""
0 - Trial Number
1 - Trial Type
2 - Trial Start
3 - Trial End
4 - Reaction Times
5 - Drift Times
6 - Trial Outcomes
"""


def plot_delay_performance_by_bin(behaviour_matrix, min=500, max=2000, bin_size=300):

    """assumes given bins span uniform distribution of all time points"""
    bin_start_list = list(range(min, max, bin_size))
    bin_stop_list = np.add(bin_start_list, bin_size)
    n_bins = len(bin_start_list)
    print("bin start list", bin_start_list)
    print("bin stop list", bin_stop_list)

    # Estimate Number Of Bin trials
    delay_trial_indicies = np.where(behaviour_matrix[:, 1] == 1)[0]
    n_delay_trials = len(delay_trial_indicies)
    estimated_bin_trials = n_delay_trials / n_bins
    estimated_bin_trials = int(np.around(estimated_bin_trials, 0))
    print("estimated_bin_trials", estimated_bin_trials)

    n_correct_list = []
    for bin_index in range(n_bins):
        bin_start = bin_start_list[bin_index]
        bin_stop = bin_stop_list[bin_index]
        bin_correct_count = 0
        for trial in delay_trial_indicies:
            trial_data = behaviour_matrix[trial]
            outcome = trial_data[6]
            drift_time = trial_data[5]

            if outcome == 1:
                if drift_time > bin_start and drift_time <= bin_stop:
                    bin_correct_count += 1

        n_correct_list.append(bin_correct_count)


    n_correct_list = np.array(n_correct_list)
    print("n correct list", n_correct_list)
    n_correct_list = np.divide(n_correct_list, estimated_bin_trials)
    print("n correct list", n_correct_list)

    figure_1 = figure()
    axis_1 = figure_1.add_subplot(1,1,1)
    axis_1.plot(bin_stop_list, n_correct_list)
    axis_1.scatter(bin_stop_list, n_correct_list)
    axis_1.set_ylim([0, 1])


    # Remove Borders
    axis_1.spines[['right', 'top']].set_visible(False)

    axis_1.set_ylabel("Fraction Correct")
    axis_1.set_xlabel("Delay Duration")


    plt.show()
    # How many Correct
    # Estimate How Many Total



def extreme_value_corrections(selected_value, number_of_trials):

    if selected_value == 0:
        selected_value = float(1) / number_of_trials

    elif selected_value == 1:
        selected_value = float((number_of_trials - 1)) / number_of_trials

    return selected_value


def calculate_d_prime(hits, misses, false_alarms, correct_rejections):

    # Calculate Hit Rates and False Alarm Rates
    number_of_rewarded_trials = hits + misses
    number_of_unrewarded_trials = false_alarms + correct_rejections

    if number_of_unrewarded_trials == 0 or number_of_rewarded_trials == 0:
        return np.nan
    else:

        hit_rate = float(hits) / number_of_rewarded_trials
        false_alarm_rate = float(false_alarms) / number_of_unrewarded_trials

        # Ensure Either Value Does Not Equal Zero or One
        hit_rate = extreme_value_corrections(hit_rate, number_of_rewarded_trials)
        false_alarm_rate = extreme_value_corrections(false_alarm_rate, number_of_unrewarded_trials)

        # Get The Standard Normal Distribution
        Z = norm.ppf

        # Z Transform Both The Hit Rates And The False Alarm Rates
        hit_rate_z_transform = Z(hit_rate)
        false_alarm_rate_z_transform = Z(false_alarm_rate)

        # Calculate D Prime
        d_prime = hit_rate_z_transform - false_alarm_rate_z_transform

    d_prime = np.around(d_prime, 2)
    return d_prime



def get_static_v_drift_d_prime(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"), allow_pickle=True)

    # Drift Hits - Drift Misses
    # Static CRs - Static FAs

    n_go_hits = len(get_hit_trials(behaviour_matrix))
    n_go_misses = len(get_go_trial_misses(behaviour_matrix))
    n_delay_hits = len(get_correct_delay_trials(behaviour_matrix))
    n_delay_misses = len(get_delay_trial_misses(behaviour_matrix))
    n_delay_fas = len(get_premature_trials(behaviour_matrix))

    drift_hits = n_go_hits + n_delay_hits
    drift_misses = n_go_misses + n_delay_misses
    static_crs = n_delay_hits + n_delay_misses
    static_fas = n_delay_fas

    combined_d_prime = calculate_d_prime(drift_hits, drift_misses, static_fas, static_crs)

    return combined_d_prime


def get_tone_v_no_tone_d_prime(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"), allow_pickle=True)

    # Drift Hits - Drift Misses
    # Static CRs - Static FAs
    n_crs = len(get_correct_stop_trials(behaviour_matrix))
    n_fas = len(get_failed_stop_trials(behaviour_matrix))

    n_go_hits = len(get_hit_trials(behaviour_matrix))
    n_delay_hits = len(get_correct_delay_trials(behaviour_matrix))
    n_go_misses = len(get_go_trial_misses(behaviour_matrix))
    n_delay_misses = len(get_delay_trial_misses(behaviour_matrix))
    n_hits = n_go_hits + n_delay_hits
    n_misses = n_go_misses + n_delay_misses

    """
    print("n_go_hits", n_go_hits)
    print("n_go_misses", n_go_misses)
    print("n_crs", n_crs)
    print("n_fas", n_fas)
    """

    combined_d_prime = calculate_d_prime(n_hits, n_misses, n_fas, n_crs)
    print("tone_d_prime", combined_d_prime)
    print(" ")
    return combined_d_prime


def get_stop_d_prime(base_directory):

    """
    d’ = z(FA) – z(H)

    -- In Both Cases We Will Look only At Times When you have waited untill the drift

    Stop Hits = No stop drifts correctly licked to
    Stop Misses = no stop drifts incorrectly ignored
    Stop CRs = stop drifts correctly ignored
    Stop Fas = stop drifts incorrectly licked to

    """

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Get Trial Indicies
    delay_trial_indicies = np.where(behaviour_matrix[:, 1] == 1)[0]
    stop_trial_indicies = np.where(behaviour_matrix[:, 1] == 2)[0]
    #print("stop strial indicies", stop_trial_indicies)

    delay_trial_outcomes = list(behaviour_matrix[delay_trial_indicies, 6])
    stop_trial_outcomes = list(behaviour_matrix[stop_trial_indicies, 6])

    # Get CRs
    crs = stop_trial_outcomes.count(1)

    # Get FAs
    fas = stop_trial_outcomes.count(2)

    # Get Hits
    hits = delay_trial_outcomes.count(1)

    # Get Misses
    misses = delay_trial_outcomes.count(0)
    #print("crs", crs, "fas", fas, "hits", hits, "misses", misses)

    stop_d_prime = calculate_d_prime(hits, misses, fas, crs)
    #print("stop dprime", stop_d_prime)

    return stop_d_prime


def calculate_go_trial_performance(behaviour_matrix, go_trial_indicies):
    go_trial_outcomes = behaviour_matrix[go_trial_indicies, 6]
    go_trial_outcomes = list(go_trial_outcomes)
    go_trial_hits = go_trial_outcomes.count(1)
    go_trial_misses = go_trial_outcomes.count(0)
    n_go_trials = len(go_trial_indicies)
    go_trial_hit_percentage = float(go_trial_hits) / n_go_trials
    go_trial_miss_percentage = float(go_trial_misses) / n_go_trials
    go_trial_hit_percentage = np.around(go_trial_hit_percentage, 2)
    go_trial_miss_percentage = np.around(go_trial_miss_percentage, 2)
    return go_trial_hit_percentage, go_trial_miss_percentage


def calculate_delay_trial_performance(behaviour_matrix, delay_trial_indicies):

    # Get Outcomes
    delay_trial_outcomes = behaviour_matrix[delay_trial_indicies, 6]
    delay_trial_outcomes = list(delay_trial_outcomes)
    n_delay_trials = len(delay_trial_outcomes)
    delay_trial_hits = delay_trial_outcomes.count(1)
    delay_trial_misses = delay_trial_outcomes.count(0)
    delay_trial_fas = delay_trial_outcomes.count(2)

    # Convert To Percentage
    delay_trial_hit_percentage = float(delay_trial_hits) / n_delay_trials
    delay_trial_miss_percentage = float(delay_trial_misses) / n_delay_trials
    delay_trial_fa_percentage = float(delay_trial_fas) / n_delay_trials

    # Round Performance
    delay_trial_hit_percentage = np.around(delay_trial_hit_percentage, 2)
    delay_trial_miss_percentage = np.around(delay_trial_miss_percentage, 2)
    delay_trial_fa_percentage = np.around(delay_trial_fa_percentage, 2)

    return delay_trial_hit_percentage, delay_trial_miss_percentage, delay_trial_fa_percentage


def calculate_stop_performance(behaviour_matrix, stop_trial_indicies):

    # Stop Trial Outcomes
    stop_trial_outcomes = behaviour_matrix[stop_trial_indicies, 6]
    stop_trial_outcomes = list(stop_trial_outcomes)
    n_stop_trials = len(stop_trial_outcomes)
    stop_trial_correct_rejections = stop_trial_outcomes.count(1)
    stop_trial_false_alarms = stop_trial_outcomes.count(2)

    # Convert To Percentage
    stop_trial_correct_reject_percentage = float(stop_trial_correct_rejections) / n_stop_trials
    stop_trial_false_alarm_percentage = float(stop_trial_false_alarms) / n_stop_trials

    # Round Performance
    stop_trial_correct_reject_percentage = np.around(stop_trial_correct_reject_percentage, 2)
    stop_trial_false_alarm_percentage = np.around(stop_trial_false_alarm_percentage, 2)

    return stop_trial_correct_reject_percentage, stop_trial_false_alarm_percentage



def get_performance(base_directory):

    # Go Hit Percentage
    # Go Miss Percentage

    # Delay Miss Percentage
    # Delay False Alarm Percentage
    # Delay Correct Wait Percentage

    # Stop False Alarm Percentage
    # Stop Correct Wait Percentage

    # Set Save Directory
    save_directory = os.path.join(base_directory, "Behaviour_Analysis")

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Get Trial Indicies
    go_trial_indicies = np.where(behaviour_matrix[:, 1] == 0)[0]
    delay_trial_indicies = np.where(behaviour_matrix[:, 1] == 1)[0]
    stop_trial_indicies = np.where(behaviour_matrix[:, 1] == 2)[0]

    # Get Go Trial Performance
    if len(go_trial_indicies) > 0:
        go_trial_hit_percentage, go_trial_miss_percentage = calculate_go_trial_performance(behaviour_matrix, go_trial_indicies)
        np.save(os.path.join(save_directory, "go_trial_hit_percentage.npy"), go_trial_hit_percentage)
        np.save(os.path.join(save_directory, "go_trial_miss_percentage.npy"), go_trial_miss_percentage)
        print("go_trial_hit_percentage", go_trial_hit_percentage)
        print("go_trial_miss_percentage", go_trial_miss_percentage)

    # Get Delay Trial Performance
    if len(delay_trial_indicies) > 0:
        delay_trial_hit_percentage, delay_trial_miss_percentage, delay_trial_fa_percentage = calculate_delay_trial_performance(behaviour_matrix, delay_trial_indicies)
        static_drift_d_prime = get_static_v_drift_d_prime(base_directory)
        np.save(os.path.join(save_directory, "delay_trial_hit_percentage.npy"), delay_trial_hit_percentage)
        np.save(os.path.join(save_directory, "delay_trial_miss_percentage.npy"), delay_trial_miss_percentage)
        np.save(os.path.join(save_directory, "delay_trial_fa_percentage.npy"), delay_trial_fa_percentage)
        np.save(os.path.join(save_directory, "static_drift_d_prime.npy"), static_drift_d_prime)
        print("delay_trial_hit_percentage", delay_trial_hit_percentage)
        print("delay_trial_miss_percentage", delay_trial_miss_percentage)
        print("delay_trial_fa_percentage", delay_trial_fa_percentage)

    # Get Stop Trial Performance
    if len(stop_trial_indicies) > 0:
        stop_trial_correct_reject_percentage, stop_trial_false_alarm_percentage = calculate_stop_performance(behaviour_matrix, stop_trial_indicies)
        tone_d_prime = get_tone_v_no_tone_d_prime(base_directory)
        np.save(os.path.join(save_directory, "stop_trial_correct_reject_percentage.npy"), stop_trial_correct_reject_percentage)
        np.save(os.path.join(save_directory, "stop_trial_false_alarm_percentage.npy"), stop_trial_false_alarm_percentage)
        np.save(os.path.join(save_directory, "tone_d_prime.npy"), tone_d_prime)
        print("stop_trial_correct_reject_percentage", stop_trial_correct_reject_percentage)
        print("stop_trial_false_alarm_percentage", stop_trial_false_alarm_percentage)





def get_hit_trials(behaviour_matrix):

    hit_trial_indicies = []
    n_trials =np.shape(behaviour_matrix)[0]
    for trial_index in range(n_trials):
        trial_data = behaviour_matrix[trial_index]
        trial_type = trial_data[1]
        trial_outcome = trial_data[6]

        if trial_type == 0 and trial_outcome == 1:
            hit_trial_indicies.append(trial_index)

    hit_trial_indicies = np.array(hit_trial_indicies)
    return hit_trial_indicies


def get_go_trial_misses(behaviour_matrix):
    trial_indicies = []
    n_trials =np.shape(behaviour_matrix)[0]
    for trial_index in range(n_trials):
        trial_data = behaviour_matrix[trial_index]
        trial_type = trial_data[1]
        trial_outcome = trial_data[6]

        if trial_type == 0 and trial_outcome == 0:
            trial_indicies.append(trial_index)

    trial_indicies = np.array(trial_indicies)
    return trial_indicies


def get_delay_trial_misses(behaviour_matrix):
    trial_indicies = []
    n_trials =np.shape(behaviour_matrix)[0]
    for trial_index in range(n_trials):
        trial_data = behaviour_matrix[trial_index]
        trial_type = trial_data[1]
        trial_outcome = trial_data[6]

        if trial_type == 1 and trial_outcome == 0:
            trial_indicies.append(trial_index)

    trial_indicies = np.array(trial_indicies)
    return trial_indicies


def get_correct_delay_trials(behaviour_matrix):
    trial_indicies = []
    n_trials = np.shape(behaviour_matrix)[0]
    for trial_index in range(n_trials):
        trial_data = behaviour_matrix[trial_index]
        trial_type = trial_data[1]
        trial_outcome = trial_data[6]

        if trial_type == 1 and trial_outcome == 1:
            trial_indicies.append(trial_index)

    trial_indicies = np.array(trial_indicies)
    return trial_indicies



def get_correct_stop_trials(behaviour_matrix):
    trial_indicies = []
    n_trials = np.shape(behaviour_matrix)[0]
    for trial_index in range(n_trials):
        trial_data = behaviour_matrix[trial_index]
        trial_type = trial_data[1]
        trial_outcome = trial_data[6]

        if trial_type == 2 and trial_outcome == 1:
            trial_indicies.append(trial_index)

    trial_indicies = np.array(trial_indicies)
    return trial_indicies



def get_failed_stop_trials(behaviour_matrix):
    trial_indicies = []
    n_trials = np.shape(behaviour_matrix)[0]
    for trial_index in range(n_trials):
        trial_data = behaviour_matrix[trial_index]
        trial_type = trial_data[1]
        trial_outcome = trial_data[6]

        if trial_type == 2 and trial_outcome == 2:
            trial_indicies.append(trial_index)

    trial_indicies = np.array(trial_indicies)
    return trial_indicies


def get_premature_trials(behaviour_matrix):
    trial_indicies = []
    n_trials =np.shape(behaviour_matrix)[0]
    for trial_index in range(n_trials):
        trial_data = behaviour_matrix[trial_index]
        trial_type = trial_data[1]
        trial_outcome = trial_data[6]

        if trial_type == 1 and trial_outcome == 2:
            trial_indicies.append(trial_index)

    trial_indicies = np.array(trial_indicies)
    return trial_indicies




def get_delay_trials_with_response(behaviour_matrix):
    trial_indicies = []
    n_trials = np.shape(behaviour_matrix)[0]
    for trial_index in range(n_trials):
        trial_data = behaviour_matrix[trial_index]
        trial_type = trial_data[1]
        trial_outcome = trial_data[6]

        if trial_type == 1:
            if trial_outcome != 0:
                trial_indicies.append(trial_index)
    return trial_indicies




def get_hit_reaction_times(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Get Hit Trials
    hit_trial_indicies = get_hit_trials(behaviour_matrix)

    # Get Hit Trial RTs
    hit_trial_rts = behaviour_matrix[hit_trial_indicies, 4]

    return hit_trial_rts


def get_delay_reaction_times(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Get Hit Trials
    hit_trial_indicies = get_hit_trials(behaviour_matrix)

    # Get Hit Trial RTs
    hit_trial_rts = behaviour_matrix[hit_trial_indicies, 4]

    return hit_trial_rts



def get_correct_delay_reaction_times(base_directory, post_drift=True):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Get Correct Delay Trials
    delay_trial_rts = []
    n_trials = np.shape(behaviour_matrix)[0]
    for trial_index in range(n_trials):
        trial_data = behaviour_matrix[trial_index]

        # Check Is Delay Trial
        if trial_data[1] == 1:

            # Check Correct
            if trial_data[6] == 1:

                # Get Trial RT and Drift Time
                trial_rt = trial_data[4]
                trial_delay_time = trial_data[5]

                if post_drift == True:
                    post_drift_delay_time = trial_rt - trial_delay_time
                    delay_trial_rts.append(post_drift_delay_time)

                else:
                    delay_trial_rts.append(trial_rt)

    return delay_trial_rts





def correlate_delay_duration_and_rt(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Get Correct Delay Trials
    delay_duration_list = []
    rt_list = []

    n_trials = np.shape(behaviour_matrix)[0]
    for trial_index in range(n_trials):
        trial_data = behaviour_matrix[trial_index]

        # Check Is Delay Trial
        if trial_data[1] == 1:

            # Check Correct
            if trial_data[6] == 1:

                # Get Trial RT and Drift Time
                trial_rt = trial_data[4]
                trial_delay_time = trial_data[5]

                post_drift_rt = np.subtract(trial_rt, trial_delay_time)

                delay_duration_list.append(trial_delay_time)
                rt_list.append(post_drift_rt)


    plt.scatter(delay_duration_list, rt_list)
    plt.show()





def get_premature_reaction_times(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Get Premature Trials
    premature_trials = get_premature_trials(behaviour_matrix)

    # Get Premature Trial RTs
    premature_trial_rts = behaviour_matrix[premature_trials, 4]

    return premature_trial_rts


def get_delay_trials_which_have_not_yet_drifted(behaviour_matrix, bin_start, bin_stop):

    trial_index_list = []
    n_trials = np.shape(behaviour_matrix)[0]

    for trial_index in range(n_trials):
        trial_data = behaviour_matrix[trial_index]
        trial_drift_time = trial_data[5]
        trial_reaction_time = trial_data[4]

        # If Trial Never Drifts - Check We Have not licked by the start of the window
        if np.isnan(trial_drift_time):
            if trial_reaction_time > bin_start:
                trial_index_list.append(trial_index)

        # If Trial Drifts - Check Drift Is
        elif trial_drift_time > bin_stop:
            trial_index_list.append(trial_index)

    return trial_index_list


def filter_trials_by_reaction_window(behaviour_martrix, trial_index_list, window_stop):

    filtered_trial_list = []
    for trial_index in trial_index_list:
        trial_data = behaviour_martrix[trial_index]
        trial_reaction_time = trial_data[4]
        if trial_reaction_time <= window_stop:
            filtered_trial_list.append(trial_index)

    return filtered_trial_list



def get_performance_by_bin(base_directory, bin_width=250):

    """
    For Each Bin -
    For Delay Trials which have not yet drifted
    What percentage have been waited
    What percentage have licked either before or after

    Go Trials
    what percentage have an RT < bi n end
    """

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Get Go Trials
    go_trial_indicies = np.where(behaviour_matrix[:, 1]==0)[0]
    go_trial_rts = behaviour_matrix[go_trial_indicies, 4]
    n_go_trials = len(go_trial_indicies)

    # Create Bins
    bin_start_list = list(range(500, 2000, bin_width))
    bin_stop_list = np.add(bin_start_list, bin_width)
    n_bins = len(bin_start_list)

    # Create Bin Score Lists
    bin_delay_performance_list = []
    bin_go_performance_list = []

    # Iterate Through Each Bin
    for bin_index in range(n_bins):
        bin_start = bin_start_list[bin_index]
        bin_stop = bin_stop_list[bin_index]

        # Get Delay Trials Which Had Not Drifted By The End of This Window
        window_delay_trials = get_delay_trials_which_have_not_yet_drifted(behaviour_matrix, bin_start, bin_stop)

        # Get Proportion of these trials where lick happend prior To End of this window
        window_delay_error_trials = filter_trials_by_reaction_window(behaviour_matrix, window_delay_trials, bin_stop)

        # Get Bin Delay Performance
        n_delay_trials = len(window_delay_trials)
        n_delay_errors = len(window_delay_error_trials)
        print("bin_stop", bin_stop)
        print("n_delay_trials", n_delay_trials)
        print("n_delay_errors", n_delay_errors)

        if n_delay_trials > 0:
            bin_delay_performance = float(n_delay_errors) / n_delay_trials
        else:
            bin_delay_performance = np.nan

        bin_delay_performance_list.append(bin_delay_performance)


        # Get Bin Go Performance
        n_bin_go_trials = len(np.where(go_trial_rts <= bin_stop)[0])
        bin_go_performance = float(n_bin_go_trials) / n_go_trials
        bin_go_performance_list.append(bin_go_performance)

    # Save This
    print("bin_go_performance_list", bin_go_performance_list)
    print("bin_delay_performance_list", bin_delay_performance_list)
    np.save(os.path.join(base_directory, "Behaviour_Analysis", "bin_delay_performance_list.npy"), bin_delay_performance_list)
    np.save(os.path.join(base_directory, "Behaviour_Analysis", "bin_go_performance_list.npy"), bin_go_performance_list)

    plot_performance_by_bin(base_directory, bin_start_list, bin_width, bin_delay_performance_list, bin_go_performance_list)



def get_correct_delay_distribution(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Get Correct Trials
    correct_delay_trials = get_correct_delay_trials(behaviour_matrix)

    # Get Drift Time For Each Of These Trials
    correct_drift_times = behaviour_matrix[correct_delay_trials, 5]

    return correct_drift_times


def get_false_alarm_distribution(base_directory):

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Get Incorrect delay Trials
    false_alarm_trials = get_false_alarm_delay_trials(behaviour_matrix)

    # False Alarm Lick Times
    false_alarm_rts = behaviour_matrix[false_alarm_trials, 4]

    return false_alarm_rts


def plot_performance_by_bin(base_directory, bin_start_list, bin_size, bin_delay_performance_list, bin_go_performance_list):

    bin_go_performance_list = np.multiply(bin_go_performance_list, 100)
    bin_delay_performance_list = np.multiply(bin_delay_performance_list, 100)

    x_ticks = np.concatenate([bin_start_list, [bin_start_list[-1]+bin_size]])
    x_values = np.add(bin_start_list, bin_size)

    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1,1,1)

    axis_1.plot(x_values, bin_go_performance_list, c='g')
    axis_1.scatter(x_values, bin_go_performance_list, c='g')

    axis_1.plot(x_values, bin_delay_performance_list, c='b')
    axis_1.scatter(x_values, bin_delay_performance_list, c='b')
    axis_1.set_xticks(x_ticks)

    axis_1.set_ylim([0, 110])

    y_ticks = list(range(0, 110, 10))
    print("y_ticks", y_ticks)
    axis_1.set_yticks(y_ticks)

    # Remove Borders
    axis_1.spines[['right', 'top']].set_visible(False)

    axis_1.set_ylabel("Lick Percentage")
    axis_1.set_xlabel("Delay Duration")

    plt.savefig(os.path.join(base_directory, "Behaviour_Analysis", "Performance_by_Bin.png"))
    plt.close()


