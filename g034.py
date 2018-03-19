"""Created by jwk 19 March 2018"""
import urllib2 #import pacakages we might need
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Computer Modern Roman','Helvetica']})#makes the plots have pretty fonts
rc('text', usetex=True)

r = urllib2.urlopen('http://astro.phys.wvu.edu/hii/G034.133.dat')#gets the data
g034 = np.genfromtxt(r,delimiter=' ')#parses the data
print('shape(g034)={0}'.format(g034.shape))
g034 = g034[2300:3300,:]
print('shape(g034\')={0}'.format(g034.shape))
"""
plt.plot(g034[:,0], g034[:,1],label="Antenna Temperature")
plt.title(r"Determining Telescope Beamwidth")
plt.ylabel(r"Antenna Temperature [K]")
plt.xlabel(r"RA [Degree]")
plt.show()"""
#first look at data, uncomment to see

def guassian(x, a, b, c, m):#defines the guassian function
    return a*np.exp(-1.0*(x-b)**2/(2.0*c**2)) + m
a0 = max(g034[:,1]) #Guess for A
b0 = g034[np.argmax(g034[:,1]),0]
m0 = np.mean(g034[:,1])
print('a0={0}'.format(a0))
print('b0={0}'.format(b0))
print('m0={0}'.format(m0))
popt,pcov = curve_fit(guassian, g034[:,0], g034[:,1],p0=[a0,b0,0.01,m0])#fits the guassian,p0 is inital guess for variables
perr = np.sqrt(np.diag(pcov))#finds the errors on the fit parms
print("a={0}+/-{1}, b={2}+/-{3}, c={4}+/-{5}, m={6}+/-{7}".\
          format(popt[0],perr[0],popt[1],perr[1],popt[2],perr[2],popt[3],perr[3]))
xdata = np.linspace(min(g034[:,0]), max(g034[:,0]),1000)#use the best fit numbers to plot 
ydata = guassian(xdata,*popt)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(g034[:,0]/1000.0, g034[:,1],marker="s",color='r',label='Observed')
ax1.plot(xdata/1000.0,ydata,label="Best Fit Guassian\n $a={0:.4f}\pm{1:.4f}$\n$b={2:.6f}\pm{3:.6f}$\n$c={4:.3f}\pm{5:.3f}$\n$m={6:.5f}\pm{7:.5f}$".\
             format(popt[0],perr[0],popt[1]/1000.0,perr[1]/1000.0,popt[2],perr[2],popt[3],perr[3]))
plt.title(r"Fitting Spectral Line with  Guassian, $g(x) = a\exp\Big[{-\frac{(x-b)^2}{2c^2}}\Big]+m$")
plt.ylabel(r"Antenna Temperature [K]")
plt.xlabel(r"Frequency [MHz]")
plt.legend()
plt.savefig('G034.pdf', bbox_inches='tight')#saves the output pdf
plt.show() #shows plot