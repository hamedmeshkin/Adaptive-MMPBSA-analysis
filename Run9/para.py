#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 12:23:39 2021

@author: smeshkin
"""
import sys
import os
import glob
import random
import operator
import shutil
import scipy.optimize # used for its nice minimization functions
import numpy
import math
import time
import pickle
import subprocess
import datetime
import textwrap
import copy
import multiprocessing
import string
import os.path
from os import path
import pandas as pd
from multiprocessing import Pool


def define_defaults(): # this function is first to make it easy for the user to modify the default parameters (see, especially, the boxes below)
    """Sets the command-line parameters to their default values."""
    
    vars = {}
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    
    ################################################################# FILE-LOCATION VARIABLES ###################################################################################
    vars['mgltools_directory'] = "/opt/mgltools/"                               # Example: vars['mgltools_directory'] = "/home/myname/MGLTools-1.5.4/"
    vars['openbabel_bin_directory'] = "/usr/bin/"                           # Example: vars['openbabel_bin_directory'] = "/home/myname/openbabel-2.2.0/bin/"
    vars['executable'] = "source "                               # Example: vars['executable'] ="/home/myname/autodock_vina_1_1_2_linux_x86/bin/vina"
    # Example: vars['nn2_script'] ="/home/myname/NNScore/NNScore_2.01/NNScore2.01.py"
    #############################################################################################################################################################################
    
 
    
    vars['center_x'] = 0.00
    vars['center_y'] = 0.00
    vars['center_z'] = 11.0
    vars['size_x'] = 13.0
    vars['size_y'] = 13.0
    vars['size_z'] = 15.0
    vars['num_processors'] = 30 # with this setting, the program will use all processors available
    vars['directory_of_source_compounds'] = "File/" 
    vars['filename_of_receptor'] = "HexChainH.pdbqt" 
    vars['output_dir'] = "." + os.sep + "output" + os.sep
    vars['scoring_function'] = "VINA"
 
    
    return vars


class multi_threading(): 
    """Launch jobs on multiple processors"""
    
    def __init__(self, inputs, task_class_name, variables_to_pass):
        """Launches jobs on multiple processors
        
        Arguments:
        inputs -- the data to be processed, in a list
        task_class_name -- the name of the class charged with managing the jobs assigned to each processor, a string
        variables_to_pass -- additional variables (usually command-line parameters) to be passed to each processor, a dictionary

        """
        
        if len(inputs) == 0: return

        vars = define_defaults()
        num_processors = vars['num_processors']
        
        if num_processors == 1: # so it's running on just one processor, don't even try to parallelize it
            run_class = task_class_name()
            for inp in inputs: run_class.value_func(inp, variables_to_pass)

        else: # so run in parallel
            # first, if num_processors <= 0, determine the number of processors to use programatically
            if num_processors <= 0: num_processors = multiprocessing.cpu_count()
    
            # reduce the number of processors if too many have been specified
            if len(inputs) < num_processors: num_processors = len(inputs)
    
            # if the appropriate filename is present, write the contents for record-keeping purposes
            if 'log_filename' in variables_to_pass.keys():
                f = open(variables_to_pass['log_filename'],'w')
                for an_input in inputs: f.write(an_input + "\n")
                f.close()
    
            # now, divide the inputs into the appropriate number of processors
            inputs_divided = {}
            for t in range(num_processors): inputs_divided[t] = []
    
            for t in range(0, len(inputs), num_processors):
                for t2 in range(num_processors):
                    index = t + t2
                    if index < len(inputs): inputs_divided[t2].append(inputs[index])
    
            # now, run each division on its own processor
            running = multiprocessing.Value('i', num_processors)
            mutex = multiprocessing.Lock()
    
            arrays = []
            threads = []
            for i in range(num_processors):
                threads.append(task_class_name())
                arrays.append(multiprocessing.Array('i',[0, 1]))
    
            processes = []
            for i in range(num_processors):
                p = multiprocessing.Process(target=threads[i].runit, args=(running, mutex, inputs_divided[i], variables_to_pass))
                p.start()
                processes.append(p)
    
            while running.value > 0: is_running = 0 # wait for everything to finish

class general_task: # other, more specific classes with inherit this one
    """Run jobs on a single processor"""
    
    def runit(self, running, mutex, items, variables_to_pass):
        """Run jobs on a single processor
        
        Arguments:
        running -- a multiprocessing.Value() object
        mutex -- a multiprocessing.Lock() object
        items -- the data to be processed, in a list
        variables_to_pass -- additional variables (usually command-line parameters) to be passed to each processor, a dictionary

        """

        for item in items: self.value_func(item, variables_to_pass)
        mutex.acquire()
        running.value -= 1
        mutex.release()


class execute_command(general_task):
    """Run shell commands on a single processor"""
    
    def value_func(self, command, variables_to_pass):
        """Run a single shell command
        
        Arguments:
        command -- the command to run, a string
        variables_to_pass -- additional variables (usually command-line parameters)

        """

        log("Executing: " + command)
        proc = subprocess.Popen(command, shell=True)
        for idx in range(variables_to_pass['seconds_per_job']):
            if proc.poll() is not None: # so it is not running
                break
            time.sleep(1)
        if proc.poll() is None: # so it is still running
            proc.terminate()
            log("Had to terminate a job early: " + command)


def log(thestring):
    """Print text to the screen and to a log file

    Arguments:
    thestring -- the text to print, a string.
    
    """

    global log_text_file

    print(thestring)

    # Ensure log_text_file variable is defined. If so, write to file.
    try:
        log_text_file
    except NameError:
        log_text_file = None
    
    # Test whether variable is defined to be None
    if not log_text_file is None: log_text_file.write(str(thestring) + "\n")

def dock_compounds(directory):
    """Dock the ligand pdbqt files in a given directory using AutoDock Vina
    
    Arguments:
    directory -- the filename, a string.
    
    """
    vars = define_defaults()
    count = 0
    
    count = count + 1
    if count > 10000:
        log("ERROR: I've tried 10,000 times to dock the PDBQT files of " + directory + ". Aborting program...")
        sys.exit(0)
     
    # receptors = vars['filename_of_receptor']
    
    # find ligands that have not been docked
    need_to_dock = []
    for filename in glob.glob(directory + "/*.sh"):
        if not os.path.exists(filename + ".vina"): need_to_dock.append(filename)
    
    # do the docking of the needed ligands
    jobs = []
    output = vars['output_dir'] 
    def dock_vina(lig_filename):
        receptors = vars['filename_of_receptor']
        torun = vars['executable'] + lig_filename   
        return(torun)
        dock_vina()
        
    for lig_filename in need_to_dock:
        torun = dock_vina(lig_filename)
        jobs.append(torun)
    print(jobs)
    multi_threading(jobs, execute_command, {'seconds_per_job': 6000000}) # give it only ten minutes per docking

class run_main():    #
    vars = define_defaults()
    source_compounds = vars['directory_of_source_compounds'] 
    try:
        os.makedirs(vars['output_dir'] + source_compounds )
    except:
        print('The output Directory already exsists')
        
    log("Docking compounds using AutoDock Vina...")
    dock_compounds(source_compounds)
# if __name__=="__main__": dorun = run_main(sys.argv)
