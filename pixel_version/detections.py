"""File including convenience classes that hold information about
observing runs and detections"""
import numpy as np
import healpy as hp
import joblib
import h5py

class Event(object):
    """Convenience object holding information about a detection.
    By default downsamples the events
    ---------------------------
    Note:
        Currently useful only for posterior calculation. Might later edit
        this to include information for pofd calculation as well

        Add default downsampling
    ---------------------------
    Parameters:
        name: str
            Event name
        run: str
            Observing run
        time: int
            GPS detection time
        samples_path: str
            Path to the posterior samples file
        pofd_path: str
            Path to the probability of detection file
        pdf_dist: py:func
            Probability density function for luminosity distance.
            By default assumes Euclidean geometry $p(d)\propto d^2$
        dlmax: float, int (default 7500)
            Maximum luminosity distance Mpc in the analysis. Important that
            this matches value used in pofd calculation.
        nposts: int (default 10000)
            To how many posterior samples should it be downsampled
        seed: int (default=12345)
            Random seed. Recommended to stick with default for deterministic
            results.
        alpha: float (default -2.35)
            powelaw index for the pdf of the primary
        min_mass: int (default 5)
            Minimum component mass
    """
    def __init__(self, name, run, time, samples_path, pofd_path,
                 pdf_dist=None, dlmax=7500, nposts=500, seed=12345,
                 alpha=-2.35, min_mass=5):
        self._name = None
        self._run = None
        self._time = None
        self._post_samples = None
        self._pofd = None
        self._seed = seed
        # some default values
        self._alpha = alpha
        self.min_mass = min_mass
        self._nposts = nposts
        # Store inputs
        self.name = name
        self.run = run
        self.time = time
        self.post_samples = samples_path
        self.pofd = pofd_path
        self.dlmax = dlmax
        # Precalculate the probability of distance and mass
        self._pdist = self.pdf_dist(pdf_dist)
        self._pmass = self._pdf_mass()
        self._pmass /= np.sum(self._pmass)

        # Precalculate the position vectors on the sky
        try:
            theta = np.pi / 2 - self.post_samples['declination']
            phi = self.post_samples['right_ascension']
        except ValueError:
            theta = np.pi / 2 - self.post_samples['dec']
            phi = self.post_samples['ra']
        self._sky_vectors = hp.ang2vec(theta, phi).T
        # Pixel centers of the pofd map
        self._nside = hp.npix2nside(self.pofd.size)
        self._pofd_pixel_vectors = hp.pix2vec(self._nside,
                                              np.arange(self.pofd.size))

    @property
    def name(self):
        """Event name"""
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise ValueError('provide a str for name')
        self._name = name

    @property
    def run(self):
        """Which run the event was detected in"""
        return self._run

    @run.setter
    def run(self, run):
        if not isinstance(run, str):
            raise ValueError('provide a str for run')
        elif not run in ['O1', 'O2','O3a','O3b']:
            raise ValueError('invalid run identifier')
        self._run = run

    @property
    def time(self):
        """GPS detection time, ensures correct orientation of the
        interferometers selectino function"""
        return self._time

    @time.setter
    def time(self, time):
        if not isinstance(time, int):
            raise ValueError('provide int for time')
        self._time = time

    @property
    def post_samples(self):
        """Detection posterior samples"""
        return self._post_samples

    @post_samples.setter
    def post_samples(self, path):
        try:
            post_samples = h5py.File(path, 'r')['IMRPhenomPv2_posterior']
        except OSError:
            raise OSError('provide a valid file')
        except KeyError:
            try:
                post_samples = h5py.File(path, 'r')['IMRPhenomPv3HM_posterior']
            except KeyError:
                try:
                    post_samples = h5py.File(path, 'r')['IMRPhenomXPHM_posterior']
                except KeyError:
                    print("Unknown waveform for posterior samples, check in file which was used")
                    post_samples = h5py.File(path, 'r')['posterior']
                    
        names = post_samples.dtype.names
        arr = np.zeros(self._nposts, dtype={'names': names,\
                       'formats': ['float64']*len(names)})
        # randomly downsample the posterior samples
        np.random.seed(self._seed)
        mask = np.random.choice(np.arange(len(post_samples[names[0]])),
                                size=self._nposts, replace=False)
        for name in names:
            arr[name] = (post_samples[name])[mask]
        self._post_samples = arr

    @property
    def pofd(self):
        """p(detection | RA, DEC) as a Healpy map"""
        return self._pofd

    @pofd.setter
    def pofd(self, path):
        try:
            self._pofd = joblib.load(path)
        except IOError:
            raise IOError('bad file')

    @property
    def dlmax(self):
        """Distance cutoff for probability of distance"""
        return self._dlmax

    @dlmax.setter
    def dlmax(self, dlmax):
        if not isinstance(dlmax, (float ,int)):
            raise ValueError('provide float or int')
        self._dlmax = dlmax

    def pdf_dist(self, pdf_dist):
        if pdf_dist is None:
            try:
                dist = self.post_samples['luminosity_distance_Mpc']
            except ValueError:
                dist = self.post_samples['luminosity_distance'] # O3 h5 files have different formats to GWTC1
            return (3 / self.dlmax**3) * (dist**2)
        else:
            raise ValueError('not implemented')

    def _pdf_mass(self):
        try:
            m1 = self.post_samples['m1_detector_frame_Msun']
        except ValueError:
            m1 = self.post_samples['mass_1_source'] # O3 h5 files have different formats to GWTC1
        return m1**(self._alpha) / (m1 - self.min_mass)

    def rotate_sky_samples(self, rotmat):
        """Rotates the position vectors on the sky
        ---------------------
        Parameters:
            rotmat: np.array (3,3)
                Rotation matrix
        """
        return hp.rotator.rotateVector(rotmat, self._sky_vectors)

    @staticmethod
    def _rotate_pofd(rotmat, pofd, nside, pixel_vectors):
        """Rotates the Healpy map pixels corresponding to the
        probability of detection
        -----------------------
        Parameters:
            rotmat: np.array (3,3)
                Rotation matrix
            pofd
            nside
            pixel_vectors
        """
        # Rotate where the future pixel centres positin will be into the
        # old frame
        old_centres = np.matmul(rotmat.T, pixel_vectors)
        # get the pixel numbers of the old-centres in the original map
        old_order = hp.vec2pix(nside, old_centres[0, :],
                               old_centres[1, :], old_centres[2, :])
        return pofd[old_order]

    def rotate_pofd(self, rotmat):
        return self._rotate_pofd(rotmat, self.pofd, self._nside,
                                 self._pofd_pixel_vectors)


