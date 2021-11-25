"""Posterior model for detecting BBH signals isotropy"""
import numpy as np
from scipy.integrate import quad

import healpy as hp

from transforms3d.euler import euler2mat

class Model(object):
    """Posterior model for the aniso pixel version of BBH isotropy code.

    Parameters
    ----------
        events: list
            List of detection.Event objects containing information about
            individual detections.
        runs: list
            List of detection.Run objects containing information about
            the observing runs under consideration.
        weights_nside: int
            Healpy nside for the pixel weights. For 12 weights nside=1
        rate_bounds: length-2 tuple (default (1e-5, 750))
            Min and max rate
        axes: str (default 'rzyz')
            Order of Euler rotations
    """
    def __init__(self, events, runs, weights_nside,
                 rate_bounds=(1e-5, 750), axes='rzyz'):
        # store inputs
        self.runs = runs
        self.events = events
        self._weights_nside = weights_nside
        self.rate_bounds = rate_bounds
        self._axes = axes

        self._nside = events[0]._nside # nside of the pofd maps
        # observing volume
        self._volume = 4 / 3 * np.pi * (events[0]._dlmax*1e-3)**3

        # det pixel centres in weights map
        x, y, z = events[0]._pofd_pixel_vectors
        self._weights_cents = hp.vec2pix(weights_nside, x, y, z)
        self.weight_pars = ['a{}'.format(i)
                            for i in range(hp.nside2npix(weights_nside))]
        self.rot_pars = ['a', 'cosb', 'c']
        # supporting objects used to check out of bounds rotation
        self._weight_pix_order = np.arange(hp.nside2npix(weights_nside))
        self._weight_pixs_centres = hp.pix2vec(weights_nside,\
                                np.arange(hp.nside2npix(weights_nside)))
        self._weight_pixs_centres = np.array(self._weight_pixs_centres)

    def _change_basis(self, weights):
        """Switches dimensions of a healpy map. Here used to render the
        12 pixel weights on a higher dimensional basis.
        """
        return weights[self._weights_cents]

    def logprior_rotation(self, rotmat):
        """Checks whether any original pixel weight gets rotated beyond
        its original boundaries.
        """
        # Rotate pixel centres and test if all remain in the original pixel
        rot_vecs = hp.rotator.rotateVector(rotmat, self._weight_pixs_centres)
        rot_pixs = hp.vec2pix(self._weights_nside, rot_vecs[0, :],
                              rot_vecs[1, :], rot_vecs[2, :])
        if not np.alltrue(rot_pixs == self._weight_pix_order):
            return -np.infty
        return 0.0

    def logprior_rate(self, weights):
        """Log prior on the astrophysical rate."""
        if np.any(weights < 0):
            return -np.infty
        N = len(weights)
        R = np.sum(weights) * 4 * np.pi / N
        if not self.rate_bounds[0] < R < self.rate_bounds[1]:
            return -np.infty
        return - (N - 0.5) * np.log(R)

    def nexp(self, rotmat, weights):
        """Expected number of detections over the observing time."""
        nexp = 0
        dOmega = 4 * np.pi / len(weights)
        for run in self.runs:
            pofd = run.rotate_pofd(rotmat)
            VT = self._volume * run.observing_time
            nexp += VT * np.sum(weights * pofd) * dOmega
        return nexp

    def logprob_detections(self, rotmat, weights):
        """Detections likelihood, gives the product of expected number of
        detections at the detection time and likelihood of the posterior
        samples.
        """
        logprob = 0.0
        for event in self.events:
            pofd = event.rotate_pofd(rotmat)
            # rotated sky vectors of the posterior samples
            vects = event.rotate_sky_samples(rotmat)
            # find in which pixel the rotated vectors now are
            npix = hp.vec2pix(self._nside, vects[0, :], vects[1, :],
                              vects[2, :])
            num = np.mean(weights[npix] * event._pdist * event._pmass)
            logprob += np.log(num)
        return logprob

    def logprior(self, pars):
        """Log prior."""
        # check rotations
        rotmat = euler2mat(pars['a'], np.arccos(pars['cosb']), pars['c'],
                           axes=self._axes)
        if not np.isfinite(self.logprior_rotation(rotmat)):
            return -np.infty
        # calc rate prior
        weights = np.array([pars[p] for p in self.weight_pars])
        lp = self.logprior_rate(weights)
        if not np.isfinite(lp):
            return -np.infty
        return lp

    def loglikelihood(self, pars):
        """Log likelihood."""
        weights = np.array([pars[p] for p in self.weight_pars])
        rotmat = euler2mat(pars['a'], np.arccos(pars['cosb']), pars['c'],
                           axes=self._axes)
        #recast the weights into a higher dimensional basis matching pofd map
        weights = self._change_basis(weights)
        Nexp = self.nexp(rotmat, weights)
        return - Nexp + self.logprob_detections(rotmat, weights)


class IsotropicModel(object):
    """Collection of constants for the posterior analytic isotropic model.

    -----------------------
    Parameters:
        events: list
            List of detection.Event objects containing information about
            individual detections.
        runs: list
            List of detection.Run objects containing information about
            the observing runs under consideration.
        rate_bounds: length-2 tuple (default (1e-5, 750))
            Min and max rate
    """
    def __init__(self, events, runs, rate_bounds=(1e-5, 750)):
        # store inputs
        self.runs = runs
        self.events = events
        self.rate_bounds = rate_bounds
        # observing volume
        self._volume = 4 / 3 * np.pi * (events[0]._dlmax*1e-3)**3
        # list of str that gives weight names

    @property
    def alpha_const(self):
        """Constant used to evaluate the expected number of events
        """
        alpha = 0.0
        for run in self.runs:
            alpha += 4*np.pi / hp.nside2npix(run._nside) * self._volume\
                     * run.observing_time * np.sum(run.pofd)
        return alpha

    @property
    def beta_const(self):
        beta = 1.0
        for event in self.events:
            beta *= np.mean(event._pdist * event._pmass) / event.pofd.size
        return beta


class NumericalIsotropicModel(object):
    """
    Numerical solution equivalent to ``IsotropicModel`` which is solved
    analytically. Imports the likelihood functions from the anisotropic
    ``Model``.
    """
    def __init__(self, events, runs, rate_bounds=(1e-5, 750)):
        self.aniso_model = Model(events=events, runs=runs, weights_nside=1,
                                 rate_bounds=rate_bounds, axes='rzyz')

    @staticmethod
    def _log_prior(a0):
        return -0.5 *  np.log(4 * np.pi * a0)

    def _log_likelihood(self, a0):
        pars = {'a{}'.format(i): a0 for i in range(12)}
        pars.update({'a': 0, 'cosb': 1, 'c': 0})
        return self.aniso_model.loglikelihood(pars)

    def log_posterior(self, a0):
        return self._log_prior(a0) + self._log_likelihood(a0)

    def _posterior(self, a0):
        return np.exp(self.log_posterior(a0))

    @property
    def log_evidence(self):
        evidence, std = quad(self._posterior, 1e-5, 100, epsabs=1e-200,
                             epsrel=1e-200)
        return np.log(evidence)

    @property
    def maximum_logpost(self):
        x = np.linspace(1e-5, 20, 1000)
        y = [self.log_posterior(i) for i in x]
        x *= 4 * np.pi

        return x, y, x[np.argmax(y)]
