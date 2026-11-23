import os
import numpy as np
import matplotlib.pyplot as plt

from inhibitory_behaviour_pipeline.Behaviour_Analysis_Utils import Behaviour_Analysis_Utils, Behaviour_Analysis_Functions
from inhibitory_behaviour_pipeline.Lick_Raster_Plotting_Functions import Get_Lick_Raster_Data, Create_Lick_Raster


def create_group_rasters(mouse_list, session_list, preceeding_window, following_window):


    group_go_raster = []
    group_correct_delay_raster = []
    group_premature_delay_raster = []
    group_correct_stop_raster = []
    group_failed_stop_raster = []

    # Loop Through Each Mouse
    n_mice = len(mouse_list)
    for mouse_index in range(n_mice):

        mouse_root = mouse_list[mouse_index]
        mouse_sessions = session_list[mouse_index]

        # Loop Through Each Session
        for session in mouse_sessions:

            base_directory = os.path.join(data_directory_root, mouse_root, session)
            print("base directory", base_directory)

            # Load Lick Threshold
            lick_threshold_file = os.path.join(base_directory, "Lick_Threshold.npy")
            print("lick_threshold_file", lick_threshold_file)

            if os.path.exists(lick_threshold_file):
                lick_threshold = np.load(lick_threshold_file)
            else:
                lick_threshold = 3

            # Load Lick Trace
            lick_trace = Behaviour_Analysis_Utils.load_lick_trace(base_directory)

            # Load Behaviour Matrix
            behaviour_matrix = np.load(os.path.join(base_directory, "Behaviour_Matrix.npy"), allow_pickle=True)

            # Get Trial Indicies
            hit_trial_indicies = Behaviour_Analysis_Functions.get_hit_trials(behaviour_matrix)
            correct_delay_trial_indicies = Behaviour_Analysis_Functions.get_correct_delay_trials(behaviour_matrix)
            premature_delay_trial_indicies = Behaviour_Analysis_Functions.get_premature_trials(behaviour_matrix)
            correct_stop_trial_indicies = Behaviour_Analysis_Functions.get_correct_stop_trials(behaviour_matrix)
            failed_stop_trial_indicies = Behaviour_Analysis_Functions.get_failed_stop_trials(behaviour_matrix)

            # Get Data Matricies
            hit_trial_raster_matrix = Get_Lick_Raster_Data.get_lick_raster_data(behaviour_matrix, hit_trial_indicies, preceeding_window, following_window, lick_trace, lick_threshold)
            correct_delay_trial_matrix = Get_Lick_Raster_Data.get_lick_raster_data(behaviour_matrix, correct_delay_trial_indicies, preceeding_window, following_window, lick_trace, lick_threshold)
            premature_delay_trial_matrix = Get_Lick_Raster_Data.get_lick_raster_data(behaviour_matrix, premature_delay_trial_indicies, preceeding_window, following_window, lick_trace, lick_threshold)
            correct_stop_trial_matrix = Get_Lick_Raster_Data.get_lick_raster_data(behaviour_matrix, correct_stop_trial_indicies, preceeding_window, following_window, lick_trace, lick_threshold)
            failed_stop_trial_matrix = Get_Lick_Raster_Data.get_lick_raster_data(behaviour_matrix, failed_stop_trial_indicies, preceeding_window, following_window, lick_trace, lick_threshold)

            print("hit_trial_raster_matrix", np.shape(hit_trial_raster_matrix))

            # Add To Lists
            group_go_raster.append(hit_trial_raster_matrix)
            group_correct_delay_raster.append(correct_delay_trial_matrix)
            group_premature_delay_raster.append(premature_delay_trial_matrix)
            group_correct_stop_raster.append(correct_stop_trial_matrix)
            group_failed_stop_raster.append(failed_stop_trial_matrix)

    # Concataneate Lists
    group_go_raster = np.vstack(group_go_raster)
    group_correct_delay_raster = np.vstack(group_correct_delay_raster)
    group_premature_delay_raster = np.vstack(group_premature_delay_raster)
    group_correct_stop_raster = np.vstack(group_correct_stop_raster)
    group_failed_stop_raster = np.vstack(group_failed_stop_raster)

    np.save(os.path.join(output_root, "Group_Rasters", "group_go_raster.npy"), group_go_raster)
    np.save(os.path.join(output_root, "Group_Rasters", "group_correct_delay_raster.npy"), group_correct_delay_raster)
    np.save(os.path.join(output_root, "Group_Rasters", "group_premature_delay_raster.npy"), group_premature_delay_raster)
    np.save(os.path.join(output_root, "Group_Rasters", "group_correct_stop_raster.npy"), group_correct_stop_raster)
    np.save(os.path.join(output_root, "Group_Rasters", "group_failed_stop_raster.npy"), group_failed_stop_raster)