class Run(object):
    """Convenience object holding information about an observing run.
    ---------------------------
    Note:
        Currently useful only for posterior calculation. Might later edit
        this to include information for pofd calculation as well

    ---------------------------
    Parameters:
        name: str
            Event name
        pofd_path: str
            Path to the mean probability of detection file
        observing_times_path: str
            Path to the file holding information about observing times.
    """
    def __init__(self, name, pofd_path, observing_times_path):
        self._name = None
        self._pofd = None
        self._observing_time = None
        # store values
        self.name = name
        self.pofd = pofd_path
        self.observing_time = observing_times_path
        # Pixel centers of the pofd map
        self._nside = hp.npix2nside(self.pofd.size)
        self._pofd_pixel_vectors = hp.pix2vec(self._nside,
                                              np.arange(self.pofd.size))

    @property
    def name(self):
        """Event name"""
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise ValueError('provide a str for name')
        self._name = name

    @property
    def observing_time(self):
        return self._observing_time

    @observing_time.setter
    def observing_time(self, path):
        try:
            times = np.genfromtxt(path, names=True)
        except IOError:
            raise IOError('provide a valid file')
        time = np.sum(times['GPSend'] - times['GPSstart'])
        # set the observing time in units of years
        self._observing_time = time / 31557600

    @property
    def pofd(self):
        """p(detection | RA, DEC) as a Healpy map"""
        return self._pofd

    @pofd.setter
    def pofd(self, path):
        try:
            self._pofd = joblib.load(path)
        except IOError:
            raise IOError('bad file')

    def rotate_pofd(self, rotmat):
        return Event._rotate_pofd(rotmat, self.pofd, self._nside,
                                  self._pofd_pixel_vectors)
