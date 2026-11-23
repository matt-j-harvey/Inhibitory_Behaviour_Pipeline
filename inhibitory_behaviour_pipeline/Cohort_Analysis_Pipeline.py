import os
import Organise_DAQ_Files
import Set_Lick_Thresholds
import Session_Analysis_Pipeline


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





# Set Data Directories
data_directory_root = r"Z:\home\shared\harveym\Behaviour_Data"
output_directory_root = r"Z:\home\shared\harveym\Analysed_Data"

mouse_directory_list = [
                        # r"Cohort 4\BRAC12136.4a_White",

                        # r"Cohort 4\BRAC12136.4b_Pink",
                        # r"Cohort 5\BRAC12688.4e Mint (MH8)",
                        # r"Cohort 5\BRAC12700.2i Purple (MH3)",
                        # r"Cohort 5\BRAC12700.2j Blue (MH6)",
                        # r"Cohort 5\BRAC12934.2a Aqua (MH7)",
                        # r"Cohort 5\BRAC12700.2k Brown (MH5)",
                        # r"Cohort 5\BRAC12700.2h Green (MH1)"
                        # r"Cohort 5\BRAC12934.2b Black (MH8)",

                        r"Cohort_6\BRAC12546.5c_Green",
                        r"Cohort_6\BRAC12546_5b_Brown",
                        r"Cohort_6\BRAC13080_3a_Pink",
                        r"Cohort_6\BRAC13223.4d_White",
                        r"Cohort_6\BRAC13223.4e_Blue",
                        r"Cohort_6\BRAC13379_4e_Orange",



                        ]

# Organise DAQ Files
for mouse_directory in mouse_directory_list:
    Organise_DAQ_Files.organise_daq_files_by_day(os.path.join(data_directory_root, mouse_directory))


# Iterate Through Mice
for mouse_directory in mouse_directory_list:

    mouse_data_root = os.path.join(data_directory_root, mouse_directory)
    mouse_output_root = os.path.join(output_directory_root, mouse_directory)
    print("mouse_data_root", mouse_data_root)
    print("mouse_output_root", mouse_data_root)

    # Get Mouse Sessions
    mouse_sessions = get_mouse_sessions(mouse_data_root)

    # Set Lick Thresholds
    #Set_Lick_Thresholds.set_lick_thresholds(mouse_data_root, mouse_sessions)

    for session in mouse_sessions:
        print(mouse_directory, session)

        # Check If Already Analysed
        if not os.path.exists(os.path.join(mouse_output_root, session, "Truncated_Behaviour_Matrix.npy")):
            Session_Analysis_Pipeline.behaviour_analysis_pipeline(mouse_data_root, session, mouse_output_root)

            
"""
    # Get Subdirectory List
"""

