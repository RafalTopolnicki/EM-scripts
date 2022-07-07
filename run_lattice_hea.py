import numpy as np
import sys
import os
import argparse
import string
import random
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from write_akai_input import scf_input

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def run_scf(lattice, args):
    tmpfilename = f'{args.output}_{lattice:.3f}'
    scf_input(filename=f'{tmpfilename}', elements=args.elements, concentrations=args.concentrations, symmetry=args.sym,
              lattice_constant=lattice, ew=args.ew, xc=args.xc, rel=args.rel,
              bzqlty=args.bzqlty, pmix=args.pmix, edelt=args.edelt, mxl=args.mxl)
    os.system(f"/home/rto/HEA/RKKY/bin/specx.ifort < {tmpfilename}.inp > {tmpfilename}.out")
    energy = subprocess.check_output([f"grep \"total energy\" {tmpfilename}.out | tail -1"], shell=True)
    # parse outputed energy
    energy = str(energy)
    pos = energy.find('=') + 2
    energy = float(energy[pos:-3])
    return energy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, required=True, help="prefix for the outputfile")
    parser.add_argument("--sym", type=str, default="bcc", choices=["bcc", "fcc"], help="lattice symmetry")
    parser.add_argument("--elements", nargs="+", help="list of atomic masses")
    parser.add_argument("--concentrations", nargs="+", help="list of atomic concentrations")
    parser.add_argument("--min", type=float, required=True, help="minimal lattice constant to consider")
    parser.add_argument("--max", type=float, required=True, help="maximal lattice constant to consider")
    parser.add_argument("--step", type=float, required=True, help="incrementation step for lattice constants")

    parser.add_argument("--ew", type=float, default=0.7, help="ewidth")
    parser.add_argument("--xc", type=str, default='pbe', help="XC potential")
    parser.add_argument("--rel", type=str, default="nrl", choices=["nrl", "sra", "srals"], help="relativity mode")

    parser.add_argument("--bzqlty", type=float, default=10, help="bzqlty parameter")
    parser.add_argument("--pmix", type=float, default=0.01, help="pmix parameter")
    parser.add_argument("--edelt", type=float, default=0.001, help="edelt parameter")
    parser.add_argument("--mxl", type=int, default=3, help="mxl parameter")

    args = parser.parse_args()

    concentration_str = [f'{c*100}.1f' for c in args.concentrations]
    concentration_str = ' '.join(concentration_str)

    lattice = args.min
    results = []
    while lattice <= args.max:
        energy = run_scf(lattice, args)
        results.append([lattice, energy] + args.elements + args.concentrations)
        lattice += args.step

    # write output
    df = pd.DataFrame(results, columns=['lattice', 'energy'])
    df.to_csv(f'{args.output}_results.csv', index=False)
    # write min energy to separate file
    min_energy = np.min(results.iloc[:, 1])
    with open('best_energy.txt', 'w') as f:
        f.write(f'{min_energy} {concentration_str}')
    f.close()
    # make a plot
    plt.plot(df.iloc[:, 0], df.iloc[:, 1])
    plt.title(concentration_str)
    plt.savefig('energy_lattice.png')

if __name__ == "__main__":
    main()