import numpy as np

from detections import Event, Run

GenPath = '/root/Home/BH-Iso/'

def events_list(nposts=5000, simulated=False, multiplicity=10):
    events = list()
    O1_events = ['GW150914', 'GW151012', 'GW151226',]
    O2_events = ['GW170104', 'GW170608', 'GW170729', 'GW170809', 'GW170814',
                 'GW170818', 'GW170823']
    if simulated:
        O1_events = []
        O2_events = ['GW170814'] * multiplicity

    for name in O1_events:
        print('Loading event {}'.format(name))
        run = 'O1'
        samp = '../../Data/GWTC-1_sample_release/{}_GWTC-1.hdf5'.format(name)
        pofd = '../../Data/Run_O1/Events/Pofd_{}_marg.p'.format(name)
        time = int(np.genfromtxt('../../Data/times/{}.txt'.format(name)))
        events.append(Event(name, run, time, samp, pofd, nposts=nposts))

    for name in O2_events:
        print('Loading event {}'.format(name))
        run = 'O2'
        samp = '../../Data/GWTC-1_sample_release/{}_GWTC-1.hdf5'.format(name)
        pofd = '../../Data/Run_O2/Events/Pofd_{}_marg.p'.format(name)
        time = int(np.genfromtxt('../../Data/times/{}.txt'.format(name)))
        events.append(Event(name, run, time, samp, pofd, nposts=nposts))

    return events

def runs_list():
    mean_pofd_path_O1 = '../../Data/Run_O1/Events/Pofd_early_average.p'
    obs_times_O1 = '../../Data/PSD_data/Obs_time_O1.txt'
    mean_pofd_path_O2 = '../../Data/Run_O2/Events/Pofd_mid_average.p'
    obs_times_O2 = '../../Data/PSD_data/Obs_time_O2.txt'
    runs = [Run('O1', mean_pofd_path_O1, obs_times_O1),
            Run('O2', mean_pofd_path_O2, obs_times_O2)]
    print('Loaded runs')
    return runs
