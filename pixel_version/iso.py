import numpy as np
import healpy as hp
import shutil
import os
from pathlib import Path
import matplotlib.pyplot as plt

from detections import Event, Run
from setup import events_list, runs_list
from model import IsotropicModel, NumericalIsotropicModel

"""Location of directory"""
GenPath = '/home/2311453s/BH-Iso/pixel_version'

events = events_list()
runs = runs_list()

"""Numerical Isotropic Solution"""
num_model = NumericalIsotropicModel(events, runs)

result = num_model.maximum_logpost
x = result[0]
x = x.tolist()
log_y = result[1]
#log_y.tolist()
x_y = list(zip(x,log_y))

output = 'iso_result/'               
out_file ='iso_max_logpost.txt'
output_ = Path(output,sep ='\t')
output_.mkdir(parents=True, exist_ok=True)
np.savetxt(os.path.join(GenPath , output + out_file), x_y)

evidence_header = "log_evidence"
evidence = num_model.log_evidence

o = open(os.path.join(GenPath , 'iso_result/iso_evidence.txt'),'w')
print(evidence_header,evidence,sep = '\n', file=o)
o.close()

"""Isotropic Solution"""
iso_model = IsotropicModel(events, runs)

header = ("alpha","beta")
result = (iso_model.alpha_const,iso_model.beta_const)

o = open(os.path.join(GenPath , 'iso_result/iso.txt'),'w')
print(header,result,sep = '\n', file=o)
o.close()