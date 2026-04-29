import numpy as np

def flatten_nested_list(nested_list):
    flat_list = []
    for mouse in nested_list:
        for session in mouse:
            flat_list.append(session)
    return flat_list



behaviour_criteria_meeting = [

    [r"Cohort 3\BRAC_11935_1D_Pink\2025_12_16"],

    [r"Cohort 3\BRAC_11935_1C_Black\2025_12_11",
     r"Cohort 3\BRAC_11935_1C_Black\2025_12_18"],

    [r"Cohort 3\BRAC_11935_1A_Green\2025_12_04",
     r"Cohort 3\BRAC_11935_1A_Green\2025_12_10",
     r"Cohort 3\BRAC_11935_1A_Green\2025_12_11",
     r"Cohort 3\BRAC_11935_1A_Green\2025_12_16",
     r"Cohort 3\BRAC_11935_1A_Green\2025_12_18"],

    [r"Cohort 3\BRAC_11766_1E_Purple\2025_12_09",
     r"Cohort 3\BRAC_11766_1E_Purple\2025_12_10",
     r"Cohort 3\BRAC_11766_1E_Purple\2025_12_11",
     r"Cohort 3\BRAC_11766_1E_Purple\2025_12_12",
     r"Cohort 3\BRAC_11766_1E_Purple\2025_12_15",
     r"Cohort 3\BRAC_11766_1E_Purple\2025_12_16",
     r"Cohort 3\BRAC_11766_1E_Purple\2025_12_18"],

    [r"Cohort 2\BRAC_10695_4F_Blue\2025_08_08",
     r"Cohort 2\BRAC_10695_4F_Blue\2025_08_14",
     r"Cohort 2\BRAC_10695_4F_Blue\2025_09_02"],

]



delay_only_criteria_sessions = [

    [r"Cohort 3\BRAC_11935_1D_Pink\2025_11_18",
    r"Cohort 3\BRAC_11935_1D_Pink\2025_11_28",
    r"Cohort 3\BRAC_11935_1D_Pink\2025_12_02",
    r"Cohort 3\BRAC_11935_1D_Pink\2025_12_04",
    r"Cohort 3\BRAC_11935_1D_Pink\2025_12_09",
    r"Cohort 3\BRAC_11935_1D_Pink\2025_12_16"],

    [r"Cohort 3\BRAC_11935_1C_Black\2024_12_04",
    r"Cohort 3\BRAC_11935_1C_Black\2025_11_18",
    r"Cohort 3\BRAC_11935_1C_Black\2025_11_28",
    r"Cohort 3\BRAC_11935_1C_Black\2025_12_02",
    r"Cohort 3\BRAC_11935_1C_Black\2025_12_09",
    r"Cohort 3\BRAC_11935_1C_Black\2025_12_11",
    r"Cohort 3\BRAC_11935_1C_Black\2025_12_15",
    r"Cohort 3\BRAC_11935_1C_Black\2025_12_16",
    r"Cohort 3\BRAC_11935_1C_Black\2025_12_18"],

    [r"Cohort 3\BRAC_11935_1A_Green\2025_12_02",
    r"Cohort 3\BRAC_11935_1A_Green\2025_12_04",
    r"Cohort 3\BRAC_11935_1A_Green\2025_12_05",
    r"Cohort 3\BRAC_11935_1A_Green\2025_12_09",
    r"Cohort 3\BRAC_11935_1A_Green\2025_12_10",
    r"Cohort 3\BRAC_11935_1A_Green\2025_12_11",
    r"Cohort 3\BRAC_11935_1A_Green\2025_12_16",
    r"Cohort 3\BRAC_11935_1A_Green\2025_12_18"],

    [r"Cohort 3\BRAC_11766_1E_Purple\2025_11_18",
    r"Cohort 3\BRAC_11766_1E_Purple\2025_11_28",
    r"Cohort 3\BRAC_11766_1E_Purple\2025_12_02",
    r"Cohort 3\BRAC_11766_1E_Purple\2025_12_04",
    r"Cohort 3\BRAC_11766_1E_Purple\2025_12_05",
    r"Cohort 3\BRAC_11766_1E_Purple\2025_12_09",
    r"Cohort 3\BRAC_11766_1E_Purple\2025_12_10",
    r"Cohort 3\BRAC_11766_1E_Purple\2025_12_11",
    r"Cohort 3\BRAC_11766_1E_Purple\2025_12_12",
    r"Cohort 3\BRAC_11766_1E_Purple\2025_12_15",
    r"Cohort 3\BRAC_11766_1E_Purple\2025_12_16",
    r"Cohort 3\BRAC_11766_1E_Purple\2025_12_18"],

    [r"Cohort 2\BRAC_10695_4F_Blue\2025_07_08",
    r"Cohort 2\BRAC_10695_4F_Blue\2025_07_11",
    r"Cohort 2\BRAC_10695_4F_Blue\2025_07_16",
    r"Cohort 2\BRAC_10695_4F_Blue\2025_07_21",
    r"Cohort 2\BRAC_10695_4F_Blue\2025_07_22",
    r"Cohort 2\BRAC_10695_4F_Blue\2025_07_23",
    r"Cohort 2\BRAC_10695_4F_Blue\2025_07_24",
    r"Cohort 2\BRAC_10695_4F_Blue\2025_07_25",
    r"Cohort 2\BRAC_10695_4F_Blue\2025_07_28",
    r"Cohort 2\BRAC_10695_4F_Blue\2025_08_01",
    r"Cohort 2\BRAC_10695_4F_Blue\2025_08_08",
    r"Cohort 2\BRAC_10695_4F_Blue\2025_08_14",
    r"Cohort 2\BRAC_10695_4F_Blue\2025_09_02"],

]