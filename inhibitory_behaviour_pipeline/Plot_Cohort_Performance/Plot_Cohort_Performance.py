import os
import numpy as np
import matplotlib.pyplot as plt


def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def check_folder_is_session(folder):

    folder_is_session = False
    folder_component_list = folder.split("_")

    if len(folder_component_list[0]) == 4 and is_integer(folder_component_list[0]):
        if len(folder_component_list[1]) == 2 and is_integer(folder_component_list[1]):
            if len(folder_component_list[2]) == 2 and is_integer(folder_component_list[2]):
                folder_is_session = True

    return folder_is_session


def get_mouse_sessions(mouse_directory):
    sub_directory_list = os.listdir(mouse_directory)
    mouse_sessions = []
    for folder in sub_directory_list:
        if check_folder_is_session(folder):
            mouse_sessions.append(folder)
    return mouse_sessions



def load_mouse_performance(mouse_data_root, mouse_sessions):

    mouse_delay_d_prime = []
    mouse_stop_d_prime = []

    # Iterate Through Mice
    for session in mouse_sessions:

        # Get FIle Names
        static_d_prime_file = os.path.join(mouse_data_root, session, "Behaviour_Analysis", "static_drift_d_prime.npy")
        tone_d_prime_file = os.path.join(mouse_data_root, session, "Behaviour_Analysis", "tone_d_prime.npy")
        behaviour_matrix_file = os.path.join(mouse_data_root, session, "Behaviour_Matrix.npy")

        # Check Min Trials
        if os.path.exists(behaviour_matrix_file):
            behaviour_matrix = np.load(behaviour_matrix_file)
            n_trials = np.shape(behaviour_matrix)[0]
            if n_trials > 50:

                if os.path.exists(static_d_prime_file):
                    session_static_d_prime = np.load(static_d_prime_file)
                    mouse_delay_d_prime.append(session_static_d_prime)

                if os.path.exists(tone_d_prime_file):
                    session_tone_d_prime = np.load(tone_d_prime_file)
                    mouse_stop_d_prime.append(session_tone_d_prime)

    return mouse_delay_d_prime, mouse_stop_d_prime




def get_cohort_performance(data_root, mouse_list):

    cohort_delay_d_prime = []
    cohort_stop_d_prime = []

    # Iterate Through Mice
    for mouse_directory in mouse_list:
        mouse_data_root = os.path.join(data_root, mouse_directory)
        print("mouse_data_root", mouse_data_root)

        # Get Mouse Sessions
        mouse_sessions = get_mouse_sessions(mouse_data_root)

        # Get Mouse Performance
        mouse_delay_performance, mouse_stop_performance = load_mouse_performance(mouse_data_root, mouse_sessions)
        cohort_delay_d_prime.append(mouse_delay_performance)
        cohort_stop_d_prime.append(mouse_stop_performance)

    return cohort_delay_d_prime, cohort_stop_d_prime


def plot_performance(performance_list, colour_list):

    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1,1,1)

    n_mice = len(performance_list)
    for mouse_index in range(n_mice):
        mouse_performance = performance_list[mouse_index]
        mouse_colour = colour_list[mouse_index]
        axis_1.plot(mouse_performance, c=mouse_colour, alpha=0.5)
        axis_1.scatter(list(range(len(mouse_performance))), mouse_performance, c=mouse_colour, alpha=0.5)

    axis_1.axhline(2, c='k', linestyle='dashed')
    axis_1.set_ylim([-1, 4])
    axis_1.spines[['right', 'top']].set_visible(False)
    plt.show()


# Set Data Directories
data_root = r"C:\Users\matth\Dropbox\Behaviour_Data"
data_root = r"C:\Users\matth\Dropbox\Analysed_Data"
data_root = r"C:\Users\harveym\Dropbox\Analysed_Data"
data_root = r"Z:\home\shared\harveym\Analysed_Data"


mouse_list = [
    r"Cohort 4\BRAC12136.4a_White",
    r"Cohort 4\BRAC12136.4b_Pink",
    r"Cohort 5\BRAC12700.2i Purple (MH3)",
    r"Cohort 5\BRAC12700.2h Green (MH1)",
    r"Cohort 5\BRAC12700.2j Blue (MH6)",
    r"Cohort 5\BRAC12934.2a Aqua (MH7)",
    r"Cohort 5\BRAC12934.2b Black (MH8)"
]

mouse_list = [
    r"Cohort_6\BRAC12546.5c_Green",
    r"Cohort_6\BRAC12546_5b_Brown",
    r"Cohort_6\BRAC13080_3a_Pink",
    r"Cohort_6\BRAC13223.4d_White",
    r"Cohort_6\BRAC13223.4e_Blue",
    r"Cohort_6\BRAC13379_4e_Orange",
]

mouse_colours = [
    "green",
    "brown",
    "pink",
    "k",
    "blue",
    "orange",
]

# Load Cohort Performance
cohort_delay_d_prime, cohort_stop_d_prime =  get_cohort_performance(data_root, mouse_list)

plot_performance(cohort_delay_d_prime, mouse_colours)
#plot_performance(cohort_stop_d_prime, mouse_colours)