#!/usr/bin/env python3
import numpy as np
import healpy as hp
import cpnest
import cpnest.model
import argparse
import shutil
import os

from detections import Event, Run
from setup import events_list, runs_list
from model import Model

GenPath = '/home/2311453s/BH-Iso/' ##change this to match directory of code

class PixelPosterior(cpnest.model.Model):
    def __init__(self, model):
        self.model = model

        self.names = self.model.weight_pars.copy()
        self.bounds = [(1e-5, 25)] * len(self.model.weight_pars)
        self.names += self.model.rot_pars.copy()
        if model._weights_nside == 1:
            self.bounds += [(0, 2*np.pi), (0.75,  1.0), (0, 2*np.pi)]
        else:
            self.bounds += [(0, 2*np.pi), (0.94,  1.0), (0, 2*np.pi)]

    def log_prior(self, x):
        if self.in_bounds(x):
            return self.model.logprior(x)
        else:
            return -np.infty

    def log_likelihood(self, x):
        return self.model.loglikelihood(x)


def main():
    parser = argparse.ArgumentParser(description='Anisotropy analysis code')
    parser.add_argument('--simulated', action='store_true', default=False,
                        help='10x GW170814 (default: False)')
    parser.add_argument('--mult', type=int, default=10,
                        help='Multiplicity of simulated GW170814')
    parser.add_argument('--nthreads', type=int, default=8,
                        help='Number of cores to request')
    parser.add_argument('--output',default='nested_sampling',
                        help='Output directory')
    parser.add_argument('--nside', default=1, type=int,help='nside for pixel model')
    args = parser.parse_args()
    events = events_list(simulated=args.simulated, multiplicity=args.mult)
    runs = runs_list()
    model = Model(events, runs, weights_nside=args.nside)
    post = PixelPosterior(model)
    # if output file already exists clear it
    if os.path.exists(args.output):
        #inp = input('Clear {}? ("yes" to confirm)'.format(args.output))
        inp = 'yes'
        if inp == 'yes':
            shutil.rmtree(args.output)
            os.mkdir(args.output)
    ns = cpnest.CPNest(post, nlive=10000, output=args.output,
                       nthreads=args.nthreads, verbose=2, maxmcmc=20000,
                       resume=False)
    ns.run()
    ns.plot()
    posterior_samples = ns.get_posterior_samples(\
                        filename=GenPath+args.output+'posterior.dat')


if __name__=='__main__':
    main()
