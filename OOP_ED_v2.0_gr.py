# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:55:25 2024

@author: varad
"""
#OOP model for a real ED with 3 processes and 3 resources
#import libraries
import simpy
import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import random
import csv
import gradio as gr

class g (object):
    '''
    A class that holds all the global variables that will be passed into the different processes.
    It's easier to change the global variables here rather than change them in the process code as it could lead to errors
    '''
    #service times (these are more or less constant and hence won't be changed through user input, although it is possible to change them too,
    #but for the sake of this program, they won't be changed)
    ed_inter_arrival = 6 #mins
    mean_registeration = 2 #mins
    mean_triage = 6 #mins
    mean_acu_ass = 60 #mins
    mean_ed_ass = 30 #mins
    
    #resources (this will need to me moved from a static variable to a variable within the ED class as it will then be fed into the gradio app
    #as variables to be modified through user input)
    receptionist = 1
    nurse = 2
    ed_doc = 2
    acu_doc = 1
    
    #simulation variables
    number_of_runs = 100
    warmup_time = 1440 #24 hours and 60 minutes per hour
    run_time = 100 # mins

class ed_patient (object):
    '''
    Defines the patient characteristics. Could be interesting if we have different types of patients
    But for this exercise we have only one type of patient that is a regular patient that has a 20% chance 
    of going to the ACU. Also important to store patient level variables to then summarize and plot
    '''
    def __init__(self, uhid):
        self.id = uhid
        
        #declaring these variables as they will be recorded and manipulated with later
        self.time_entered_in_system = 0
        self.q_reception = 0 
        self.service_reception = 0
        self.q_nurse = 0
        self.service_nurse = 0
        self.q_edd_ass = 0
        self.ed_ass_time = 0
        self.acu_ass_time = 0
        self.q_acu_ass = 0
        self.time_exit_system = 0
        self.tot_system_time = 0

class ED_sim (object):
    '''
    This is the actual clinic where everything is simulated.
    '''
    def __init__(self, run_number,receptionist = 3, nurse = 2, ed_doc = 2, acu_doc = 1  ):
        #declaring the environment
        self.env = simpy.Environment()
        
        
        
        #declaring resource capacity as variables to later be changed through gradio inputs
        self.receptionist = receptionist
        self.nurse = nurse
        self.ed_doc = ed_doc
        self.acu_doc = acu_doc
        

        self.patient_counter = 0
        #declaring resources
        self.receptionist = simpy.Resource(self.env, capacity = self.receptionist)
        self.nurse = simpy.Resource(self.env, capacity = self.nurse)
        self.ed_doc = simpy.Resource(self.env, capacity = self.ed_doc)
        self.acu_doc = simpy.Resource(self.env, capacity = self.acu_doc)
        self.run_number = run_number + 1
        
        #initiating a dataframe with required columns
        self.individual_level_results = pd.DataFrame({
            "UHID" :[],
            "Time_entered_in_system" : [],
             "Q_time_receptionist":[], 
             "Q_time_nurse":[],
             "Q_time_acu_doc":[],
             "Q_time_ed_doc":[],
             "Service_time_receptionist":[],
             "Service_time_nurse":[],
             "Service_time_acu_doc":[],
             "Service_time_ed_doc":[],
             "Time_exit_system":[],
             "Total time in System":[]
             })
        self.individual_level_results.set_index('UHID', inplace= True) #sets the index to UHID which is just 1,2,3,4 etc
        
        #declaring mean variables for or KPIs to be calculated at the end of one run
        self.Mean_Q_Rec_time = 0
        self.Mean_Q_Nurse_time = 0
        self.Mean_Q_ED_time = 0
        self.Mean_Q_ACU_time = 0
        self.Rec_utilize = 0
        self.Nurse_utilize = 0
        self.ED_doc_utilize = 0
        self.ACU_doc_utilize = 0
        
        
        
    def generate_ed_arrivals(self):
        while True:
            self.patient_counter += 1 #this is also the UHID of the patient
            
            ed_pt = ed_patient(self.patient_counter)
            
            ed_pt.time_entered_in_system = self.env.now #Used to calculate total time spent in the system
            
            #Patient goes to registeration
            self.env.process(self.registration(ed_pt))
            
            #print(self.individual_level_results)
            #draws a random value from an exponential distribution with lambda = interarrival time
            ed_arrival_time = random.expovariate(1/g.ed_inter_arrival)
            
            yield self.env.timeout(ed_arrival_time)
        
    
    def registration(self, patient):
        
        start_q_rec = self.env.now
        
        with self.receptionist.request() as req:
            yield req
        
            end_q_rec = self.env.now
            
        #storing patient level values in patient level variables
            patient.q_reception = end_q_rec - start_q_rec
        
        #patient goes to triage
            self.env.process(self.triage(patient))
        
        #register_time = random.triangular(0,g.mean_registeration, 2*g.mean_registeration)
            register_time = random.expovariate(1/g.mean_registeration)
        
            patient.service_reception = register_time
       
     
        
            yield self.env.timeout(register_time)
    
    def triage (self, patient):
        start_q_nurse = self.env.now
        with self.nurse.request() as req:
            yield req
        
            end_q_nurse = self.env.now
        
            patient.q_nurse = end_q_nurse - start_q_nurse
        
        #patient goes either to ACU or to ED based on probability
            if random.random() > 0.2: #80% chance that the patient goes to ED
                self.env.process(self.ed_ass(patient))
            else:
                self.env.process(self.acu_ass(patient))

        
            triage_time = random.triangular(g.mean_triage/2, g.mean_triage, g.mean_triage*2 )
        
            patient.service_nurse = triage_time
        
        
        
            yield self.env.timeout(triage_time)
        
        
    
    def ed_ass (self, patient):
        start_ed_q = self.env.now
        with self.ed_doc.request() as req:
            yield req
            end_ed_q = self.env.now
            patient.q_edd_ass = end_ed_q - start_ed_q
        
        
            ed_ass_time = random.triangular(g.mean_ed_ass/2, g.mean_ed_ass, g.mean_ed_ass*2)
            patient.ed_ass_time = ed_ass_time
        
        
        
            yield self.env.timeout(ed_ass_time)
            
            patient.time_exit_system = self.env.now    
        
            patient.tot_system_time = patient.time_exit_system - patient.time_entered_in_system
    
            ED_sim.add_to_df(self, patient)
        
        
    def acu_ass (self, patient):
        start_acu_q = self.env.now
        
        with self.acu_doc.request() as req:
            yield req
            
            end_acu_q = self.env.now
            patient.q_acu_ass = end_acu_q - start_acu_q
        
            acu_ass_time = random.triangular(g.mean_acu_ass/2, g.mean_acu_ass, g.mean_acu_ass*2)
        
            patient.acu_ass_time = acu_ass_time
            yield self.env.timeout(acu_ass_time)
        
            patient.time_exit_system = self.env.now
            
            patient.tot_system_time = patient.time_exit_system - patient.time_entered_in_system
            ED_sim.add_to_df(self, patient)
        
    
    def add_to_df(self, patient):
        '''
        Basically takes all the variables and adds them to the dataframe without having to enter them manually with 
        12 line codes in every function
        '''
        df_to_add = pd.DataFrame({
            "UHID" :[patient.id],
            "Time_entered_in_system" : [patient.time_entered_in_system],
            "Q_time_receptionist":[patient.q_reception],
            
            #using zeros as placeholders
            "Q_time_nurse":[patient.q_nurse],
            "Q_time_acu_doc":[patient.q_acu_ass],
            "Q_time_ed_doc":[patient.q_edd_ass],
            "Service_time_receptionist":[patient.service_reception],
            "Service_time_nurse":[patient.service_nurse],
            "Service_time_acu_doc":[patient.acu_ass_time],
            "Service_time_ed_doc":[patient.ed_ass_time],
            "Time_exit_system" :[patient.time_exit_system],
            "Total time in System":[patient.tot_system_time]        
              })
        
        df_to_add.set_index('UHID', inplace=True)
        self.individual_level_results = self.individual_level_results._append(df_to_add)
        #print(self.individual_level_results)
        
        
    def mean_calculator (self):
        '''
        calculates the average statistic for each individual run for all the different KPIs and maybe stores it in a global database
        '''
        #mean queuing times
        self.Mean_Q_Rec_time = self.individual_level_results['Q_time_receptionist'].mean()
        self.Mean_Q_Nurse_time = self.individual_level_results['Q_time_nurse'].mean()
        self.Mean_Q_ED_time = self.individual_level_results['Q_time_ed_doc'].mean()
        self.Mean_Q_ACU_time = self.individual_level_results['Q_time_acu_doc'].mean()
        
        #%resource utilisation
        self.Rec_utilize = self.individual_level_results[
            'Service_time_receptionist'].sum()/(g.run_time*g.receptionist)
        self.Nurse_utilize = self.individual_level_results['Service_time_nurse'].sum()/(g.run_time*g.nurse)
        self.ED_doc_utilize = self.individual_level_results['Service_time_ed_doc'].sum()/(g.run_time*g.ed_doc)
        self.ACU_doc_utilize = self.individual_level_results['Service_time_acu_doc'].sum()/(g.run_time*g.acu_doc)
    
        
    
    def export_row_to_csv(self):
        '''
        Writes the results of an individual run as a row in a csv file in the desired folder
        '''
    
        with open (r"C:\Users\varad\Desktop\Education Material\Mathematical Modelling\HSMA\HSMA_modelling_ED\trial_results.csv",'a') as f:
            writer = csv.writer(f, delimiter = ',')
            row_to_add = [self.run_number,
                self.Mean_Q_Rec_time,
                               self.Mean_Q_Nurse_time,
                               self.Mean_Q_ED_time,
                               self.Mean_Q_ACU_time,
                               self.Rec_utilize,
                               self.Nurse_utilize,
                               self.ED_doc_utilize,
                               self.ACU_doc_utilize]
            writer.writerow(row_to_add)
            
            
    def run (self):
        '''
        suns the simulation program
        '''
        self.env.process(self.generate_ed_arrivals())
        self.env.run(until = g.run_time)
        #print(self.individual_level_results)
        self.individual_level_results.to_csv(r"C:\Users\varad\Desktop\Education Material\Mathematical Modelling\HSMA\HSMA_modelling_ED\individual_results.csv")
        self.mean_calculator()
        self.export_row_to_csv()

class summary_statistics(object):
    '''
    This object calculates the mean, median or other summary statistics from a dataframe that has means of individual runs
    So this object calculates the means of means
    '''
    def __init__(self):
        self.total_mean_df = pd.DataFrame({
            "Median_q_rec_time":[],
            "25_q_rec_time":[],
            "75_q_rec_time":[],
            
            "Median_q_nurse_time":[],
            "25_q_nurse_time":[],
            "75_q_nurse_time":[],
            
            "Median_q_ed_doc_time":[],
            "25_q_ed_doc_time":[],
            "75_q_ed_doc_time":[],
            
            "Median_q_acu_doc_time":[],
            "25_q_acu_doc_time":[],
            "75_q_acu_doc_time":[],
            
            "Median_%_utilize_rec":[],
           
            "Median_%_utilize_nurse":[],
            
            
            "Median_%_utilize_ed_doc":[],
           
            
            "Median_%_utilize_acu_doc":[],
            
            })
        filepath = r"C:\Users\varad\Desktop\Education Material\Mathematical Modelling\HSMA\HSMA_modelling_ED\trial_results.csv"
        self.dataframe = pd.read_csv(filepath)
    
    def mean_of_means(self):
        
        median_q_rec = self.dataframe["Mean_Q_Rec_time"].median()
        twofive_q_rec = self.dataframe["Mean_Q_Rec_time"].quantile(0.25)
        sevfive_q_rec = self.dataframe["Mean_Q_Rec_time"].quantile(0.75)
        
        median_q_nurse = self.dataframe["Mean_Q_Nurse_time"].median()
        twofive_q_nurse = self.dataframe["Mean_Q_Nurse_time"].quantile(0.25)
        sevfive_q_nurse = self.dataframe["Mean_Q_Nurse_time"].quantile(0.75)
        
        median_q_ed_doc = self.dataframe["Mean_Q_ED_time"].median()
        twofive_q_ed_doc = self.dataframe["Mean_Q_ED_time"].quantile(0.25)
        sevfive_q_ed_doc = self.dataframe["Mean_Q_ED_time"].quantile(0.75)
        
        median_q_acu_doc = self.dataframe["Mean_Q_ACU_time"].median()
        twofive_q_acu_doc = self.dataframe["Mean_Q_ACU_time"].quantile(0.25)
        sevfive_q_acu_doc = self.dataframe["Mean_Q_ACU_time"].quantile(0.75)
        
        median_rec_uti = self.dataframe["Rec_%_utilize"].median()
        median_nurse_uti = self.dataframe["Nurse_%_utilize"].median()
        median_ed_doc_uti = self.dataframe["ED_doc_%_utilize"].median()
        median_acu_doc_uti = self.dataframe["ACU_doc_%_utilize"].median()
        
        
        print("Results of " +  str(g.number_of_runs) + " runs")
        print("-------------")
        
        self.total_mean_df = pd.DataFrame({
            "Median_q_rec_time":[median_q_rec],
            "25_q_rec_time":[twofive_q_rec],
            "75_q_rec_time":[sevfive_q_rec],
            
            "Median_q_nurse_time":[median_q_nurse],
            "25_q_nurse_time":[twofive_q_nurse],
            "75_q_nurse_time":[sevfive_q_nurse],
            
            "Median_q_ed_doc_time":[median_q_ed_doc],
            "25_q_ed_doc_time":[twofive_q_ed_doc],
            "75_q_ed_doc_time":[sevfive_q_ed_doc],
            
            "Median_q_acu_doc_time":[median_q_acu_doc],
            "25_q_acu_doc_time":[twofive_q_acu_doc],
            "75_q_acu_doc_time":[sevfive_q_acu_doc],
            
            "Median_%_utilize_rec":[median_rec_uti],
           
            
            "Median_%_utilize_nurse":[median_nurse_uti],
           
            
            "Median_%_utilize_ed_doc":[median_ed_doc_uti],
          
            
            "Median_%_utilize_acu_doc":[median_acu_doc_uti],
           
            })
    
        print(self.total_mean_df)
        
        with open (r"C:\Users\varad\Desktop\Education Material\Mathematical Modelling\HSMA\HSMA_modelling_ED\mean_per_lambda.csv",'a') as f:
            writer = csv.writer(f, delimiter = ',')
            row_to_add = [g.ed_inter_arrival,
                          median_q_rec,
                          twofive_q_rec,
                          sevfive_q_rec,
                          
                          median_q_nurse,
                          twofive_q_nurse,
                          sevfive_q_nurse,
                          
                          median_q_ed_doc,
                          twofive_q_ed_doc,
                          sevfive_q_ed_doc,
                          
                          median_q_acu_doc,
                          twofive_q_acu_doc,
                          sevfive_q_acu_doc,
                          
                          median_rec_uti,
                          median_nurse_uti,
                          median_ed_doc_uti,
                          median_acu_doc_uti
                          ]
            writer.writerow(row_to_add)
        
def file_opener():
    '''
    Adds one row to the filename that is passed to it
    '''
    #This is not the most compulsory function here as the above function will also create a file if it does not exist already
    
    with open (r"C:\Users\varad\Desktop\Education Material\Mathematical Modelling\HSMA\HSMA_modelling_ED\trial_results.csv",'w') as f:
        writer = csv.writer(f, delimiter = ',')
        columns_headers = ["Run_Number",
                          "Mean_Q_Rec_time",
                          "Mean_Q_Nurse_time",
                          "Mean_Q_ED_time",
                          "Mean_Q_ACU_time",
                          "Rec_%_utilize",
                          "Nurse_%_utilize",
                          "ED_doc_%_utilize",
                          "ACU_doc_%_utilize"]
        writer.writerow(columns_headers)
        
        with open (r"C:\Users\varad\Desktop\Education Material\Mathematical Modelling\HSMA\HSMA_modelling_ED\mean_per_lambda.csv",'w') as f:
            writer = csv.writer(f, delimiter = ',')
            columns_headers = ["Pt Interarrival Time (lambda)",
                              "Median_Q_Rec_time",
                              "25_Q_rec_time",
                              "75_Q_rec_time",
                              
                              "Median_Q_Nurse_time",
                              "25_Q_Nurse_time",
                              "75_Q_Nurse_time",
                              
                              "Median_Q_ED_time",
                              "25_Q_ED_time",
                              "75_Q_ED_time",
                              
                              "Median_Q_ACU_time",
                              "25_Q_ACU_time",
                              "75_Q_ACU_time",
                              
                              "Median_Rec_%_utilize",
                              "Median_Nurse_%_utilize",
                              "Median_ED_doc_%_utilize",
                              "Median_ACU_doc_%_utilize"]
            
            writer.writerow(columns_headers)

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


def main():
    file_opener()
    for l in range(1,11):
        print("Pt interarrival time = ", l)
        for run in range (g.number_of_runs):
            print(f"Run {run + 1} of {g.number_of_runs}")
            my_ED_model = ED_sim(run)
            my_ED_model.run()
        g.ed_inter_arrival = l 
        my_sum_stats = summary_statistics()
        my_sum_stats.mean_of_means()
    Plotter()

def get_data_gradio():
    filepath = r"C:\Users\varad\Desktop\Education Material\Mathematical Modelling\HSMA\HSMA_modelling_ED\mean_per_lambda.csv"
    return pd.read_csv(filepath)



#main()


    
with gr.Blocks() as demo:
    gr.Markdown(r"A Discrete Event Simulation run of an imaginary Emergency Room")

    with gr.Row():
        gr.Textbox(label = "Modify these parameters (number of different human resources) using the sliders below")
    with gr.Row():
        receptionist = gr.Slider(minimum=1, maximum=10,label = "No of Receptionists")
        nurse = gr.Slider(minimum=1, maximum=10, label = "No of Nurses")
    with gr.Row():    
        ed_doc = gr.Slider(minimum=1, maximum=10, label = "No of ED doctors")
        acu_doc = gr.Slider(minimum=1, maximum=10,label = "No of ACU Doctors")
    
    output = gr.LinePlot(get_data_gradio, x = "Pt Interarrival Time (lambda)", y="Median_Q_Rec_time", y_title="Median queue time for receptionist (min)", overlay_point=True, width=500, height=500)

    with gr.Row():
        btn = gr.Button(value = "Run the Simulation")
        btn.click(main,[receptionist,nurse,ed_doc,acu_doc], output)

demo.launch()




    
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
