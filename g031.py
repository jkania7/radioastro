"""Created by jwk 19 March 2018"""
import urllib2 #import pacakages we might need
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Computer Modern Roman','Helvetica']})#makes the plots have pretty fonts
rc('text', usetex=True)

r = urllib2.urlopen('http://astro.phys.wvu.edu/hii/G031.727.dat')#gets the data
g031 = np.genfromtxt(r,delimiter=' ')#parses the data
print('shape(g031)={0}'.format(g031.shape))
g031 = g031[0:4096-550,:]#cut off bad parts of passband, found via trial and error
print('shape(g031\')={0}'.format(g031.shape))#makes sure that the cut array is the correct size
"""
plt.plot(g031[:,0], g031[:,1],label="Antenna Temperature")
plt.title(r"Determining Telescope Beamwidth")
plt.ylabel(r"Antenna Temperature [K]")
plt.xlabel(r"Frequency [Hz]")
plt.show()"""
#first look at data, uncomment to see

def guassian(x, a, b, c, p, s, m):#defines the guassian function
    return a*np.exp(-1.0*(x-b)**2.0/(2.0*c**2.0)) + p*x**2.0 + s*x + m
a0 = max(g031[:,1]) #Guess for A
b0 = g031[np.argmax(g031[:,1]),0]+0.3#look at where that A occured,0.3 is added so it fitts the correct hump 
c0 = 0.01 #guess from visual inspection
m0 = np.mean(g031[:,1])#guess for the mean
s0 = 0.5 #guess for the slope, found visually
p0 = 0.2 #guess for polynomial, found visually
print('a0={0}'.format(a0))
print('b0={0}'.format(b0))
print('c0={0}'.format(c0))
print('p0={0}'.format(p0))
print('s0={0}'.format(s0))
print('m0={0}'.format(m0))

popt,pcov = curve_fit(guassian, g031[:,0], g031[:,1],p0=[a0,b0,c0,p0,s0,m0])
#fits the guassian,p0 is inital guess for variables
perr = np.sqrt(np.diag(pcov))#finds the errors on the fit parms
print("a={0}+/-{1}, b={2}+/-{3}, c={4}+/-{5}, p={6}+/-{7}, s={8}+/-{9}, m={10}+/-{11}".\
          format(popt[0],perr[0],popt[1],perr[1],popt[2],perr[2],popt[3],perr[3],popt[4],perr[4],popt[5],perr[5]))
xdata = np.linspace(min(g031[:,0]), max(g031[:,0]),1000)#use the best fit numbers to plot 
ydata = guassian(xdata,*popt)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(g031[:,0], g031[:,1],marker="s",color='r',label='Observed',s=1)
ax1.plot(xdata,ydata,label="Best Fit Guassian\n $a={0:.2e}\pm{1:.1e}K$\n$b={2:.3f}\pm{3:.3f} Hz$\n$c={4:.3f}\pm{5:.3f}Hz$\n$p={6:.2e}\pm{7:.1e}K/Hz^2$\n$s={8:.4f}\pm{9:.4f}K/Hz$\n$m={10:d}\pm{11:2d}K$".\
             format(popt[0],perr[0],popt[1],perr[1],popt[2],perr[2],popt[3],perr[3],popt[4],perr[4],int(round(popt[5],-2)),int(perr[5])))
plt.title(r"Fitting Spectral Line with  Guassian, $g(x) = a\exp\Big[{-\frac{(x-b)^2}{2c^2}}\Big]+px^2+sx+m$")
plt.ylabel(r"Antenna Temperature [K]")
plt.xlabel(r"Frequency [Hz]")
plt.legend(loc='best')
plt.savefig('G031.pdf', bbox_inches='tight')#saves the output pdf
plt.show() #shows plot
