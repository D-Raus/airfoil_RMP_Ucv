"""
Class and methods for calculating the Convection Velocity (Ucv) between two flush-mounted Remote Microphone Probes (RMP) along an airfoil chord

D-Raus
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy import signal




class RMP_ConvectionVelocityCalculator:
    """
    Class for calculating the Convection Velocity (Ucv) between two flush-mounted Remote Microphone Probes (RMP), using:
        - compute_freqdomain : Frequency-domain method (Moreau and Roger - 2005 - Effect of Airfoil Aerodynamic Loading on Trailing-Edge Noise Sources) 
        - compute_timedomain : Time-domain method (Bertagnolio - 2015 - Experimental characterization of stall noise toward its modelling )
    """

    def __init__(self, RMP_data_1, RMP_data_2, RMP_x1, RMP_x2, fs):
        """
        Parameters
        ----------
        data_1, data_2 (1D np.ndarray) : Remote Microphone-Probe (RMP) signals of two probes along the chord.
        x1, x2 (float) : Positions of the two microphones along the chord (m).
        fs (float) : Sampling frequency (Hz).
        """
        self.RMP_data_1 = RMP_data_1
        self.RMP_data_2 = RMP_data_2
        self.RMP_x1 = RMP_x1
        self.RMP_x2 = RMP_x2
        self.fs = fs


    def compute_freqdomain(self, N_window, N_overlap):
        """
        Compute convection velocity using cross-spectral phase fit.
            1. Computes the Cross-Spectral Density  (CSD) of the two RMPs signal
            2. Computes the magnitude squared coherence gamma2 of the two RMPs signal using the Welch's method
            3. Perform linear fit of the unwrapped phase of the CSD
            4. Compute the the convection velocity (Ucv)
        """

        ### Cross-spectral density of the two RMPs signal
        f_Pxy, Pxy = signal.csd(self.RMP_data_1,
                                self.RMP_data_2, 
                                self.fs,
                                nperseg=N_window, 
                                noverlap=N_overlap,
                                window='hann', 
                                nfft=N_window)
        
        ### Estimation of magnitude squared coherence gamma2 of the two RMPs signal using the Welch's method
        _,Pxx = signal.welch(self.RMP_data_1, 
                             self.fs,nperseg=N_window, 
                             noverlap=N_overlap,
                             window='hann', 
                             nfft=N_window)
        _,Pyy = signal.welch(self.RMP_data_2, 
                             self.fs,nperseg=N_window, 
                             noverlap=N_overlap,
                             window='hann', 
                             nfft=N_window)
        gamma2 = abs(Pxy)**2/(Pxx*Pyy)

        ### The upper limit of the linear fit interval is determined as the frequency at wich the coherence drops below a threshold 
        ind_tmp = [ind for ind, val in enumerate(gamma2) if val >= 0.1]
        ind_fmax_fit = ind_tmp[-1]

        ### Linear fit of the unwrapped phase of the cross-spectral density
        phi_xy = np.angle(Pxy[1:ind_fmax_fit])
        P = np.polyfit(f_Pxy[1:ind_fmax_fit], np.unwrap(phi_xy), 1)

        ### Convection speed
        Ucv = (self.RMP_x2 - self.RMP_x1) / P[0] * 2 * np.pi
        
        ### Store data for plotting in a dictionnary
        result_plot = {'gamma2' : gamma2,'ind_fmax_fit' : ind_fmax_fit,
                       'f_Pxy' : f_Pxy,'P' : P,'Pxy' : Pxy}
        
        
        return Ucv, result_plot


    def compute_timedomain(self):
        """
        Compute convection velocity in the time-domain using cross-correlation.
            1. Substract the mean of each signal to keep the fluctuations signals
            2. Computes the Cross-correlation of the fluctuations signals 
            3. Find the maximum of cross-correlation 
            4. Compute the the convection velocity (Ucv)
        """
        
        ### Substract the mean of each signal to keep the fluctuations signals
        RMP_data_f_1 = self.RMP_data_1 - np.mean(self.RMP_data_1)
        RMP_data_f_2 = self.RMP_data_2 - np.mean(self.RMP_data_2)

        ### Cross-correlation of the fluctuations signals d1 and d2
        Rxy = signal.correlate(RMP_data_f_1, RMP_data_f_2)
        
        ### Cross-correlation lags/discplacement for the cross-correlation
        lags = signal.correlation_lags(len(RMP_data_f_1), len(RMP_data_f_2))

        ### Lag and time of the maximum cross-correlation
        _, ind_Rxy_max = max((val, idx) for (idx, val) in enumerate(abs(Rxy)))
        lagDiff = lags[ind_Rxy_max]
        timeDiff = lagDiff / self.fs

        ### Convection speed = delta_x/delta_t
        Ucv = (self.RMP_x2 - self.RMP_x1) / timeDiff

        ### Store data for plotting in a dictionnary
        result_plot = {'Rxy' : Rxy,'lags' : lags}
        
        return Ucv, result_plot


    def plot_freqdomain(self,result_plot):
        """
        Plot the results of the computation in the frequency domain
        """
        
        
        fmax = result_plot['f_Pxy'][result_plot['ind_fmax_fit']]
        size_font = 14
        
        fig, axs = plt.subplots(1, 2, figsize=(14, 5))
        axs[0].axvspan(result_plot['f_Pxy'][result_plot['ind_fmax_fit']], 8000, alpha=0.3, color='grey')
        axs[0].semilogx(result_plot['f_Pxy'], result_plot['gamma2'])
        axs[0].semilogx(result_plot['f_Pxy'][result_plot['ind_fmax_fit']], result_plot['gamma2'][result_plot['ind_fmax_fit']], 'ro')
        axs[0].set_xlabel('f(Hz)',fontsize = size_font)
        axs[0].set_ylabel('$\gamma^2$',fontsize = size_font)
        axs[0].set_ylim(0, 1)
        axs[0].set_xlim(60, 8000)

        axs[1].axvspan(result_plot['f_Pxy'][result_plot['ind_fmax_fit']], 4000, alpha=0.3, color='grey')
        axs[1].plot(result_plot['f_Pxy'], np.unwrap(np.angle(result_plot['Pxy'])) * 180 / np.pi)
        axs[1].plot(result_plot['f_Pxy'], result_plot['P'][0] * result_plot['f_Pxy'] * 180 / np.pi +result_plot['P'][1] * 180 / np.pi, 'r--')
        axs[1].plot(fmax, result_plot['P'][0] * fmax * 180 / np.pi + result_plot['P'][1] * 180 / np.pi, 'ro')
        axs[1].set_xlabel('f(Hz)',fontsize = size_font)
        axs[1].set_ylabel('Unwraped cross spectral phase (°)',fontsize = size_font)
        axs[1].set_ylim(0, 1000)
        axs[1].set_xlim(0, 4000)
        axs[1].legend(['Mesure', 'Linear Fit', 'Limite fit'], loc='best')
        fig.tight_layout(pad=2.0)
        plt.xticks(fontsize=12)

        fig.savefig('freqdomain.png', dpi=300)

    def plot_timedomain(self,result_plot):
        """
        Plot the results of the computation in the time domain
        """
        size_font = 14

        fig = plt.figure(figsize=(12, 6))
        plt.plot(result_plot['lags'] / self.fs, result_plot['Rxy'] / max(result_plot['Rxy']),label = 'Cross-correlation')
        plt.axvline(x=result_plot['lags'][result_plot['Rxy'] == max(result_plot['Rxy'])]/self.fs,linestyle = '--',color = 'tab:red',label = 'Max Cross-correlation')
        plt.xlabel(r'$\tau$ (s)',fontsize = size_font)
        plt.ylabel('$R_{xy}$',fontsize = size_font)
        plt.xlim(-0.01, 0.01)
        plt.legend()
        plt.show()
        plt.xticks(fontsize=12)

        fig.savefig('timedomain.png', dpi=300)



