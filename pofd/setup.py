import scipy.constants as sc
import common_func as cf
# Basic constants
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

# Sampler set up
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

"""Location of directory; this could be automated with OS"""
GenPath = '/home/2311453s/BH-Iso/'
"""Output directory, set equal to GenPath if you don't need the output to be sent elsewhere"""
OutPath = '/scratch/wiay/2311453s/'

runsList = [cf.dictRun('O1', 'aligo_early.txt', 'advirgo_early.txt', 'Obs_time_O1.txt', 'early'),
            cf.dictRun('O2', 'aligo_mid.txt', 'advirgo_mid.txt', 'Obs_time_O2.txt', 'mid'),
            cf.dictRun('O3a', 'aligo_mid.txt', 'advirgo_mid.txt', 'Obs_time_O3a.txt','mid'),
            cf.dictRun('O3b', 'aligo_late.txt', 'advirgo_late.txt', 'Obs_time_O3b.txt','late')
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
              cf.dictEventO3a('GW190408_181802', 'O3a'),
              #cf.dictEventO3a('GW190412', 'O3a'), # had issues with this one in interpolation
              #cf.dictEventO3a('GW190413_052954', 'O3a'),
              cf.dictEventO3a('GW190413_134308', 'O3a'),
              cf.dictEventO3a('GW190421_213856', 'O3a'),
              cf.dictEventO3a('GW190424_180648', 'O3a'),
              cf.dictEventO3a('GW190426_152155', 'O3a'),
              cf.dictEventO3a('GW190503_185404', 'O3a'),
              cf.dictEventO3a('GW190426_152155', 'O3a'),
              cf.dictEventO3a('GW190503_185404', 'O3a'),
              cf.dictEventO3a('GW190426_152155', 'O3a'),
              cf.dictEventO3a('GW190426_152155', 'O3a'),
              cf.dictEventO3a('GW190503_185404', 'O3a'),
              cf.dictEventO3a('GW190512_180714', 'O3a'),
              cf.dictEventO3a('GW190513_205428', 'O3a'),
              cf.dictEventO3a('GW190514_065416', 'O3a'),
              cf.dictEventO3a('GW190517_055101', 'O3a'),
              cf.dictEventO3a('GW190519_153544', 'O3a'),
              cf.dictEventO3a('GW190521', 'O3a'),
              cf.dictEventO3a('GW190527_092055', 'O3a'),
              cf.dictEventO3a('GW190602_175927','O3a'),
              cf.dictEventO3a('GW190620_030421', 'O3a'),
              cf.dictEventO3a('GW190630_185205', 'O3a'),
              cf.dictEventO3a('GW190701_203306', 'O3a'),
              cf.dictEventO3a('GW190706_222641', 'O3a'),
              cf.dictEventO3a('GW190707_093326', 'O3a'),
              cf.dictEventO3a('GW190708_232457', 'O3a'),
              cf.dictEventO3a('GW190719_215514', 'O3a'),
              cf.dictEventO3a('GW190727_060333', 'O3a'),
              cf.dictEventO3a('GW190728_064510','O3a'),
              cf.dictEventO3a('GW190731_140936', 'O3a'),
              cf.dictEventO3a('GW190803_022701', 'O3a'),
              cf.dictEventO3a('GW190814', 'O3a'),
              cf.dictEventO3a('GW190828_063405', 'O3a'),
              cf.dictEventO3a('GW190828_065509', 'O3a'),
              cf.dictEventO3a('GW190909_114149', 'O3a'),
              cf.dictEventO3a('GW190910_112807', 'O3a'),
              cf.dictEventO3a('GW190915_235702', 'O3a'),
              cf.dictEventO3a('GW190924_021846','O3a'),
              cf.dictEventO3a('GW190929_012149','O3a'),
              cf.dictEventO3a('GW190930_133541','O3a'),
              cf.dictEventO3b('GW191103_012549', 'O3b'),
              cf.dictEventO3b('GW191105_143521', 'O3b'),
              cf.dictEventO3b('GW191109_010717', 'O3b'),
              cf.dictEventO3b('GW191113_071753', 'O3b'),
              cf.dictEventO3b('GW191126_115259', 'O3b'),
              cf.dictEventO3b('GW191127_050227', 'O3b'),
              cf.dictEventO3b('GW191129_134029', 'O3b'),
              cf.dictEventO3b('GW191204_110529', 'O3b'),
              cf.dictEventO3b('GW191204_171526', 'O3b'),
              cf.dictEventO3b('GW191215_223052', 'O3b'),
              cf.dictEventO3b('GW191216_213338', 'O3b'),
              cf.dictEventO3b('GW191219_163120', 'O3b'),
              cf.dictEventO3b('GW191222_033537', 'O3b'),
              cf.dictEventO3b('GW191230_180458', 'O3b'),
              cf.dictEventO3b('GW200112_155838', 'O3b'),
              cf.dictEventO3b('GW200115_042309', 'O3b'),
              cf.dictEventO3b('GW200128_022011', 'O3b'),
              cf.dictEventO3b('GW200129_065458', 'O3b'),
              cf.dictEventO3b('GW200202_154313', 'O3b'),
              cf.dictEventO3b('GW200208_130117', 'O3b'),
              cf.dictEventO3b('GW200208_222617', 'O3b'),
              cf.dictEventO3b('GW200209_085452', 'O3b'),
              cf.dictEventO3b('GW200210_092254', 'O3b'),
              cf.dictEventO3b('GW200216_220804', 'O3b'),
              cf.dictEventO3b('GW200219_094415', 'O3b'),
              cf.dictEventO3b('GW200220_061928', 'O3b'),
              cf.dictEventO3b('GW200220_124850', 'O3b'),
              cf.dictEventO3b('GW200224_222234', 'O3b'),
              cf.dictEventO3b('GW200225_060421', 'O3b'),
              cf.dictEventO3b('GW200302_015811', 'O3b'),
              cf.dictEventO3b('GW200306_093714', 'O3b'),
              cf.dictEventO3b('GW200308_173609', 'O3b'),
              cf.dictEventO3b('GW200311_115853', 'O3b'),
              cf.dictEventO3b('GW200316_215756', 'O3b'),
              cf.dictEventO3b('GW200322_091133', 'O3b')
             ]

