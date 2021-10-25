import scipy.constants as sc
import common_func as cf
#Basic constants
snrThrComb = 12.0
mSolar = 1.989e30
Mpc = 3.0857e22
c = sc.c
G = sc.G

# Evenly spaced distance vector
dmax = 7500.0
dsize = 1000

# Pixels properties
nside = 1
nsideDet = 16
dpi = 250

axes = 'rzyz'
frac = 0.01
seed = 12345

# Number of samples for marginalising over inc, psi, mass
# nSamp = 50000
nSamp = 500
alpha = 2.35
pools = 24
mmin = 5
mmax = 100

#Sampler set up
nWalk = 1000
nBurn = 0
nSteps = 5000
threads = 2
rmin = 1e-5
rmax = 750
amax = 150



# Parameters to set up the num calculation
# nNum = 20000    # number of mass samples to calculate num
nNum = 500
fmin = 10       # min frequency


runsList = [cf.dictRun('O1', 'aligo_early.txt', 'Obs_time_O1.txt', 'early'),
        cf.dictRun('O2', 'aligo_mid.txt', 'Obs_time_O2.txt', 'mid')
        ]



eventsList = [cf.dictEvent('GW150914', 'O1'),
            cf.dictEvent('GW151226', 'O1'),
            cf.dictEvent('GW151012', 'O1'),
            cf.dictEvent('GW170104', 'O2'),
            cf.dictEvent('GW170608', 'O2'),
            cf.dictEvent('GW170818', 'O2'),
            cf.dictEvent('GW170809', 'O2'),
            cf.dictEvent('GW170729', 'O2'),
            cf.dictEvent('GW170823', 'O2'),
            cf.dictEvent('GW170814', 'O2'),
            ]

eventsListGW170814 = [cf.dictEvent('GW170814', 'O2')]*10

samplesPath = '/content/Results/Sampling/Data/Samples_%s.p'
probPath = '/content/Results/Sampling/Data/Prob_chain.p'
acceptancePath = '/content/Results/Sampling/Data/AcceptFrac_%s.p'
covarPath = '/content/Results/Sampling/Data/Covariance_%s.p'
meanMapPath = '/content/Results/Sampling/Plots/Mean_map_%s_%s'
stdMapPath = '/content/Results/Sampling/Plots/STD_map_%s_%s'
maxProbPath = '/content/Results/Sampling/Plots/Max_prop_%s_%s'
probPlotPath = '/content/Results/Sampling/Plots/Probability_graph.png'
rateHistPath = '/content/Results/Sampling/Plots/R_hist_%s_%s'
pixelHistPath = '/content/Results/Sampling/Plots/Hist_%s'
PSDpath = '/content/Results/Pofd/PSD_%s'


samplesLastPath = '/content/Results/Sampling/Data/Samples_last.p'
lastStepPath = '/content/Results/Sampling/Data/Last_step.p'

mapPath = '/content/Results/Pofd/Pofd_mean_%s'
sphMap = '/content/Results/Pofd/Sph_map_%s'
rsphMap = '/content/Results/Pofd/Real_sph_map_%s'

survivalPath = '/content/Results/Pofd/Survival_%s.pdf'
objSamplesPath = '/content/Results/Pofd/Samples_distribution'

distPath = '/content/Results/Pofd/Pofd_mollview_%s_%sMpc'


