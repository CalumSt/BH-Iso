import numpy as np
import h5py
import pandas as pd
from pathlib import Path

def loadSamples(name,f0 = 16, table1='C01:IMRPhenomPv2',table2 = 'posterior_samples',table3 = 'psds', H = 'H1', L='L1', V= 'V1'):
    """function to read and export relevant data from O3a data release
        --------------------------------------------------------------
        Parameters:
            name: 
                h5 or hdf5 filename without file extension
            f0:
                Low-frequency cutoff, data dependent. 16Hz by default"""

    try:
        filename = name + '.h5' # O3a format
        f = h5py.File(filename, 'r')
        output = 'O3aEvents/'
    except:
        filename = 'IGWN-GWTC3p0-v1-%s_PEDataRelease_mixed_cosmo.h5' %(name) # O3b format
        f = h5py.File(filename, 'r')
        output = 'O3bEvents/'
    print('Loading '+filename)
    e = "/C01:IMRPhenomPv2/" in h5py.File(filename, 'r')
    if e == False:
        e = "/C01:IMRPhenomPv3HM/" in h5py.File(filename, 'r')
        if e == True:
            print("IMRPhenomPv2 not found, using IMRPhenomPv3HM instead...")
            table1='C01:IMRPhenomPv3HM'
        if e == False:
            print("Using IMRPhenomXPHM...")
            table1 = 'C01:IMRPhenomXPHM'
    
    fullData = f[table1]
    post = np.array(fullData[table2])
    psds = fullData[table3]
    
    h = "/" + table1 + "/psds/H1" in h5py.File(filename, 'r')
    l = "/" + table1 + "/psds/L1" in h5py.File(filename, 'r')
    v = "/" + table1 + "/psds/V1" in h5py.File(filename, 'r')
    if h == False: 
        freq = np.nan_to_num(np.array(psds[L]),posinf=0,neginf=0)[:,0]
        """discard below 16Hz; data is unusable"""
        j = f0*4; k = len(freq) ##Start and end of discarded data
        L_psd,V_psd = [np.nan_to_num(np.array(psds[i]),posinf=0,neginf=0)[:,1] for i in (L,V)]
        df = pd.DataFrame({'Freq':freq[j:k],
                            'L1_PSD':L_psd[j:k],
                            'V1_PSD':V_psd[j:k]})
    elif l == False:
        freq = np.nan_to_num(np.array(psds[H]),posinf=0,neginf=0)[:,0]
        j = f0*4; k = len(freq)
        H_psd,V_psd = [np.nan_to_num(np.array(psds[i]),posinf=0,neginf=0)[:,1] for i in (H,V)]
        df = pd.DataFrame({'Freq':freq[j:k],
                            'H1_PSD':H_psd[j:k],
                            'V1_PSD':V_psd[j:k]})
        
    elif v == False:
        freq = np.nan_to_num(np.array(psds[L]),posinf=0,neginf=0)[:,0]
        j = f0*4; k = len(freq)
        H_psd,L_psd = [np.nan_to_num(np.array(psds[i]),posinf=0,neginf=0)[:,1] for i in (H,L)]
        df = pd.DataFrame({'Freq':freq[j:k],
                            'H1_PSD':H_psd[j:k],
                            'L1_PSD':L_psd[j:k]})
        
    else:
        freq = np.nan_to_num(np.array(psds[L]),posinf=0,neginf=0)[:,0]
        j = f0*4; k = len(freq)
        H_psd,L_psd,V_psd = [np.nan_to_num(np.array(psds[i]),posinf=0,neginf=0)[:,1] for i in (H,L,V)]
        df = pd.DataFrame({'Freq':freq[j:k],
                            'H1_PSD':H_psd[j:k],
                            'L1_PSD':L_psd[j:k],
                              'V1_PSD':V_psd[j:k]})

    
    PSD_file = name +'_PSDs.txt'
    PSD_dir = Path(output + 'PSDs/')
    post_file = name +'_posterior.h5'
    post_dir = Path(output + 'Posteriors/')

    PSD_dir.mkdir(parents=True, exist_ok=True)
    post_dir.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(PSD_dir / PSD_file,index=False,sep ='\t')
    
    with h5py.File(post_dir / post_file, 'w') as h:
        dset = h.create_dataset('IMRPhenomPv2_posterior', data = post)
    
    print("Posterior and PSD file generated for " + name)
    
nameList=['GW190408_181802',
          'GW190412',
           'GW190413_052954',
           'GW190413_134308',
           'GW190421_213856',
           'GW190426_152155',
           'GW190503_185404',
          'GW190512_180714',
          'GW190513_205428',
          'GW190514_065416',
          'GW190517_055101',
          'GW190519_153544',
          'GW190521',
          'GW190521_074359',
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
          'GW190930_133541',
          'GW191103_012549',
          'GW191105_143521',
          'GW191109_010717',
          'GW191113_071753',
          'GW191126_115259',
          'GW191127_050227',
          'GW191129_134029',
          'GW191204_110529',
          'GW191204_171526',
          'GW191215_223052',
          'GW191216_213338',
          'GW191222_033537',
          'GW191230_180458',
          'GW200112_155838',
          'GW200128_022011',
          'GW200129_065458',
          'GW200202_154313',
          'GW200208_130117',
          'GW200208_222617',
          'GW200209_085452',
          'GW200210_092254',
          'GW200216_220804',
          'GW200219_094415',
          'GW200220_061928',
          'GW200220_124850',
          'GW200224_222234',
          'GW200225_060421',
          'GW200302_015811',
          'GW200306_093714',
          'GW200308_173609',
          'GW200311_115853',
          'GW200316_215756',
          'GW200322_091133'
         ]

for name in nameList:
        loadSamples(name,f0=16)