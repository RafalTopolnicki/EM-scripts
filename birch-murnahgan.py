'''Example of fitting the Birch-Murnaghan EOS to data'''
import numpy as np
import sys, getopt
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import os
import argparse
import pandas as pd

def volume_to_lattice(vol):
	return (vol*2.0)**(1.0/3.0)

def lattice_to_volume(latt):
	return (latt**3)/2.0

def pressure_volume(v, v0, b, bP):
	P=3.0/2.0*b*((v/v0)**(-7.0/3.0) - (v/v0)**(-5.0/3.0))*(1+3.0/4.0*(bP-4)*((v/v0)**(-2.0/3.0)-1))	
	return P

def find_pressure_lattice(press, v0, b, bP):
	def obj(v, target_p, v0, b, bP):
		err = target_p - pressure_volume(v, v0, b, bP)
#		print(f'{v/v0} err={err}')
		return err
	vtrial = v0*0.9
	vol, ier = leastsq(obj, vtrial, args=(press, v0, b, bP))
	latt = volume_to_lattice(vol)
	return latt

def dist_to_si(x):
	return x*5.29177e-11

def dist_from_si(x):
	return x/5.29177e-11
	

#now we have to create the equation of state function
def Murnaghan(parameters,vol):
    '''
    given a vector of parameters and volumes, return a vector of energies.
    equation From PRB 28,5480 (1983)
    '''
    E0 = parameters[0]
    B0 = parameters[1]
    BP = parameters[2]
    V0 = parameters[3]
    
#    E = E0 + B0*vol/BP*(((V0/vol)**BP)/(BP-1)+1) - V0*B0/(BP-1.)
    E = E0 + 9*V0*B0/16.0*( ((V0/vol)**(2.0/3.0)-1)**3*BP + ((V0/vol)**(2.0/3.0)-1)**2*(6-4*(V0/vol)**(2.0/3.0)) )

    return E

# and we define an objective function that will be minimized
def objective(pars,y,x):
    #we will minimize this function
    err =  y - Murnaghan(pars,x)
    return err
	

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--f", type=str, required=True, help="csv file with latt and E in columns")

    args = parser.parse_args()

    dat = pd.read_csv(args.f)
    energy = dat.iloc[:, 1]

    # change to SI
    energy = energy * 2.1798741e-18
    latt = dist_to_si(dat.iloc[:, 0])

    # compute volume based on lattice constant
    v = lattice_to_volume(latt)


    ### fit a parabola to the data
    # y = ax^2 + bx + c
    a, b, c = np.polyfit(v, energy, 2)  # this is from pylab

    '''
    the parabola does not fit the data very well, but we can use it to get
    some analytical guesses for other parameters.

    V0 = minimum energy volume, or where dE/dV=0
    E = aV^2 + bV + c
    dE/dV = 2aV + b = 0
    V0 = -b/2a

    E0 is the minimum energy, which is:
    E0 = aV0^2 + bV0 + c

    B is equal to V0*d^2E/dV^2, which is just 2a*V0

    and from experience we know Bprime_0 is usually a small number like 4
    '''
    # now here are our initial guesses.
    v0 = -b / (2 * a)
    e0 = a * v0 ** 2 + b * v0 + c
    b0 = 2 * a * v0
    bP = 4

    x0 = [e0, b0, bP, v0] #initial guesses in the same order used in the Murnaghan function

    murnpars, ier = leastsq(objective, x0, args=(energy, v)) #this is from scipy

    #now we make a figure summarizing the results
    vfit = np.linspace(min(energy), max(energy), 100)
    plt.plot(v,energy,'ro')
    #plt.plot(vfit, a*vfit**2 + b*vfit + c,'--',label='parabolic fit')
    plt.plot(vfit, Murnaghan(murnpars,vfit), label='Murnaghan fit')
    plt.xlabel('Volume ($\AA^3$)')
    plt.ylabel('Energy (eV)')
    plt.legend(loc='best')
    plt.savefig('a-eos.png')

    v0 = murnpars[3]
    a0 = volume_to_lattice(v0)
    b0 = murnpars[1]
    bP = murnpars[2]

    print(dist_from_si(a0))
    print(b0/1e9)

if __name__ == "__main__":
    main()