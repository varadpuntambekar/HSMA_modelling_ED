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
    run_time = 10 # mins

class ed_patient (object):
    '''
    Defines the patient characteristics. Could be interesting if we have different types of patients
    But for this exercise we have only one type of patient that is a regular patient that has a 20% chance 
    of going to the ACU. Also important to store patient level variables to then summarize and plot
    '''
    def __init__(self, uhid):
        self.id = uhid
        
        #declaring these variables as they will be recorded and manipulated with later
        self.q_reception = 0 
        self.q_nurse = 0
        self.ed_ass_time = 0
        self.ace_ass_time = 0
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
        
    def generate_ed_arrivals(self):
        while True:
            self.patient_counter += 1 #this is also the UHID of the patient
            
            ed_pt = ed_patient(self.patient_counter)
            
            self.time_entered_in_system = self.env.now #Used to calculate total time spent in the system
            
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
        
        self.q_time_rec = start_q_rec - end_q_rec
        
        
        
        register_time = random.triangular(0,g.mean_registeration, 2*g.mean_registeration)
        
        self.individual_level_results['Service_time_receptionist'] = register_time
        
        
        #add variables to the df
        ED_sim.add_to_df(self)
        print(self.individual_level_results)
        
        yield self.env.timeout(register_time)
    
    def triage (self, patient):
        pass
    
    def ed_ass (self, patient):
        pass
    
    def acu_ass (self, patient):
        pass    
    
    def add_to_df(self):
        '''
        Basically takes all the variables and adds them to the dataframe without having to enter them manually with 
        4 line codes in every function
        '''
        df_to_add = pd.DataFrame({
            "UHID" :[self.patient_counter],
            "Time_entered_in_system" : [self.time_entered_in_system],
            "Q_time_receptionist":[self.q_time_rec],
            
            #using zeros as placeholders
            "Q_time_nurse":[0],
            "Q_time_acu_doc":[0],
            "Q_time_ed_doc":[0],
            "Service_time_receptionist":[0],
            "Service_time_nurse":[0],
            "Service_time_acu_doc":[0],
            "Service_time_ed_doc":[0],
            "Total time in System":[0]        
              })
        
        df_to_add.set_index('UHID', inplace=True)
        self.individual_level_results._append(df_to_add)
        
        
        
    def mean_calculator (self, dataframe):
        '''
        calculates the average statistic for each individual run for all the different KPIs and maybe stores it in a global database
        '''
        
    
    def run (self):
        '''
        suns the simulation program
        '''
        self.env.process(self.generate_ed_arrivals())
        self.env.run(g.run_time)

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

def file_writer(filename):
    '''
    Adds one row to the filename that is passed to it
    '''
    
    pass




def Plotter (dataframe):
    '''
    takes in a dataframe and returns a nice plot
    '''
    pass

ED_sim(1).run()
    

        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


