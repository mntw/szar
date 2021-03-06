from __future__ import print_function
from __future__ import division
from past.utils import old_div
import camb
import numpy as np

import matplotlib.pyplot as plt
import sys, os, time
from szar.counts import ClusterCosmology,SZ_Cluster_Model,Halo_MF
from orphics.tools.io import Plotter,dictFromSection,listFromConfig

from configparser import SafeConfigParser

clusterParams = 'LACluster' # from ini file
cosmologyName = 'LACosmology' # from ini file 
experimentName = "LATest"

iniFile = "input/params.ini"
Config = SafeConfigParser()
Config.optionxform=str
Config.read(iniFile)

beam = listFromConfig(Config,experimentName,'beams')
noise = listFromConfig(Config,experimentName,'noises')
freq = listFromConfig(Config,experimentName,'freqs')
lmax = int(Config.getfloat(experimentName,'lmax'))
lknee = Config.getfloat(experimentName,'lknee')
alpha = Config.getfloat(experimentName,'alpha')
fsky = Config.getfloat(experimentName,'fsky')

cosmoDict = dictFromSection(Config,cosmologyName)
constDict = dictFromSection(Config,'constants')
clusterDict = dictFromSection(Config,clusterParams)
cc = ClusterCosmology(cosmoDict,constDict,lmax)

zz = 0.14
MM = 0.8*3e14 #M/h

SZ = SZ_Cluster_Model(cc,clusterDict,lmax=lmax )

Mexpedge = np.arange(12.0,15.8,0.1)
zedge = np.arange(0.0,5.0,0.05)

HMF = Halo_MF(cc,Mexpedge,zedge)

#var = SZ.quickVar(MM,zz)
#var2 = SZ.filter_variance(MM,zz)

#print np.sqrt(var), np.sqrt(var2)
#print "LA", SZ.Y_M(MM,zz)
#print "Planck", SZ.Y_M_test(MM,zz)

#print "S/N", SZ.Y_M(MM,zz)/np.sqrt(var)
#print SZ.f_nu(freq[0])
#print SZ.f_nu_test(freq[0])

print("PS test")

#start = time.time()
#print SZ.Prof_tilde(3000,MM,zz)
#print "Time for new", time.time() - start
#start2 = time.time()
#print SZ.Prof_tilde_old(3000,MM,zz)
#print "Time for old", time.time() - start2

ll = np.arange(200,7000,200)
start3 = time.time()
print((HMF.Cl_ell(ll,SZ)*ll**2 / (2.*np.pi) * 1e12))
print(("Time for old", time.time() - start3))

lnYmin = np.log(1e-13)
dlnY = 0.1
lnY = np.arange(lnYmin,lnYmin+10.,dlnY)

print((SZ.P_of_q(lnY,np.array([0,MM]),zz,np.sqrt(var))))
print((SZ.P_of_qn(lnY,np.array([0,MM]),zz,np.sqrt(var),5)))
print((SZ.P_of_qn(lnY,np.array([0,MM]),zz,np.sqrt(var),6)))
print((SZ.P_of_qn(lnY,np.array([0,MM]),zz,np.sqrt(var),7)))

ells = np.arange(2,6000,10)

nl = SZ.nl#(ells,beam[0],noise[0])
nl2 = SZ.nl2#(ells,beam[0],noise[0])

cibp = SZ.cib_p(ells,freq[0],freq[0])
cibc = SZ.cib_c(ells,freq[0],freq[0])
rps  = SZ.rad_ps(ells,freq[0],freq[0])




#print nl*(ells+1.)*ells/ (2.* np.pi) * constDict['TCMBmuK']**2


pl = Plotter()                                                                                                          
pl.add(ells,old_div(nl,nl2))
#pl.add(ells,nl*(ells+1.)*ells/ (2.* np.pi) * constDict['TCMBmuK']**2)
#pl.add(ells,cibp )#/ ((ells+1.)*ells) * 2.* np.pi)
#pl.add(ells,cibc )#/ ((ells+1.)*ells) * 2.* np.pi)
#pl.add(ells,rps )#/ ((ells+1.)*ells) * 2.* np.pi)
pl.done("output/secondaries_nl_ratio.png")
#pl.done("output/secondaries_dunkley.png")



#np.savetxt('/Users/nab/Desktop/Projects/SO_forecasts/test_noise.txt',np.transpose([ells,nl]))

