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


r = urllib2.urlopen('http://astro.phys.wvu.edu/hii/G034.133.dat')#gets the data
g034 = np.genfromtxt(r,delimiter=' ')#parses the data
print('shape(g034)={0}'.format(g034.shape))
g034 = g034[0+100:4096-120,:] #cut off passband rolloff, found by trial end error
print('shape(g034\')={0}'.format(g034.shape))
g034[:,0] *= 10.0**(-3.0)#Converts from MHz to GHz
"""
plt.plot(g034[:,0], g034[:,1],label="Antenna Temperature")
plt.title(r"Determining Telescope Beamwidth")
plt.ylabel(r"Antenna Temperature [K]")
plt.xlabel(r"Frequency [GHz]")
plt.show()"""
#first look at data, uncomment to see

def guassian(x, a, b, c, m):#defines the guassian function
    return a*np.exp(-1.0*(x-b)**2.0/(2.0*c**2.0)) + m
a0 = max(g034[:,1]) #Guess for 
b0 = g034[np.argmax(g034[:,1]),0]#guess b by looking location of a
c0 = 0.001 #from visual inspection
m0 = np.mean(g034[:,1])#guess for the offset
print('a0={0}'.format(a0))#print out to check os 
print('x0={0}'.format(b0))
print('sigma0={0}'.format(c0))
print('b0={0}'.format(m0))
popt,pcov = curve_fit(guassian, g034[:,0], g034[:,1],p0=[a0,b0,c0,m0])#fits the guassian,p0 is inital guess for variables
perr = np.sqrt(np.diag(pcov))#finds the errors on the fit parms
print("a={0}+/-{1}, v0={2}+/-{3}, sigma={4}+/-{5}, b={6}+/-{7}".\
          format(popt[0],perr[0],popt[1],perr[1],popt[2],perr[2],popt[3],perr[3]))
xdata = np.linspace(min(g034[:,0]), max(g034[:,0]),1000)#use the best fit numbers to plot 
ydata = guassian(xdata,*popt)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(g034[:,0], g034[:,1],marker="s",color='r',label='Observed',s=1)
ax1.plot(xdata,ydata,label="Best Fit Guassian\n $a={0}$ K\n$\\nu_0={1}$ Hz\n$\sigma={2}$ Hz\n$b={3}$ K".\
             format(sci_not(popt[0],perr[0]),sci_not(popt[1],perr[1]),sci_not(popt[2],perr[2]),sci_not(popt[3],perr[3])))
plt.title(r"Fitting Spectral Line with  Guassian, $g(\nu) = a\exp\Big[{-\frac{(\nu-\nu_0)^2}{2\sigma^2}}\Big]+b$")
plt.ylabel(r"Antenna Temperature [K]")
plt.xlabel(r"$\nu$ [GHz]")
plt.legend(loc='best')
plt.autoscale(enable=True, axis='x', tight=True)
plt.savefig('G034.pdf', bbox_inches='tight')#saves the output pdf
plt.show() #shows plot
