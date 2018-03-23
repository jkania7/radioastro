"""Created by jwk 19 March 2018"""
import urllib2 #import pacakages we might need
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Computer Modern Roman','Helvetica']})#makes the plots have pretty fonts
rc('text', usetex=True)
plt.rcParams.update({'font.size':11})
def sci_not(v,err,rnd=2):#addapted from https://stackoverflow.com/questions/17088510/is-there-a-python-module-that-convert-a-value-and-an-error-to-a-scientific-notat
    power =  - int(('%E' % v)[-3:])
    rnd = - power - int(('%E' % float("{0:.2g}".format(err)))[-3:])
    return r"({0} \pm {1})e{2}".format(
            round(v*10**power,rnd+1),round(err*10**power,rnd+1),-power)

r = urllib2.urlopen('http://astro.phys.wvu.edu/hii/G031.727.dat')#gets the data
g031 = np.genfromtxt(r,delimiter=' ')#parses the data
print('shape(g031)={0}'.format(g031.shape))
g031 = g031[0:4096-550,:]#cut off bad parts of passband, found via trial and error
print('shape(g031\')={0}'.format(g031.shape))#makes sure that the cut array is the correct size
g031[:,0] *= 10.0**(-3.0)#Converts from MHz to GHz
"""
plt.plot(g031[:,0], g031[:,1],label="Antenna Temperature")
plt.title(r"Determining Telescope Beamwidth")
plt.ylabel(r"Antenna Temperature [K]")
plt.xlabel(r"Frequency [GHz]")
plt.show()"""
#first look at data, uncomment to see

def guassian(x, a, b, c, p, s, m):#defines the guassian function
    return a*np.exp(-1.0*(x-b)**2.0/(2.0*c**2.0)) + p*x**2.0 + s*x + m
a0 = max(g031[:,1])- np.mean(g031[:,1])#Guess for A
b0 = g031[np.argmax(g031[:,1]),0]#look at where that A occured,0.3 is added so it fitts the correct hump 
c0 = 0.001 #guess from visual inspection
m0 = np.mean(g031[:,1])#guess for the mean
s0 = 0.37 #guess for the slope, found visually
p0 = 0.05 #guess for polynomial, found visually
print('a0={0}'.format(a0))
print('v0={0}'.format(b0))
print('sigma0={0}'.format(c0))
print('p0={0}'.format(p0))
print('m0={0}'.format(s0))
print('b0={0}'.format(m0))

popt,pcov = curve_fit(guassian, g031[:,0], g031[:,1],p0=[a0,b0,c0,p0,s0,m0])
#fits the guassian,p0 is inital guess for variables
perr = np.sqrt(np.diag(pcov))#finds the errors on the fit parms
print("a={0}+/-{1}, v0={2}+/-{3}, sigma={4}+/-{5}, p={6}+/-{7}, m={8}+/-{9}, b={10}+/-{11}".\
          format(popt[0],perr[0],popt[1],perr[1],popt[2],perr[2],popt[3],perr[3],popt[4],perr[4],popt[5],perr[5]))
xdata = np.linspace(min(g031[:,0]), max(g031[:,0]),1000)#use the best fit numbers to plot 
ydata = guassian(xdata,*popt)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(g031[:,0], g031[:,1],marker="s",color='r',label='Observed',s=1)
ax1.plot(xdata,ydata,label="Best Fit Guassian\n $a={0}$ K\n$\\nu_0={1}$ GHz\n$\sigma={2}$ GHz\n$p={3}$ K/GHz$^2$\n$m={4}$ K/GHz\n$b={5}$ K".\
             format(sci_not(popt[0],perr[0]),sci_not(popt[1],perr[1]),sci_not(popt[2],perr[2]),sci_not(popt[3],perr[3]),sci_not(popt[4],perr[4]),sci_not(int(popt[5]),int(perr[5]))))
plt.title(r"Fitting Spectral Line with  Guassian, $g(\nu) = a\exp\Big[{-\frac{(\nu-\nu_0)^2}{2\sigma^2}}\Big]+p\nu^2+m\nu+b$")
plt.ylabel(r"Antenna Temperature [K]")
plt.xlabel(r"$\nu$ [GHz]")
plt.legend(loc='lower right')
plt.autoscale(enable=True, axis='x', tight=True)
plt.savefig('G031.pdf', bbox_inches='tight')#saves the output pdf
plt.show() #shows plot
