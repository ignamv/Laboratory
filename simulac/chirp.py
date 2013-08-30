import numpy as np
from peaks import find_min
from mosaic import mosaic

def mosaicPeak(mosaic):
    return np.max(mosaic[find_min(mosaic)])/np.max(mosaic)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Measure MOSAIC peak')
    parser.add_argument('input', type=argparse.FileType('r'))
    cfg = parser.parse_args()

    tau, mosaic = np.loadtxt(cfg.input, unpack=True)
    print(mosaicPeak(mosaic))
