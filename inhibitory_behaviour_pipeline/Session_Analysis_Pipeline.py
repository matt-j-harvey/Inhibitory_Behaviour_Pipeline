import os
import matplotlib.pyplot as plt
import numpy as np

import Set_Lick_Thresholds
import Create_Stop_Behaviour_Matrix


from inhibitory_behaviour_pipeline.Behaviour_Analysis_Utils import Behaviour_Analysis_Utils, Behaviour_Analysis_Functions
from inhibitory_behaviour_pipeline.Plotting_Functions import Behaviour_Plotting_Functions
from inhibitory_behaviour_pipeline.Lick_Raster_Plotting_Functions import Plot_Lick_Raster





def behaviour_analysis_pipeline(data_root, session, output_root):

    # Create Directories
    data_directory = os.path.join(data_root, session)
    output_directory = os.path.join(output_root, session)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Create Behaviour Matrix
    Create_Stop_Behaviour_Matrix.create_behaviour_matrix(data_directory, output_directory)

    # Create Behaviour Analysis Folder
    behaviour_analysis_folder = os.path.join(output_directory, "Behaviour_Analysis")
    if not os.path.exists(behaviour_analysis_folder):
        os.mkdir(behaviour_analysis_folder)

    # Load Behaviour Matrix
    behaviour_matrix = np.load(os.path.join(output_directory, "Behaviour_Matrix.npy"), allow_pickle=True)[()]

    # Truncate Behaviour Matrix
    truncated_behaviour_matrix = Behaviour_Analysis_Functions.truncate_behaviour_matrix(behaviour_matrix, threshold_n=3)

    # Save Truncated Matrix
    np.save(os.path.join(output_directory, "Truncated_Behaviour_Matrix.npy"), truncated_behaviour_matrix)

    # Save Truncated Behaviour Matrix as CSV
    Create_Stop_Behaviour_Matrix.save_behaviour_matrix_as_csv(output_directory, truncated_behaviour_matrix, filename="Truncated_Behaviour_Matrix.csv")

    # Get Performance
    Behaviour_Analysis_Functions.get_performance(output_directory, truncated_behaviour_matrix)
    Behaviour_Plotting_Functions.plot_performance(output_directory)
    Behaviour_Plotting_Functions.plot_performance_d_prime(output_directory)

    # Plot Hit and Premature Reaction Times
    hit_trial_rts = Behaviour_Analysis_Functions.get_hit_reaction_times(truncated_behaviour_matrix)
    premature_trial_rts = Behaviour_Analysis_Functions.get_premature_reaction_times(truncated_behaviour_matrix)
    Behaviour_Plotting_Functions.overlay_rt_distributions_density(output_directory, hit_trial_rts, premature_trial_rts, title="Hit v Premature RTs")
    Behaviour_Plotting_Functions.overlay_rt_distributions(output_directory, hit_trial_rts, premature_trial_rts, title="Hit v Premature RTs Number")

    # Plot Post Wait RTs
    delay_trial_rts = Behaviour_Analysis_Functions.get_correct_delay_reaction_times(truncated_behaviour_matrix)
    Behaviour_Plotting_Functions.overlay_rt_distributions_density(output_directory, hit_trial_rts, delay_trial_rts, title="Hit v Post Wait Hits")

    # Plot CR Wait Time Distribution
    correct_delay_distribution = Behaviour_Analysis_Functions.get_correct_delay_distribution(truncated_behaviour_matrix)
    Behaviour_Plotting_Functions.overlay_rt_distributions_density(output_directory, hit_trial_rts, correct_delay_distribution, title="Hit v Succsesfull Wait Times")






    # Plot PSTHs
    """
    PSTH_Plotting_Functions.plot_session_psth(base_directory)
    PSTH_Plotting_Functions.plot_failed_wait_raster_combined(base_directory)
    PSTH_Plotting_Functions.plot_combined_psth_stopping(base_directory)
    Behaviour_Plotting_Functions.plot_psths(base_directory)
    PSTH_Plotting_Functions.plot_delay_correct_raster(base_directory)
    """

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
    """


