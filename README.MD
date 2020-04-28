Scripts for producing the OMTF plots for the L1 TDR. Initial setup before github remote by @sesanche.

All plots are produced in two steps to avoid needlessly repeating the initial loading for minor aesthetic changes:

makeX.py produces the input histograms and saves them in a pickle file.

plotX.py reads the histograms and does the plotting with the appropriate style.

