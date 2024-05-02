import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import csv

def Plotter():
    filepath = r"C:\Users\varad\Desktop\Education Material\Mathematical Modelling\HSMA\HSMA_modelling_ED\mean_per_lambda.csv"
    df_to_plot = pd.read_csv(filepath)

    ax,figure = plt.subplots()
    plt.plot(df_to_plot["Pt Interarrival Time (lambda)"], df_to_plot['Median_Q_Rec_time'], color = 'green', linestyle = '-', label = 'Queue for reception')
    plt.plot(df_to_plot["Pt Interarrival Time (lambda)"], df_to_plot['Median_Q_Nurse_time'], color = 'blue', linestyle = ':', label = 'Queue for nurses')
    plt.plot(df_to_plot["Pt Interarrival Time (lambda)"], df_to_plot['Median_Q_ED_time'], color = 'red', linestyle = '--', label = 'Queue for ED_doc')
    plt.plot(df_to_plot["Pt Interarrival Time (lambda)"], df_to_plot['Median_Q_ACU_time'], color = 'black', linestyle = '-.', label = 'Queue for ACU_doc')

    plt.xlabel("Pt interarrival time (min)")
    plt.ylabel("Time in minutes")
    plt.title("Queuing times for the Emergency room")

    plt.text(3,10,"Rec = 1, Nur = 2, ED_doc = 2, ACU_doc = 1")
    plt.legend()

    plt.show()

    ax,figure = plt.subplots()
    plt.plot(df_to_plot["Pt Interarrival Time (lambda)"], df_to_plot['Median_Rec_%_utilize'], color = 'green', linestyle = '-', label = '% utilise of reception')
    plt.plot(df_to_plot["Pt Interarrival Time (lambda)"], df_to_plot['Median_Nurse_%_utilize'], color = 'blue', linestyle = ':', label = '% utilise of nurses')
    plt.plot(df_to_plot["Pt Interarrival Time (lambda)"], df_to_plot['Median_ED_doc_%_utilize'], color = 'red', linestyle = '--', label = '%utilise of ED_doc')
    plt.plot(df_to_plot["Pt Interarrival Time (lambda)"], df_to_plot['Median_ACU_doc_%_utilize'], color = 'black', linestyle = '-.', label = '%utilise of ACU_doc')

    plt.xlabel("Pt interarrival time (min)")
    plt.ylabel("Time in minutes")
    plt.title("Percentage utlisation for the Emergency room different HR")

    plt.text(3,10,"Rec = 1, Nur = 2, ED_doc = 2, ACU_doc = 1")
    plt.legend()

    plt.show()

Plotter()