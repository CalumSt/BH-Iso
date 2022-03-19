import numpy as np
import healpy as hp
from scipy import special as sp
import shutil
import os
from pathlib import Path
import matplotlib.pyplot as plt

from detections import Event, Run
from setup import events_list, runs_list
from model import IsotropicModel, NumericalIsotropicModel

"""Location of directory"""

path = os.path.dirname(__file__)
folder = os.path.basename(path)
parent = path.replace(folder,"") # parent directory of all scripts
# parent = '/home/2311453s/BH-Iso/pixel_version' # can set manually if needed

events = events_list()
runs = runs_list()

"""Numerical Isotropic Solution"""
num_model = NumericalIsotropicModel(events, runs) # read in isotropic model
R_bounds = (1e-5,750)                             # define upper and lower bounds of the Rate R
R = np.linspace(R_bounds[0],R_bounds[1],5000)
dR = R[1] - R[0]

result = num_model.maximum_logpost                # generate and save the maximum log posterior
x = result[0]
x = x.tolist()
log_y = result[1]
#log_y.tolist()
x_y = list(zip(x,log_y))
max_logpost = result[2]
print(max_logpost)

output = 'iso_result/'               
out_file ='iso_max_logpost.txt'
output_ = Path(output,sep ='\t')
output_.mkdir(parents=True, exist_ok=True)
np.savetxt(os.path.join(parent , output + out_file), x_y)

log_post = [num_model.log_posterior(i / (4*np.pi)) for i in R] # factor of 4pi given by R = 4pi * a0
shft_Post = log_post - min(log_post) - 2000 # shift by the (absolute) max to get values of log_post within (-745,709)
res = np.where(shft_Post < 0 , 0, shft_Post) # replace values outside of max - 2000 range with 0, don't care about being more accurate
post = [np.exp(i) for i in shft_Post] 
post_corrected = np.nan_to_num(post,0) # remove exp(0) and replace with 0
dR = isoR[1] - isoR[0]
post_Area = np.sum([dR * i for i in post_corrected]) # calculate the area by approximating as a histogram
post_norm = [i  / post_Area for i in post_corrected] # normalise
norm_area = np.sum([dR * i for i in post_norm]) # test line, this should be equal to 1 for it be properly normalised

    if norm_area = 1.0:
        pass
    else:
        raise Exception("Not properly normalised, check the normalisation area and input data")
        
post_header = "Rate \t log_posterior \t normalised posterior"
path = os.path.join(parent , 'iso_result/post.txt')
data = list(zip(R,list(log_post_shft),list(post_norm)))
np.savetxt(path, data,header = post_header,fmt='%.8e')

evidence_header = "log_evidence"
evidence,log_post = num_model.log_evidence # calls on log_evidence from model.py
print("log_evidence = ", evidence)

o = open(os.path.join(parent , 'iso_result/iso_evidence.txt'),'w')
print(evidence_header,evidence,sep = '\n', file=o)
o.close()


"""Isotropic Solution"""
iso_model = IsotropicModel(events, runs)

header = ("alpha","beta")
result = (iso_model.alpha_const,iso_model.beta_const)

o = open(os.path.join(parent , 'iso_result/iso.txt'),'w')
print(header,result,sep = '\n', file=o)
o.close()