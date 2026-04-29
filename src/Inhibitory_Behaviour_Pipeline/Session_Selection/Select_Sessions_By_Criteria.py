import numpy as np
import os

from Inhibitory_Behaviour_Pipeline.Behaviour_Analysis_Utils import Behaviour_Analysis_Functions


def check_session_has_all_required_trial_types(behaivour_matrix):
    trial_types = behaivour_matrix[:, 1]
    go_count = np.count_nonzero(trial_types == 0)
    delay_count = np.count_nonzero(trial_types == 1)
    stop_count = np.count_nonzero(trial_types == 2)

    if go_count > 1 and delay_count > 1 and stop_count > 1:
        return True
    else:
        return False


def check_session_criteria_both(data_root, session):

    # Set Trial Status as False By Default
    trial_status = False

    base_directory = os.path.join(data_root, session)

    # Check if even been analysed
    if not os.path.exists(os.path.join(base_directory,  "Behaviour_Matrix.npy")):
        return trial_status

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"))

    # Must Have Go, Delay and Stop Trials
    required_trial_types = check_session_has_all_required_trial_types(behaviour_matrix)

    # Must Have Static / Drift d' > 2
    drift_d_prime = Behaviour_Analysis_Functions.get_static_v_drift_d_prime(base_directory)

    # Must Have Tone / No-Tone d' > 2
    tone_d_prime = Behaviour_Analysis_Functions.get_stop_d_prime(base_directory)

    """
    print("base directory", base_directory)
    print("drift_d_prime", drift_d_prime)
    print("tone_d_prime", tone_d_prime)
    """

    if required_trial_types == True:
        if drift_d_prime >= 1.99:
            if tone_d_prime >= 1.99:
                trial_status = True

    return trial_status





def check_session_criteria_delay(data_root, session):

    # Set Trial Status as False By Default
    trial_status = False

    base_directory = os.path.join(data_root, session)

    # Check if even been analysed
    if not os.path.exists(os.path.join(base_directory,  "Behaviour_Matrix.npy")):
        return trial_status

    # Must Have Static / Drift d' > 2
    drift_d_prime = Behaviour_Analysis_Functions.get_static_v_drift_d_prime(base_directory)

    if drift_d_prime >= 1.99:
            trial_status = True

    return trial_status




def check_folder_format(folder):
    split_folder = folder.split("_")
    if len(split_folder[0]) == 4:
        if len(split_folder[1]) == 2:
            if len(split_folder[2]) == 2:
                return True


def get_mouse_sessions_delay_and_stop(mouse_directory):

    mouse_subfolders = os.listdir(mouse_directory)
    mouse_sessions = []

    for folder in mouse_subfolders:

        # Check Is Date formatted
        is_session = check_folder_format(folder)
        if is_session == True:
            session_criteria = check_session_criteria_both(mouse_directory, folder)

            if session_criteria == True:
                mouse_sessions.append(folder)

    return mouse_sessions



def get_mouse_sessions_delay(mouse_directory):

    mouse_subfolders = os.listdir(mouse_directory)
    mouse_sessions = []

    for folder in mouse_subfolders:

        # Check Is Date formatted
        is_session = check_folder_format(folder)
        if is_session == True:
            session_criteria = check_session_criteria_delay(mouse_directory, folder)

            if session_criteria == True:
                mouse_sessions.append(folder)

    return mouse_sessions



mouse_list = [
    r"C:\Users\matth\Dropbox\Behaviour_Data\Cohort 3\BRAC_11935_1D_Pink",
    r"C:\Users\matth\Dropbox\Behaviour_Data\Cohort 3\BRAC_11935_1C_Black",
    r"C:\Users\matth\Dropbox\Behaviour_Data\Cohort 3\BRAC_11935_1A_Green",
    r"C:\Users\matth\Dropbox\Behaviour_Data\Cohort 3\BRAC_11766_1E_Purple",
    r"C:\Users\matth\Dropbox\Behaviour_Data\Cohort 2\BRAC_10695_4F_Blue",
]

# Check For Both Sesssions
"""
for mouse in mouse_list:
    mouse_sessions = get_mouse_sessions_delay_and_stop(mouse)
    print("Mouse", mouse)
    print("Selected Sessions")
    for session in mouse_sessions:
        print(session)
    print("")
"""


# Check Delay Only
for mouse in mouse_list:
    mouse_sessions = get_mouse_sessions_delay(mouse)
    print("Mouse", mouse)
    print("Selected Sessions")
    for session in mouse_sessions:
        print(session)
    print("")
