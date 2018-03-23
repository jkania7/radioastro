"""Created by jwk 19 March 2018"""
import urllib2 #import pacakages we might need
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Computer Modern Roman','Helvetica']})#makes the plots have pretty fonts
rc('text', usetex=True)
plt.rcParams.update({'font.size':10})

def sci_not(v,err,rnd=2):#addapted from https://stackoverflow.com/questions/17088510/is-there-a-python-module-that-convert-a-value-and-an-error-to-a-scientific-notat
    power =  - int(('%E' % v)[-3:])
    rnd = - power - int(('%E' % float("{0:.2g}".format(err)))[-3:])
    return r"({0} \pm {1})e{2}".format(
            round(v*10**power,rnd+1),round(err*10**power,rnd+1),-power)


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
print("a={0}+/-{1}, x0={2}+/-{3}, sigma={4}+/-{5}".format(popt[0],perr[0],popt[1],perr[1],popt[2],perr[2]))
xdata = np.linspace(min(cont[:,0]), max(cont[:,0]),1000)#use the best fit numbers to plot 
ydata = guassian(xdata,*popt)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(cont[:,0], cont[:,1],marker="s",color='r',label='Observed', s=4)
ax1.plot(xdata,ydata,label="Best Fit Guassian\n $a={0}$ K\n$x_0={1}$ $^\circ$\n$\sigma={2}$ $^\circ$".\
             format(sci_not(popt[0],perr[0]),sci_not(popt[1],perr[1]),sci_not(popt[2],perr[2])))
plt.title(r"Fitting Telescope Beamwidth with a Guassian, $g(x) = a\exp\Big[{-\frac{(x-x_0)^2}{2\sigma^2}}\Big]$")
plt.ylabel(r"Antenna Temperature [K]")
plt.xlabel(r"RA [Degree]")
plt.legend(loc='best')
plt.autoscale(enable=True, axis='x', tight=True)
plt.savefig('Continuum.pdf', bbox_inches='tight')#saves the output pdf
plt.show() #shows plot
