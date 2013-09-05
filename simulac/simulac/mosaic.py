#-- encoding: utf-8 --
import numpy as np
import numpy

def mosaic(interf):
    """Process second-order autocorrelation with MOSAIC technique

    Apply MOSAIC[1]_ to an autocorrelation signal.

    Parameters
    ----------
    interf : ndarray
        Input second-order autocorrelation

    Returns
    -------
    mos : ndarray
        Autocorrelation filtered with MOSAIC

    References
    ----------
    .. [1]  T. Hirayama y M. Sheik-Bahae, «Real-time chirp diagnostic for ultrashort laser pulses», Optics letters, vol. 27, n.Âº 10, pp. 860-862, 2002.
    """
    spectrum = numpy.fft.fft(interf)
    absfft = np.abs(spectrum)

    # Safe margin around the 0-frequency peak
    exclude_lim = 20*np.nonzero(absfft < absfft[1]/2)[0][0]
    # Take first point that looks like a peak...
    prelim_peak = exclude_lim+np.nonzero(absfft[exclude_lim:] 
                                         > absfft[1]/2)[0][0]
    # Then take the center of mass of a window around it
    window = np.arange(prelim_peak-exclude_lim, prelim_peak+exclude_lim)
    # Index of first peak in FFT
    peak = int(np.sum(window*absfft[window])/np.sum(absfft[window]))
    halfpeak = int(peak/2)
    half = int(len(spectrum)/2)

    # Perform MOSAIC
    spectrum[halfpeak:3*halfpeak] = 0
    spectrum[-3*halfpeak:-halfpeak] = 0
    spectrum[3*halfpeak:half] *= 2
    spectrum[-half:-3*halfpeak] *= 2

    return np.abs(np.fft.ifft(spectrum))

if __name__ == '__main__':
    import argparse
    from matplotlib import pyplot as plt

    parser = argparse.ArgumentParser(description='Apply MOSAIC to autocorrelation figure')
    parser.add_argument('input', type=argparse.FileType('rb'))
    parser.add_argument('output', type=argparse.FileType('wb'))

    cfg = parser.parse_args()

    # Pass through header comments
    while True:
        pos = cfg.input.tell()
        line = cfg.input.readline()
        if line[0] == '#':
            cfg.output.write(line)
        else:
            # Unread line
            cfg.input.seek(pos)
            break
    cfg.output.write('# MOSAIC applied'.encode('ascii'))

    tau, interf = np.loadtxt(cfg.input, unpack=True)
    result = mosaic(interf)
    np.savetxt(cfg.output, np.vstack((tau,result)).T)
