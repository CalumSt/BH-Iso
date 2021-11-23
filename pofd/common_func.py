import datetime
import os
import errno
import pickle
import joblib
import os
import errno
import numpy as np

GenPath = '/root/Home/BH-Iso/'

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


def dictEvent(name, run):
	t = np.genfromtxt(GenPath + 'data/times/%s.txt'%(name))
	d = {
		'name' :            name,
		'run' :             run,
		'postSamplePath' :  GenPath + 'data/GWTC-1_sample_release/%s_GWTC-1.hdf5' %(name),
		'pofdPath':     GenPath + 'data/Run_%s/Events/Pofd_%s.p' %(run, name),
		'pofdMargPath' : GenPath + 'data/Run_%s/Events/Pofd_%s_marg.p' %(run, name),
		'psdPath':      GenPath + 'data/Run_%s/Posterior_samples/GWTC1_%s_PSDs.dat.txt' %(run,name),
                'time': t
		}
	return d


def dictRun(run, psdFile, obsTfile, desc):
    d = {
        'run' :         run,
        'psdPath':      GenPath + 'data/PSD_data/%s' %(psdFile),
        'obsTpath':     GenPath + 'data/PSD_data/%s' %(obsTfile),
        'pofdPath':     GenPath + 'data/Run_%s/Events/Pofd_%s.p' %(run, desc),
        'pofdMargPath': GenPath + 'data/Run_%s/Events/Pofd_%s_marg.p' %(run, desc),
        'pofdAvPath' :  GenPath + 'data/Run_%s/Events/Pofd_%s_average.p' %(run, desc),        
        }
    return d

def loadSamples(filename, table='IMRPhenomPv2_posterior'):
    import h5py
    print('Loading '+filename)
    f = h5py.File(filename, 'r')
    return f[table]

