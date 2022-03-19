import pickle
import joblib
import datetime
import errno
import numpy as np
import os

"""Location of directory"""
path = os.path.dirname(__file__)
folder = os.path.basename(path)
parent = path.replace(folder,"") # parent directory
"""Output directory, set equal to parent if you don't need the output to be sent elsewhere"""
# DataPath = parent
DataPath = '/scratch/wiay/2311453s/'



def addSecs(tm, secs):
	fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
	fulldate = fulldate + datetime.timedelta(seconds=secs)
	return fulldate.time()


def openPickle(path):
	try:
		obj = joblib.load(path)
		return obj
	except IOError as e:
		print((os.strerror(e.errno)))
		return -1


def savePickle(obj, path):
	if not os.path.exists(os.path.dirname(path)):
		try:
			os.makedirs(os.path.dirname(path))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	joblib.dump(obj, path, compress=True, protocol=pickle.HIGHEST_PROTOCOL)


def dictEvent(name, run,detectors):
	t = np.genfromtxt(DataPath + 'Data/times/%s.txt'%(name))
	d = {
		'name' :            name,
		'run' :             run,
        'detectors':        detectors,
		'postSamplePath' :  DataPath + 'Data/GWTC-1_sample_release/%s_GWTC-1.hdf5' %(name),
		'pofdPath':     DataPath + 'Data/Run_%s/Events/Pofd_%s.p' %(run, name),
		'pofdMargPath' : DataPath + 'Data/Run_%s/Events/Pofd_%s_marg.p' %(run, name),
		'psdPath':      DataPath + 'Data/Run_%s/Posterior_samples/GWTC1_%s_PSDs.dat.txt' %(run,name),
                'time': t
		}
	return d

def dictEventO3a(name, run, detectors):
	t = np.genfromtxt(DataPath + 'Data/times/%s.txt'%(name))
	d = {
		'name' :            name,
		'run' :             run,
        'detectors':        detectors,
		'postSamplePath' :  DataPath + 'Data/GWTC-2/%s_posterior.h5' %(name),
		'pofdPath':     DataPath + 'Data/Run_%s/Events/Pofd_%s.p' %(run, name),
		'pofdMargPath' : DataPath + 'Data/Run_%s/Events/Pofd_%s_marg.p' %(run, name),
		'psdPath':      DataPath + 'Data/Run_%s/Posterior_samples/%s_PSDs.txt' %(run,name),
                'time': t
		}
	return d

def dictEventO3b(name, run,detectors):
	t = np.genfromtxt(DataPath + 'Data/times/%s.txt'%(name))
	d = {
		'name' :            name,
		'run' :             run,
        'detectors':        detectors,
		'postSamplePath' :  DataPath + 'Data/GWTC-3/%s_posterior.h5' %(name),
		'pofdPath':     DataPath + 'Data/Run_%s/Events/Pofd_%s.p' %(run, name),
		'pofdMargPath' : DataPath + 'Data/Run_%s/Events/Pofd_%s_marg.p' %(run, name),
		'psdPath':      DataPath + 'Data/Run_%s/Posterior_samples/%s_PSDs.txt' %(run,name),
                'time': t
		}
	return d

def dictRun(run, psdFile,VpsdFile, obsTfile, desc):
    d = {
        'run' :         run,
        'psdPath':      DataPath + 'Data/PSD_data/%s' %(psdFile), # LIGO PSD
        'VpsdPath':     DataPath + 'Data/PSD_data/%s' %(VpsdFile), # Virgo PSD, included but redundant for O1
        'obsTpath':     DataPath + 'Data/PSD_data/%s' %(obsTfile),
        'pofdPath':     DataPath + 'Data/Run_%s/Events/Pofd_%s.p' %(run, desc),
        'pofdMargPath': DataPath + 'Data/Run_%s/Events/Pofd_%s_marg.p' %(run, desc),
        'pofdAvPath' :  DataPath + 'Data/Run_%s/Events/Pofd_%s_average.p' %(run, desc),        
        }
    return d

def loadSamples(filename, table='IMRPhenomPv2_posterior'):
    import h5py
    print('Loading '+filename)
    f = h5py.File(filename, 'r')
    try:
        return f[table]
    except KeyError:
        try:
            return f['IMRPhenomPv3HM_posterior']
        except KeyError:
            try:
                return f['IMRPhenomXPHM_posterior']
            except KeyError:
                print('Unknown waveform type for posterior samples')
                return f['posterior']

