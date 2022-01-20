import numpy as np
import h5py
import pandas as pd
from pathlib import Path

"""Low freq cutoff, general directory & output directory"""

f0 = 16
GenPath = 'home/calum/BH-Iso/'
output = 'O3aEvents/'

def loadSamples(path,name,f0, table1='C01:IMRPhenomPv2',table2 = 'posterior_samples',table3 = 'psds', H = 'H1', L='L1', V= 'V1'):
    """function to read and export relevant data from O3a data release
        --------------------------------------------------------------
        Parameters:
            name: 
                h5 or hdf5 filename without file extension
            path:
                location of file within directory"""
    
    filename = name + '.h5'
    print('Loading '+filename)
    e = "/C01:IMRPhenomPv2/" in h5py.File(filename, 'r')
    if e == False:
        print("IMRPhenomPv2 not found, using IMRPhenomPv3HM instead")
        table1='C01:IMRPhenomPv3HM'
    
    fullData = h5py.File(filename, 'r')[table1]
    post = np.array(fullData[table2])
    psds = fullData[table3]
    
    h = "/C01:IMRPhenomPv2/psds/H1" in h5py.File(filename, 'r')
    l = "/C01:IMRPhenomPv2/psds/L1" in h5py.File(filename, 'r')
    v = "/C01:IMRPhenomPv2/psds/V1" in h5py.File(filename, 'r')
    if h == True and l == True:
        freq = np.nan_to_num(np.array(psds[H]),posinf=0,neginf=0)[:,0]
        """discard below 16Hz; data is unusable"""
        j = f0*4; k = len(freq) ##Start and end of discarded data
        if v == True:
            H_psd,L_psd,V_psd = [np.nan_to_num(np.array(psds[i]),posinf=0,neginf=0)[:,1] for i in (H,L,V)]
            df = pd.DataFrame({'Freq':freq[j:k],
                            'H1_PSD':H_psd[j:k],
                            'L1_PSD':L_psd[j:k],
                              'V1_PSD':V_psd[j:k]})
        elif v == False:
            H_psd,L_psd = [np.nan_to_num(np.array(psds[i]),posinf=0,neginf=0)[:,1] for i in (H,L)]
            df = pd.DataFrame({'Freq':freq[j:k],
                            'H1_PSD':H_psd[j:k],
                            'L1_PSD':L_psd[j:k]})
    
        PSD_file = name +'_PSDs.txt'
        PSD_dir = Path(path + 'PSDs/')
        post_file = name +'_posterior.h5'
        post_dir = Path(path + 'Posteriors/')

        PSD_dir.mkdir(parents=True, exist_ok=True)
        post_dir.mkdir(parents=True, exist_ok=True)
    
        df.to_csv(PSD_dir / PSD_file,index=False,sep ='\t')
    
        with h5py.File(post_dir / post_file, 'w') as h:
            dset = h.create_dataset('IMRPhenomPv2_posterior', data = post)
    
        print("Posterior and PSD file generated for " + name)
    else:
        print("H1 or L1 data not found; skipping candidate...")
    
nameList=['GW190408_181802',
           'GW190412',
           'GW190413_052954',
           'GW190413_134308',
           'GW190421_213856',
           'GW190424_180648',
           'GW190426_152155',
           'GW190503_185404',
          'GW190512_180714',
          'GW190513_205428',
          'GW190514_065416',
          'GW190517_055101',
          'GW190519_153544',
          'GW190521',
          'GW190527_092055',
          'GW190602_175927',
          'GW190620_030421',
          'GW190630_185205',
          'GW190701_203306',
          'GW190706_222641',
          'GW190707_093326',
          'GW190708_232457',
          'GW190719_215514',
          'GW190727_060333',
          'GW190728_064510',
          'GW190731_140936',
          'GW190803_022701',
          'GW190814',
          'GW190828_063405',
          'GW190828_065509',
          'GW190909_114149',
          'GW190910_112807',
          'GW190915_235702',
          'GW190924_021846',
          'GW190929_012149',
          'GW190930_133541']

for name in nameList:
        loadSamples(output,name,f0)