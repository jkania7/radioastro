"""Created by jwk 19 March 2018"""
import urllib2 #import pacakages we might need
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Computer Modern Roman','Helvetica']})#makes the plots have pretty fonts
rc('text', usetex=True)

r = urllib2.urlopen('http://astro.phys.wvu.edu/hii/continuum.dat')#gets the data
cont = np.genfromtxt(r,delimiter=' ')#parses the data
"""
plt.plot(cont[:,0], cont[:,1],label="Antenna Temperature")
plt.title(r"Determining Telescope Beamwidth")
plt.ylabel(r"Antenna Temperature [K]")
plt.xlabel(r"RA [Degree]")
plt.show()"""#first look at data, uncomment to see

def guassian(x, a, b, c):#defines the guassian function
    return a*np.exp(-1.0*(x-b)**2.0/(2.0*c**2.0))
popt,pcov = curve_fit(guassian, cont[:,0], cont[:,1],p0=[1.1,283,0.01])#fits the guassian,p0 is inital guess for variables
perr = np.sqrt(np.diag(pcov))#finds the errors on the fit parms
print("a={0}+/-{1}, b={2}+/-{3}, c={4}+/-{5}".format(popt[0],perr[0],popt[1],perr[1],popt[2],perr[2]))
xdata = np.linspace(min(cont[:,0]), max(cont[:,0]),1000)#use the best fit numbers to plot 
ydata = guassian(xdata,*popt)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(cont[:,0], cont[:,1],marker="s",color='r',label='Observed')
ax1.plot(xdata,ydata,label="Best Fit Guassian\n $a={0:.3f}\pm{1:.3f}$\n$b={2:.5f}\pm{3:.5f}$\n$c={4:.5f}\pm{5:.5f}$".format(popt[0],perr[0],popt[1],perr[1],popt[2],perr[2]))
plt.title(r"Fitting Telescope Beamwidth with a Guassian, $g(x) = a\exp\Big[{-\frac{(x-b)^2}{2c^2}}\Big]$")
plt.ylabel(r"Antenna Temperature [K]")
plt.xlabel(r"RA [Degree]")
plt.legend(loc='best')
plt.savefig('Continuum.pdf', bbox_inches='tight')#saves the output pdf
plt.show() #shows plot
