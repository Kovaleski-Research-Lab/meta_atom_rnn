"""
Purpose: Evaluate Trained Systems
Author: Andy
"""


import os
import shutil
import yaml
import numpy as np
import pickle
from IPython import embed

#from utils.data import load_data
from utils.general import create_folder
from utils.measures import get_all_measures
from utils.network.support import get_all_model_predictions, organize_analysis
from utils.plots import plot_loss, plot_bars
import utils.plots as plots
from utils.network.load_results import get_save_folders


def run(params):

    # N O T E!! we are running eval for real-valued results.
    print("------ Running Evaluation ------")

    if params['deployment_mode'] == 0:
        path_analysis = params['mounted_paths']['results']['analysis']
        path_results = params['mounted_paths']['results']['checkpoints']
    elif params['deployment_mode'] == 1:
        path_analysis = params['kube']['train_job']['paths']['results']['analysis']
        path_results = params['kube']['train_job']['paths']['results']['model_results']
    else:
        raise NotImplementedError

    all_measures = pickle.load(open(os.path.join(path_analysis,'all_measures.pkl'),'rb')) # this returns aggregates for bar plots
    all_preds = pickle.load(open(os.path.join(path_analysis,'all_preds.pkl'),'rb'))
    all_loss = pickle.load(open(os.path.join(path_analysis,'all_loss.pkl'),'rb'))

    print("------ Plotting Loss ------")
    plot_loss(params, all_loss, path_results) #pass domain_choice='imag' if you want imaginary vals 
    
    print("------ Plotting Bar Plots ------")
    plot_bars(params, all_measures, path_results)     
    
    print("------ Plotting Images ------\n")
    plots.plot_truth_and_pred_images(params, all_preds, path_results) 
    
    print("------ Creating Images Flipbooks ------\n")
    plots.create_flipbook_videos(params,'images', path_results)
     
    print("------ Plotting Measures ------\n")
    plots.plot_truth_and_pred_measures(params, all_preds, path_results)
    
    print("------ Creating Measures Flipbooks ------\n")
    plots.create_flipbook_videos(params,'measures', path_results) 
  
    print("----- Creating scatter plot across all experiments ------\n")
    plots.scatter_plots(params, all_measures, path_results, path_analysis) 
    
    print("----- Evaluation complete. -----")

    # move all presentation files to a single folder because it's convenient #
  
    flipbooks_dir = "all_flipbooks"
    organize_analysis(params, path_analysis, flipbooks_dir, 'flipbooks', '.avi')     

    loss_dir = "all_loss"
    organize_analysis(params, path_analysis, loss_dir, 'loss', '.pdf')     

    bars_dir = "all_bars"
    organize_analysis(params, path_analysis, bars_dir, 'measures', '.pdf')
    
    
