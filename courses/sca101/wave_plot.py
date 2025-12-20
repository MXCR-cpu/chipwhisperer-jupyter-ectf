import scipy
import pylab
import matplotlib.pylab as plt
import numpy as np

from scipy.fft import fft, ifft
from IPython.display import display

def plot_traces(scope, waves_data, time_axis=True):
    plt.clf()
    fig, ax = plt.subplots(figsize=(15,5))

    if time_axis:
        ax.set_xlabel("Time (ms)")
    else:
        ax.set_xlabel("Sample")
    ax.set_ylabel("ADC output (leakage signal)")
    ax.set_title("Power trace")
    ax.grid(True)

    time_domain = np.arange(scope.adc.samples)
    plotted_waves = []
    
    if time_axis:
        time_domain = (time_domain / scope.clock.adc_freq) * (1e6)

    for wave, description, *color in waves_data:
        plotted_wave, = ax.plot(time_domain, wave, label=description, color=color[0])
        plotted_waves.append(plotted_wave)
    
    leg = ax.legend(ncol=16, loc='center', bbox_to_anchor=(0.8, 0.2), fontsize='small', columnspacing=1)
    lined = {}

    for legline, origline in zip(leg.get_lines(), plotted_waves):
        legline.set_picker(True)  # Enable picking
        lined[legline] = origline

    def on_pick(event):
        legline = event.artist
        origline = lined[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        legline.set_alpha(1.0 if visible else 0.2)  # fade legend entry
        fig.canvas.draw()

    fig.canvas.mpl_connect("pick_event", on_pick)
    plt.show()

def plot_trace_FFT(scope, wave_data):
    plt.clf()
    #fig, ax = plt.subplots(figsize=(15,5))
    #ax.set_xlabel("Time (ms)")
    #ax.set_ylabel("ADC output (leakage signal)")
    #ax.set_title("Power trace")
    #ax.grid(True)

    (wave, description) = wave_data
    time_domain = (np.arange(scope.adc.samples) / scope.clock.adc_freq) * (1e6)
    wave_FFT = abs(fft(wave))
    freqs = scipy.fftpack.fftfreq(wave.size, time_domain[1]-time_domain[0])
    
    pylab.subplot(211)
    pylab.plot(time_domain, wave)
    pylab.subplot(212)
    pylab.plot(freqs,20*np.log10(wave_FFT),'x')
    pylab.show()

def plot_reset():
    plt.close('all')