eventsListGW170814 = [cf.dictEvent('GW170814', 'O2')]*10
samplesPath = GenPath + 'Data/Samples_%s.p'
probPath = OutPath + 'Results/Sampling/Data/Prob_chain.p'
acceptancePath = OutPath + 'Results/Sampling/Data/AcceptFrac_%s.p'
covarPath = OutPath + 'Results/Sampling/Data/Covariance_%s.p'
meanMapPath = OutPath + 'Results/Sampling/Plots/Mean_map_%s_%s'
stdMapPath = OutPath + 'Results/Sampling/Plots/STD_map_%s_%s'
maxProbPath = OutPath + 'Results/Sampling/Plots/Max_prop_%s_%s'
probPlotPath = OutPath + 'Results/Sampling/Plots/Probability_graph.png'
rateHistPath = OutPath + 'Results/Sampling/Plots/R_hist_%s_%s'
pixelHistPath = OutPath + 'Results/Sampling/Plots/Hist_%s'
PSDpath = OutPath + 'Results/Pofd/PSD_%s'


samplesLastPath = OutPath + 'Results/Sampling/Data/Samples_last.p'
lastStepPath = OutPath + 'Results/Sampling/Data/Last_step.p'

mapPath = OutPath + 'Results/Pofd/Pofd_mean_%s'
sphMap = OutPath + 'Results/Pofd/Sph_map_%s'
rsphMap = OutPath + 'Results/Pofd/Real_sph_map_%s'

survivalPath = OutPath + 'Results/Pofd/Survival_%s.pdf'
objSamplesPath = OutPath + 'Results/Pofd/Samples_distribution'

distPath = OutPath + 'Results/Pofd/Pofd_mollview_%s_%sMpc'


