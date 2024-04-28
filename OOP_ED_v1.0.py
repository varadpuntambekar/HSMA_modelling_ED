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

class g (object):
    '''
    A class that holds all the global variables that will be passed into the different processes.
    It's easier to change the global variables here rather than change them in the process code as it could lead to errors
    '''
    #service times
    ed_inter_arrival = 9 #mins
    mean_registeration = 2 #mins
    mean_triage = 6 #mins
    mean_acu_ass = 60 #mins
    mean_ed_ass = 30 #mins
    
    #resources
    receptionist = 1
    nurse = 2
    ed_doc = 2
    acu_doc = 1
    
    #simulation variables
    number_of_runs = 1
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
        self.tot_system_time = 0

class ED_sim (object):
    '''
    This is the actual clinic where everything is simulated.
    '''
    def __init__(self, run_number):
        #declaring the environment
        self.env = simpy.Environment()
        self.patient_counter = 0
        
        #declaring resources
        self.receptionist = simpy.Resource(self.env, capacity = g.receptionist)
        self.nurse = simpy.Resource(self.env, capacity = g.nurse)
        self.ed_doc = simpy.Resource(self.env, capacity = g.ed_doc)
        self.acu_doc = simpy.Resource(self.env, capacity = g.acu_doc)
        self.run_number = run_number
        
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
        
        register_time = random.triangular(0,g.mean_registeration, 2*g.mean_registeration)
        
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
        
        patient.tot_system_time = self.env.now - patient.time_entered_in_system
    
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
        
        
        patient.tot_system_time = self.env.now - patient.time_entered_in_system
        ED_sim.add_to_df(self, patient)
        
    
    def add_to_df(self, patient):
        '''
        Basically takes all the variables and adds them to the dataframe without having to enter them manually with 
        4 line codes in every function
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
            'Service_time_receptionist'].sum()/g.run_time
        self.Nurse_utilize = self.individual_level_results['Service_time_nurse'].sum()/g.run_time
        self.ED_doc_utilize = self.individual_level_results['Service_time_ed_doc'].sum()/g.run_time
        self.ACU_doc_utilize = self.individual_level_results['Service_time_acu_doc'].sum()/g.run_time
    
        
    
    def export_row_to_csv(self):
        '''
        Writes the results of an individual run as a row in a csv file in the desired folder
        '''
    
        with open (r"C:\Users\varad\Desktop\Education Material\Mathematical Modelling\HSMA\HSMA_modelling_ED\trial_results.csv",'a') as f:
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
            row_to_add = [self.Mean_Q_Rec_time,
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
        self.env.run(g.run_time)
        print(self.individual_level_results)
        self.individual_level_results.to_csv(r"C:\Users\varad\Desktop\Education Material\Mathematical Modelling\HSMA\HSMA_modelling_ED\individual_results.csv")
        self.mean_calculator()
        #self.export_to_csv()

class summary_statistics(object):
    '''
    This object calculates the mean, median or other summary statistics from a dataframe that has means of individual runs
    So this object calculates the means of means
    '''
    def __init__(self):
        pass
    
    def mean_of_means(self, dataframe):
        
        #mean of reg times
        #mean of q time for rec
        #mean of q time for nurse
        #mean of q time for ed doc
        #mean of q time for acu doc
        #mean of sum of all q times
        #sum of ed service times
        #sum of acu service times
        #percent service utilisation
        pass
        

def sim(number_of_runs):
    '''
    runs the simulation for the specified number of times
    '''
    pass


def change_initial_condition(independent_variable):
    '''
    This function, modifies the initial condition once such as increases the inter-arrival time by a certain increment
    And stores the results of all the sims for the different initial condition in a different dataframe
    '''

def file_opener(filename):
    '''
    Opens a file when given a filename or a filepath and makes it suitable for writing
    '''
    pass

def file_opener(filename):
    '''
    Adds one row to the filename that is passed to it
    '''
    #This is not the most compulsory function here as the above function will also create a file if it does not exist already
    with open (r"C:\Users\varad\Desktop\Education Material\
               Mathematical Modelling\HSMA\HSMA_modelling_ED\trial_results",'w') as f:
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




def Plotter (dataframe):
    '''
    takes in a dataframe and returns a nice plot
    '''
    pass

ED_sim(1).run()
    

        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


