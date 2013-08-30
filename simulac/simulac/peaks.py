import numpy as np
def find_max(signal):
    return np.nonzero((signal[1:-1] > signal[:-2]) * 
                      (signal[1:-1] > signal[2:]))[0]+1

def find_min(signal):
    return np.nonzero((signal[1:-1] < signal[:-2]) * 
                      (signal[1:-1] < signal[2:]))[0]+1

if __name__ == '__main__':
    import argparse
    import numpy
    import scipy.signal
    from matplotlib import pyplot as plt

    parser = argparse.ArgumentParser(description='Plot peaks')
    parser.add_argument('input', type=argparse.FileType('r'))

    cfg = parser.parse_args()

    tau, interf = np.loadtxt(cfg.input, unpack=True)


    maxima = find_max(interf)
    minima = find_min(interf)

    plt.figure()
    plt.plot(tau, interf, label='AC', color=(.9,.9,.9))
    plt.plot(tau[maxima], interf[maxima], 'r-', label='Maxima')
    plt.plot(tau[minima], interf[minima], 'g-', label='Minima')
    plt.show()

