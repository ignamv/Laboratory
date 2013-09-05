#-- encoding: utf-8 --
import numpy as np
from .peaks import find_min
from .mosaic import mosaic
from .generate_ac import center_ac

def mosaicPeak(mos):
    """Calculate MOSAIC peak of a MOSAIC-processed autocorrelation

    Estimate a pulse's chirp using the MOSAIC technique [1].

    [1]T. Hirayama y M. Sheik-Bahae, «Real-time chirp diagnostic for ultrashort laser pulses», Optics letters, vol. 27, n.º 10, pp. 860-862, 2002.
    """

    mos = center_ac(mos)
    return np.max(mos[find_min(mos)])/np.max(mos)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Measure MOSAIC peak')
    parser.add_argument('input', type=argparse.FileType('r'))
    cfg = parser.parse_args()

    tau, mosaic = np.loadtxt(cfg.input, unpack=True)
    print(mosaicPeak(mosaic))
