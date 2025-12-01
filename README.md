Computation of the Convection Velocity between two flush mounted Remote Microphone Probes (RMP) along an airfoil chord.

A Remote Microphone Probe (RMP) consists of a capillary tube that connect a small size perforation on the airfoil wall to a microphone located outside the wetted part of the airfoil mock up.
By distributing RMPs in the chordwise and spanwise direction, they allow the measurements of wall-pressure fluctuations at multiple locations on the airfoil, even if in the thinnest area of the airfoil trailing edge.
These measurements are used to characterize the development of instability waves or turbulence in the airfoil boundary layers.

By using a pair of two chordwise RMPs located at the midspan, one can estimate the convection velocity of propagating or convected pressure field on the airfoil.
Two methods to compute the convection velocity between two flush mounted RMPs are implemented here:

# In the frequency domain
slope of the phase of the complex cross-spectral density
![Tex2Img_1764606505](https://github.com/user-attachments/assets/d65ee804-25c4-4fca-ab9c-e28596cab917)



<img width="4200" height="1500" alt="freqdomain" src="https://github.com/user-attachments/assets/8a079e1d-0825-4995-bf57-6c29fb9a9d18" />

# In the time domain
The cross-correlation function of the two RMPs signals is computed. Then the time lag delta_tau_max corresponding to the peak of this function is identified. 
Under the assumption of frozen turbulence, the convection velocity can thus be estimated using the simple relation [3]:
Uc = delta_x / delta_tau_max

<img width="3600" height="1800" alt="timedomain" src="https://github.com/user-attachments/assets/8e74c753-3e5a-41e3-a679-d2a0bf71f17b" />

# References
[1] Moreau, S.; Roger, M. Effect of airfoil aerodynamic loading on trailing edge noise sources. AIAA J. 2005, 43, 41–52.
[2] Yakhina, Gyuzel, et al. "Experimental and analytical investigation of the tonal trailing-edge noise radiated by low Reynolds number aerofoils." Acoustics. Vol. 2. No. 2. MDPI, 2020.
[3] Bertagnolio, F., Aagaard Madsen , H., Fischer, A., & Bak, C. (2015). Experimental Characterization of Stall Noise Toward its Modelling. In Proceedings of the 6th International Conference on Wind Turbine Noise
