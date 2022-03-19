import numpy as np
import os

from detections import Event, Run

"""Location of directory"""
path = os.path.dirname(__file__)
folder = os.path.basename(path)
parent = path.replace(folder,"") # parent directory
"""Seperate directory if you want your data and output to be sent elsewhere"""
DataPath = parent
# DataPath = '/scratch/wiay/2311453s/'

def events_list(nposts=500, simulated=False, multiplicity=10):
    events = list()
    O1_events = ['GW150914', 'GW151012', 'GW151226',]
    O2_events = ['GW170104', 'GW170608', 'GW170729', 'GW170809', 'GW170814','GW170818', 'GW170823']
    O3a_events = ['GW190408_181802',
              'GW190412',
              'GW190413_052954',
              'GW190413_134308',
              'GW190421_213856',
              'GW190503_185404',
              'GW190426_152155',
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
              'GW190803_022701',
              'GW190814',
              'GW190828_063405',
              'GW190828_065509',
              'GW190909_114149',
              'GW190910_112807',
              'GW190915_235702',
              'GW190924_021846',
              'GW190929_012149',
              'GW190930_133541'
                 ]
    O3b_events = ['GW191103_012549',
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

    if simulated:
        O1_events = []
        O2_events = ['GW170814'] * multiplicity

    for name in O1_events:
        print('Loading event {}'.format(name))
        run = 'O1'
        samp = DataPath + 'Data/GWTC-1_sample_release/{}_GWTC-1.hdf5'.format(name)
        pofd = DataPath + 'Data/Run_O1/Events/Pofd_{}_marg.p'.format(name)
        time = int(np.genfromtxt(DataPath + 'Data/times/{}.txt'.format(name)))
        events.append(Event(name, run, time, samp, pofd, nposts=nposts))

    for name in O2_events:
        print('Loading event {}'.format(name))
        run = 'O2'
        samp = DataPath + 'Data/GWTC-1_sample_release/{}_GWTC-1.hdf5'.format(name)
        pofd = DataPath + 'Data/Run_O2/Events/Pofd_{}_marg.p'.format(name)
        time = int(np.genfromtxt(DataPath + 'Data/times/{}.txt'.format(name)))
        events.append(Event(name, run, time, samp, pofd, nposts=nposts))
        
    for name in O3a_events:
        print('Loading event {}'.format(name))
        run = 'O3a'
        samp = DataPath + 'Data/GWTC-2/{}_posterior.h5'.format(name)
        pofd = DataPath + 'Data/Run_O3a/Events/Pofd_{}_marg.p'.format(name)
        time = int(np.genfromtxt(DataPath + 'Data/times/{}.txt'.format(name)))
        events.append(Event(name, run, time, samp, pofd, nposts=nposts))
        
    for name in O3b_events:
        print('Loading event {}'.format(name))
        run = 'O3b'
        samp = DataPath + 'Data/GWTC-3/{}_posterior.h5'.format(name)
        pofd = DataPath + 'Data/Run_O3b/Events/Pofd_{}_marg.p'.format(name)
        time = int(np.genfromtxt(DataPath + 'Data/times/{}.txt'.format(name)))
        events.append(Event(name, run, time, samp, pofd, nposts=nposts))

    return events

def runs_list():
    mean_pofd_path_O1 = DataPath + 'Data/Run_O1/Events/Pofd_early_average.p'
    obs_times_O1 = DataPath + 'Data/PSD_data/Obs_time_O1.txt'
    mean_pofd_path_O2 = DataPath + 'Data/Run_O2/Events/Pofd_mid_average.p'
    obs_times_O2 = DataPath + 'Data/PSD_data/Obs_time_O2.txt'
    mean_pofd_path_O3a = DataPath + 'Data/Run_O3a/Events/Pofd_mid_average.p'
    obs_times_O3a = DataPath + 'Data/PSD_data/Obs_time_O3a.txt'
    mean_pofd_path_O3b = DataPath + 'Data/Run_O3b/Events/Pofd_late_average.p'
    obs_times_O3b = DataPath + 'Data/PSD_data/Obs_time_O3b.txt'
    runs = [Run('O1', mean_pofd_path_O1, obs_times_O1),
            Run('O2', mean_pofd_path_O2, obs_times_O2),
            Run('O3a', mean_pofd_path_O3a, obs_times_O3a),
            Run('O3b', mean_pofd_path_O3b, obs_times_O3b)]
    print('Loaded runs')
    return runs