def sort_raster(raster, metric):

    if metric == "rts":
        times = raster[:, 3]

    if metric == "drifts":
        times = raster[:, 0]

    if metric == "tone":
        times = raster[:, 2]

    sorting_indicies = np.argsort(times)
    raster = raster[sorting_indicies]
    return raster



def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

def plot_raster(raster, save_directory, title):

    figure_1 = plt.figure(figsize=(10,5))
    axis_1 = figure_1.add_subplot(1,1,1)
    axis_1.imshow(raster)

    forceAspect(axis_1, 5)

    plt.savefig(os.path.join(save_directory, title + ".svg"))
    plt.close()





# Set Data Directories
data_directory_root = r"C:\Users\matth\Dropbox\Behaviour_Data"
output_root = r"C:\Fens_Analysis"


# Load Post Criteria Session Dict
session_dict = np.load(os.path.join(output_root, "Sessions_Above_Both_Criteria.npy"), allow_pickle=True)[()]
mouse_list = session_dict['data_root_list']
session_list = session_dict['session_lists']

preceeding_window = 0
following_window = 6000

#create_group_rasters(mouse_list, session_list, preceeding_window, following_window)

group_go_raster = np.load(os.path.join(output_root, "Group_Rasters", "group_go_raster.npy"))
group_correct_delay_raster = np.load(os.path.join(output_root, "Group_Rasters", "group_correct_delay_raster.npy"))
group_premature_delay_raster = np.load(os.path.join(output_root, "Group_Rasters", "group_premature_delay_raster.npy"))
group_correct_stop_raster = np.load(os.path.join(output_root, "Group_Rasters", "group_correct_stop_raster.npy"))
group_failed_stop_raster = np.load(os.path.join(output_root, "Group_Rasters", "group_failed_stop_raster.npy"))
print("group_go_raster",np.shape(group_go_raster))
print("group_correct_delay_raster",np.shape(group_correct_delay_raster))
print("group_premature_delay_raster",np.shape(group_premature_delay_raster))
print("group_correct_stop_raster",np.shape(group_correct_stop_raster))
print("group_failed_stop_raster",np.shape(group_failed_stop_raster))

combined_stop_raster = np.vstack([group_correct_stop_raster, group_failed_stop_raster])

# Sort Lick Rasters
group_go_raster = sort_raster(group_go_raster, "rts")
group_correct_delay_raster = sort_raster(group_correct_delay_raster, "rts")
group_premature_delay_raster = sort_raster(group_premature_delay_raster, "rts")
group_correct_stop_raster = sort_raster(group_correct_stop_raster, "drifts")
group_failed_stop_raster = sort_raster(group_failed_stop_raster, "rts")
combined_stop_raster = sort_raster(combined_stop_raster, "drifts")

# Convert To Lick Raster
group_go_raster_image = Create_Lick_Raster.create_combined_psth(group_go_raster, preceeding_window, following_window, fill_static=False, fill_drift=False)
group_correct_delay_raster_image = Create_Lick_Raster.create_combined_psth(group_correct_delay_raster, preceeding_window, following_window, fill_static=False, fill_drift=False)
group_premature_delay_raster_image = Create_Lick_Raster.create_combined_psth(group_premature_delay_raster, preceeding_window, following_window, fill_static=False, fill_drift=False)
group_correct_stop_raster_image = Create_Lick_Raster.create_combined_psth(group_correct_stop_raster, preceeding_window, following_window, fill_static=False, fill_drift=False)
group_failed_stop_raster_image = Create_Lick_Raster.create_combined_psth(group_failed_stop_raster, preceeding_window, following_window, fill_static=False, fill_drift=False)
combined_stop_raster_image = Create_Lick_Raster.create_combined_psth(combined_stop_raster, preceeding_window, following_window, fill_static=False, fill_drift=False)


save_directory = r"C:\Users\matth\OneDrive - The Francis Crick Institute\Impulsivity Project\Posters\FENS_2026\Lick_Raster_Images"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

plot_raster(group_go_raster_image, save_directory, "Go Hits")
plot_raster(group_correct_delay_raster_image, save_directory, "Correct Delays")
plot_raster(group_premature_delay_raster_image, save_directory, "Premature Delays")
plot_raster(group_correct_stop_raster_image, save_directory, "Correct Stop")
plot_raster(group_failed_stop_raster_image, save_directory, "Failed Stop")
plot_raster(combined_stop_raster_image, save_directory, "Combined Stop")