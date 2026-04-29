import os
import matplotlib.pyplot as plt
import numpy as np

import Set_Lick_Thresholds
import Create_Stop_Behaviour_Matrix

from Inhibitory_Behaviour_Pipeline.Behaviour_Analysis_Utils import Behaviour_Analysis_Utils, Behaviour_Analysis_Functions
from Inhibitory_Behaviour_Pipeline.Plotting_Functions import Behaviour_Plotting_Functions
from Inhibitory_Behaviour_Pipeline.Lick_Raster_Plotting_Functions import Plot_Lick_Raster

def behaviour_analysis_pipeline(base_directory):

    # Create Behaviour Matrix
    Create_Stop_Behaviour_Matrix.create_behaviour_matrix(base_directory)

    # Create Behaviour Analysis Folder
    behaviour_analysis_folder = os.path.join(base_directory, "Behaviour_Analysis")
    if not os.path.exists(behaviour_analysis_folder):
        os.mkdir(behaviour_analysis_folder)

    # Get Performance
    Behaviour_Analysis_Functions.get_performance(base_directory)
    Behaviour_Plotting_Functions.plot_performance(base_directory)
    Behaviour_Plotting_Functions.plot_performance_d_prime(base_directory)

    # Plot Hit and Premature Reaction Times
    hit_trial_rts = Behaviour_Analysis_Functions.get_hit_reaction_times(base_directory)
    premature_trial_rts = Behaviour_Analysis_Functions.get_premature_reaction_times(base_directory)
    Behaviour_Plotting_Functions.overlay_rt_distributions_density(base_directory, hit_trial_rts, premature_trial_rts, title="Hit v Premature RTs")
    Behaviour_Plotting_Functions.overlay_rt_distributions(base_directory, hit_trial_rts, premature_trial_rts, title="Hit v Premature RTs Number")

    # Plot Post Wait RTs
    delay_trial_rts = Behaviour_Analysis_Functions.get_correct_delay_reaction_times(base_directory)
    Behaviour_Plotting_Functions.overlay_rt_distributions_density(base_directory, hit_trial_rts, delay_trial_rts, title="Hit v Post Wait Hits")

    # Plot CR Wait Time Distribution
    correct_delay_distribution = Behaviour_Analysis_Functions.get_correct_delay_distribution(base_directory)
    Behaviour_Plotting_Functions.overlay_rt_distributions_density(base_directory, hit_trial_rts, correct_delay_distribution, title="Hit v Succsesfull Wait Times")


    # Plot PSTHs
    """
    PSTH_Plotting_Functions.plot_session_psth(base_directory)
    PSTH_Plotting_Functions.plot_failed_wait_raster_combined(base_directory)
    PSTH_Plotting_Functions.plot_combined_psth_stopping(base_directory)
    Behaviour_Plotting_Functions.plot_psths(base_directory)
    PSTH_Plotting_Functions.plot_delay_correct_raster(base_directory)
    """

    # Plot Hit and Premature Reaction Times
    hit_trial_rts = Behaviour_Analysis_Functions.get_hit_reaction_times(base_directory)
    premature_trial_rts = Behaviour_Analysis_Functions.get_premature_reaction_times(base_directory)
    Behaviour_Plotting_Functions.overlay_rt_distributions_density(base_directory, hit_trial_rts, premature_trial_rts, title="Hit v Premature RTs")
    Behaviour_Plotting_Functions.overlay_rt_distributions(base_directory, hit_trial_rts, premature_trial_rts, title="Hit v Premature RTs Number")

    # Plot Post Wait RTs
    delay_trial_rts = Behaviour_Analysis_Functions.get_correct_delay_reaction_times(base_directory)
    Behaviour_Plotting_Functions.overlay_rt_distributions_density(base_directory, hit_trial_rts, delay_trial_rts, title="Hit v Post Wait Hits")

    # Plot CR Wait Time Distribution
    correct_delay_distribution = Behaviour_Analysis_Functions.get_correct_delay_distribution(base_directory)
    Behaviour_Plotting_Functions.overlay_rt_distributions_density(base_directory, hit_trial_rts, correct_delay_distribution, title="Hit v Succsesfull Wait Times")



flat_session_list = [r"Cohort 4\BRAC12136.4a_White\2026_04_29"]
data_root = r"C:\Users\matth\Dropbox\Behaviour_Data"

# Set Lick Thresholds
Set_Lick_Thresholds.set_lick_thresholds(data_root, flat_session_list)

# Analyse Sessions
for session in flat_session_list:
    behaviour_analysis_pipeline(os.path.join(data_root, session))

