import numpy as np
from pathlib import Path
import pandas as pd


conv = 1126086553.0 / 36124.446480869694

genPath = '/scratch/wiay/2311453s/Data/PSD_data/'
def GPSconvert(path,name):
    fullData = np.genfromtxt(path)
    GPSStart = fullData[:,0]
    GPSEnd = fullData[:,1]
    GMSTStart = [i / conv for i in GPSStart]
    GMSTEnd = [i / conv for i in GPSEnd]

    df = pd.DataFrame({'GPSstart':GPSStart,
                            'GPSend':GPSEnd,
                            'GMSTstart':GMSTStart,
                              'GMSTend':GMSTEnd})
    output_dir = Path('/home/2311453s/BH-Iso/obs_times/')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_dir / name,index=False,sep ='\t')
    
timeList = ['Obs_time_O3a.txt','Obs_time_O3b.txt']

for i in timeList:
    GPSconvert(genPath + i,i)