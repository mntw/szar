import numpy as np
import szar.likelihood as lk
import matplotlib.pyplot as plt
from scipy import stats
from configparser import SafeConfigParser
from orphics.tools.io import dictFromSection
from szar.counts import ClusterCosmology,Halo_MF
import emcee
import time
from emcee.utils import MPIPool

iniFile = "input/pipeline.ini"
Config = SafeConfigParser()
Config.optionxform=str
Config.read(iniFile)
bigDataDir = Config.get('general','bigDataDirectory')
clttfile = Config.get('general','clttfile')
constDict = dictFromSection(Config,'constants')
version = Config.get('general','version')
expName = "S4-1.0-CDT"
gridName = "grid-owl2"

nemoOutputDir = '/Users/nab/Desktop/Projects/ACTPol_Cluster_Like/ACTdata/'
nemoOutputDirOut = '/Users/nab/Desktop/Projects/ACTPol_Cluster_Like/'
pardict = nemoOutputDir + 'equD56.par'
noise_file = 'RMSMap_Arnaud_M2e14_z0p4.fits'

CL = lk.clusterLike(iniFile,expName,gridName,pardict,nemoOutputDir,noise_file)

parlist = ['omch2','ombh2','H0','As','ns','tau','massbias','yslope','scat']
parvals = [0.1194,0.022,67.0,2.2e-09,0.96,0.06,0.80,0.08,0.2]

priorlist = ['tau','ns','H0','massbias','scat']
prioravg = np.array([0.06,0.96,67,0.8,0.2])
priorwth = np.array([0.01,0.01,3,0.12,0.1])
priorvals = np.array([prioravg,priorwth])

print CL.lnprior(parvals,parlist,priorvals,priorlist)

Ndim, nwalkers = len(parvals), len(parvals)*2
P0 = np.array(parvals)

pos = [P0 + P0*1e-1*np.random.randn(Ndim) for i in range(nwalkers)]

start = time.time()

pool = MPIPool()
if not pool.is_master():
    pool.wait()
    sys.exit(0)

sampler = emcee.EnsembleSampler(nwalkers,Ndim,CL.lnprob,args =(parlist,priorvals,priorlist))#,pool=pool)
sampler.run_mcmc(pos,1000)
#pool.close()

print (time.time() - start)  
