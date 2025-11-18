"""
Example of computation of the Convection Velocity between two flush mounted Remote Microphone Probes (RMP)

D-Raus
"""

import matplotlib.pyplot as plt
from scipy import signal
import pickle

from compute_RMP_ConvectionVelocity import RMP_ConvectionVelocityCalculator



def main():
    """
    Example of computation of the Convection Velocity between two RMPs
    """

    ### Load the RMPs data    
    path_data_x1 = 'RMP_data/RMP_data_x0p097.pkl'
    path_data_x2 = 'RMP_data/RMP_data_x0p110.pkl'
    
    RMP_data_x1 = load_PKL_file(path_data_x1)
    RMP_data_x2 = load_PKL_file(path_data_x2)

    ### Position along the chord of the two flush mounted RMPs
    x1_RMP, x2_RMP = 0.097, 0.110

    ### Sampling frequency of the RMPs
    fs = 51200
    
    ### Preprocessing of the RMPs signals to remove the background noise of the wind tunnel
    f_HighPass = 60
    sos = signal.butter(2, f_HighPass, 'hp', fs=fs, output='sos')
    RMP_data_x1_filter = signal.sosfilt(sos, RMP_data_x1)
    RMP_data_x2_filter = signal.sosfilt(sos, RMP_data_x2)

    ### Choice of the Welch method parameters of the frequency domain computation
    df = 16
    window = int(fs * (1 / df))
    overlap = window // 2

    ### Create an instance of the RMP_ConvectionVelocityCalculator class
    Ucv_calculator = RMP_ConvectionVelocityCalculator(RMP_data_x1_filter, RMP_data_x2_filter, x1_RMP, x2_RMP, fs)
    
    ### Computation of the convection speed
    Ucv_fitCSD, result_plot_fitCSD = Ucv_calculator.compute_freqdomain(window, overlap)
    Ucv_xcorr, result_plot_xcorr = Ucv_calculator.compute_timedomain()

    ### Plot the result
    Ucv_calculator.plot_freqdomain(result_plot_fitCSD)
    Ucv_calculator.plot_timedomain(result_plot_xcorr)

    print(f"Frequency domain method: Uc = {Ucv_fitCSD:.2f}")
    print(f"Time domain method: Uc = {Ucv_xcorr:.2f}")
    
    
def load_PKL_file(path):
    """ Load a pickle file into memory"""
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data
    
if __name__ == '__main__':
    main()




    
    