import matplotlib.pyplot as plt
import numpy as np
import os

from Inhibitory_Behaviour_Pipeline.Behaviour_Analysis_Utils import Behaviour_Analysis_Utils


def get_sessions_above_criteria(data_root, session_list):

    sessions_above_criteria = []
    delay_d_prime_list = []
    stop_d_prime_list = []

    for session in session_list:
        delay_d_prime = None
        stop_d_prime = None

        delay_d_prime_file = os.path.join(data_root, session, "Behaviour_Analysis", "static_drift_d_prime.npy")
        stop_d_prime_file = os.path.join(data_root, session, "Behaviour_Analysis", "tone_d_prime.npy")

        if os.path.exists(delay_d_prime_file):
            delay_d_prime = np.load(delay_d_prime_file)

        if os.path.exists(stop_d_prime_file):
            stop_d_prime = np.load(stop_d_prime_file)

        if delay_d_prime is not None and stop_d_prime is not None:
            if delay_d_prime >=2 and stop_d_prime >= 2:
                sessions_above_criteria.append(session)
                delay_d_prime_list.append(delay_d_prime)
                stop_d_prime_list.append(stop_d_prime)


    return sessions_above_criteria, delay_d_prime_list, stop_d_prime_list



def plot_mean_performance_above_criteria(group_delay_performance_list, group_stop_performance_list):

    # Create Figure
    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1,1,1)
    axis_1.set_ylim([0, 3.5])
    axis_1.set_xlim([-0.5, 1.5])
    axis_1.set_xticks([0, 1], ["Static d Prime", "Tone d Prime"])
    axis_1.axhline(2, c='k', linestyle='dashed')
    axis_1.set_xlim([-0.5, 1.5])
    axis_1.spines[['right', 'top']].set_visible(False)

    n_mice = len(group_delay_performance_list)
    for mouse_index in range(n_mice):
        mouse_delay_performance = group_delay_performance_list[mouse_index]
        mouse_stop_performance = group_stop_performance_list[mouse_index]
        mouse_mean_delay = np.mean(mouse_delay_performance)
        mouse_mean_stop = np.mean(mouse_stop_performance)

        axis_1.scatter([0, 1], [mouse_mean_delay, mouse_mean_stop])
        axis_1.plot([0, 1], [mouse_mean_delay, mouse_mean_stop])


    plt.show()


    pass





# Set Data Directories
data_directory_root = r"C:\Users\matth\Dropbox\Behaviour_Data"


mouse_directory_list = [
                        r"Cohort 2\BRAC_10695_4F_Blue",

                        r"Cohort 3\BRAC_11766_1E_Purple",
                        r"Cohort 3\BRAC_11935_1A_Green",
                        r"Cohort 3\BRAC_11935_1D_Pink",
                        r"Cohort 3\BRAC_11935_1C_Black",

                        r"Cohort 4\BRAC12136.4a_White",
                        r"Cohort 4\BRAC12136.4b_Pink",

                        r"Cohort 5\BRAC12700.2j Blue (MH6)",
                        r"Cohort 5\BRAC12700.2i Purple (MH3)",
                        r"Cohort 5\BRAC12934.2a Aqua (MH7)",
                        ]

output_root = r"C:\Fens_Analysis"


# Iterate Through Mice
group_delay_performance_list = []
group_stop_performance_list = []
group_root_directory_list = []
group_session_list = []

for mouse_directory in mouse_directory_list:

    mouse_data_root = os.path.join(data_directory_root, mouse_directory)
    print("mouse_data_root", mouse_data_root)

    # Get Mouse Sessions
    mouse_sessions = Behaviour_Analysis_Utils.get_mouse_sessions(mouse_data_root)

    # Get Sessions Above Criteria
    mouse_sessions_above_criteria, mouse_delay_d_prime_list, mouse_stop_d_prime_list = get_sessions_above_criteria(mouse_data_root, mouse_sessions)
    print("mouse_sessions_above_criteria", mouse_sessions_above_criteria)

    if len(mouse_sessions_above_criteria) > 0:
        group_root_directory_list.append(mouse_directory)
        group_session_list.append(mouse_sessions_above_criteria)
        group_delay_performance_list.append(mouse_delay_d_prime_list)
        group_stop_performance_list.append(mouse_stop_d_prime_list)


# Save Dict
post_session_dict = {
    "data_root_list":group_root_directory_list,
    "session_lists":group_session_list,
    "delay_performance_lists":group_delay_performance_list,
    "stop_performance_lists":group_stop_performance_list,
}

np.save(os.path.join(output_root, "Sessions_Above_Both_Criteria"), post_session_dict)

plot_mean_performance_above_criteria(group_delay_performance_list, group_stop_performance_list)