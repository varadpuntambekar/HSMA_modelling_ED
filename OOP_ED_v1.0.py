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
    number_of_runs = 100
    warmup_time = 1440 #24 hours and 60 minutes per hour
    run_time = 48*60 # mins

class ed_patient (object):
    '''
    Defines the patient characteristics. Could be interesting if we have different types of patients
    But for this exercise we have only one type of patient that is a regular patient that has a 20% chance 
    of going to the ACU. Also important to store patient level variables to then summarize and plot
    '''
    def __init__(self, uhid):
        self.id = uhid
        self.q_reception = 0 #declaring these variables as they will be recorded and manipulated with later
        self.q_nurse = 0
        self.ed_ass_time = 0
        self.ace_ass_time = 0
        self.tot_system_time = 0

class ED_sim (object):
    '''
    This is the actual clinic where everything is simulated.
    '''
    def __init__(self, run_number):
        self.env = simpy.Environment()
        #declaring resources
        self.receptionist = simpy.Resource(self.env, capacity = g.receptionist)
        self.nurse = simpy.Resource(self.env, capacity = g.nurse)
        self.ed_doc = simpy.Resource(self.env, capacity = g.ed_doc)
        self.acu_doc = simpy.Resource(self.env, capacity = g.acu_doc)
        self.run_number = run_number
        
        #initiating a dataframe with required columns
        self.individual_level_results = pd.DataFrame({
            "UHID" :[], 
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
        
        
    def generate_ed_arrivals(self):
        pass
    
    def registration(self, patient):
        pass
    
    def triage (self, patient):
        pass
    
    def ed_ass (self, patient):
        pass
    
    def acu_ass (self, patient):
        pass    
    
    def mean_calculator (self, dataframe):
        '''
        calculates the average statistic for each individual run for all the different KPIs and maybe stores it in a global database
        '''
        pass
    
    def run (self):
        '''
        suns the simulation program
        '''

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


    

        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


