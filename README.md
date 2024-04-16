# HSMA_modelling_ED
Doing the final exercise of the HSMA DES modelling exercise. Will try to build a gradio app for this if possible as proof of concept
This is the code for the HSMA modelling Discrete Event Simulation exercise's final exercise. We're in a ED, we have 3 successive pathways, We have 4 resources and one branching activity. Every process uses a different queue and doesn't compete for the same resources. Model parameters for service time and inter arrival times are as follows
1) Mean inter-arrival time - 8 mins
2) Mean registration time - 2 mins
3) Mean Triage
4) Mean ACU assessment
5) Probability of going to ACU
6) Number of receptionists
7) Number of nurses
8) Number of ED doctors
9) Number of ACU doctors
10) Warm up time - 24 hours
11) Number of simulation runs - 100

Key output indicators
1) Queuing times for each patient for each process
2) Mean of all queuing times for 100 runs

Store information and write it in a pandas dataframe. This will be very helpful later on to manipulate the data
